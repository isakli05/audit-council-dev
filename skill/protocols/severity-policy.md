# Protocol: Severity Policy — spec §14

Severity reflects impact, not rhetorical intensity. These definitions are embedded in the
Audit Contract's `severity_definitions` and are binding on BOTH models.

## Definitions

- CRITICAL — catastrophic security/data/correctness/business failure; a realistic trigger
  path; broad or irreversible impact (e.g., auth bypass, data loss, silent corruption
  reachable in normal operation).
- HIGH — major user/system/security correctness failure; significant scope; meaningful
  production impact.
- MEDIUM — real defect or requirement breach, but constrained blast radius or a workable
  workaround exists.
- LOW — limited correctness/maintainability/reliability issue; low immediate impact.
- INFO — observation, inconsistency, or improvement note that is not itself a defect.

## Calibration rules

- A finding may not be labeled CRITICAL because it "sounds concerning": CRITICAL requires
  a concrete, realistic failure scenario (`failure_scenario` field) and an impact path
  that survives scrutiny.
- Theoretical issues requiring unrealistic preconditions (attacker already controls X,
  pathological input that valid callers never produce) cap at MEDIUM and lower confidence.
- Severity without a requirement basis: if the "expected" behavior is not required by an
  authoritative source, the finding is at most INFO unless it violates a stated
  acceptance criterion.
- Severity is about the defect's impact in scope; scope exclusions from the contract
  remove the finding entirely, not merely lower it.
- Cross-examination MUST explicitly recalibrate severity: every challenge reviews severity
  against these definitions and records `severity_recalibration` where the original was
  miscalibrated (up or down).
- Adjudication may settle a severity divergence on evidence; the final report uses the
  adjudicated severity and preserves the original divergence in provenance/notes.

Confidence (HIGH/MEDIUM/LOW) is assigned per evidence-policy calibration and is
independent of severity: a CRITICAL-severity hypothesis with no OBSERVED_FACT support is
confidence LOW and cannot be CONFIRMED.
