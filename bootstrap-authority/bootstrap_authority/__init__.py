"""AUCDEV-023 PCH6-B PATH-B candidate-specific target-independent
bootstrap authority (wholly NEW lineage).

IMPLEMENTATION_CANDIDATE_ONLY / NO_EXECUTION_AUTHORITY: the Control
Room design-readback-accepted (2026-10-02) NEW authority plane for a
FUTURE fresh independent audit of the frozen candidate target
`730d2b29f7c0e7d33af3451b6d9205ec27c143ed` — strictly target-
independent (no runtime import of, or authority dependency on, the
audit target's bootstrap-supervisor / qualification-harness / skill
code), controllerless on the authority path, process-bound one-shot,
free of substantive audit-verdict logic.  Four pre-target EBS
primitives are reused as EXACT historical blobs (MANIFEST.json
source_provenance); binding.py and runtime.py are NEW source.  The
design-reserved event/attempt identities are binding CONSTANTS ONLY:
importing this package instantiates nothing and grants nothing.  See
README.md and the canonical implementation record
docs/chatgpt-project/AUCDEV-023-PCH6-B-CANDIDATE-SPECIFIC-BOOTSTRAP-AUTHORITY-IMPLEMENTATION.md.
"""
from .binding import (AUDITOR_SELECTIONS, BINDING_SCHEMA, EVENT_ID,
                      FROZEN_TARGET, POLICY_ID, RESERVED_ATTEMPT_IDS,
                      Binding, BindingError, binding_projection,
                      canonical_bytes, parse_binding, strict_loads)
from .runtime import (AttemptResult, AuthorityError, AuthorityRefused,
                      BootstrapAuthority,
                      PostConsumptionTerminalAccountingError,
                      accounting_name, check_report_binding)

__all__ = [
    "AUDITOR_SELECTIONS", "BINDING_SCHEMA", "EVENT_ID", "FROZEN_TARGET",
    "POLICY_ID", "RESERVED_ATTEMPT_IDS", "Binding", "BindingError",
    "binding_projection", "canonical_bytes", "parse_binding",
    "strict_loads", "AttemptResult", "AuthorityError", "AuthorityRefused",
    "BootstrapAuthority", "PostConsumptionTerminalAccountingError",
    "accounting_name", "check_report_binding",
]
