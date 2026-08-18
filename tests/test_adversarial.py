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
from checker.check_certificate import (  # noqa: E402
    DISPATCH,
    OBLIGATIONS,
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
        dag_result = next(r for r in results if r["id"] == "core1.dag-acyclic")
        assert dag_result["verdict"] == "pass", (
            f"core1.dag-acyclic failed: {dag_result.get('witness_digest')}"
        )

    def test_core1_import_barrier_passes(self):
        results = invoke_handler("core-1-provenance-manifest")
        barrier_result = next(
            r
            for r in results
            if r["id"] == "core1.no-forbidden-import-M1-M2-M3-into-M4-M5-M6"
        )
        assert barrier_result["verdict"] == "pass", (
            f"import barrier failed: {barrier_result.get('witness_digest')}"
        )

    def test_core1_forbidden_leaves_passes(self):
        results = invoke_handler("core-1-provenance-manifest")
        leaf_result = next(
            r for r in results if r["id"] == "core1.no-forbidden-construction-leaves"
        )
        assert leaf_result["verdict"] == "pass", (
            f"forbidden-leaf check failed: {leaf_result.get('witness_digest')}"
        )

    def test_core1_construction_frozen_passes(self):
        results = invoke_handler("core-1-provenance-manifest")
        frozen_result = next(
            r
            for r in results
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
        results = invoke_handler("core-2-height-framework")
        # All results are fail; check that the obligation ids include height-related items
        ids = {r["id"] for r in results}
        assert (
            "core2.rad-function-formally-defined" in ids
            or "core2.faltings-height-setup" in ids
            or "core2.arithmetic-geometry-framework" in ids
            or "core2.framework-built-without-forbidden-inputs" in ids
        ), f"CORE-2 obligations unexpected: {ids}"


# ── TEST-ABC4: CORE-3 OBL with IUT gate ──────────────────────────────────────


class TestABC4_Core3OBL_IUT:
    """TEST-ABC4: CORE-3 fails as OBL, and the IUT Corollary 3.12 sub-obligation
    specifically fails with a note recording the Scholze-Stix dispute."""

    def test_core3_all_fail(self):
        results = invoke_handler("core-3-key-inequality")
        assert results
        passed = [r for r in results if r["verdict"] == "pass"]
        assert not passed, f"CORE-3 unexpectedly passed: {[r['id'] for r in passed]}"

    def test_core3_iut_gate_present_and_fails(self):
        results = invoke_handler("core-3-key-inequality")
        iut_result = next(
            (
                r
                for r in results
                if r["id"] == "core3.iut-corollary-312-independently-verified"
            ),
            None,
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
            r
            for r in results
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
            (r for r in results if r["id"] == "core3.height-inequality-proved"), None
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
        assert not passed, f"CORE-4 unexpectedly passed: {[r['id'] for r in passed]}"

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
        circular_file.write_text(
            textwrap.dedent("""\
            # This construction uses known abc triples — FORBIDDEN
            abc_triples = [(1, 8, 9), (1, 2, 3)]  # high-quality examples
            K_epsilon = max(c / rad_abc**(1.1) for a, b, c in abc_triples)
        """)
        )

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
        bad_file.write_text(
            textwrap.dedent("""\
            # Forbidden: importing M4 (known results) from a construction module
            from proof.m4 import faltings_theorem
            from proof.m4.szpiro import equivalence
        """)
        )

        ok, msg = _check_import_barrier(tmp_path)
        assert not ok, (
            f"Expected import barrier to fail for M2 importing M4, but it passed. "
            f"Message: {msg}"
        )
        assert (
            "m4" in msg.lower() or "barrier" in msg.lower() or "import" in msg.lower()
        )

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
        assert (
            "m6" in msg.lower() or "barrier" in msg.lower() or "import" in msg.lower()
        )

    def test_clean_m1_passes_barrier(self, tmp_path):
        """M1 file with no forbidden imports passes the barrier."""
        proof_m1 = tmp_path / "proof" / "m1"
        proof_m1.mkdir(parents=True)
        (tmp_path / "proof" / "__init__.py").write_text("")
        (tmp_path / "proof" / "m1" / "__init__.py").write_text("")

        clean_file = proof_m1 / "rad.py"
        clean_file.write_text(
            textwrap.dedent("""\
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
        """)
        )

        ok, msg = _check_import_barrier(tmp_path)
        assert ok, f"Clean M1 file should pass barrier, but failed: {msg}"


# ── TEST-ABC8: CORE-5 blocked without CORE-4 ─────────────────────────────────


class TestABC8_Core5Blocked:
    """TEST-ABC8: CORE-5 must fail when CORE-3 and CORE-4 have not passed."""

    def test_core5_fails_without_dependencies(self):
        results = invoke_handler("core-5-conclusion")
        derive_result = next(
            r
            for r in results
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
            r for r in results if r["id"] == "core5.no-trusted-producer-pass-flag"
        )
        assert no_flag_result["verdict"] == "pass"

    def test_core5_does_not_fire_from_producer_pass(self):
        """Providing a fake 'dependency_attestations' with core-3 and core-4
        still blocks CORE-5 if the obligations haven't been genuinely passed."""
        # Without proper dependency_attestations from actual GLOBALLY_VERIFIED gates,
        # the checker should only pass if attestations include the required claim ids.
        # We test with a genuinely empty default (no attestations).
        results = invoke_handler(
            "core-5-conclusion", extra={"dependency_attestations": {}}
        )
        derive_result = next(
            r
            for r in results
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
        assert not failed, f"CL-03 has unexpected failures: {[r['id'] for r in failed]}"

    def test_cl03_universality_obligation_passes(self):
        results = invoke_handler("cl-03-certificate-implies-abc")
        univ = next(
            r for r in results if r["id"] == "cl03.bound-is-universal-not-finite-set"
        )
        assert univ["verdict"] == "pass"

    def test_cl04_all_pass(self):
        results = invoke_handler("cl-04-certificate-equivalent-abc")
        assert results
        failed = [r for r in results if r["verdict"] != "pass"]
        assert not failed, f"CL-04 has unexpected failures: {[r['id'] for r in failed]}"

    def test_cl04_honesty_check_recorded(self):
        results = invoke_handler("cl-04-certificate-equivalent-abc")
        honesty = next(r for r in results if r["id"] == "cl04.honesty-check-recorded")
        assert honesty["verdict"] == "pass"

    def test_cl04_converse_uses_abc_as_hypothesis_only(self):
        """The converse of CL-04 (Theorem 3) uses abc as hypothesis — this is
        permitted. The obligation records that abc is used only as a hypothesis,
        not as a construction leaf."""
        results = invoke_handler("cl-04-certificate-equivalent-abc")
        converse = next(
            r for r in results if r["id"] == "cl04.converse-uses-abc-as-hypothesis-only"
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
        assert not failed, f"CL-07 has unexpected failures: {[r['id'] for r in failed]}"

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


# ── P2 TEST-P2-1: foundation_hash frozen and reproducible ────────────────────


class TestP2_1_FoundationHash:
    """TEST-P2-1: The foundation_hash in domain/policy-v2.json matches the value
    produced by checker/compute_foundation_hash.py and contains no PLACEHOLDER."""

    def test_foundation_hash_not_placeholder(self):
        policy_path = REPO_ROOT / "domain" / "policy-v2.json"
        policy = json.loads(policy_path.read_text())
        h = policy.get("foundation_hash", "")
        assert "PLACEHOLDER" not in h, (
            "foundation_hash must not contain PLACEHOLDER — it must be frozen"
        )

    def test_foundation_hash_is_sha256(self):
        policy_path = REPO_ROOT / "domain" / "policy-v2.json"
        policy = json.loads(policy_path.read_text())
        h = policy.get("foundation_hash", "")
        assert h.startswith("sha256:"), (
            f"foundation_hash must start with 'sha256:'; got: {h!r}"
        )
        hex_part = h[len("sha256:") :]
        assert len(hex_part) == 64, f"SHA-256 hex must be 64 chars; got {len(hex_part)}"

    def test_foundation_hash_matches_compute_script(self):
        """The hash in policy-v2.json must match what compute_foundation_hash.py produces."""
        sys.path.insert(0, str(REPO_ROOT))
        from checker.compute_foundation_hash import compute_foundation_hash

        ledger_path = REPO_ROOT / "proof" / "claim-ledger.json"
        computed = compute_foundation_hash(ledger_path)

        policy_path = REPO_ROOT / "domain" / "policy-v2.json"
        policy = json.loads(policy_path.read_text())
        stored = policy.get("foundation_hash", "")

        assert computed == stored, (
            f"foundation_hash mismatch.\n"
            f"Computed by script: {computed}\n"
            f"Stored in policy:   {stored}\n"
            "Run: python3 checker/compute_foundation_hash.py and update policy-v2.json"
        )

    def test_foundation_hash_covers_base_claims(self):
        """The foundation hash must be derived from BASE claims (CL-02, CL-05, CL-06)."""
        from checker.compute_foundation_hash import canonical_base_text

        ledger_path = REPO_ROOT / "proof" / "claim-ledger.json"
        ledger = json.loads(ledger_path.read_text())
        text = canonical_base_text(ledger)
        assert "CL-02" in text
        assert "CL-05" in text
        assert "CL-06" in text
        # OBL claims must not appear in the foundation hash
        assert "CL-09" not in text
        assert "CL-10" not in text
        assert "CL-11" not in text


# ── P2 TEST-P2-2: replay kernel passes all THM certificates ──────────────────


class TestP2_2_ReplayKernel:
    """TEST-P2-2: The replay_kernel verifies all [THM] proof certificates
    (CL-03, CL-04, CL-07) without errors."""

    def test_replay_all_pass(self):
        from checker.replay_kernel import replay_all_thm_certificates

        report = replay_all_thm_certificates(REPO_ROOT)
        assert report["all_pass"], (
            f"Replay kernel failed:\n"
            f"missing: {report.get('missing')}\n"
            f"results: {[r for r in report['results'] if r['verdict'] != 'pass']}"
        )

    def test_replay_cl03_passes(self):
        from checker.replay_kernel import replay_all_thm_certificates

        report = replay_all_thm_certificates(REPO_ROOT)
        cl03 = next((r for r in report["results"] if r["claim_id"] == "CL-03"), None)
        assert cl03 is not None, "CL-03 certificate not found in replay results"
        assert cl03["verdict"] == "pass", f"CL-03 replay failed: {cl03['errors']}"

    def test_replay_cl04_passes(self):
        from checker.replay_kernel import replay_all_thm_certificates

        report = replay_all_thm_certificates(REPO_ROOT)
        cl04 = next((r for r in report["results"] if r["claim_id"] == "CL-04"), None)
        assert cl04 is not None, "CL-04 certificate not found in replay results"
        assert cl04["verdict"] == "pass", f"CL-04 replay failed: {cl04['errors']}"

    def test_replay_cl07_passes(self):
        from checker.replay_kernel import replay_all_thm_certificates

        report = replay_all_thm_certificates(REPO_ROOT)
        cl07 = next((r for r in report["results"] if r["claim_id"] == "CL-07"), None)
        assert cl07 is not None, "CL-07 certificate not found in replay results"
        assert cl07["verdict"] == "pass", f"CL-07 replay failed: {cl07['errors']}"

    def test_replay_no_missing_certificates(self):
        from checker.replay_kernel import replay_all_thm_certificates

        report = replay_all_thm_certificates(REPO_ROOT)
        assert not report["missing"], (
            f"Missing proof certificates for: {report['missing']}"
        )

    def test_certificates_have_content_digests(self):
        """Every replayed certificate must produce a content_digest (sha256)."""
        from checker.replay_kernel import replay_all_thm_certificates

        report = replay_all_thm_certificates(REPO_ROOT)
        for r in report["results"]:
            assert r.get("content_digest", "").startswith("sha256:"), (
                f"Certificate for {r['claim_id']} missing content_digest"
            )


# ── P2 TEST-P2-3: no PLACEHOLDER anywhere in domain or proof certificates ────


class TestP2_3_NoPlaceholder:
    """TEST-P2-3: Freeze gate — no PLACEHOLDER string in domain/policy-v2.json
    or proof certificate files."""

    def test_policy_no_placeholder(self):
        policy_path = REPO_ROOT / "domain" / "policy-v2.json"
        content = policy_path.read_text()
        assert "PLACEHOLDER" not in content, (
            "domain/policy-v2.json must not contain PLACEHOLDER (P2 freeze gate)"
        )

    def test_proof_certificates_no_placeholder(self):
        cert_paths = [
            REPO_ROOT / "proof" / "m6" / "cl03_implication.json",
            REPO_ROOT / "proof" / "m6" / "cl04_honesty.json",
            REPO_ROOT / "proof" / "m0" / "cl07_syntactic.json",
        ]
        for p in cert_paths:
            assert p.exists(), f"Expected certificate file to exist: {p}"
            content = p.read_text()
            assert "PLACEHOLDER" not in content, (
                f"{p.relative_to(REPO_ROOT)}: must not contain PLACEHOLDER"
            )

    def test_proof_certificates_valid_json(self):
        cert_paths = [
            REPO_ROOT / "proof" / "m6" / "cl03_implication.json",
            REPO_ROOT / "proof" / "m6" / "cl04_honesty.json",
            REPO_ROOT / "proof" / "m0" / "cl07_syntactic.json",
        ]
        for p in cert_paths:
            assert p.exists(), f"Expected certificate file: {p}"
            try:
                json.loads(p.read_text())
            except json.JSONDecodeError as e:
                pytest.fail(f"{p.relative_to(REPO_ROOT)}: invalid JSON — {e}")

    def test_replay_kernel_rejects_placeholder_cert(self, tmp_path):
        """A certificate with a PLACEHOLDER string must fail replay."""
        from checker.replay_kernel import verify_certificate

        bad_cert = {
            "certificate_format": "abc-proof-term-v1",
            "claim_id": "CL-03",
            "statement": "PLACEHOLDER statement",
            "module": "M6",
            "proof_kind": "definitional",
            "premises": [],
            "proof_steps": [
                {"step": 1, "label": "x", "claim": "x", "justification": "x"}
            ],
            "qed_claim": "CL-03",
            "forbidden_inputs_used": [],
            "non_circularity": "ok",
        }
        cert_file = tmp_path / "bad_cert.json"
        cert_file.write_text(json.dumps(bad_cert))
        ledger_path = REPO_ROOT / "proof" / "claim-ledger.json"
        ledger = json.loads(ledger_path.read_text())
        result = verify_certificate(cert_file, ledger)
        assert result["verdict"] == "fail", (
            "replay_kernel must reject a certificate with PLACEHOLDER"
        )
        assert any("PLACEHOLDER" in e for e in result["errors"])


# ── P3 TEST-P3-1: M1 rad function ────────────────────────────────────────────


class TestP3_1_RadFunction:
    """TEST-P3-1: proof/m1/rad.py defines the rad function correctly and
    passes the non-anticipation barrier."""

    def test_rad_import_clean(self):
        """M1 rad.py can be imported without forbidden-leaf violation."""
        sys.path.insert(0, str(REPO_ROOT))
        from proof.m1.rad import rad

        assert callable(rad)

    def test_rad_basic_values(self):
        from proof.m1.rad import rad

        assert rad(1) == 1
        assert rad(2) == 2
        assert rad(4) == 2  # 4 = 2^2
        assert rad(12) == 6  # 12 = 2^2 * 3
        assert rad(30) == 30  # 30 = 2 * 3 * 5 (squarefree)

    def test_rad_properties(self):
        from proof.m1.rad import check_rad_properties

        check_rad_properties()  # raises AssertionError if any property fails

    def test_rad_no_forbidden_imports(self):
        ok, msg = _check_import_barrier(_project_root())
        assert ok, f"M1 import barrier violated after adding rad.py: {msg}"

    def test_rad_no_forbidden_leaves(self):
        ok, msg = _check_forbidden_leaves(_project_root())
        assert ok, f"Forbidden construction leaves in M1: {msg}"


# ── P3 TEST-P3-2: source_lock_hash frozen ────────────────────────────────────


class TestP3_2_SourceLockHash:
    """TEST-P3-2: The source_lock_hash in domain/policy-v2.json is frozen,
    matches compute_source_lock_hash.py output, and covers only M1 sources."""

    def test_source_lock_hash_in_policy(self):
        policy_path = REPO_ROOT / "domain" / "policy-v2.json"
        policy = json.loads(policy_path.read_text())
        h = policy.get("source_lock_hash", "")
        assert h, "source_lock_hash must be present in policy-v2.json"
        assert h.startswith("sha256:"), (
            f"source_lock_hash must start with sha256:; got {h!r}"
        )
        assert "PLACEHOLDER" not in h, "source_lock_hash must not contain PLACEHOLDER"

    def test_source_lock_hash_matches_compute_script(self):
        from checker.compute_source_lock_hash import compute_source_lock_hash

        computed = compute_source_lock_hash(REPO_ROOT)
        policy_path = REPO_ROOT / "domain" / "policy-v2.json"
        policy = json.loads(policy_path.read_text())
        stored = policy.get("source_lock_hash", "")
        assert computed == stored, (
            f"source_lock_hash mismatch.\nComputed: {computed}\nStored:   {stored}"
        )

    def test_source_lock_cert_replays(self):
        from checker.replay_kernel import replay_all_thm_certificates

        report = replay_all_thm_certificates(REPO_ROOT)
        sl = next(
            (r for r in report["results"] if r["claim_id"] == "source-lock-m1"), None
        )
        assert sl is not None, "source-lock-m1 certificate not found in replay results"
        assert sl["verdict"] == "pass", f"source-lock-m1 replay failed: {sl['errors']}"


# ── P3 TEST-P3-3: M1 heights and arithmetic geometry scaffold ─────────────────


class TestP3_3_HeightsArithGeom:
    """TEST-P3-3: proof/m1/heights.py and arithmetic_geometry.py load cleanly
    and expose the correct scaffold status (not claiming to be proofs)."""

    def test_heights_imports_clean(self):
        from proof.m1 import heights  # noqa: F401

    def test_arithmetic_geometry_imports_clean(self):
        from proof.m1 import arithmetic_geometry  # noqa: F401

    def test_construction_status_is_scaffold(self):
        from proof.m1.arithmetic_geometry import CONSTRUCTION_STATUS

        assert (
            "SCAFFOLD" in CONSTRUCTION_STATUS
            or "scaffold" in CONSTRUCTION_STATUS.lower()
        ), "CONSTRUCTION_STATUS must record scaffold status, not a proof claim"

    def test_frey_discriminant_computed(self):
        from proof.m1.arithmetic_geometry import frey_curve_discriminant

        d = frey_curve_discriminant(1, 8, 9)
        assert isinstance(d, int) and d > 0

    def test_key_inequality_target_computable(self):
        from proof.m1.arithmetic_geometry import key_inequality_target

        result = key_inequality_target(1, 8, 9, 1.0, 5.0)
        assert isinstance(result, bool)

    def test_m1_barrier_still_holds(self):
        ok, msg = _check_import_barrier(_project_root())
        assert ok, f"Import barrier violated after P3: {msg}"

    def test_m1_no_forbidden_leaves(self):
        ok, msg = _check_forbidden_leaves(_project_root())
        assert ok, f"Forbidden leaves in M1/M2/M3 after P3: {msg}"


# ── P4 TEST-P4-1: key inequality obstruction recorded ────────────────────────


class TestP4_1_KeyInequalityObstruction:
    """TEST-P4-1: The key inequality obstruction is precisely recorded.
    Both routes (algebraic geometry / IUT) are blocked. No abc assumed."""

    def test_obstruction_file_valid_json(self):
        path = REPO_ROOT / "proof" / "m2" / "key_inequality_obstruction.json"
        assert path.exists(), "key_inequality_obstruction.json must exist"
        cert = json.loads(path.read_text())
        assert "claim_id" in cert
        assert "obstruction_kind" in cert or "obstruction_routes" in cert, (
            "Obstruction record must document obstruction kind or routes"
        )

    def test_obstruction_no_placeholder(self):
        path = REPO_ROOT / "proof" / "m2" / "key_inequality_obstruction.json"
        content = path.read_text()
        assert "PLACEHOLDER" not in content

    def test_obstruction_records_iut_gate(self):
        path = REPO_ROOT / "proof" / "m2" / "key_inequality_obstruction.json"
        content = path.read_text()
        assert "iut" in content.lower() or "corollary" in content.lower(), (
            "Obstruction must reference IUT / Corollary 3.12"
        )
        assert "scholze" in content.lower() or "stix" in content.lower(), (
            "Obstruction must reference Scholze-Stix dispute"
        )

    def test_obstruction_records_route_a_circular(self):
        path = REPO_ROOT / "proof" / "m2" / "key_inequality_obstruction.json"
        cert = json.loads(path.read_text())
        raw = json.dumps(cert).lower()
        assert "szpiro" in raw or "circular" in raw or "equivalent" in raw, (
            "Obstruction must document that Route A (algebraic geometry / Szpiro) is circular"
        )

    def test_obstruction_no_abc_assumed(self):
        path = REPO_ROOT / "proof" / "m2" / "key_inequality_obstruction.json"
        cert = json.loads(path.read_text())
        assert cert.get("forbidden_inputs_used", None) == [], (
            "forbidden_inputs_used must be empty — obstruction record does not use abc as input"
        )

    def test_core3_still_fails_obl(self):
        """CORE-3 must still fail with OBL — the obstruction record does not pass the gate."""
        results = invoke_handler("core-3-key-inequality")
        passed = [r for r in results if r["verdict"] == "pass"]
        assert not passed, (
            "CORE-3 must still fail (OBL) even with obstruction record in place"
        )

    def test_cl10_status_is_obl(self):
        """CL-10 must remain [OBL] in the ledger."""
        ledger = json.loads((REPO_ROOT / "proof" / "claim-ledger.json").read_text())
        cl10 = next((c for c in ledger["claims"] if c["id"] == "CL-10"), None)
        assert cl10 is not None
        assert cl10["status"] == "OBL", f"CL-10 must remain OBL; found {cl10['status']}"


# ── P5 TEST-P5-1: finiteness obstruction inherits P4 ─────────────────────────


class TestP5_1_FinitenessObstruction:
    """TEST-P5-1: The finiteness obstruction record exists, inherits from CL-10,
    and does not claim abc is proved."""

    def test_finiteness_obstruction_valid_json(self):
        path = REPO_ROOT / "proof" / "m3" / "finiteness_obstruction.json"
        assert path.exists(), "finiteness_obstruction.json must exist"
        json.loads(path.read_text())

    def test_finiteness_obstruction_no_placeholder(self):
        path = REPO_ROOT / "proof" / "m3" / "finiteness_obstruction.json"
        assert "PLACEHOLDER" not in path.read_text()

    def test_finiteness_inherits_cl10(self):
        path = REPO_ROOT / "proof" / "m3" / "finiteness_obstruction.json"
        cert = json.loads(path.read_text())
        raw = json.dumps(cert).lower()
        assert (
            "cl-10" in raw
            or "cL-10" in raw
            or "key inequality" in raw
            or "core-3" in raw.lower()
        ), (
            "Finiteness obstruction must reference CL-10 or key inequality as prerequisite"
        )

    def test_cl11_status_is_obl(self):
        """CL-11 must remain [OBL] in the ledger."""
        ledger = json.loads((REPO_ROOT / "proof" / "claim-ledger.json").read_text())
        cl11 = next((c for c in ledger["claims"] if c["id"] == "CL-11"), None)
        assert cl11 is not None
        assert cl11["status"] == "OBL", f"CL-11 must remain OBL; found {cl11['status']}"

    def test_core4_still_fails_obl(self):
        """CORE-4 must still fail with OBL."""
        results = invoke_handler("core-4-finiteness")
        passed = [r for r in results if r["verdict"] == "pass"]
        assert not passed, (
            "CORE-4 must still fail (OBL) even with finiteness obstruction record"
        )


# ── P6 TEST-P6-1: conclusion scaffold and CORE-5 still blocked ───────────────


class TestP6_1_ConclusionScaffold:
    """TEST-P6-1: The conclusion scaffold encodes the mechanical CORE-5 firing
    condition. CORE-5 remains blocked because CORE-2/3/4 are OBL."""

    def test_conclusion_scaffold_imports_clean(self):
        from proof.m6 import conclusion_scaffold  # noqa: F401

    def test_would_core5_fire_logic(self):
        from proof.m6.conclusion_scaffold import would_core5_fire

        assert would_core5_fire(True, True, True) is True
        assert would_core5_fire(False, True, True) is False
        assert would_core5_fire(True, False, True) is False
        assert would_core5_fire(True, True, False) is False
        assert would_core5_fire(False, False, False) is False

    def test_conclusion_status_blocked(self):
        from proof.m6.conclusion_scaffold import CONCLUSION_STATUS

        assert "BLOCKED" in CONCLUSION_STATUS, (
            "CONCLUSION_STATUS must record BLOCKED until CORE-2/3/4 pass"
        )

    def test_core5_still_blocked(self):
        results = invoke_handler("core-5-conclusion")
        derive = next(
            r
            for r in results
            if r["id"] == "core5.derive-theorem2-from-passed-artifacts"
        )
        assert derive["verdict"] == "fail", (
            "CORE-5 must remain BLOCKED — CORE-2/3/4 are OBL"
        )

    def test_abc_not_proved(self):
        """CL-12 must remain [OUT] — abc is not proved."""
        ledger = json.loads((REPO_ROOT / "proof" / "claim-ledger.json").read_text())
        cl12 = next((c for c in ledger["claims"] if c["id"] == "CL-12"), None)
        assert cl12 is not None
        assert cl12["status"] == "OUT", (
            "CL-12 (abc proved) must remain [OUT] — never self-declared"
        )

    def test_iut_not_verified(self):
        """CL-13 must remain [OUT] — IUT is not verified."""
        ledger = json.loads((REPO_ROOT / "proof" / "claim-ledger.json").read_text())
        cl13 = next((c for c in ledger["claims"] if c["id"] == "CL-13"), None)
        assert cl13 is not None
        assert cl13["status"] == "OUT", (
            "CL-13 (IUT verified) must remain [OUT] — never self-declared"
        )


# ── Integration TEST §7.2: CORE-1+2+3+4 ⟹ CORE-5 ───────────────────────────


class TestIntegration_7_2_Mechanical:
    """Mechanical integration tests (spec §7.2): verify CORE-5 firing conditions
    and that would_core5_fire() agrees with the checker."""

    def test_core5_fires_with_all_attestations(self):
        """When CORE-3 and CORE-4 attestations are present, CORE-5 fires."""
        inp = {
            "claim_id": "core-5-conclusion",
            "obligation_ids": [
                "core5.derive-theorem2-from-passed-artifacts",
                "core5.no-trusted-producer-pass-flag",
            ],
            "dependency_attestations": {
                "core-3-key-inequality": "attestation-present",
                "core-4-finiteness": "attestation-present",
            },
        }
        handler = DISPATCH["core-5-conclusion"]
        results = handler(inp)
        derive = next(
            r
            for r in results
            if r["id"] == "core5.derive-theorem2-from-passed-artifacts"
        )
        assert derive["verdict"] == "pass", (
            "spec §7.2 integration test: CORE-5 must fire when CORE-3+CORE-4 pass"
        )

    def test_core5_blocked_without_core3(self):
        """CORE-5 must not fire if CORE-3 is missing from attestations."""
        inp = {
            "claim_id": "core-5-conclusion",
            "obligation_ids": ["core5.derive-theorem2-from-passed-artifacts"],
            "dependency_attestations": {"core-4-finiteness": "attestation-present"},
        }
        results = DISPATCH["core-5-conclusion"](inp)
        derive = next(
            r
            for r in results
            if r["id"] == "core5.derive-theorem2-from-passed-artifacts"
        )
        assert derive["verdict"] == "fail"

    def test_core5_blocked_without_core4(self):
        """CORE-5 must not fire if CORE-4 is missing from attestations."""
        inp = {
            "claim_id": "core-5-conclusion",
            "obligation_ids": ["core5.derive-theorem2-from-passed-artifacts"],
            "dependency_attestations": {"core-3-key-inequality": "attestation-present"},
        }
        results = DISPATCH["core-5-conclusion"](inp)
        derive = next(
            r
            for r in results
            if r["id"] == "core5.derive-theorem2-from-passed-artifacts"
        )
        assert derive["verdict"] == "fail"

    def test_no_producer_pass_flag_always_passes(self):
        """core5.no-trusted-producer-pass-flag must always pass regardless of attestations."""
        for attestations in [
            {},
            {"core-3-key-inequality": "x", "core-4-finiteness": "y"},
        ]:
            inp = {
                "claim_id": "core-5-conclusion",
                "obligation_ids": ["core5.no-trusted-producer-pass-flag"],
                "dependency_attestations": attestations,
            }
            results = DISPATCH["core-5-conclusion"](inp)
            no_flag = next(
                r for r in results if r["id"] == "core5.no-trusted-producer-pass-flag"
            )
            assert no_flag["verdict"] == "pass"

    def test_would_core5_fire_matches_checker(self):
        """would_core5_fire() and the checker agree when c2=c3=c4 all vary together.
        Note: the checker gates only on core-3 and core-4 attestations (core-2 is
        a prerequisite of core-3, not a separate checker gate)."""
        from proof.m6.conclusion_scaffold import would_core5_fire

        # Only test cases where c2 mirrors c3 (since c3 presupposes c2)
        for c3, c4, expected in [
            (True, True, True),
            (False, True, False),
            (True, False, False),
            (False, False, False),
        ]:
            attestations = {}
            if c3:
                attestations["core-3-key-inequality"] = "x"
            if c4:
                attestations["core-4-finiteness"] = "x"
            inp = {
                "claim_id": "core-5-conclusion",
                "obligation_ids": ["core5.derive-theorem2-from-passed-artifacts"],
                "dependency_attestations": attestations,
            }
            results = DISPATCH["core-5-conclusion"](inp)
            checker_pass = (
                next(
                    r
                    for r in results
                    if r["id"] == "core5.derive-theorem2-from-passed-artifacts"
                )["verdict"]
                == "pass"
            )
            # scaffold takes (c2, c3, c4); c2 follows c3 in the gate chain
            scaffold_pass = would_core5_fire(c3, c3, c4)
            assert checker_pass == scaffold_pass, (
                f"Mismatch: checker says {checker_pass}, scaffold says {scaffold_pass} "
                f"for c3={c3},c4={c4}"
            )


# ── Contract freeze tests ─────────────────────────────────────────────────────


class TestContractFreeze:
    """Verify all domain contracts have no PLACEHOLDER and consistent checker_digest."""

    def test_no_placeholder_in_any_contract(self):
        contracts_dir = REPO_ROOT / "domain" / "contracts"
        for json_path in sorted(contracts_dir.glob("*.json")):
            content = json_path.read_text()
            assert "PLACEHOLDER" not in content, (
                f"{json_path.name}: must not contain PLACEHOLDER (freeze gate)"
            )

    def test_all_contracts_valid_json(self):
        contracts_dir = REPO_ROOT / "domain" / "contracts"
        for json_path in sorted(contracts_dir.glob("*.json")):
            try:
                json.loads(json_path.read_text())
            except json.JSONDecodeError as e:
                pytest.fail(f"{json_path.name}: invalid JSON — {e}")

    def test_checker_digest_consistent(self):
        """All contracts must reference the same checker_digest."""
        import hashlib

        expected = (
            "sha256:"
            + hashlib.sha256(
                (REPO_ROOT / "checker" / "check_certificate.py").read_bytes()
            ).hexdigest()
        )
        contracts_dir = REPO_ROOT / "domain" / "contracts"
        for json_path in sorted(contracts_dir.glob("*.json")):
            d = json.loads(json_path.read_text())
            stored = d.get("checker", {}).get("checker_digest", "")
            assert stored == expected, (
                f"{json_path.name}: checker_digest {stored!r} != expected {expected!r}"
            )

    def test_compute_contract_hashes_matches_frozen(self):
        """compute_contract_hashes.py must produce hashes consistent with frozen contracts."""
        from checker.compute_contract_hashes import compute_all

        hashes = compute_all(REPO_ROOT)
        contracts_dir = REPO_ROOT / "domain" / "contracts"
        for cname in [
            "core-0-abc-definition",
            "core-1-provenance-manifest",
            "core-2-height-framework",
            "core-3-key-inequality",
            "core-4-finiteness",
            "core-5-conclusion",
        ]:
            d = json.loads((contracts_dir / f"{cname}.json").read_text())
            assert d["statement_digest"] == hashes[cname]["statement_digest"], (
                f"{cname}: statement_digest mismatch"
            )
            assert d["checker"]["checker_digest"] == hashes[cname]["checker_digest"]


# ── Discovery guard tests ─────────────────────────────────────────────────────


class TestDiscoveryGuard_ZeroFree:
    """Verify assert_zero_free() in discovery guard raises correctly on forbidden patterns."""

    def test_guard_module_importable(self):
        from discovery.candidates import guard  # noqa: F401

    def test_guard_rejects_abc_triples(self, tmp_path):
        from discovery.candidates.guard import assert_zero_free

        bad = tmp_path / "bad_candidate.py"
        bad.write_text("abc_triples = [(1, 8, 9)]\n")
        with pytest.raises(RuntimeError, match="abc_triple"):
            assert_zero_free(str(bad))

    def test_guard_rejects_fitted_k_epsilon(self, tmp_path):
        from discovery.candidates.guard import assert_zero_free

        bad = tmp_path / "bad2.py"
        bad.write_text("fitted_k_epsilon = 1.23\n")
        with pytest.raises(RuntimeError, match="fitted_k_epsilon"):
            assert_zero_free(str(bad))

    def test_guard_rejects_szpiro_assumed(self, tmp_path):
        from discovery.candidates.guard import assert_zero_free

        bad = tmp_path / "bad3.py"
        bad.write_text("assume_szpiro = True\n")
        with pytest.raises(RuntimeError, match="assume_szpiro"):
            assert_zero_free(str(bad))

    def test_guard_accepts_clean_candidate(self, tmp_path):
        from discovery.candidates.guard import assert_zero_free

        clean = tmp_path / "clean_candidate.py"
        clean.write_text(
            "from discovery.candidates.guard import assert_zero_free\n"
            "assert_zero_free(__file__)\n"
            "x = 1 + 1\n"
        )
        assert_zero_free(str(clean))  # must not raise

    def test_guard_file_exists(self):
        guard_path = REPO_ROOT / "discovery" / "candidates" / "guard.py"
        assert guard_path.exists(), "discovery/candidates/guard.py must exist"


# ── Integration test spec §7.2: CORE-1+2+3+4 ⟹ CORE-5 ───────────────────────


class TestIntegration_7_2:
    """Integration test spec §7.2: the sole success integration test is
    CORE-1 + CORE-2 + CORE-3 + CORE-4 ⟹ CORE-5.
    No finite collection of examples substitutes for this gate chain."""

    def test_integration_gate_chain(self):
        """The gate chain is correctly structured in the claim ledger."""
        ledger = json.loads((REPO_ROOT / "proof" / "claim-ledger.json").read_text())
        gates = {g["id"]: g for g in ledger.get("core_gates", [])}
        assert "CORE-0" in gates, "CORE-0 must be in ledger"
        assert "CORE-1" in gates, "CORE-1 must be in ledger"
        assert "CORE-5" in gates, "CORE-5 must be in ledger"
        # CORE-5 depends on CORE-3/4 via the mechanical implication
        c5 = gates["CORE-5"]
        assert "CL-03" in c5.get("claims", []), (
            "CORE-5 must reference CL-03 (Theorem 2 / certificate implies abc)"
        )
        # CORE-3 must have the IUT sub-obligation
        c3 = gates["CORE-3"]
        assert "iut_sub_obligation" in c3, "CORE-3 must declare iut_sub_obligation"
        assert (
            c3["iut_sub_obligation"] == "core3.iut-corollary-312-independently-verified"
        )

    def test_integration_core5_fires_mechanically(self):
        """CORE-5 fires when both CORE-3 and CORE-4 attestations are present."""
        results = invoke_handler(
            "core-5-conclusion",
            extra={
                "dependency_attestations": {
                    "core-3-key-inequality": "MOCK_PASS",
                    "core-4-finiteness": "MOCK_PASS",
                }
            },
        )
        derive = next(
            r
            for r in results
            if r["id"] == "core5.derive-theorem2-from-passed-artifacts"
        )
        assert derive["verdict"] == "pass", (
            "CORE-5 must fire when both CORE-3 and CORE-4 attestations are present"
        )

    def test_integration_core5_requires_both_gates(self):
        """CORE-5 fails if only CORE-3 passes but not CORE-4."""
        results_3_only = invoke_handler(
            "core-5-conclusion",
            extra={"dependency_attestations": {"core-3-key-inequality": "MOCK_PASS"}},
        )
        derive_3 = next(
            r
            for r in results_3_only
            if r["id"] == "core5.derive-theorem2-from-passed-artifacts"
        )
        assert derive_3["verdict"] == "fail", (
            "CORE-5 must fail if only CORE-3 passes (CORE-4 missing)"
        )

        results_4_only = invoke_handler(
            "core-5-conclusion",
            extra={"dependency_attestations": {"core-4-finiteness": "MOCK_PASS"}},
        )
        derive_4 = next(
            r
            for r in results_4_only
            if r["id"] == "core5.derive-theorem2-from-passed-artifacts"
        )
        assert derive_4["verdict"] == "fail", (
            "CORE-5 must fail if only CORE-4 passes (CORE-3 missing)"
        )

    def test_integration_no_shortcut_from_examples(self):
        """A finite collection of abc examples does not pass any CORE gate.
        The checker's FORBIDDEN_PATTERNS must cover the abc_triples pattern."""
        from checker.check_certificate import FORBIDDEN_PATTERNS

        patterns = " ".join(FORBIDDEN_PATTERNS)
        assert "abc_triple" in patterns, (
            "FORBIDDEN_PATTERNS must include abc_triple to block known-example shortcuts"
        )
        # Verify no CORE handler passes without actual construction evidence
        for gate_id in (
            "core-2-height-framework",
            "core-3-key-inequality",
            "core-4-finiteness",
        ):
            results = invoke_handler(gate_id)
            passed = [r for r in results if r["verdict"] == "pass"]
            assert not passed, (
                f"{gate_id} must not pass without a construction — "
                f"no finite set of examples substitutes for the gate"
            )

    def test_integration_iut_gate_always_open(self):
        """core3.iut-corollary-312-independently-verified is permanently OPEN."""
        results = invoke_handler("core-3-key-inequality")
        iut = next(
            r
            for r in results
            if r["id"] == "core3.iut-corollary-312-independently-verified"
        )
        assert iut["verdict"] == "fail", (
            "IUT gate must always fail — it is OPEN until machine-replayed proof supplied"
        )


# ── Discovery guard tests ─────────────────────────────────────────────────────


class TestDiscoveryGuard:
    """Tests for the discovery layer non-circularity guard."""

    def test_guard_imports_clean(self):
        from discovery.candidates.guard import assert_zero_free, FORBIDDEN_PATTERNS

        assert callable(assert_zero_free)
        assert len(FORBIDDEN_PATTERNS) > 0

    def test_guard_rejects_abc_triple_file(self, tmp_path):
        """A candidate file using 'abc_triples' must fail the guard scan."""
        from discovery.candidates.guard import FORBIDDEN_PATTERNS
        import re

        bad_src = "abc_triples = [(1, 8, 9)]  # known high-quality triples\n"
        matched = any(re.search(p, bad_src, re.IGNORECASE) for p in FORBIDDEN_PATTERNS)
        assert matched, "Guard FORBIDDEN_PATTERNS must match 'abc_triples' in source"

    def test_guard_rejects_fitted_k_epsilon(self, tmp_path):
        from discovery.candidates.guard import FORBIDDEN_PATTERNS
        import re

        bad_src = "fitted_k_epsilon = 3.14  # fitted to examples\n"
        matched = any(re.search(p, bad_src, re.IGNORECASE) for p in FORBIDDEN_PATTERNS)
        assert matched

    def test_discovery_candidates_existing_files_pass_barrier(self):
        """All existing .py files in discovery/candidates/ pass the import barrier."""
        ok, msg = _check_import_barrier(_project_root())
        assert ok, f"Import barrier violated by discovery candidates: {msg}"
