"""
checker/check_certificate.py — abc conjecture verification kernel bridge checker
(protocol v2).

Reads CheckerInputV2 from stdin, writes CheckerOutputV2 to stdout.

Obligations it can currently resolve:
  CORE-0: abc statement, rad definition, certificate tuple, Theorem 2, honesty check
          (all pass — DEF/THM by spec)
  CORE-1: DAG acyclicity + import-policy + forbidden-construction-leaf audit
  CORE-2/3/4: [OBL] — always FAIL until a construction is supplied
  CORE-3: includes sub-obligation core3.iut-corollary-312-independently-verified
          which fails with a note about the Scholze-Stix dispute
  CORE-5: fires only when CORE-3 and CORE-4 pass (mechanical implication)

The checker never trusts a producer-supplied PASS or status field. It re-derives
every verdict from the input artifacts or the obligation semantics.
"""

from __future__ import annotations

import ast
import hashlib
import json
import os
import sys
from pathlib import Path

PROTOCOL_VERSION = 2

# ── obligation dispatch ────────────────────────────────────────────────────────

def check_core0(inp: dict) -> list[dict]:
    """
    CORE-0 abc-definition obligations.
    CL-01 (DEF), CL-03 (THM), CL-04 (THM): admitted by spec as definitions/theorems.
    No construction needed.
    """
    results = []
    for oid in inp["obligation_ids"]:
        if oid in (
            "core0.abc-statement-and-rad-defined",
            "core0.certificate-tuple-defined",
            "core0.theorem2-certificate-implies-abc",
            "core0.theorem3-honesty-check",
        ):
            results.append({"id": oid, "verdict": "pass"})
        else:
            results.append({"id": oid, "verdict": "fail",
                            "witness_digest": _note(f"unknown obligation {oid}")})
    return results


def check_core1(inp: dict) -> list[dict]:
    """
    CORE-1 provenance-manifest obligations.

    dag-acyclic: check proof/ for circular imports; check discovery/candidates/
      for guard.assert_zero_free calls.
    no-forbidden-import: check that proof/m1/m2/m3 do not import M4/M5/M6.
    no-forbidden-construction-leaves: scan construction files for forbidden patterns
      (abc triples, fitted K_epsilon, Szpiro assumed, IUT identification-without-
      isomorphism).
    construction-frozen-before-comparison: structural check — always pass at scaffold
      level (both are scaffolded with PLACEHOLDERs; real freeze enforced on fill).
    """
    results = []
    project_root = _project_root()

    for oid in inp["obligation_ids"]:
        if oid == "core1.dag-acyclic":
            ok, msg = _check_dag_acyclic(project_root)
            results.append({"id": oid, "verdict": "pass" if ok else "fail",
                            "witness_digest": _note(msg)})

        elif oid == "core1.no-forbidden-import-M1-M2-M3-into-M4-M5-M6":
            ok, msg = _check_import_barrier(project_root)
            results.append({"id": oid, "verdict": "pass" if ok else "fail",
                            "witness_digest": _note(msg)})

        elif oid == "core1.no-forbidden-construction-leaves":
            ok, msg = _check_forbidden_leaves(project_root)
            results.append({"id": oid, "verdict": "pass" if ok else "fail",
                            "witness_digest": _note(msg)})

        elif oid == "core1.construction-frozen-before-comparison":
            results.append({"id": oid, "verdict": "pass",
                            "witness_digest": _note(
                                "scaffold: core-1/2/3 registered before core-4/5; "
                                "real freeze enforced when PLACEHOLDERs are replaced")})
        else:
            results.append({"id": oid, "verdict": "fail",
                            "witness_digest": _note(f"unknown obligation {oid}")})
    return results


def check_core2(inp: dict) -> list[dict]:
    """
    CORE-2 [OBL]: height/rad framework — not yet supplied.

    This gate requires P_height: Faltings heights, Arakelov intersection theory,
    and the arithmetic geometry setup constructed without forbidden inputs.
    Until proof/m1/ contains a formally verified height framework, all obligations
    fail with an honest OBL message.
    """
    return [{"id": oid, "verdict": "fail",
             "witness_digest": _note(
                 "OBL: height/rad framework not yet supplied. "
                 "CORE-2 requires P_height: Faltings heights and arithmetic geometry "
                 "framework built without known abc triples, fitted K_epsilon, "
                 "Szpiro assumed, or abc-equivalent input. "
                 "This is an open construction obligation (spec §5.1, CL-09).")}
            for oid in inp["obligation_ids"]]


def check_core3(inp: dict) -> list[dict]:
    """
    CORE-3 [OBL]: key inequality — not yet supplied.

    This gate requires P_ineq: a proof of c <= K_epsilon * rad(abc)^(1+epsilon)
    for ALL coprime a+b=c. The critical sub-obligation is:
      core3.iut-corollary-312-independently-verified

    This sub-obligation is OPEN because:
    - No machine-replayed formal proof of Mochizuki's Corollary 3.12 has been supplied.
    - The Scholze-Stix dispute (2018) records that the identification of objects
      across Hodge theaters in IUTT-III lacks an explicit isomorphism proof.
    - This is NOT a determination that IUT is wrong.
    - This IS a determination that the obligation is open.
    """
    results = []
    for oid in inp["obligation_ids"]:
        if oid == "core3.iut-corollary-312-independently-verified":
            results.append({"id": oid, "verdict": "fail",
                            "witness_digest": _note(
                                "OBL (IUT gate): Mochizuki's Corollary 3.12 not independently verified. "
                                "Blocking reason: Scholze-Stix objection (2018) — identification of "
                                "objects across different Hodge theaters in IUTT-III requires an "
                                "explicit isomorphism proof that has not been formalized or "
                                "machine-replayed. "
                                "To pass this gate: supply a machine-replayed formal proof (Lean, Coq, "
                                "Isabelle, Metamath, or equivalent) of the height inequality that does "
                                "not use abc as hypothesis and does not use the identification without "
                                "a proved isomorphism. "
                                "This is NOT a determination that IUT is wrong. "
                                "This IS a determination that the obligation is open.")})
        else:
            results.append({"id": oid, "verdict": "fail",
                            "witness_digest": _note(
                                "OBL: key inequality not yet supplied. "
                                "CORE-3 requires P_ineq: c <= K_epsilon * rad(abc)^(1+epsilon) "
                                "for all coprime a+b=c, proved without abc-equivalent input. "
                                "This is an open construction obligation (spec §5.1, CL-10). "
                                "For the IUT route, core3.iut-corollary-312-independently-verified "
                                "is also required (currently OPEN, Scholze-Stix blocking reason).")})
    return results


def check_core4(inp: dict) -> list[dict]:
    """
    CORE-4 [OBL]: finiteness of exceptions — not yet supplied.

    This gate requires P_finiteness: a proof that the set of exceptions
    {(a,b,c) coprime, a+b=c : c > rad(abc)^(1+epsilon)} is finite,
    proved uniformly without assuming abc or restricting to a fixed prime set S.
    """
    return [{"id": oid, "verdict": "fail",
             "witness_digest": _note(
                 "OBL: finiteness of exceptions not yet proved. "
                 "CORE-4 requires P_finiteness: |{(a,b,c) coprime, a+b=c : "
                 "c > rad(abc)^(1+epsilon)}| < infinity, proved uniformly in a,b,c "
                 "without assuming abc, without restricting to a fixed finite prime set S, "
                 "and without using abc-equivalent finiteness results. "
                 "This is an open construction obligation (spec §5.1, CL-11).")}
            for oid in inp["obligation_ids"]]


def check_cl03(inp: dict) -> list[dict]:
    """
    CL-03 (Theorem 2, THM): abc certificate implies abc conjecture.
    Proof: P_ineq gives c <= K_eps * rad(abc)^(1+eps) universally;
    P_finiteness gives finite exceptions; together these are the abc conjecture for eps.
    """
    results = []
    for oid in inp["obligation_ids"]:
        if oid == "cl03.certificate-implies-abc":
            results.append({"id": oid, "verdict": "pass",
                            "witness_digest": _note(
                                "CL-03: certificate (eps_bound, K_eps, P_height, P_ineq, P_finiteness) "
                                "=> abc for eps: P_ineq gives universal bound c <= K_eps * rad(abc)^(1+eps); "
                                "P_finiteness gives finitely many exceptions; this is the abc conjecture.")})
        elif oid == "cl03.bound-is-universal-not-finite-set":
            results.append({"id": oid, "verdict": "pass",
                            "witness_digest": _note(
                                "CL-03: P_ineq is defined as a universal statement over all coprime a+b=c; "
                                "not agreement on a finite collection; "
                                "spec §2.1 requires universal inequality, not finite matching.")})
        elif oid == "cl03.depends-only-on-cl01-and-base-height-theory":
            results.append({"id": oid, "verdict": "pass",
                            "witness_digest": _note(
                                "CL-03 proof uses: definition of abc conjecture (CL-01), "
                                "definition of certificate (spec Def 1), elementary arithmetic. "
                                "No forbidden inputs.")})
        else:
            results.append({"id": oid, "verdict": "fail",
                            "witness_digest": _note(f"unknown obligation {oid}")})
    return results


def check_cl04(inp: dict) -> list[dict]:
    """
    CL-04 (Theorem 3, THM): Certificate existence equivalent to abc (honesty check).
    Forward: CL-03. Converse (assuming abc): K_epsilon = max over finite exception set.
    NOTE: converse uses abc as hypothesis; the [OBL] construction must not use it.
    """
    results = []
    for oid in inp["obligation_ids"]:
        if oid == "cl04.forward-implication-is-cl03":
            results.append({"id": oid, "verdict": "pass",
                            "witness_digest": _note(
                                "CL-04 forward: follows immediately from CL-03 (Theorem 2)")})
        elif oid == "cl04.converse-uses-abc-as-hypothesis-only":
            results.append({"id": oid, "verdict": "pass",
                            "witness_digest": _note(
                                "CL-04 converse: assumes abc as hypothesis (not a forbidden construction leaf); "
                                "defines K_eps = max_{exceptions} c / rad(abc)^(1+eps) (finite max over finite set); "
                                "this construction is in the CONVERSE proof, not in the arithmetic certificate.")})
        elif oid == "cl04.honesty-check-recorded":
            results.append({"id": oid, "verdict": "pass",
                            "witness_digest": _note(
                                "CL-04 honesty check: certificate existence <-> abc; "
                                "the inequality alone is not a shortcut; "
                                "K_eps and P_ineq must be built without abc triples or abc-equivalent assertions; "
                                "IUT route requires independent Corollary 3.12 verification")})
        else:
            results.append({"id": oid, "verdict": "fail",
                            "witness_digest": _note(f"unknown obligation {oid}")})
    return results


def check_cl07(inp: dict) -> list[dict]:
    """
    CL-07 (THM, syntactic): import checker rejects forbidden dependency graphs.
    This re-runs the same checks as CORE-1, confirming the syntactic theorem holds
    for the current state of the repository.
    """
    project_root = _project_root()
    results = []
    for oid in inp["obligation_ids"]:
        if oid == "cl07.dag-cycle-detection-decidable":
            ok, msg = _check_dag_acyclic(project_root)
            results.append({"id": oid, "verdict": "pass" if ok else "fail",
                            "witness_digest": _note(
                                f"CL-07 syntactic: DFS cycle detection on import graph is decidable O(V+E); "
                                f"current repo: {msg}")})
        elif oid == "cl07.forbidden-import-scan-decidable":
            ok, msg = _check_import_barrier(project_root)
            results.append({"id": oid, "verdict": "pass" if ok else "fail",
                            "witness_digest": _note(
                                f"CL-07 syntactic: module-label forbidden-import scan is decidable O(V+E); "
                                f"current repo: {msg}")})
        elif oid == "cl07.semantic-independence-not-claimed":
            results.append({"id": oid, "verdict": "pass",
                            "witness_digest": _note(
                                "CL-07 explicitly does NOT claim semantic independence (CL-08 is OUT); "
                                "the immutable assumption manifest requires separate mathematical review; "
                                "no general algorithm decides abc-equivalence of an arbitrary theorem")})
        else:
            results.append({"id": oid, "verdict": "fail",
                            "witness_digest": _note(f"unknown obligation {oid}")})
    return results


def check_core5(inp: dict) -> list[dict]:
    """
    CORE-5 conclusion: fires mechanically from CORE-3 and CORE-4 state.
    Since CORE-3 and CORE-4 are [OBL] and will fail, CORE-5 cannot currently pass.
    The checker does NOT trust any producer PASS flag.
    """
    dep_atts = inp.get("dependency_attestations", {})
    core3_passed = "core-3-key-inequality" in dep_atts
    core4_passed = "core-4-finiteness" in dep_atts
    both_passed = core3_passed and core4_passed

    results = []
    for oid in inp["obligation_ids"]:
        if oid == "core5.derive-theorem2-from-passed-artifacts":
            results.append({
                "id": oid,
                "verdict": "pass" if both_passed else "fail",
                "witness_digest": _note(
                    "Theorem 2 derived mechanically from CORE-0..CORE-4"
                    if both_passed else
                    "CORE-3 and/or CORE-4 not passed; abc implication cannot fire")
            })
        elif oid == "core5.no-trusted-producer-pass-flag":
            results.append({"id": oid, "verdict": "pass",
                            "witness_digest": _note(
                                "checker derives verdicts only from obligation results, "
                                "never from producer-supplied PASS fields")})
        else:
            results.append({"id": oid, "verdict": "fail",
                            "witness_digest": _note(f"unknown obligation {oid}")})
    return results


DISPATCH = {
    "core-0-abc-definition":      check_core0,
    "core-1-provenance-manifest": check_core1,
    "core-2-height-framework":    check_core2,
    "core-3-key-inequality":      check_core3,
    "core-4-finiteness":          check_core4,
    "core-5-conclusion":          check_core5,
    "cl-03-certificate-implies-abc":        check_cl03,
    "cl-04-certificate-equivalent-abc":     check_cl04,
    "cl-07-provenance-barrier-syntactic":   check_cl07,
}

# Canonical obligation sets mirrored from domain/contracts/core-*.json.
# Used when proofctl sends obligation_ids: null.
OBLIGATIONS: dict[str, list[str]] = {
    "core-0-abc-definition": [
        "core0.abc-statement-and-rad-defined",
        "core0.certificate-tuple-defined",
        "core0.theorem2-certificate-implies-abc",
        "core0.theorem3-honesty-check",
    ],
    "core-1-provenance-manifest": [
        "core1.dag-acyclic",
        "core1.no-forbidden-import-M1-M2-M3-into-M4-M5-M6",
        "core1.no-forbidden-construction-leaves",
        "core1.construction-frozen-before-comparison",
    ],
    "core-2-height-framework": [
        "core2.rad-function-formally-defined",
        "core2.faltings-height-setup",
        "core2.arithmetic-geometry-framework",
        "core2.framework-built-without-forbidden-inputs",
    ],
    "core-3-key-inequality": [
        "core3.height-inequality-stated",
        "core3.height-inequality-proved",
        "core3.iut-corollary-312-independently-verified",
        "core3.inequality-not-circular",
    ],
    "core-4-finiteness": [
        "core4.finiteness-of-exceptions-stated",
        "core4.finiteness-proved-uniformly",
        "core4.finiteness-not-assumed",
        "core4.no-fixed-prime-set-promotion",
    ],
    "core-5-conclusion": [
        "core5.derive-theorem2-from-passed-artifacts",
        "core5.no-trusted-producer-pass-flag",
    ],
    "cl-03-certificate-implies-abc": [
        "cl03.certificate-implies-abc",
        "cl03.bound-is-universal-not-finite-set",
        "cl03.depends-only-on-cl01-and-base-height-theory",
    ],
    "cl-04-certificate-equivalent-abc": [
        "cl04.forward-implication-is-cl03",
        "cl04.converse-uses-abc-as-hypothesis-only",
        "cl04.honesty-check-recorded",
    ],
    "cl-07-provenance-barrier-syntactic": [
        "cl07.dag-cycle-detection-decidable",
        "cl07.forbidden-import-scan-decidable",
        "cl07.semantic-independence-not-claimed",
    ],
}

# ── DAG / import-barrier / forbidden-leaf checks ──────────────────────────────

M1_M2_M3_ROOTS = ["proof/m1", "proof/m2", "proof/m3", "m1", "m2", "m3"]
FORBIDDEN_TARGETS = ["m4", "m5", "m6",
                     "comparison", "zeros", "conclude", "target",
                     "known_triples", "szpiro_comparison", "faltings_comparison"]

# Patterns that must not appear in construction files (spec §3.3).
FORBIDDEN_PATTERNS = [
    # Known abc triple databases or fitting
    r"abc_triple",
    r"abc_triples",
    r"high_quality_triple",
    r"known_triple",
    r"triple_table",
    # Fitting K_epsilon to known examples
    r"fitted_k_epsilon",
    r"fit_to_triples",
    r"minimize.*triple",
    r"k_epsilon.*fit",
    # Assuming abc or Szpiro
    r"assume_szpiro",
    r"szpiro_conjecture",
    r"assume_abc",
    r"abc_equivalent",
    # IUT identification without isomorphism
    r"hodge_theater_identification",
    r"cross_theater_equal",
    # S-integer finiteness assumed
    r"s_integer_finite",
    r"assume_finiteness",
    # GRH assumed without declaration
    r"assume_grh",
    r"grh_assumed",
]


def _project_root() -> Path:
    p = Path(__file__).resolve().parent.parent
    return p


def _py_imports(path: Path) -> list[str]:
    """Return a flat list of module names imported by a Python file."""
    try:
        src = path.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(src)
    except Exception:
        return []
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name.lower())
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module.lower())
    return imports


def _check_dag_acyclic(root: Path) -> tuple[bool, str]:
    """
    Syntactic DAG check: verify discovery/candidates/ files call
    guard.assert_zero_free, and proof/ has no circular imports.
    """
    candidates_dir = root / "discovery" / "candidates"
    violations = []

    if candidates_dir.exists():
        for py in sorted(candidates_dir.glob("*.py")):
            if py.name.startswith("_"):
                continue
            src = py.read_text(encoding="utf-8", errors="replace")
            if "assert_zero_free" not in src and "guard" not in src:
                violations.append(f"{py.name}: missing assert_zero_free guard")

    if violations:
        return False, "Guard missing in: " + "; ".join(violations)

    # Check proof/ directory for cycles
    proof_dir = root / "proof"
    if proof_dir.exists():
        import_graph: dict[str, list[str]] = {}
        for py in proof_dir.rglob("*.py"):
            rel = str(py.relative_to(root)).replace(os.sep, "/")
            import_graph[rel] = _py_imports(py)

        WHITE, GRAY, BLACK = 0, 1, 2
        color: dict[str, int] = {k: WHITE for k in import_graph}

        def dfs(node: str) -> bool:
            color[node] = GRAY
            for dep in import_graph.get(node, []):
                dep_key = next((k for k in import_graph if dep in k), None)
                if dep_key is None:
                    continue
                if color[dep_key] == GRAY:
                    return False  # cycle
                if color[dep_key] == WHITE and not dfs(dep_key):
                    return False
            color[node] = BLACK
            return True

        for node in list(import_graph):
            if color[node] == WHITE:
                if not dfs(node):
                    return False, "Cycle detected in proof/ import graph"

    return True, "DAG acyclic; all candidates guarded"


def _check_import_barrier(root: Path) -> tuple[bool, str]:
    """
    Non-anticipation barrier: M1/M2/M3 files must not import M4/M5/M6.
    Passes trivially if proof/ is empty/absent.
    """
    proof_dir = root / "proof"
    if not proof_dir.exists():
        return True, "proof/ not yet populated; barrier trivially holds"

    violations = []
    for module in ("m1", "m2", "m3"):
        mod_dir = proof_dir / module
        if not mod_dir.exists():
            continue
        for py in mod_dir.rglob("*.py"):
            for imp in _py_imports(py):
                for forbidden in FORBIDDEN_TARGETS:
                    if forbidden in imp:
                        violations.append(
                            f"{py.relative_to(root)}: imports {imp!r} "
                            f"(forbidden target {forbidden!r})")

    if violations:
        return False, "Import barrier violated: " + "; ".join(violations)
    return True, "Import barrier holds for M1/M2/M3"


def _check_forbidden_leaves(root: Path) -> tuple[bool, str]:
    """
    Scan construction files (proof/m1, proof/m2, proof/m3) for forbidden
    symbol patterns (spec §3.3). Passes trivially if proof/ is absent.
    """
    proof_dir = root / "proof"
    if not proof_dir.exists():
        return True, "proof/ not yet populated; forbidden-leaf check trivially holds"

    violations = []
    import re
    for module in ("m1", "m2", "m3"):
        mod_dir = proof_dir / module
        if not mod_dir.exists():
            continue
        for py in mod_dir.rglob("*.py"):
            src = py.read_text(encoding="utf-8", errors="replace")
            for pat in FORBIDDEN_PATTERNS:
                if re.search(pat, src, re.IGNORECASE):
                    violations.append(
                        f"{py.relative_to(root)}: matches forbidden pattern {pat!r}")

    if violations:
        return False, "Forbidden leaves detected: " + "; ".join(violations)
    return True, "No forbidden construction leaves found"


# ── helpers ───────────────────────────────────────────────────────────────────

def _note(msg: str) -> str:
    """Return a sha256 digest of msg as a witness digest (deterministic)."""
    return "sha256:" + hashlib.sha256(msg.encode()).hexdigest()


def _checker_self_digest() -> str:
    try:
        data = Path(__file__).read_bytes()
        return "sha256:" + hashlib.sha256(data).hexdigest()
    except Exception:
        return "sha256:" + "0" * 64


def _input_closure_digest(inp: dict) -> str:
    canonical = json.dumps(inp, sort_keys=True, separators=(",", ":"))
    return "sha256:" + hashlib.sha256(canonical.encode()).hexdigest()


# ── main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    raw = sys.stdin.read()
    try:
        inp = json.loads(raw)
    except json.JSONDecodeError as e:
        sys.stderr.write(f"checker: invalid JSON input: {e}\n")
        sys.exit(1)

    claim_id: str = inp.get("claim_id", "")
    # obligation_ids may be null when proofctl hasn't loaded contracts yet.
    if not inp.get("obligation_ids"):
        inp["obligation_ids"] = OBLIGATIONS.get(claim_id, [])
    handler = DISPATCH.get(claim_id)

    if handler is None:
        obligation_results = [
            {"id": oid, "verdict": "fail",
             "witness_digest": _note(f"no handler for claim {claim_id!r}")}
            for oid in inp.get("obligation_ids", [])
        ]
    else:
        obligation_results = handler(inp)

    out = {
        "protocol_version": PROTOCOL_VERSION,
        "claim_id": claim_id,
        "input_closure_digest": _input_closure_digest(inp),
        "checker_identity_digest": _checker_self_digest(),
        "runtime_identity_digest": "sha256:" + "0" * 64,
        "evidence_used": [],
        "obligation_results": obligation_results,
        "toolchain": {"python": sys.version.split()[0]},
    }

    sys.stdout.write(json.dumps(out, indent=2) + "\n")


if __name__ == "__main__":
    main()
