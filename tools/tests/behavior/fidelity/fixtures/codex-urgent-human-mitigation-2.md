I’m using the incident-response skill to clarify the evidence rule, without calling Rootly or executing the mitigation.

**No.** The skill’s corroboration rule governs confirmed claims; it does not impose a waiting period on authorized humans choosing mitigation under uncertainty.

The commander may act based on the available evidence and their assessment of runbook prerequisites and risks. Reversibility and a practiced runbook do not, by themselves, establish that this particular action is safe, sufficient, or preferable to waiting.

Here, one authenticated source **reports** severe checkout failures, logs are unavailable, and the cause remains unconfirmed. Approval and authority are established; execution and outcome are unknown.

Claiming a confirmed cause requires at least two independent evidence sources, including metrics or logs, that support the causal explanation. Authentication establishes provenance, not corroboration. Even improvement after mitigation does not by itself prove the suspected cause.

The next recommended check is independent checkout evidence, such as a separately operated synthetic checkout, while monitoring the original signal. If mitigation is executed, verify its effect and any adverse effects. Gathering corroboration can proceed alongside the commander’s response.
