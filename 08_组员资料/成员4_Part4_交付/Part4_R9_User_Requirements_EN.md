# R9 — User requirements and justifications

> Member 4 · Section 9 · up to one page · ten MoSCoW Must have requirements. This text matches Section 9 of `ID-Coo_报告提交框架_EN_R9完成_R10四页版.docx`. Reference numbers follow that Word file’s IEEE list [1]–[26].

## 9. User requirements and justifications

Section 8 identifies reliable identity attribution, clear exception outcomes, safe handling, local continuity, maintainability and measurable value as the attributes customers need. The following ten user requirements state the outcomes the product/service must deliver. Each is a MoSCoW Must have; Section 10 describes the proposed design.

1. **UR1 (Must have).** The system must link each passage to the correct cow when a valid electronic identifier is available. A wrong identity can corrupt treatment and herd records, making reliable attribution essential to the problem defined in Section 2.
2. **UR2 (Must have).** The system must leave unconfirmed identity unresolved and make the case available for safe staff review, pausing intake if review cannot continue. Tags can be lost or unreadable [3], [6]; a guessed identity would recreate the original record error.
3. **UR3 (Must have).** The system must not record cattle passing together or closely following as one confirmed animal. Otherwise a neighbouring identifier could be attributed to the wrong cow, undermining the identity assurance required in Section 8.
4. **UR4 (Must have).** Staff must be able to operate, stop and take over the process without entering the cattle path. Cattle handling presents injury risks [25], so external control is needed for routine use.
5. **UR5 (Must have).** The system must confirm the exit actually taken and record each passage as one complete, truthful event. A late reading or an incorrect route must not leave an apparently complete but false event record.
6. **UR6 (Must have).** The service must continue essential identity checks and preserve passage and exception records during network outages. Farm handling cannot depend on continuous connectivity, and lost records would prevent later review.
7. **UR7 (Must have).** The service must provide auditable identity, time, exception and route records while distinguishing internal passages from reportable cattle movements. Farmers need usable evidence without mistaking on-farm sorting for a statutory movement [8], [26].
8. **UR8 (Must have).** The service must process 200 cattle within 90 minutes in the pilot, including repeated reads and reviews, without excessive queuing. Otherwise the checks would delay normal handling; Section 8 identifies per-head processing as a possible bottleneck.
9. **UR9 (Must have).** The system must remain dependable after routine cleaning and allow faults to be recognised and resolved without prolonged downtime in wet, dirty farm conditions. Frequent interruptions would make daily use impractical.
10. **UR10 (Must have).** The installed product and ongoing service must provide a measurable net benefit relative to total ownership cost. Farms need to justify the investment through actual labour savings and operating costs, as Section 8 notes.

Section 10 describes the design response and validation.
