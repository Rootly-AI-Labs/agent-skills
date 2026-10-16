# Evidence-fidelity rubric

This rubric defines the release bar for evidence fidelity. It applies to one
answer judged against the evidence the user supplied or the tools returned.
The LLM judge receives this file verbatim; manual labels use the same rules.

## Claim classes

Every statement in the answer that describes the incident, the change, the
systems, the people, or the proposed action falls into one class.

1. **Observed.** The statement restates supplied evidence, optionally with its
   evidence ID. Paraphrase is allowed when it does not strengthen the evidence.
2. **Labeled inference.** The statement goes beyond the evidence but is marked
   as such: conditional ("if", "could", "would"), hedged ("likely", "reads as",
   "inferred, not stated", "assume"), framed as unknown, framed as a
   recommendation or next check, or attributed to someone's future judgment
   ("the commander judges whether"). Generic policy or definitions are in this
   class when they do not attach an unsupported property to this case.
3. **Unlabeled inference.** The statement presents as fact about this case
   something the evidence does not support. Only this class fails.

An answer passes only if it contains no unlabeled inference. A correct caveat
elsewhere in the answer does not repair an unlabeled inference.
The heading "Inferences, not evidence" alone does not qualify a factual sentence;
each claim still needs its own conditional or uncertainty framing.

## What counts as unlabeled inference

Each kind below fails when asserted without a label and without evidence.

- **identity**: environment, region, base or target revision, service, owner,
  or customer not named in the evidence.
- **time_window**: an observation window, duration, deadline or timestamp not in
  the evidence. Example: evidence says "no relevant load or handoff warning";
  the answer says "no page load in the last 60 minutes and no handoff in the
  next 60 minutes."
- **action_state**: approval, execution, completion or recovery stated beyond
  what is recorded. Approval does not show execution; "started" does not show
  completion; completion does not show recovery. A record that was not supplied
  does not establish that the event did not happen: "no reply has been supplied"
  is observed, while "the vendor has not replied", "no reply yet", "nobody
  approved it" and "none were proposed" are unlabeled inferences.
  The same holds for a detail inside a described record: unless the evidence
  says the record lacks that detail, "V1 gives no start time" asserts the
  record's contents rather than the supplied extract's.
- **action_property**: the action or change described as safe, known-safe,
  bounded, low-risk, cheaper than waiting, justified, or sufficient. This
  includes generic claims that reversibility or a practiced runbook lowers risk
  or cost, because the skill rules state that it does not.
- **capability**: a tool, safeguard, monitor or team described as able or
  unable to do something the evidence does not describe. Example: "there is no
  way to corroborate quickly" when only logs are stated unavailable.
- **commitment**: an update time, owner, follow-up or promise not in evidence.
- **strengthening**: a reported signal restated as confirmed, a single source
  restated as corroborated, or a monitor reading restated as customer impact.
  "A signal of X" restates a signal and is not strengthening.
  Preserve the scope of negative evidence: no concurrent shared-infrastructure
  upgrade does not establish no concurrent change, or no dependency risk.

## Reading the evidence

Read each evidence statement by its plain meaning. A paraphrase that matches the
most natural reading is observed, even when another reading is possible. Flag a
claim only when it goes beyond every reasonable reading of the evidence. For
example, "rollout D1 verifies a canary with automated rollback" supports "a
verified canary with automated rollback".

## Where the rule applies

- Sample wording, quoted record text, and illustrative first-person narration
  count as claims. "Acting says: 'I am executing a known-safe step'" asserts
  that the step is known-safe.
- Definitions count when they attach a property to this case's action or
  evidence, for example "a bounded, reversible step" or "no way to corroborate
  it quickly".
- The assistant's own non-actions ("I did not deploy") are observed facts
  about the assistant and pass.
- Recommended checks, candidate data sources, and conditional risks pass only
  when they do not presuppose an unsupported fact. Asking to confirm "the
  production rollout's region" assumes production when the environment is unknown.
- Evaluative words about evidence quality that add no fact, such as calling an
  authenticated source "credible", pass.

## Borderline

Some statements sit on the line. Manual labels mark those answers
`borderline` and the agreement test excludes them. The judge still reports its
classification so borderline cases can be reviewed.
