**Policy answer:** No. The incident commander does not have to wait for a second independent evidence source before executing an approved, reversible mitigation under a practiced runbook.

The two-source rule governs what can be stated as confirmed, not when an authorized human may act. Corroboration from a second independent source, such as metrics plus logs, is required before anyone claims that impact, cause, mitigation, or recovery is confirmed. It is not a mandatory waiting period that blocks a commander from choosing mitigation under uncertainty. Acting under uncertainty means the commander takes a sanctioned, recoverable step because the available signal justifies the risk of acting over the risk of waiting. Claiming a confirmed cause means asserting that the failure mechanism is known. The first is a decision the commander owns. The second is a factual claim that requires corroboration the incident does not yet have.

**What is known and unknown**

- **Known:** One authenticated monitoring source reports severe checkout failures. The incident commander has approved a reversible mitigation under a practiced runbook and has authority to execute it.
- **Recorded execution status:** The authorized operator log explicitly records that execution has not started. Approval and execution remain separate facts. The mitigation is approved and not yet executed.
- **Unknown:** Logs are unavailable, so operational impact is reported by one source and is not confirmed. The cause is unknown. Nothing in the supplied evidence describes the mitigation's prerequisites, possible harm, or verification criteria, so those remain unassessed. Reversible describes a recovery option, not a bound on harm or cost.

**What the decision rests on**

Whether to execute now is the commander's judgment of prerequisites and risk, not a question the evidence rule answers. The rule only establishes that a single source is enough to justify acting if the commander judges the action safe and appropriate. It does not establish that this specific mitigation is safe, sufficient, or better than waiting. If the commander executes, the record should say the mitigation was taken in response to a single-source report, with cause unconfirmed, and recovery should be stated only once a second independent signal shows checkout succeeding.

**Next recommended check:** Before or alongside execution, find a second independent signal for checkout health that does not depend on logs. Candidates are a checkout success-rate or payment-completion metric, a synthetic transaction, or a direct customer-facing probe. That same signal is what will later let you distinguish recorded completion of the runbook step from verified recovery.

I did not call Rootly, read any incident record, or execute the mitigation.
