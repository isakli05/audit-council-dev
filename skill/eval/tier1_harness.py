#!/usr/bin/env python3
"""Tier-1 deterministic harness eval (pillar D, Task D.1).

Runs, with NO model calls:
  * the A0 environment regression matrix (the three env test modules,
    discovered BY NAME from their checklist comments), and
  * the full unittest harness suite,
then emits a tier-1 scorecard via `scoring.score_tier1`.

This module is a PURE LIBRARY plus a CLI hook: nothing here writes files.
Children are spawned strictly via /usr/bin/python3 (host quirk: the
`python3` shim's sys.executable is the ZCode AppImage).
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
from typing import Any, Callable

if __package__ in (None, "") or __package__ == "eval":  # direct execution
    sys.path.insert(0, os.path.dirname(os.path.dirname(
        os.path.realpath(__file__))))
    from eval import scoring
else:  # pragma: no cover - alternate import spelling
    from . import scoring

PYTHON = "/usr/bin/python3"
EVAL_DIR = os.path.dirname(os.path.realpath(__file__))
SKILL_DIR = os.path.dirname(EVAL_DIR)
DEFAULT_TESTS_DIR = os.path.join(SKILL_DIR, "tests")

# The environment regression matrix modules (run in this exact order).
ENV_MATRIX_MODULES = ("tests.test_env_binding",
                      "tests.test_path_guard",
                      "tests.test_env_lifecycle")
ENV_MATRIX_FILES = {
    "tests.test_env_binding": "test_env_binding.py",
    "tests.test_path_guard": "test_path_guard.py",
    "tests.test_env_lifecycle": "test_env_lifecycle.py",
}

_RAN_RE = re.compile(r"^Ran (\d+) tests? in ", re.M)
_FAIL_LINE_RE = re.compile(r"^(?:FAIL|ERROR):\s+(\S+)\s+\(([^)]+)\)")
_CLASS_RE = re.compile(r"^class\s+([A-Za-z_]\w*)")
_DEF_RE = re.compile(r"^\s+def\s+(test_\w+)\s*\(")
_CASE_NUM_RE = re.compile(r"^\s*(\d{1,2})\.\s+\S")
_ARROW_RE = re.compile(r"->\s*([A-Za-z_]\w*)\.([A-Za-z_]\w*)")
_BULLET_RE = re.compile(r"^\s*-\s+(.+?)\s*->\s+(.+?)\s*$")

# Lifecycle checklist hints -> test-name matchers (normalized substrings).
# The lifecycle docstring maps spec cases to tests descriptively; these
# keywords resolve each hint to a concrete test method deterministically.
_LIFECYCLE_HINTS = (
    (("root_mismatch", "root mismatch"), ("root_mismatch",)),
    (("head_mismatch", "head mismatch"), ("head_mismatch",)),
    (("fake_codex", "fake codex", "e2e"), ("fake_codex",)),
    (("inert",), ("inert_prose",)),
    (("resume",), ("resume_check",)),
    (("advance", "start"), ("blocks_all_inference",)),
    (("grep", "sniffing"), ("no_isdir_git_discovery",)),
)


def _module_tests(path: str) -> list[str]:
    """Collect 'TestClass.test_name' ids from a test module by static scan."""
    tests: list[str] = []
    current = None
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            m = _CLASS_RE.match(line)
            if m:
                current = m.group(1)
                continue
            m = _DEF_RE.match(line)
            if m and current:
                tests.append("%s.%s" % (current, m.group(1)))
    return tests


def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")


def discover_env_matrix(tests_dir: str = DEFAULT_TESTS_DIR) -> dict[str, Any]:
    """Full discovery: numbered A0.6 matrix cases + lifecycle bullets.

    Returns {"case_tests": {case_id: [test ids]},
             "mapping": {case_id: primary test id},
             "unmapped": [{"case": id, "wanted": str, "module": str}],
             "tests_by_module": {module: [test ids]}}.
    Anything unresolved lands in "unmapped" and counts as NOT PASSING.
    """
    tests_by_module: dict[str, list[str]] = {}
    for module in ENV_MATRIX_MODULES:
        path = os.path.join(tests_dir, ENV_MATRIX_FILES[module])
        tests_by_module[module] = _module_tests(path) if \
            os.path.isfile(path) else []

    case_tests: dict[str, list[str]] = {}
    unmapped: list[dict[str, str]] = []

    def _add(case: str, class_name: str, method: str, module: str) -> None:
        test_id = "%s.%s.%s" % (module.split(".")[-1], class_name, method)
        case_tests.setdefault(case, [])
        if test_id not in case_tests[case]:
            case_tests[case].append(test_id)

    # 1) numbered checklist blocks in test_env_binding / test_path_guard:
    #    " N. description" lines followed by "      -> Test.test_name" arrows
    for module in ("tests.test_env_binding", "tests.test_path_guard"):
        path = os.path.join(tests_dir, ENV_MATRIX_FILES[module])
        if not os.path.isfile(path):
            continue
        known = set(tests_by_module[module])
        current_case = None
        with open(path, "r", encoding="utf-8") as fh:
            for line in fh:
                m = _CASE_NUM_RE.match(line)
                if m:
                    current_case = m.group(1)
                    # NO continue: single-line cases (" 3. desc -> T.test")
                    # carry their arrow on the same line
                m = _ARROW_RE.search(line)
                if m and current_case is not None:
                    cls, meth = m.group(1), m.group(2)
                    if "%s.%s" % (cls, meth) in known:
                        _add(current_case, cls, meth, module)
                    else:
                        unmapped.append({"case": current_case,
                                         "wanted": "%s.%s" % (cls, meth),
                                         "module": module})

    # 2) lifecycle docstring bullets: "  - description -> hint"; the hint
    #    is resolved against lifecycle test names via keyword matching
    lifecycle = "tests.test_env_lifecycle"
    path = os.path.join(tests_dir, ENV_MATRIX_FILES[lifecycle])
    if os.path.isfile(path):
        n = 0
        with open(path, "r", encoding="utf-8") as fh:
            for line in fh:
                m = _BULLET_RE.match(line)
                if not m:
                    continue
                text = _norm(m.group(1) + " " + m.group(2))
                matchers = [subs for keys, subs in _LIFECYCLE_HINTS
                            if any(_norm(k) in text for k in keys)]
                hit = None
                for test in tests_by_module[lifecycle]:
                    ntest = _norm(test)
                    for subs in matchers:
                        if all(s in ntest for s in subs):
                            hit = test
                            break
                    if hit:
                        break
                n += 1
                case = "L%d" % n
                if hit:
                    cls, meth = hit.rsplit(".", 1)
                    _add(case, cls, meth, lifecycle)
                else:
                    unmapped.append({"case": case,
                                     "wanted": m.group(2).strip(),
                                     "module": lifecycle})

    mapping = {case: tests[0] for case, tests in sorted(case_tests.items())
               if tests}
    return {"case_tests": case_tests,
            "mapping": mapping,
            "unmapped": unmapped,
            "tests_by_module": tests_by_module}


def discover_env_matrix_tests(tests_dir: str = DEFAULT_TESTS_DIR
                              ) -> dict[str, str]:
    """Spec-case -> test name map (contract surface).

    Numbered cases are "1".."20" (the program-spec A0.6 matrix); lifecycle
    checklist cases are "L1".."Ln". Unresolvable cases are omitted here but
    reported (and scored NOT PASSING) by `discover_env_matrix` /
    `run_env_matrix`.
    """
    return discover_env_matrix(tests_dir)["mapping"]


def _parse_failing(stderr: str) -> set[str]:
    failing: set[str] = set()
    for line in stderr.splitlines():
        m = _FAIL_LINE_RE.match(line)
        if m:
            failing.add(m.group(1))
    return failing


def run_env_matrix(tests_dir: str = DEFAULT_TESTS_DIR,
                   timeout: int = 300) -> dict[str, bool]:
    """Run ONLY the three env regression modules; map results to cases.

    A module-level pass marks its mapped cases True; failing test names are
    parsed from unittest's stderr so exactly the affected cases go False.
    Conservative: rc != 0 with NO parseable failing names marks ALL cases
    False; unmapped cases always count as NOT PASSING; timeout -> all
    False. Runs with cwd=skill/ via /usr/bin/python3.
    """
    discovery = discover_env_matrix(tests_dir)
    results: dict[str, bool] = {}
    try:
        proc = subprocess.run(
            [PYTHON, "-m", "unittest", *ENV_MATRIX_MODULES],
            cwd=SKILL_DIR, capture_output=True, text=True, timeout=timeout)
        rc, err = proc.returncode, proc.stderr
    except subprocess.TimeoutExpired:
        for case in discovery["case_tests"]:
            results[case] = False
        for entry in discovery["unmapped"]:
            results[entry["case"]] = False
        return results

    all_ok = rc == 0
    failing = _parse_failing(err) if rc != 0 else set()
    ambiguous = rc != 0 and not failing  # unparseable failure -> fail all

    # bare-name collisions across modules make bare-name matching unsafe
    bare_counts: dict[str, int] = {}
    for tests in discovery["tests_by_module"].values():
        for t in tests:
            bare = t.rsplit(".", 1)[1]
            bare_counts[bare] = bare_counts.get(bare, 0) + 1

    for case, test_ids in discovery["case_tests"].items():
        if all_ok:
            results[case] = True
            continue
        if ambiguous:
            results[case] = False
            continue
        case_failed = False
        for test_id in test_ids:
            bare = test_id.rsplit(".", 1)[1]
            if bare in failing and bare_counts.get(bare, 0) == 1:
                case_failed = True
            elif test_id in failing:
                case_failed = True
        results[case] = not case_failed
    for entry in discovery["unmapped"]:
        results.setdefault(entry["case"], False)
        results[entry["case"]] = False
    return results


def run_harness_suite(tests_dir: str | None = None,
                      timeout: int = 900) -> tuple[bool, int | None]:
    """Full `unittest discover -s tests` run; parse 'Ran N tests' + OK.

    tests_dir overrides the discovery start directory (used by tests to
    keep the suite fast); default is the real skill/tests tree.
    """
    start = tests_dir if tests_dir is not None else "tests"
    try:
        proc = subprocess.run(
            [PYTHON, "-m", "unittest", "discover", "-s", start],
            cwd=SKILL_DIR, capture_output=True, text=True, timeout=timeout)
        out = proc.stdout + proc.stderr
        rc = proc.returncode
    except subprocess.TimeoutExpired:
        return False, None
    m = _RAN_RE.search(out)
    total = int(m.group(1)) if m else None
    passed = rc == 0 and any(
        line.startswith("OK") for line in out.splitlines())
    return passed, total


def tier1(run_env_matrix_fn: Callable[[], dict[str, bool]] | None = None,
          run_harness_fn: Callable[[], tuple[bool, int | None]] | None = None
          ) -> dict[str, Any]:
    """Assemble the tier-1 eval result (pure: no side-effect writes).

    Injectable runners keep this testable without paying the full suite
    cost; the defaults run the real thing.
    """
    env_results = (run_env_matrix_fn or run_env_matrix)()
    harness_passed, harness_total = (run_harness_fn or run_harness_suite)()
    scorecard = scoring.score_tier1(env_results, harness_passed,
                                    harness_total)
    fraction, failing = scoring.environment_fraction(env_results)
    return {
        "schema_version": 2,
        "tier": 1,
        "env_matrix": {
            "cases": len(env_results),
            "pass_fraction": fraction,
            "failing_cases": failing,
            "case_results": env_results,
        },
        "harness_suite": {"passed": harness_passed,
                          "tests_run": harness_total},
        "scorecard": scorecard,
    }


def main(argv: list[str] | None = None) -> int:
    import json
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] == "tier1":
        print(json.dumps(tier1(), indent=2, sort_keys=True))
        return 0
    print("usage: tier1_harness.py tier1", file=sys.stderr)
    return 2


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
