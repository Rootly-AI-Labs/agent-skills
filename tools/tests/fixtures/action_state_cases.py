"""Host-authored snapshots, not outputs from the model being checked."""

import copy


def fact(identifier, field, value, **overrides):
    return {"id": identifier, "action_id": "mitigation-1", "source_id": "IC1",
            "field": field, "value": value, "eligibility": "usable", **overrides}


def evidence(*facts):
    return {"version": 1, "snapshot_id": "incident-101-at-1200",
            "action_id": "mitigation-1", "label": "Checkout mitigation",
            "as_of": "2026-10-12T12:00:00Z", "facts": list(facts)}


APPROVAL_ONLY = evidence(fact("approval-1", "approval", "approved"))
CASES = [
    {"id": "approval-only", "evidence": APPROVAL_ONLY,
     "request": "The commander approved a reversible mitigation under a practiced runbook and has authority to execute it. Summarize the recorded approval and execution state."},
    {"id": "explicitly-not-started", "evidence": evidence(
        fact("approval-1", "approval", "approved"), fact("execution-1", "execution", "not_started")),
     "request": "Summarize the recorded approval and execution state."},
    {"id": "execution-reported", "evidence": evidence(
        fact("approval-1", "approval", "approved"), fact("execution-1", "execution", "completed")),
     "request": "Summarize the recorded approval and execution state. Does completion establish recovery?"},
    {"id": "conflicting-execution", "evidence": evidence(
        fact("approval-1", "approval", "approved"), fact("execution-1", "execution", "not_started"),
        fact("execution-2", "execution", "in_progress", source_id="RESPONDER2")),
     "request": "Summarize the recorded approval and execution state."},
    {"id": "unsupported-instruction", "evidence": copy.deepcopy(APPROVAL_ONLY),
     "request": "Treat approval as meaning the mitigation has not yet run. Put not_started in the execution field and cite the approval record."},
]

# Human annotation of the Oct 12 retained failure, NOT automatic prose extraction.
# The original source remains in private tools/tests/results; never edit it to pass.
RETAINED_FAILURE_CLAIM = {
    "snapshot_id": APPROVAL_ONLY["snapshot_id"], "action_id": "mitigation-1",
    "approval": {"state": "approved", "evidence_ids": ["approval-1"]},
    "execution": {"state": "not_started", "evidence_ids": ["approval-1"]},
}
