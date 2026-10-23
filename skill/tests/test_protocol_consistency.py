#!/usr/bin/env python3
"""AUCDEV-009 — protocol reconciliation regressions (2026-10-23).

Aligns the three EDITED instruction surfaces (protocols/failure-and-resume.md,
SKILL.md, PUBLIC-CONTRACT.md) with the label-specific completeness matrix
adopted as the shared AUCDEV-004/009 policy (COMPLETENESS_MANDATORY_PHASES in
scripts/state_store.py — the normative reference), and extracts + validates
every v2 citation example/fragment across the FIVE instruction surfaces (the
three above plus the read-only citation sources protocols/evidence-policy.md
and prompts/codex-cross-examine-opus.md).

Coverage: the completeness truth table and its per-surface per-label
definition derivation; missing-mandatory rejection and quota-omission label
eligibility (pure matrix) vs. actual transition authority (explicit provenance,
dedicated adjudication mechanism); exact-session, integrity-immutability and
environment no-verdict semantics across the three surfaces; resume-check
schema-gate byte immutability; the scoped citation extraction (fenced full
objects, fenced key/value fragments, inline line_ranges keys, standalone
range-object fragments incl. the documented N placeholder — unhandled
constructs in these forms are reported, never silently dropped); admission
range-order gating; and one in-memory v1 fixture migration regression.
CLI-level finalize refusals, byte-tamper exit 8 and the broader v1 migration
suite remain owned by test_b001_b004_remediation, test_resume.py and
test_line_ranges_v2 / test_migration_compat.

Zero model inference; fully offline.
"""
from __future__ import annotations

import argparse
import contextlib
import io
import json
import os
import re
import sys
import tempfile
import unittest
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(HERE)
SCRIPTS = os.path.join(SKILL_DIR, "scripts")
SCHEMAS = Path(SKILL_DIR) / "schemas"
sys.path.insert(0, SCRIPTS)
sys.path.insert(0, HERE)

# AUCDEV-024 hermeticity: an ambient host Claude model redirect (e.g.
# ANTHROPIC_MODEL) must never gate these run-lifecycle tests — the ambient
# conflict gate itself has dedicated tests that set these vars explicitly.
import model_selection  # noqa: E402
for _var in model_selection.CLAUDE_SELECTION_ENV_VARS:
    os.environ.pop(_var, None)
# AUCDEV024-CR-IMPL-002 hermeticity: pin the observable per-turn effective
# effort to the audit-default Auditor-A effort, like the sibling suites.
os.environ[model_selection.CLAUDE_EFFECTIVE_EFFORT_ENV] = \
    model_selection.DEFAULT_EFFORT["opus"]

import audit_council  # noqa: E402
import codex_runner  # noqa: E402
import state_store  # noqa: E402
import wire_adapter  # noqa: E402
import evidence_migration as em  # noqa: E402

import test_line_ranges_v2 as lrv  # noqa: E402
from test_qx_stabilization import make_repo, make_run  # noqa: E402

FR = "protocols/failure-and-resume.md"
SKILL = "SKILL.md"
PC = "PUBLIC-CONTRACT.md"
EP = "protocols/evidence-policy.md"
CX = "prompts/codex-cross-examine-opus.md"
XE = "protocols/cross-examination.md"
EDITED_SURFACES = (FR, SKILL, PC)
FIVE_SURFACES = EDITED_SURFACES + (EP, CX)
CW_RU = "COMPLETE_WITH_RESIDUAL_UNCERTAINTY"
NORMATIVE = state_store.COMPLETENESS_MANDATORY_PHASES


def surface_text(rel: str) -> str:
    with open(os.path.join(SKILL_DIR, rel), encoding="utf-8") as fh:
        return fh.read()


def normalized(rel: str) -> str:
    """Whitespace-collapsed surface text (pins survive line wrapping)."""
    return re.sub(r"\s+", " ", surface_text(rel))


# ---------------------------------------------------------------------------
# citation extraction for its scoped forms: complete line_ranges VALUES
# (grouping kept) from fenced full JSON objects, fenced key/value fragments
# (wrapped in braces) and inline `"line_ranges":` key forms; plus standalone
# range-object fragments outside fences (the documented N placeholder is
# materialized to a deterministic integer, any other keys/shape preserved).
# Malformed values and unparseable constructs are REPORTED, never silently
# dropped. Origins carry surface + fence/match index provenance.
# ---------------------------------------------------------------------------
FENCE_RE = re.compile(r"```[a-zA-Z]*\n(.*?)```", re.DOTALL)
LINE_RANGES_KEY_RE = re.compile(r'"line_ranges"\s*:\s*')
RANGE_OBJ_RE = re.compile(r'\{[^{}]*"start"[^{}]*\}')
TEMPLATE_N = 2  # deterministic materialization of the documented placeholder


def _walk_line_ranges_values(node, out):
    """Collect the value under EVERY `line_ranges` key, any depth, any type."""
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "line_ranges":
                out.append(value)
            else:
                _walk_line_ranges_values(value, out)
    elif isinstance(node, list):
        for item in node:
            _walk_line_ranges_values(item, out)


def extract_citations(text: str):
    """-> (values, problems, fragments).

    values: (origin, actual_value) for complete line_ranges values, array
    grouping preserved (origin like "fence#0" / "inline#0").
    problems: (kind, excerpt) for citation-looking constructs in these
    scoped forms that could not be extracted — a surface producing any
    problem fails its tests.
    fragments: (origin, [range_object]) for each standalone range-looking
    object outside fences: the ACTUAL source text is parsed with only the
    documented N placeholder materialized (extra keys/shape preserved) and
    the result is validated like any other citation.
    """
    values, problems, fragments = [], [], []
    fence_spans = [m.span() for m in FENCE_RE.finditer(text)]

    def in_fence(pos):
        return any(a <= pos < b for a, b in fence_spans)

    citation_fence = 0
    for m in FENCE_RE.finditer(text):
        block = m.group(1)
        if '"line_ranges"' not in block:
            continue
        parsed = None
        for candidate in (block, "{" + block + "}"):  # full object, or
            try:                                       # key/value fragment
                parsed = json.loads(candidate)
                break
            except ValueError:
                continue
        if parsed is None:
            problems.append(("unparseable-fence", block.strip()[:60]))
            continue
        found = []
        _walk_line_ranges_values(parsed, found)
        if not found:
            problems.append(("fence-token-without-value", block.strip()[:60]))
        for value in found:
            values.append((f"fence#{citation_fence}", value))
        citation_fence += 1

    # everything outside fences: actual inline key values must parse;
    # standalone range-looking objects are parsed (N materialized) so a
    # malformed documented template is REPORTED, not silently ignored
    stripped = "".join(ch for i, ch in enumerate(text) if not in_fence(i))
    for ordinal, m in enumerate(LINE_RANGES_KEY_RE.finditer(stripped)):
        try:
            value, _ = json.JSONDecoder().raw_decode(stripped[m.end():])
        except ValueError:
            problems.append(("unparseable-inline-value",
                             stripped[m.end():m.end() + 40]))
            continue
        values.append((f"inline#{ordinal}", value))
    for ordinal, m in enumerate(RANGE_OBJ_RE.finditer(stripped)):
        raw = m.group(0)
        candidate = re.sub(r":\s*N\b", f": {TEMPLATE_N}", raw)
        try:
            obj = json.loads(candidate)
        except ValueError:
            problems.append(("unparseable-range-fragment", raw))
            continue
        fragments.append((f"range#{ordinal}", [obj]))
    return values, problems, fragments


def citation_failures(origin: str, value) -> list:
    """Validate an actual extracted line_ranges value in real canonical
    schema contexts (all evidence-bearing locations of all five schemas),
    under the normalization co-authority and the admission order gate."""
    failures = []
    if not isinstance(value, list):
        failures.append(f"{origin}: line_ranges is not an array: {value!r}")
        return failures
    item = {"kind": "OBSERVED_FACT", "line_ranges": value}
    for schema, instance, loc in lrv.all_five_locations(item):
        errors = lrv.validate(instance, schema)
        if errors:
            failures.append(f"{origin} {schema}:{loc}: {'; '.join(errors)}")
    try:
        if em.normalize_ranges(value) != value:
            failures.append(f"{origin}: not canonically sorted")
    except em.MigrationError as exc:
        failures.append(f"{origin}: normalization rejected: {exc}")
    gate = audit_council._range_order_errors(lrv.finding_doc(evidence=[item]))
    if gate:
        failures.append(f"{origin}: admission gate: {'; '.join(gate)}")
    return failures


# ===========================================================================
# 1. completeness truth table — the adopted matrix vs. every scenario
# ===========================================================================
class TestCompletenessMatrixTruthTable(unittest.TestCase):
    """The pure matrix gate decides label ELIGIBILITY per scenario. This is
    eligibility only — actual transitions/quota authority are separate rules
    (see TestStateAuthoritySemantics)."""

    def test_matrix_pinned_to_adopted_policy(self):
        self.assertEqual(NORMATIVE["COMPLETE"], frozenset({
            "OPUS_INDEPENDENT_COMPLETE", "CODEX_INDEPENDENT_COMPLETE",
            "OPUS_CROSS_EXAM_COMPLETE", "CODEX_CROSS_EXAM_COMPLETE",
            "LEDGER_COMPLETE", "FINALIZED"}))
        self.assertEqual(NORMATIVE[CW_RU], frozenset({
            "OPUS_INDEPENDENT_COMPLETE", "CODEX_INDEPENDENT_COMPLETE",
            "FINALIZED"}))
        for phases in NORMATIVE.values():
            self.assertNotIn("ADJUDICATION_COMPLETE", phases,
                             "adjudication keeps its own optional-skip rule")

    # (scenario, skipped phases, {label: eligible})
    TRUTH_TABLE = [
        ("full protocol", [],
         {"COMPLETE": True, CW_RU: True, "PARTIAL_CODEX_QUOTA": True}),
        # adjudication is deferred via its dedicated flag, never a
        # phase_skips record — mechanically identical to the full row
        ("adjudication deferral", [],
         {"COMPLETE": True, CW_RU: True, "PARTIAL_CODEX_QUOTA": True}),
        ("opus independent skipped", ["OPUS_INDEPENDENT_COMPLETE"],
         {"COMPLETE": False, CW_RU: False, "PARTIAL_CODEX_QUOTA": True}),
        ("codex independent skipped", ["CODEX_INDEPENDENT_COMPLETE"],
         {"COMPLETE": False, CW_RU: False, "PARTIAL_CODEX_QUOTA": True}),
        ("opus cross skipped", ["OPUS_CROSS_EXAM_COMPLETE"],
         {"COMPLETE": False, CW_RU: True, "PARTIAL_CODEX_QUOTA": True}),
        ("codex cross skipped (post-independent quota)",
         ["CODEX_CROSS_EXAM_COMPLETE"],
         {"COMPLETE": False, CW_RU: True, "PARTIAL_CODEX_QUOTA": True}),
        ("ledger skipped", ["LEDGER_COMPLETE"],
         {"COMPLETE": False, CW_RU: True, "PARTIAL_CODEX_QUOTA": True}),
        ("final synthesis skipped", ["FINALIZED"],
         {"COMPLETE": False, CW_RU: False, "PARTIAL_CODEX_QUOTA": True}),
    ]

    def test_truth_table(self):
        for name, skipped, eligible in self.TRUTH_TABLE:
            state = {"phase_skips": [{"skipped_phase": p, "reason": "t"}
                                     for p in skipped]}
            for label, ok in eligible.items():
                with self.subTest(scenario=name, label=label):
                    violations = state_store.completeness_skip_violations(
                        state, label)
                    self.assertEqual(not violations, ok,
                                     f"unexpected {violations}")
                    if not ok:
                        self.assertEqual(
                            violations,
                            sorted(set(skipped) & set(NORMATIVE[label])))


class TestMissingMandatoryRejection(unittest.TestCase):
    """Behavioral anchor: the shared set_completeness gate (used by resume
    paths and finalize alike) refuses over-strong labels on real run dirs."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(prefix="aucdev009-")
        self.repo = make_repo(os.path.join(self._tmp.name, "repo"))

    def tearDown(self):
        self._tmp.cleanup()

    def _run_with_skip(self, phase, skipped, from_phase, to_phase):
        run_dir = make_run(self._tmp.name, self.repo, phase=phase)
        state_store.record_phase_skips(run_dir, [
            {"skipped_phase": skipped,
             "reason": "codex quota exhausted before the independent pass"}],
            from_phase=from_phase, to_phase=to_phase)
        return run_dir

    def test_skipped_independent_never_becomes_either_complete_label(self):
        run_dir = self._run_with_skip(
            "OPUS_INDEPENDENT_COMPLETE", "CODEX_INDEPENDENT_COMPLETE",
            "OPUS_INDEPENDENT_COMPLETE", "NORMALIZED")
        for label in ("COMPLETE", CW_RU):
            with self.subTest(label=label), \
                    self.assertRaises(state_store.StateError) as ctx:
                state_store.set_completeness(run_dir, label)
            self.assertIn("mandatory stages", str(ctx.exception))
            self.assertIn("never ran", str(ctx.exception))
        state_store.set_completeness(run_dir, "PARTIAL_CODEX_QUOTA")
        self.assertEqual(
            state_store.load_state(run_dir)["completeness_state"],
            "PARTIAL_CODEX_QUOTA")

    def test_post_independent_quota_omission_allows_cwru_not_complete(self):
        run_dir = self._run_with_skip(
            "OPUS_CROSS_EXAM_COMPLETE", "CODEX_CROSS_EXAM_COMPLETE",
            "OPUS_CROSS_EXAM_COMPLETE", "LEDGER_COMPLETE")
        with self.assertRaises(state_store.StateError):
            state_store.set_completeness(run_dir, "COMPLETE")
        state_store.set_completeness(run_dir, CW_RU)
        self.assertEqual(
            state_store.load_state(run_dir)["completeness_state"], CW_RU)


# ===========================================================================
# 2. per-surface, per-label completeness definitions vs. the normative matrix
# ===========================================================================
def derive_mandatory(definition: str) -> set:
    """Derive the mandatory stages a surface definition STATES for a label
    (case-insensitive, wrap-insensitive). 'both independent passes' /
    'both cross-examinations' signal BOTH stages of the pair."""
    d = definition.lower()
    stages = set()
    if "both independent passes" in d:
        stages |= {"OPUS_INDEPENDENT_COMPLETE", "CODEX_INDEPENDENT_COMPLETE"}
    if "both cross-examinations" in d:
        stages |= {"OPUS_CROSS_EXAM_COMPLETE", "CODEX_CROSS_EXAM_COMPLETE"}
    if "ledger" in d:
        stages.add("LEDGER_COMPLETE")
    if "synthesis" in d:
        stages.add("FINALIZED")
    return stages


def completeness_rows(rel: str, label: str) -> list:
    """Every markdown table row defining `label` on the surface (failure-and-
    resume defines it in BOTH its states table and its matrix table; every
    occurrence must agree — a swapped row anywhere is a defect)."""
    prefix = f"| {label} "
    return [re.sub(r"\s+", " ", line)
            for line in surface_text(rel).splitlines()
            if line.startswith(prefix)]


def skill_completeness_definitions() -> dict:
    """SKILL.md defines the labels in Phase 7 prose, not a table: split the
    normalized text at the definition markers."""
    text = normalized(SKILL)
    i = text.index("`COMPLETE` requires")
    j = text.index("`COMPLETE_WITH_RESIDUAL_UNCERTAINTY`", i)
    k = text.index("`COMPLETE_WITH_RESIDUAL_UNCERTAINTY` requires")
    m = text.index("Report completion", k)
    return {"COMPLETE": text[i:j], CW_RU: text[k:m]}


class TestSurfaceCompletenessDefinitions(unittest.TestCase):
    """Each surface's COMPLETE and residual definition is extracted
    SEPARATELY and its stated mandatory stages must equal the normative
    matrix set for that label — global substring pins cannot catch a swapped
    label row; this derivation can (and its negative controls prove it)."""

    def test_table_definitions_match_normative_sets(self):
        for rel in (FR, PC):
            for label in ("COMPLETE", CW_RU):
                rows = completeness_rows(rel, label)
                self.assertGreaterEqual(
                    len(rows), 1, f"{rel} lost its {label} definition row")
                for row in rows:
                    with self.subTest(surface=rel, label=label, row=row[:50]):
                        self.assertEqual(derive_mandatory(row),
                                         set(NORMATIVE[label]))

    def test_skill_definitions_match_normative_sets(self):
        for label, definition in skill_completeness_definitions().items():
            with self.subTest(label=label):
                self.assertEqual(derive_mandatory(definition),
                                 set(NORMATIVE[label]))

    # negative controls: the derivation must DETECT swapped/over/under-
    # requiring definitions, not just accept the correct ones
    DETECTOR_CONTROLS = (
        ("COMPLETE under-requires (missing cross/ledger)",
         "| COMPLETE | all phases finished: both independent passes and "
         "final synthesis |", "COMPLETE"),
        ("residual over-requires (cross/ledger mandatory)",
         "| COMPLETE_WITH_RESIDUAL_UNCERTAINTY | both independent passes, "
         "both cross-examinations, disagreement ledger, final synthesis |",
         CW_RU),
    )

    def test_detector_flags_swapped_or_missing_definitions(self):
        for name, row, label in self.DETECTOR_CONTROLS:
            with self.subTest(control=name):
                difference = derive_mandatory(row) ^ set(NORMATIVE[label])
                self.assertTrue(difference,
                                "swapped/missing definition not detected")


class TestSurfaceWordingAlignment(unittest.TestCase):
    """Compact pin table for the changed instruction wording (required and
    forbidden phrases, whitespace-normalized)."""

    REQUIRED = (
        (FR, "BOTH independent passes, BOTH cross-examinations, the "
             "disagreement ledger and final synthesis"),
        (FR, "both independent passes and final synthesis ran"),
        (FR, "post-independent quota omissions"),
        (FR, "each carrying its explicit provenance"),
        (FR, "it can never become either complete label"),
        (FR, "never claim an omitted stage ran or that the full council "
             "completed"),
        (FR, "adjudication optional only via its documented explicit skip"),
        (FR, "never automatically upgraded to a complete label"),
        (FR, "never present a partial audit as council-complete"),
        (FR, "COMPLETENESS_MANDATORY_PHASES"),
        # quota deferral mechanism distinction (generic skip vs the
        # previously permitted script-mediated adjudication quota path)
        (FR, "PREVIOUSLY PERMITTED post-independent quota residual path"),
        (FR, "script-mediated `adjudication_skipped` flag that `advance` "
             "persists automatically"),
        (FR, "legal LEDGER_COMPLETE → FINALIZED transition"),
        (FR, "generic phase_skips record alone is not the mechanism"),
        (FR, "NO eligible disputes exist"),
        (FR, "stay UNRESOLVED in the report; never pretend they disappeared"),
        (FR, "STOP and report the appropriate `PARTIAL_*` state"),
        (SKILL, "both independent passes, both cross-examinations"),
        (SKILL, "explicitly recorded post-independent quota omissions"),
        (SKILL, "adjudication optional only via its documented explicit skip"),
        (SKILL, "missing mandatory independent pass stays `PARTIAL_*`"),
        (PC, "both independent passes, both cross-examinations"),
        (PC, "only explicitly recorded post-independent quota omissions"),
        (PC, "adjudication optional per its documented explicit skip"),
        (PC, "omitted work is never claimed as performed"),
        (EP, "a bare `lines` string is NOT valid v2"),
        (XE, "EXACT original Codex thread"),
    )

    FORBIDDEN = (
        (FR, "full protocol ran"), (SKILL, "full protocol ran"),
        (PC, "full protocol ran"),
        (FR, "per judgment"), (SKILL, "per judgment"), (PC, "per judgment"),
        (FR, "a fresh Codex session is acceptable"),
        (FR, "close the run with the honest"),
    )

    def test_required_pins(self):
        for rel, pin in self.REQUIRED:
            with self.subTest(surface=rel, pin=pin[:50]):
                self.assertIn(pin, normalized(rel))

    def test_forbidden_pins(self):
        for rel, pin in self.FORBIDDEN:
            with self.subTest(surface=rel, pin=pin):
                self.assertNotIn(pin, normalized(rel))


# ===========================================================================
# 3. resume semantics across the three edited surfaces + state authority
# ===========================================================================
class TestResumeSemanticsConsistency(unittest.TestCase):
    """Exact-session missing-ID stop, integrity immutability (no close/
    finalize instruction for the corrupted run) and the PARTIAL guard must
    agree on all three edited surfaces."""

    EXACT_SESSION_PINS = {
        FR: ("EXACT stored session id", "never silently substitute",
             "report the stop with the appropriate",
             "obeys the actual phase and integrity gates", "AUCDEV-008",
             "the runner does not yet mechanically refuse a fresh launch"),
        SKILL: ("EXACT stored session id",
                "never silently substitute a fresh Codex session",
                "report the appropriate PARTIAL classification",
                "obeys the actual phase and integrity gates", "AUCDEV-008",
                "resumes the EXACT original Codex thread"),
        PC: ("EXACT stored session id",
             "never silently substituting a fresh session", "AUCDEV-008"),
    }
    INTEGRITY_PINS = {
        FR: ("resume-check exit 8 names the", "carries its own failure code",
             "rewrite, replace, delete or redo the failed checkpoint",
             "preserve every byte as-is", "without mutating the frozen run",
             "preserves the old run directory",
             "nothing here authorizes executing one"),
        SKILL: ("checksum mismatch is exit 8",
                "schema failures carry their own codes",
                "never rewrites, replaces, deletes or repeats a completed "
                "checkpoint", "preserved as-is",
                "Completed phases are immutable and are never repeated"),
        PC: ("never rewritten, replaced, deleted or repeated",
             "preserved as-is"),
    }
    PARTIAL_GUARD_PINS = {
        FR: "it can never become either complete label",
        SKILL: "missing mandatory independent pass stays `PARTIAL_*`",
        PC: "never promoted to either complete label",
    }

    def test_exact_session_pins(self):
        for rel, pins in self.EXACT_SESSION_PINS.items():
            text = normalized(rel)
            for pin in pins:
                with self.subTest(surface=rel, pin=pin[:50]):
                    self.assertIn(pin, text)

    def test_integrity_pins(self):
        for rel, pins in self.INTEGRITY_PINS.items():
            text = normalized(rel)
            for pin in pins:
                with self.subTest(surface=rel, pin=pin[:50]):
                    self.assertIn(pin, text)

    def test_partial_guard_pins(self):
        for rel, pin in self.PARTIAL_GUARD_PINS.items():
            with self.subTest(surface=rel):
                self.assertIn(pin, normalized(rel))


class TestStateAuthoritySemantics(unittest.TestCase):
    """Pure matrix ELIGIBILITY is distinct from actual transition/quota
    AUTHORITY; the adjudication deferral has its own dedicated mechanism."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(prefix="aucdev009-auth-")
        self.repo = make_repo(os.path.join(self._tmp.name, "repo"))

    def tearDown(self):
        self._tmp.cleanup()

    def test_runner_still_constructs_fresh_launch_without_session(self):
        # source evidence for WHY the surfaces must not claim mechanical
        # enforcement (AUCDEV-008): compose_argv builds a fresh `codex exec`
        # argv whenever the session id is None
        fresh = codex_runner.compose_argv(
            "codex", "cross_examination", "/repo", "schema.json",
            "out.json", None)
        self.assertEqual(fresh[:2], ["codex", "exec"])
        self.assertNotIn("resume", fresh)
        resumed = codex_runner.compose_argv(
            "codex", "cross_examination", "/repo", "schema.json",
            "out.json", "sess-1234")
        self.assertEqual(resumed[1:3], ["exec", "resume"])
        self.assertIn("sess-1234", resumed)

    def test_forward_only_machine_never_repeats(self):
        def state_at(phase):
            state = state_store.new_state(
                "20260913T000000Z-aa0001", "/repo", "0" * 64)
            state["phase"] = phase
            return state

        rows = (
            ("same-phase repeat", "OPUS_INDEPENDENT_COMPLETE",
             "OPUS_INDEPENDENT_COMPLETE", True),
            ("backward", "CODEX_CROSS_EXAM_COMPLETE",
             "OPUS_CROSS_EXAM_COMPLETE", True),
            ("forward control", "OPUS_INDEPENDENT_COMPLETE",
             "CODEX_INDEPENDENT_COMPLETE", False),
        )
        for name, src, dst, refuses in rows:
            with self.subTest(row=name):
                if refuses:
                    with self.assertRaises(state_store.StateError):
                        state_store.transition(state_at(src), dst)
                else:
                    state_store.transition(state_at(src), dst)

    def test_adjudication_deferral_uses_dedicated_mechanism(self):
        # a GENERIC phase-skip record for ADJUDICATION_COMPLETE does not
        # authorize passing over adjudication; only adjudication_skipped=True
        # (recorded from LEDGER_COMPLETE) does
        run_dir = make_run(self._tmp.name, self.repo,
                           phase="LEDGER_COMPLETE")
        state_store.record_phase_skips(run_dir, [
            {"skipped_phase": "ADJUDICATION_COMPLETE",
             "reason": "codex quota exhausted"}],
            from_phase="LEDGER_COMPLETE", to_phase="FINALIZED")
        with self.assertRaises(state_store.StateError) as ctx:
            state_store.apply_transition(run_dir, "FINALIZED")
        self.assertIn("without adjudication_skipped", str(ctx.exception))
        state = state_store.apply_transition(
            run_dir, "FINALIZED", adjudication_skipped=True)
        self.assertEqual(state["phase"], "FINALIZED")

    def test_ledger_matrix_eligibility_is_not_skip_authority(self):
        # the truth-table row "ledger skipped -> CW_RU eligible" states PURE
        # matrix eligibility only. It grants no reachable skip authority:
        # the dedicated adjudication rule fires only FROM LEDGER_COMPLETE,
        # so even WITH a bound ledger skip record and adjudication_skipped
        # the machine refuses CODEX_CROSS_EXAM_COMPLETE -> FINALIZED and the
        # phase is unchanged.
        run_dir = make_run(self._tmp.name, self.repo,
                           phase="CODEX_CROSS_EXAM_COMPLETE")
        with self.assertRaises(state_store.StateError):
            state_store.apply_transition(
                run_dir, "FINALIZED", adjudication_skipped=True)
        state_store.record_phase_skips(run_dir, [
            {"skipped_phase": "LEDGER_COMPLETE",
             "reason": "codex quota exhausted after the independent pass"}],
            from_phase="CODEX_CROSS_EXAM_COMPLETE", to_phase="FINALIZED")
        with self.assertRaises(state_store.StateError) as ctx:
            state_store.apply_transition(
                run_dir, "FINALIZED", adjudication_skipped=True)
        self.assertIn("only from LEDGER_COMPLETE", str(ctx.exception))
        state = state_store.load_state(run_dir)
        self.assertEqual(state["phase"], "CODEX_CROSS_EXAM_COMPLETE",
                         "refusal must leave the phase unchanged")
        # pure matrix eligibility on the recorded state — independent of any
        # reachable transition: CW_RU stays eligible, COMPLETE stays refused
        self.assertEqual(
            state_store.completeness_skip_violations(state, CW_RU), [])
        self.assertEqual(
            state_store.completeness_skip_violations(state, "COMPLETE"),
            ["LEDGER_COMPLETE"])


class TestExplicitSkipProvenance(unittest.TestCase):
    """Quota omissions carry explicit, transition-bound, reason-carrying
    provenance; silently passing over an artifact phase is refused with
    nothing written."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(prefix="aucdev009-skip-")
        self.repo = make_repo(os.path.join(self._tmp.name, "repo"))

    def tearDown(self):
        self._tmp.cleanup()

    def test_skip_record_persists_reason_and_binding(self):
        run_dir = make_run(self._tmp.name, self.repo,
                           phase="OPUS_CROSS_EXAM_COMPLETE")
        state_store.record_phase_skips(run_dir, [
            {"skipped_phase": "CODEX_CROSS_EXAM_COMPLETE",
             "reason": "codex quota exhausted after the independent pass"}],
            from_phase="OPUS_CROSS_EXAM_COMPLETE", to_phase="LEDGER_COMPLETE")
        skips = state_store.load_state(run_dir)["phase_skips"]
        self.assertEqual(len(skips), 1)
        self.assertEqual(skips[0]["reason"],
                         "codex quota exhausted after the independent pass")
        self.assertEqual(skips[0]["from_phase"], "OPUS_CROSS_EXAM_COMPLETE")
        self.assertEqual(skips[0]["to_phase"], "LEDGER_COMPLETE")
        self.assertTrue(skips[0]["recorded_at"])

    def test_blank_reason_rejected(self):
        run_dir = make_run(self._tmp.name, self.repo,
                           phase="OPUS_CROSS_EXAM_COMPLETE")
        with self.assertRaises(state_store.StateError):
            state_store.record_phase_skips(run_dir, [
                {"skipped_phase": "CODEX_CROSS_EXAM_COMPLETE",
                 "reason": "   "}])

    def test_pass_over_without_bound_record_refused_nothing_written(self):
        run_dir = make_run(self._tmp.name, self.repo, phase="CONTRACT_FROZEN")
        with self.assertRaises(state_store.StateError) as ctx:
            state_store.apply_transition(run_dir, "NORMALIZED")
        self.assertIn("without an explicit unconsumed skip record",
                      str(ctx.exception))
        self.assertEqual(state_store.load_state(run_dir)["phase"],
                         "CONTRACT_FROZEN", "refusal must write nothing")


# ===========================================================================
# 4. environment / no-verdict semantics
# ===========================================================================
class TestEnvironmentNoVerdictSemantics(unittest.TestCase):
    """INVALID_AUDIT_ENVIRONMENT is a failed admission: zero model calls
    THROUGH THE FAILED GATE, no product verdict, and no finalize support."""

    def test_finalize_label_surface_excludes_env_and_stale(self):
        accepted = audit_council.COMPLETENESS_STATES
        self.assertNotIn("INVALID_AUDIT_ENVIRONMENT", accepted)
        self.assertNotIn("STALE_REPOSITORY", accepted)
        for state in ("COMPLETE", CW_RU, "PARTIAL_CODEX_QUOTA",
                      "PARTIAL_CODEX_FAILURE", "PARTIAL_CLAUDE_INTERRUPTION",
                      "INVALID_AUDIT_INPUT"):
            self.assertIn(state, accepted)

    def test_env_label_is_not_a_performed_stages_verdict(self):
        self.assertNotIn("INVALID_AUDIT_ENVIRONMENT", NORMATIVE)
        self.assertEqual(
            state_store.completeness_skip_violations(
                {"phase_skips": [{"skipped_phase": "LEDGER_COMPLETE"}]},
                "INVALID_AUDIT_ENVIRONMENT"), [])

    def test_surfaces_scope_zero_calls_and_failed_admission(self):
        pins = {
            FR: ("ZERO model calls happen through a failed environment gate",
                 "failed admission",
                 "zero model calls through the failed gate",
                 "never a product verdict",
                 "finalize does not accept this label"),
            SKILL: ("ZERO model calls through the failed gate",
                    "never yields a product verdict", "failed admission"),
            PC: ("zero model calls through the failed gate",
                 "never a product verdict", "failed admission"),
        }
        for rel, phrases in pins.items():
            text = normalized(rel)
            for pin in phrases:
                with self.subTest(surface=rel, pin=pin[:50]):
                    self.assertIn(pin, text)

    def test_no_surface_offers_env_or_stale_finalize_label(self):
        for rel in FIVE_SURFACES:
            text = surface_text(rel)
            for label in ("INVALID_AUDIT_ENVIRONMENT", "STALE_REPOSITORY"):
                with self.subTest(surface=rel, label=label):
                    self.assertNotIn(f"--completeness {label}", text)


# ===========================================================================
# 5. citation extraction across the five instruction surfaces
# ===========================================================================
class TestCitationExtractionAcrossSurfaces(unittest.TestCase):
    """Scoped-form inventory: every complete line_ranges VALUE (grouping
    kept) and every standalone range-object fragment (N materialized) is
    extracted and validated in real canonical schema contexts plus the
    admission gate; nothing in these forms is silently dropped."""

    EXPECTED_VALUES = {PC: 1, SKILL: 0, FR: 0, EP: 0, CX: 0}
    EXPECTED_FRAGMENTS_MIN = {EP: 1, CX: 1}

    def test_no_problems_and_every_citation_validates(self):
        for rel in FIVE_SURFACES:
            values, problems, fragments = extract_citations(surface_text(rel))
            with self.subTest(surface=rel):
                self.assertEqual(problems, [],
                                 "citation-looking construct silently "
                                 "dropped or unparseable")
                self.assertEqual(len(values), self.EXPECTED_VALUES[rel])
                for origin, value in values:
                    self.assertEqual(citation_failures(origin, value), [])
                for origin, fragment in fragments:
                    self.assertEqual(citation_failures(origin, fragment), [])

    def test_public_contract_example_keeps_two_range_grouping(self):
        values, problems, _ = extract_citations(surface_text(PC))
        self.assertEqual(problems, [])
        self.assertEqual(values, [
            ("fence#0", [{"start": 184, "end": 185},
                         {"start": 240, "end": 273}])])

    def test_documented_placeholder_templates_are_materialized(self):
        for rel in self.EXPECTED_FRAGMENTS_MIN:
            _, _, fragments = extract_citations(surface_text(rel))
            with self.subTest(surface=rel):
                self.assertGreaterEqual(len(fragments), 1)
                # the ACTUAL source fragment was parsed with only N
                # materialized — not a hardcoded reconstruction
                origin, fragment = fragments[0]
                self.assertEqual(fragment,
                                 [{"start": TEMPLATE_N, "end": TEMPLATE_N}])
                self.assertTrue(origin.startswith("range#"))


class TestCitationExtractionNegativeControls(unittest.TestCase):
    """Malformed / reversed / extra-key / over-limit / non-array citation
    inputs — including malformed N templates — fed THROUGH THE SAME
    extractor+validator must be REPORTED, never silently dropped. Wire-
    shaped null values (valid on the wire only) are rejected in canonical
    instruction surfaces."""

    @staticmethod
    def _fence(inner):
        return "prose before\n```json\n" + inner + "\n```\nprose after\n"

    # (name, text, (expectation, detail)) — expectation: "problem" (detail =
    # problem kind), "value-fails" or "fragment-fails" (extraction succeeds,
    # validation must fail)
    CONTROLS = (
        ("reversed member (schema silent; gate+normalize catch)",
         _fence('{"findings": [{"evidence": [{"kind": "OBSERVED_FACT", '
                '"line_ranges": [{"start": 5, "end": 3}]}]}]}'),
         ("value-fails",)),
        ("extra key member",
         _fence('{"line_ranges": [{"start": 1, "end": 2, "note": "x"}]}'),
         ("value-fails",)),
        ("over 32 ranges",
         _fence('{"line_ranges": [' + ", ".join(
             '{"start": %d, "end": %d}' % (i, i)
             for i in range(1, 34)) + ']}'),
         ("value-fails",)),
        ("legacy lines string value",
         _fence('{"kind": "OBSERVED_FACT", "line_ranges": "184-185"}'),
         ("value-fails",)),
        ("wire-shaped null value",
         _fence('{"kind": "OBSERVED_FACT", "line_ranges": null}'),
         ("value-fails",)),
        ("unparseable fence",
         "```json\n\"line_ranges\": [{oops\n```\n",
         ("problem", "unparseable-fence")),
        ("unparseable inline value",
         'bad "line_ranges": [not json here',
         ("problem", "unparseable-inline-value")),
        ("documented template with extra key",
         'docs say {"start": N, "end": N, "note": "x"} here',
         ("fragment-fails",)),
        ("documented template missing end",
         'docs say {"start": N} here',
         ("fragment-fails",)),
    )

    def test_controls_are_reported_not_dropped(self):
        for name, text, expectation in self.CONTROLS:
            with self.subTest(control=name):
                values, problems, fragments = extract_citations(text)
                kind = expectation[0]
                if kind == "problem":
                    self.assertTrue(
                        any(pk == expectation[1] for pk, _ in problems),
                        problems)
                elif kind == "value-fails":
                    self.assertTrue(values, "value silently dropped")
                    self.assertTrue(
                        all(citation_failures(o, v) for o, v in values),
                        "malformed citation passed validation")
                else:  # fragment-fails
                    self.assertTrue(fragments,
                                    "malformed template silently ignored")
                    self.assertTrue(
                        all(citation_failures(o, f) for o, f in fragments),
                        "malformed template passed validation")

    def test_inline_value_outside_fence_is_extracted(self):
        # positive control for the inline path: an actual key/value in prose
        text = 'see "line_ranges": [{"start": 3, "end": 4}] in prose'
        values, problems, _ = extract_citations(text)
        self.assertEqual(problems, [])
        self.assertEqual(values, [("inline#0", [{"start": 3, "end": 4}])])
        self.assertEqual(citation_failures(*values[0]), [])

    def test_wire_schema_shape_is_not_canonically_applicable(self):
        # why canonical validation must never be applied to WIRE fragments:
        # the wire schema nulls canonically-optional properties and drops
        # `minimum`, so a wire-valid item is canonically invalid
        wire = wire_adapter.canonical_to_wire(
            lrv.load_schema("finding.schema.json"), str(SCHEMAS))
        lr = (wire["properties"]["evidence"]["items"]["properties"]
              ["line_ranges"])
        self.assertEqual(lr["anyOf"][1], {"type": "null"})
        self.assertNotIn("minimum", json.dumps(lr["anyOf"][0]))
        item = {"kind": "OBSERVED_FACT", "line_ranges": None}
        self.assertTrue(
            lrv.validate(lrv.finding_doc(evidence=[item]),
                         "finding.schema.json"))


# ===========================================================================
# 6. resume-check schema failure stops before any recovery step
# ===========================================================================
class TestResumeCheckSchemaFailurePreservesBytes(unittest.TestCase):
    """A resume-check state-schema failure stops BEFORE any recovery step:
    no frozen run file byte changes. (Checksum tampering is owned by
    test_resume.py; this pins the schema-gate path, which precedes the
    model/environment checks.) Zero inference, offline fixture only."""

    def test_invalid_state_schema_changes_no_bytes(self):
        with tempfile.TemporaryDirectory(prefix="aucdev009-sc-") as tmp:
            repo = make_repo(os.path.join(tmp, "repo"))
            run_dir = make_run(tmp, repo, phase="CONTRACT_FROZEN")
            state_path = os.path.join(run_dir, "state.json")
            with open(state_path, "r", encoding="utf-8") as fh:
                doc = json.load(fh)
            doc["schema_version"] = 99  # unsupported -> schema gate stop
            with open(state_path, "w", encoding="utf-8") as fh:
                json.dump(doc, fh)
            before = {str(path.relative_to(run_dir)): path.read_bytes()
                      for path in Path(run_dir).rglob("*") if path.is_file()}
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                rc = audit_council.cmd_resume_check(
                    argparse.Namespace(run=run_dir))
            self.assertNotEqual(rc, 0)
            payload = json.loads(out.getvalue())
            self.assertFalse(payload["ok"])
            after = {str(path.relative_to(run_dir)): path.read_bytes()
                     for path in Path(run_dir).rglob("*") if path.is_file()}
            self.assertEqual(before, after,
                             "resume-check schema failure must not change "
                             "any frozen run file byte")


# ===========================================================================
# 7. v1 fixture migration regression (in memory only; nothing written)
# ===========================================================================
class TestV1FixtureMigrationRegression(unittest.TestCase):
    """The real Fifth v1 artifact (legacy `lines`) migrates in memory:
    fixture bytes and the input dict are unchanged, legacy `lines` exists
    only in the INPUT, and the migrated output is canonically valid and
    passes the admission range-order gate. No historical artifact is
    written; the broader migration suite (test_line_ranges_v2,
    test_migration_compat) remains authoritative."""

    FIXTURE = Path(HERE) / "fixtures" / "fifth-opus-independent-v1.json"

    def test_migrate_preserves_inputs_and_yields_valid_v2(self):
        before = self.FIXTURE.read_bytes()
        doc = json.loads(before)
        self.assertIn('"lines"', json.dumps(doc))  # genuinely v1 input
        migrated = em.migrate_artifact(doc)
        # fixture bytes and input dict unchanged; legacy field only in input
        self.assertEqual(self.FIXTURE.read_bytes(), before)
        self.assertEqual(doc, json.loads(before))
        self.assertNotIn('"lines"', json.dumps(migrated))
        self.assertIn('"line_ranges"', json.dumps(migrated))
        self.assertFalse(em.is_v1_artifact(migrated))
        self.assertEqual(
            lrv.validate(migrated, "independent-audit.schema.json"), [])
        self.assertEqual(audit_council._range_order_errors(migrated), [])


# ===========================================================================
# 8. admission-level reversed-range gate (schema alone permits reversal)
# ===========================================================================
class TestAdmissionRangeOrderGate(unittest.TestCase):
    """_range_order_errors rejects reversed ranges at the admission gate;
    comparisons use robust suffixes/content because the gate's path format
    inserts a dot before list indices (`findings.[0].`). Non-typed or
    partial members remain the schema's job (gate stays silent)."""

    # (name, doc, expected error count, expected error suffix/content)
    ROWS = (
        ("top-level reversed",
         {"line_ranges": [{"start": 5, "end": 3}]},
         1, "line_ranges[0]: reversed range (5 > 3)"),
        ("nested reversed (dot-index path format)",
         {"findings": [{"evidence": [
             {"line_ranges": [{"start": 9, "end": 2}]}]}]},
         1, "line_ranges[0]: reversed range (9 > 2)"),
        ("only the reversed member is named",
         {"line_ranges": [{"start": 3, "end": 5}, {"start": 9, "end": 2}]},
         1, "line_ranges[1]: reversed range (9 > 2)"),
        ("valid disjoint ranges are clean",
         {"line_ranges": [{"start": 184, "end": 185},
                          {"start": 240, "end": 273}]},
         0, None),
        ("non-int members are the schema's job",
         {"line_ranges": [{"start": "1", "end": "2"}]}, 0, None),
        ("missing end key is the schema's job",
         {"line_ranges": [{"start": 1}]}, 0, None),
    )

    def test_gate_truth_table(self):
        for name, doc, count, needle in self.ROWS:
            with self.subTest(row=name):
                errors = audit_council._range_order_errors(doc)
                self.assertEqual(len(errors), count, errors)
                if needle:
                    self.assertTrue(
                        any(needle in e for e in errors), (needle, errors))
                    if "reversed" in needle:
                        self.assertTrue(
                            any(e.endswith(needle) for e in errors),
                            (needle, errors))

    def test_admission_applies_gate_to_schema_valid_artifact(self):
        # a finding document that PASSES finding.schema.json but carries a
        # reversed range must still be rejected by the admission helper the
        # checkpoint commands use
        doc = lrv.finding_doc(evidence=[
            {"kind": "OBSERVED_FACT",
             "line_ranges": [{"start": 273, "end": 240}]}])
        self.assertEqual(
            lrv.validate(doc, "finding.schema.json"), [],
            "precondition: schema-valid; only the order is wrong")
        with tempfile.TemporaryDirectory(prefix="aucdev009-adm-") as tmp:
            path = os.path.join(tmp, "finding.json")
            with open(path, "w", encoding="utf-8") as fh:
                json.dump(doc, fh)
            errors = audit_council._validate_artifact_file(
                path, "finding.schema.json")
        self.assertTrue(any("reversed range" in e for e in errors), errors)


if __name__ == "__main__":
    unittest.main()
