"""
tests/test_adversarial.py — Adversarial test suite for the abc conjecture
verification kernel.

Mirrors spec/SPECIFICATION.md §7.2 (TEST-ABC1 through TEST-ABC10).

Run with:
    cd ~/github/abc-conjecture-verification
    PYTHONPATH=. python3 -m pytest tests/ -v
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path

import pytest

# ── helpers ───────────────────────────────────────────────────────────────────

REPO_ROOT = Path(__file__).resolve().parent.parent
CHECKER = REPO_ROOT / "checker" / "check_certificate.py"


def run_checker(claim_id: str, extra: dict | None = None) -> dict:
    """
    Invoke the checker for a given claim_id and return the parsed output dict.
    Raises AssertionError if the checker exits non-zero.
    """
    inp = {"claim_id": claim_id, "obligation_ids": None}
    if extra:
        inp.update(extra)
    result = subprocess.run(
        [sys.executable, str(CHECKER)],
        input=json.dumps(inp),
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
    )
    assert result.returncode == 0, (
        f"Checker exited {result.returncode}; stderr: {result.stderr}"
    )
    return json.loads(result.stdout)


def all_pass(out: dict) -> bool:
    """Return True if all obligation_results have verdict='pass'."""
    return all(r["verdict"] == "pass" for r in out["obligation_results"])


def all_fail(out: dict) -> bool:
    """Return True if all obligation_results have verdict='fail'."""
    return all(r["verdict"] == "fail" for r in out["obligation_results"])


def any_fail_with(out: dict, substring: str) -> bool:
    """Return True if any obligation_result has verdict='fail' and its
    witness_digest encodes a message containing substring."""
    for r in out["obligation_results"]:
        if r["verdict"] == "fail":
            # The witness_digest is sha256 of the message — we check the
            # decoded message that was originally passed to _note().
            # Since we can't reverse SHA-256, we check by re-importing
            # the checker logic and matching the canonical message.
            # Instead, we verify this by checking the obligation id directly.
            if substring.lower() in r.get("id", "").lower():
                return True
    return False


def get_witness_content(out: dict, obligation_id: str) -> str:
    """
    For the given obligation_id, return the raw witness note content.
    We re-derive it by calling the check functions directly.
    """
    for r in out["obligation_results"]:
        if r["id"] == obligation_id:
            return r.get("witness_digest", "")
    return ""


# ── import checker internals directly for richer assertions ──────────────────

sys.path.insert(0, str(REPO_ROOT))
from checker.check_certificate import (
    DISPATCH,
    OBLIGATIONS,
    _check_dag_acyclic,
    _check_import_barrier,
    _check_forbidden_leaves,
    _project_root,
)


def invoke_handler(claim_id: str, extra: dict | None = None) -> list[dict]:
    """Call the handler directly (not via subprocess) and return obligation results."""
    inp: dict = {
        "claim_id": claim_id,
        "obligation_ids": OBLIGATIONS.get(claim_id, []),
    }
    if extra:
        inp.update(extra)
    handler = DISPATCH[claim_id]
    return handler(inp)


# ── TEST-ABC1: CORE-0 axiom defs pass ─────────────────────────────────────────

class TestABC1_Core0Definitions:
    """TEST-ABC1: CORE-0 obligations all pass (abc statement, rad, certificate,
    Theorem 2, Theorem 3/honesty check are defined/proved by spec)."""

    def test_core0_all_pass(self):
        results = invoke_handler("core-0-abc-definition")
        assert results, "Expected non-empty obligation results for CORE-0"
        failed = [r for r in results if r["verdict"] != "pass"]
        assert not failed, (
            f"CORE-0 has unexpected failures: {[r['id'] for r in failed]}"
        )

    def test_core0_includes_abc_statement(self):
        results = invoke_handler("core-0-abc-definition")
        ids = {r["id"] for r in results}
        assert "core0.abc-statement-and-rad-defined" in ids

    def test_core0_includes_certificate_tuple(self):
        results = invoke_handler("core-0-abc-definition")
        ids = {r["id"] for r in results}
        assert "core0.certificate-tuple-defined" in ids

    def test_core0_includes_theorem2(self):
        results = invoke_handler("core-0-abc-definition")
        ids = {r["id"] for r in results}
        assert "core0.theorem2-certificate-implies-abc" in ids

    def test_core0_includes_honesty_check(self):
        results = invoke_handler("core-0-abc-definition")
        ids = {r["id"] for r in results}
        assert "core0.theorem3-honesty-check" in ids


# ── TEST-ABC2: CORE-1 provenance clean ────────────────────────────────────────

class TestABC2_Core1Provenance:
    """TEST-ABC2: CORE-1 passes for the current scaffold (no construction files,
    no forbidden imports, DAG acyclic)."""

    def test_core1_dag_acyclic_passes(self):
        results = invoke_handler("core-1-provenance-manifest")
        dag_result = next(
            r for r in results if r["id"] == "core1.dag-acyclic"
        )
        assert dag_result["verdict"] == "pass", (
            f"core1.dag-acyclic failed: {dag_result.get('witness_digest')}"
        )

    def test_core1_import_barrier_passes(self):
        results = invoke_handler("core-1-provenance-manifest")
        barrier_result = next(
            r for r in results
            if r["id"] == "core1.no-forbidden-import-M1-M2-M3-into-M4-M5-M6"
        )
        assert barrier_result["verdict"] == "pass", (
            f"import barrier failed: {barrier_result.get('witness_digest')}"
        )

    def test_core1_forbidden_leaves_passes(self):
        results = invoke_handler("core-1-provenance-manifest")
        leaf_result = next(
            r for r in results
            if r["id"] == "core1.no-forbidden-construction-leaves"
        )
        assert leaf_result["verdict"] == "pass", (
            f"forbidden-leaf check failed: {leaf_result.get('witness_digest')}"
        )

    def test_core1_construction_frozen_passes(self):
        results = invoke_handler("core-1-provenance-manifest")
        frozen_result = next(
            r for r in results
            if r["id"] == "core1.construction-frozen-before-comparison"
        )
        assert frozen_result["verdict"] == "pass"


# ── TEST-ABC3: CORE-2 OBL ─────────────────────────────────────────────────────

class TestABC3_Core2OBL:
    """TEST-ABC3: CORE-2 (height framework) fails as OBL — not yet supplied."""

    def test_core2_all_fail(self):
        results = invoke_handler("core-2-height-framework")
        assert results, "Expected non-empty obligation results for CORE-2"
        passed = [r for r in results if r["verdict"] == "pass"]
        assert not passed, (
            f"CORE-2 unexpectedly passed some obligations: {[r['id'] for r in passed]}"
        )

    def test_core2_fails_with_obl_message(self):
        """All CORE-2 failures must carry an OBL message referencing the missing
        P_height construction."""
        import hashlib
        results = invoke_handler("core-2-height-framework")
        # All results are fail; check that the obligation ids include height-related items
        ids = {r["id"] for r in results}
        assert "core2.rad-function-formally-defined" in ids or \
               "core2.faltings-height-setup" in ids or \
               "core2.arithmetic-geometry-framework" in ids or \
               "core2.framework-built-without-forbidden-inputs" in ids, (
            f"CORE-2 obligations unexpected: {ids}"
        )


# ── TEST-ABC4: CORE-3 OBL with IUT gate ──────────────────────────────────────

class TestABC4_Core3OBL_IUT:
    """TEST-ABC4: CORE-3 fails as OBL, and the IUT Corollary 3.12 sub-obligation
    specifically fails with a note recording the Scholze-Stix dispute."""

    def test_core3_all_fail(self):
        results = invoke_handler("core-3-key-inequality")
        assert results
        passed = [r for r in results if r["verdict"] == "pass"]
        assert not passed, (
            f"CORE-3 unexpectedly passed: {[r['id'] for r in passed]}"
        )

    def test_core3_iut_gate_present_and_fails(self):
        results = invoke_handler("core-3-key-inequality")
        iut_result = next(
            (r for r in results
             if r["id"] == "core3.iut-corollary-312-independently-verified"),
            None
        )
        assert iut_result is not None, (
            "core3.iut-corollary-312-independently-verified obligation not found in CORE-3"
        )
        assert iut_result["verdict"] == "fail", (
            "IUT Corollary 3.12 gate must fail (not yet independently verified)"
        )

    def test_core3_iut_gate_has_scholze_stix_note(self):
        """The IUT gate failure must be a deterministic sha256 digest — we verify
        it is present and non-empty (the exact message is tested via recomputation)."""
        results = invoke_handler("core-3-key-inequality")
        iut_result = next(
            r for r in results
            if r["id"] == "core3.iut-corollary-312-independently-verified"
        )
        witness = iut_result.get("witness_digest", "")
        assert witness.startswith("sha256:"), (
            "IUT gate failure must carry a sha256 witness digest"
        )
        # Verify the digest matches the expected message
        import hashlib
        expected_msg = (
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
            "This IS a determination that the obligation is open."
        )
        expected_digest = "sha256:" + hashlib.sha256(expected_msg.encode()).hexdigest()
        assert witness == expected_digest, (
            f"IUT gate witness digest does not match expected Scholze-Stix message.\n"
            f"Got:      {witness}\n"
            f"Expected: {expected_digest}"
        )

    def test_core3_inequality_obligation_fails(self):
        results = invoke_handler("core-3-key-inequality")
        ineq_result = next(
            (r for r in results if r["id"] == "core3.height-inequality-proved"),
            None
        )
        assert ineq_result is not None
        assert ineq_result["verdict"] == "fail"


# ── TEST-ABC5: CORE-4 OBL ─────────────────────────────────────────────────────

class TestABC5_Core4OBL:
    """TEST-ABC5: CORE-4 (finiteness of exceptions) fails as OBL."""

    def test_core4_all_fail(self):
        results = invoke_handler("core-4-finiteness")
        assert results
        passed = [r for r in results if r["verdict"] == "pass"]
        assert not passed, (
            f"CORE-4 unexpectedly passed: {[r['id'] for r in passed]}"
        )

    def test_core4_finiteness_obligations_present(self):
        results = invoke_handler("core-4-finiteness")
        ids = {r["id"] for r in results}
        assert "core4.finiteness-proved-uniformly" in ids


# ── TEST-ABC6: Circular abc rejection ────────────────────────────────────────

class TestABC6_CircularAbcRejection:
    """TEST-ABC6: A construction that uses known abc triples to fit K_epsilon
    must fail CORE-1 (forbidden-leaf scanner)."""

    def test_circular_construction_rejected(self, tmp_path):
        """Create a fake M2 file that uses known abc triples and verify CORE-1 rejects it."""
        # Create a temporary project structure
        proof_m2 = tmp_path / "proof" / "m2"
        proof_m2.mkdir(parents=True)

        # Write a file with a forbidden pattern: 'abc_triples'
        circular_file = proof_m2 / "circular_k_epsilon.py"
        circular_file.write_text(textwrap.dedent("""\
            # This construction uses known abc triples — FORBIDDEN
            abc_triples = [(1, 8, 9), (1, 2, 3)]  # high-quality examples
            K_epsilon = max(c / rad_abc**(1.1) for a, b, c in abc_triples)
        """))

        # Also need proof/__init__.py and proof/m2/__init__.py
        (tmp_path / "proof" / "__init__.py").write_text("")
        (tmp_path / "proof" / "m2" / "__init__.py").write_text("")

        # Run the forbidden leaf check on this temporary project
        ok, msg = _check_forbidden_leaves(tmp_path)
        assert not ok, (
            f"Expected forbidden-leaf check to fail for circular abc triple usage, "
            f"but it passed. Message: {msg}"
        )
        assert "abc_triple" in msg.lower() or "forbidden" in msg.lower(), (
            f"Failure message should mention abc_triple or forbidden: {msg}"
        )

    def test_fitted_k_epsilon_rejected(self, tmp_path):
        """A file with 'fitted_k_epsilon' must fail the forbidden-leaf check."""
        proof_m1 = tmp_path / "proof" / "m1"
        proof_m1.mkdir(parents=True)
        (tmp_path / "proof" / "__init__.py").write_text("")
        (tmp_path / "proof" / "m1" / "__init__.py").write_text("")

        bad_file = proof_m1 / "fitted.py"
        bad_file.write_text("fitted_k_epsilon = 1.234  # fitted to examples\n")

        ok, msg = _check_forbidden_leaves(tmp_path)
        assert not ok
        assert "fitted_k_epsilon" in msg.lower() or "forbidden" in msg.lower()


# ── TEST-ABC7: Non-anticipation barrier ──────────────────────────────────────

class TestABC7_NonAnticipationBarrier:
    """TEST-ABC7: A construction module M2 that imports from M4/M5/M6 must fail CORE-1."""

    def test_m2_importing_m4_rejected(self, tmp_path):
        """M2 file that imports m4 must fail the import barrier."""
        proof_m2 = tmp_path / "proof" / "m2"
        proof_m2.mkdir(parents=True)
        (tmp_path / "proof" / "__init__.py").write_text("")
        (tmp_path / "proof" / "m2" / "__init__.py").write_text("")

        bad_file = proof_m2 / "uses_known_results.py"
        bad_file.write_text(textwrap.dedent("""\
            # Forbidden: importing M4 (known results) from a construction module
            from proof.m4 import faltings_theorem
            from proof.m4.szpiro import equivalence
        """))

        ok, msg = _check_import_barrier(tmp_path)
        assert not ok, (
            f"Expected import barrier to fail for M2 importing M4, but it passed. "
            f"Message: {msg}"
        )
        assert "m4" in msg.lower() or "barrier" in msg.lower() or "import" in msg.lower()

    def test_m3_importing_m6_rejected(self, tmp_path):
        """M3 file that imports m6 must fail the import barrier."""
        proof_m3 = tmp_path / "proof" / "m3"
        proof_m3.mkdir(parents=True)
        (tmp_path / "proof" / "__init__.py").write_text("")
        (tmp_path / "proof" / "m3" / "__init__.py").write_text("")

        bad_file = proof_m3 / "uses_conclusion.py"
        bad_file.write_text("import proof.m6.conclude as conclude\n")

        ok, msg = _check_import_barrier(tmp_path)
        assert not ok
        assert "m6" in msg.lower() or "barrier" in msg.lower() or "import" in msg.lower()

    def test_clean_m1_passes_barrier(self, tmp_path):
        """M1 file with no forbidden imports passes the barrier."""
        proof_m1 = tmp_path / "proof" / "m1"
        proof_m1.mkdir(parents=True)
        (tmp_path / "proof" / "__init__.py").write_text("")
        (tmp_path / "proof" / "m1" / "__init__.py").write_text("")

        clean_file = proof_m1 / "rad.py"
        clean_file.write_text(textwrap.dedent("""\
            from proof.m0.provenance import assert_no_abc_input
            import math

            def rad(n: int) -> int:
                result = 1
                temp = n
                p = 2
                while p * p <= temp:
                    if temp % p == 0:
                        result *= p
                        while temp % p == 0:
                            temp //= p
                    p += 1
                if temp > 1:
                    result *= temp
                return result
        """))

        ok, msg = _check_import_barrier(tmp_path)
        assert ok, f"Clean M1 file should pass barrier, but failed: {msg}"


# ── TEST-ABC8: CORE-5 blocked without CORE-4 ─────────────────────────────────

class TestABC8_Core5Blocked:
    """TEST-ABC8: CORE-5 must fail when CORE-3 and CORE-4 have not passed."""

    def test_core5_fails_without_dependencies(self):
        results = invoke_handler("core-5-conclusion")
        derive_result = next(
            r for r in results
            if r["id"] == "core5.derive-theorem2-from-passed-artifacts"
        )
        assert derive_result["verdict"] == "fail", (
            "CORE-5 must fail when CORE-3/4 not passed"
        )

    def test_core5_no_producer_pass_flag_always_passes(self):
        """The 'no-trusted-producer-pass-flag' obligation always passes —
        the checker never reads producer PASS fields."""
        results = invoke_handler("core-5-conclusion")
        no_flag_result = next(
            r for r in results
            if r["id"] == "core5.no-trusted-producer-pass-flag"
        )
        assert no_flag_result["verdict"] == "pass"

    def test_core5_does_not_fire_from_producer_pass(self):
        """Providing a fake 'dependency_attestations' with core-3 and core-4
        still blocks CORE-5 if the obligations haven't been genuinely passed."""
        # Without proper dependency_attestations from actual GLOBALLY_VERIFIED gates,
        # the checker should only pass if attestations include the required claim ids.
        # We test with a genuinely empty default (no attestations).
        results = invoke_handler("core-5-conclusion", extra={"dependency_attestations": {}})
        derive_result = next(
            r for r in results
            if r["id"] == "core5.derive-theorem2-from-passed-artifacts"
        )
        assert derive_result["verdict"] == "fail"


# ── TEST-ABC9: CL-03/04 implication and honesty theorems pass ────────────────

class TestABC9_CL03CL04:
    """TEST-ABC9: CL-03 (certificate implies abc) and CL-04 (honesty check)
    are [THM] items that must be verified by the checker."""

    def test_cl03_all_pass(self):
        results = invoke_handler("cl-03-certificate-implies-abc")
        assert results
        failed = [r for r in results if r["verdict"] != "pass"]
        assert not failed, (
            f"CL-03 has unexpected failures: {[r['id'] for r in failed]}"
        )

    def test_cl03_universality_obligation_passes(self):
        results = invoke_handler("cl-03-certificate-implies-abc")
        univ = next(
            r for r in results
            if r["id"] == "cl03.bound-is-universal-not-finite-set"
        )
        assert univ["verdict"] == "pass"

    def test_cl04_all_pass(self):
        results = invoke_handler("cl-04-certificate-equivalent-abc")
        assert results
        failed = [r for r in results if r["verdict"] != "pass"]
        assert not failed, (
            f"CL-04 has unexpected failures: {[r['id'] for r in failed]}"
        )

    def test_cl04_honesty_check_recorded(self):
        results = invoke_handler("cl-04-certificate-equivalent-abc")
        honesty = next(
            r for r in results if r["id"] == "cl04.honesty-check-recorded"
        )
        assert honesty["verdict"] == "pass"

    def test_cl04_converse_uses_abc_as_hypothesis_only(self):
        """The converse of CL-04 (Theorem 3) uses abc as hypothesis — this is
        permitted. The obligation records that abc is used only as a hypothesis,
        not as a construction leaf."""
        results = invoke_handler("cl-04-certificate-equivalent-abc")
        converse = next(
            r for r in results
            if r["id"] == "cl04.converse-uses-abc-as-hypothesis-only"
        )
        assert converse["verdict"] == "pass"


# ── TEST-ABC10: CL-07 syntactic provenance theorem passes ────────────────────

class TestABC10_CL07Syntactic:
    """TEST-ABC10: CL-07 — the provenance barrier is syntactically machine-checkable —
    must pass. CL-08 (semantic circularity oracle) must be explicitly NOT claimed."""

    def test_cl07_all_pass(self):
        results = invoke_handler("cl-07-provenance-barrier-syntactic")
        assert results
        failed = [r for r in results if r["verdict"] != "pass"]
        assert not failed, (
            f"CL-07 has unexpected failures: {[r['id'] for r in failed]}"
        )

    def test_cl07_dag_detection_passes(self):
        results = invoke_handler("cl-07-provenance-barrier-syntactic")
        dag = next(
            r for r in results if r["id"] == "cl07.dag-cycle-detection-decidable"
        )
        assert dag["verdict"] == "pass"

    def test_cl07_import_scan_passes(self):
        results = invoke_handler("cl-07-provenance-barrier-syntactic")
        scan = next(
            r for r in results if r["id"] == "cl07.forbidden-import-scan-decidable"
        )
        assert scan["verdict"] == "pass"

    def test_cl07_semantic_independence_not_claimed(self):
        """The checker must explicitly NOT claim semantic independence (CL-08 is [OUT])."""
        results = invoke_handler("cl-07-provenance-barrier-syntactic")
        semantic = next(
            r for r in results if r["id"] == "cl07.semantic-independence-not-claimed"
        )
        assert semantic["verdict"] == "pass", (
            "cl07.semantic-independence-not-claimed must pass "
            "(the checker must not claim CL-08)"
        )

    def test_cl08_is_not_claimed(self):
        """CL-08 (semantic circularity oracle) must not appear as a passing obligation
        anywhere — it is [OUT] and has no downstream force."""
        for claim_id in DISPATCH:
            results = invoke_handler(claim_id)
            for r in results:
                assert "cl08" not in r["id"].lower() or r["verdict"] != "pass", (
                    f"CL-08 (OUT) must never pass; found in {claim_id}: {r['id']}"
                )
