**Policy answer**

No. The incident commander does not have to wait for a second independent evidence source before executing an approved, reversible mitigation under the practiced runbook. The two-source rule governs what may be stated as confirmed. It is not a mandatory waiting period for an authorized human choosing to mitigate under uncertainty.

**The distinction**

- **Acting under uncertainty** is a risk decision. The commander weighs the cost of acting on a possibly wrong signal against the cost of leaving a possibly real checkout outage running. A reversible, rehearsed action lowers the cost of being wrong, which is exactly why runbooks exist for this situation.
- **Claiming a confirmed cause or impact** is an evidence claim. "Checkout is down" or "the mitigation fixed it" needs at least two independent sources, including metrics or logs. One authenticated monitor supports "monitor X reports severe checkout failures," not "checkout failures are confirmed."

Executing the mitigation does not raise the evidence level. If the monitor recovers afterward, that is still one source. Recovery stays unconfirmed until a second independent signal agrees.

**What is known and unknown from the supplied facts**

- **Known:** one authenticated monitoring source reports severe checkout failures. The commander has approved a reversible mitigation and has authority to execute it.
- **Unknown:** whether the mitigation has been executed, and its outcome. Approval establishes permission, not execution.
- **Unknown:** whether the action is safe, sufficient, or preferable to waiting. "Reversible" describes a recovery option, not a bound on harm or cost. The runbook's prerequisites and failure modes are not described here, so they stay unassessed.
- **Unknown:** actual customer impact and blast radius. Logs being unavailable is a stated gap, not evidence of a healthy service.

**Next recommended check**

Before or in parallel with executing, look for any second signal that is independent of the monitor: checkout order rate or payment-success metrics, a synthetic transaction, or support reports. The same check is what will later let you state that the mitigation worked rather than that the monitor went quiet.

I did not call Rootly, change any incident record, or execute the mitigation.
