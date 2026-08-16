---
name: project-state
description: Current phase status, proved results, and open obligations in the abc verification kernel
metadata:
  type: project
---

Phase status as of 2026-08-16.

## Proved results

- **ω*=2:** nd ≤ v_max·R trivially. ✓
- **ω*=3:** OB-15 fully proved. Three structural types for R<c triples:
  - (1,1,1): zero-out-Pc construction. Norm ≤ v_max·p₂ ≤ v_max·R^{1/2}.
  - (0,2,1): within-group Pb (unequal vals). Norm ≤ v_max·R^{1/2}.
  - (0,1,2): zero-out larger Pc prime. Norm ≤ v_max·R^{1/2}.
  All 14 ω*=3 R<c triples (c≤5000) verified. Proof committed in OB-15/OB-16.
- **vmax ≥ 3 for ALL R<c triples (NEW, proved 2026-08-16):**
  Proof: vmax≤2 ⟹ a≤Ra², b≤Rb², c≤Rc². WLOG Ra≤Rb.
  (1) R<c≤Rc²: Ra·Rb < Rc.  (2) R<c≤2Rb²: Ra·Rc < 2Rb.
  Multiply: Ra²<2 → Ra=1 (a=1). Then Rb<Rc, Rb·Rc<1+Rb², but Rb·Rc≥Rb²+Rb → Rb<1. ✗.
  Computational confirmation: 5,055,295 triples with vmax≤2, c≤5000 — 0 with R<c.

## Numerical evidence

- c≤5000: 80 R<c triples (14×ω*=3, 53×ω*=4, 12×ω*=5), 0 violations.
- Max construction ratio: 0.28 (ω*=4), 0.54 (ω*=5).
- ω*=3 CONFIRMED-3 in OB-16. ω*=4 open (OB-17).

## Open obligations

- **OB-15 conjecture (ω*≥4):** Strong numerical support, no proof.
  - KEY-4 inequality: q ≤ v_max·R^{1/3} for within-group prime q.
  - With v_max≥3: KEY-4 holds for q≤972 (γ=2, p₁=2,p₂=3) and q≤54 (γ≥3, p₁=2,p₂=3).
  - Remaining open: γ=2, q∈(54,972], v_max=3 from a or b. Computationally: 0 such
    triples found for c≤20,000. Likely closed by Diophantine constraints on a+b=s².
- **OB-16:** ω*=3 CONFIRMED-3. ω*=4 construction proof needed.
- **OB-17:** Targets ω*≥4 uniform proof via KEY-4 + v_max≥3 structure.

## Outsource files ready for external review

- **OB-14:** All lint passes, conditional/unconditional structure clear. Ready.
- **OB-15:** ω*=3 proved inline + vmax≥3 proved; overall conjecture open. Numerical anchors c≤5000.
- **OB-16:** CONFIRMED-3 marked; ω*=4 skeleton with v_max≥3 key lemma.
- **OB-17:** New, targets ω*≥4 proof; vmax≥3 narrows KEY-4 gap to q∈(54,972].

## Key structural theorems proved

1. R<c ⟹ c composite non-squarefree ⟹ v_max ≥ 2.
2. **R<c ⟹ v_max ≥ 3 (NEW, proved 2026-08-16).** Strictly stronger than (1).
3. For ω*=3: nd ≤ v_max·R^{1/2} (proved in all cases).
4. KEY-4 sufficient: q^3 ≤ v_max^3·R ⟹ nd ≤ v_max·R^{1/3} for within-group ω*=4.
5. ω*≤4 for R<c DISPROVED — explicit (1,8191²-1,8191²) counterexample with ω*=6.

**Why:** vmax≥3 proof uses Ra·Rb<Rc and Ra·Rc<2Rb; multiplying gives Ra²<2 so Ra=1,
then Rb<Rc gives Rb·Rc≥Rb²+Rb, contradicting Rb·Rc<1+Rb². KEY-4 with vmax≥3 covers
q≤972 for the dominant p₁p₂=6,γ=2 case (up from q≤288 with vmax≥2).

**How to apply:** Use v_max≥3 in all KEY-4 estimates. The bound 27(p₁p₂)²q replaces
8(p₁p₂)²q throughout OB-16 and OB-17.
