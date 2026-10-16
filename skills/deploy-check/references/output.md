# Deploy assessment

Return exactly the sections below, in this order, and nothing else. The table
holds what the evidence says. Everything you reason beyond the evidence goes in
**Inferences, not evidence**. These are recommendations, not permission to deploy.

```
**Verdict: GO | CAUTION | NO-GO | INCOMPLETE.** One sentence naming the deciding factor and its evidence ID.

| Check | Finding | Source |
|---|---|---|
| Artifact | ... | ... |
| Base and target | ... | ... |
| Environment | ... | ... |
| Mapped services | ... | ... |
| Review and CI | ... | ... |
| Pre-production | ... | ... |
| Rollout safeguards | ... | ... |
| Incidents | ... | ... |
| Release policy | ... | ... |
| Concurrent changes | ... | ... |
| Staffing | ... | ... |

**Inferences, not evidence**
- Conditional risks and reasoning beyond the table, each labeled. Or "None."

**Unresolved checks**
- Missing evidence and identities needed for a real release. Or "None."

**What would change the verdict**
- Specific evidence and the verdict it would produce.

I did not deploy, approve, roll back, or notify anyone.
```

## Table rules

- Keep all eleven rows, in this order, even when the evidence is silent.
- **Source** holds the evidence identifier as supplied (R1, P2), or the tool and
  record it came from. Use `—` only when the finding is `unknown` or
  `not supplied`.
- **Finding** restates its source. Do not add an environment, window, duration,
  time, count, owner or capability the source does not state. Any number in a
  finding must appear in its cited source.
- An unspecified environment, base or target is `unknown`. Never fill it from
  convention or from the rollout style.
- Missing incident data does not establish no incident; write `not supplied`.
- Preserve the scope of negative evidence everywhere, including the verdict:
  no concurrent shared-infrastructure upgrade does not mean no concurrent change
  or no dependency risk. Unknown identities must stay unknown in recommendations
  too; do not presuppose production when asking what remains to be confirmed.
- **Staffing** is reported separately and never changes the technical verdict.
  Write the staffing record's own words. When it gives no window, add "window
  not stated" in that row, so the reader can tell an unscoped record from one
  that covers this deploy window. Never supply the window yourself.

## Verdict rules

- A failing required check, missing human review, active incident on the
  service, or freeze supports NO-GO. A green canary does not cancel failing tests.
- A relevant major upgrade (in the change or concurrent shared infrastructure),
  broad diff, no pre-prod, related recent failures, or all-environment rollout
  supports CAUTION.
- A required check that is unavailable makes the verdict INCOMPLETE; do not
  preserve GO by treating it as passed.
- Apply the customer's release policy, or say which stated defaults you used.
  An emergency exception needs the customer's authorized decision-maker.

## Inferences, not evidence

Put every statement that goes beyond the table here, each worded as an
inference: "If ...", "could", "is not stated". The heading alone does not qualify
an otherwise factual assertion. Explanations of why a factor
matters, possible interactions between changes, and guesses about scope belong
here and nowhere else. Never describe the customer's safeguards, monitors or
teams as able or unable to do something the evidence does not state.

The final line covers only your own non-actions. Do not extend it to the release team.
