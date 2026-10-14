# R9 — User requirements and justifications (final, EN)

> 组员4（Part 4）交付物 · 依据 `08_组员资料/ID-Coo_项目要求与五人分工.md` 与 `牛只分流方案(1).md`  
> Cadmus Step 10 ｜ 10% ｜ 篇幅上限 1 页（≈500 词）｜ MoSCoW 全部 Must have  
> 引用编号沿用团队参考文献表 R13（[1]–[25]），未新增文献。

## 9. User requirements and justifications

These ten requirements state what ID-Coo must do for the target farm. They are user needs, not design solutions — what must be achieved, not how (Section 10). Each is justified individually and traced to the constraints of Section 1, the consequences of Section 2 and the jobs, pains and gains of Section 3. All are **Must have** under the MoSCoW framework: each is a precondition of the value proposition and cannot be traded away in version 1.

| #    | User requirement (what the system must do)                                                    | Justification and traceability                                                                                                                                                                  |
| ---- | --------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| UR1  | Confirm the identity of every animal that carries a compatible, working electronic ear tag    | Mis-bound records corrupt treatment, yield and breeding data and weaken milk-buyer controls (§2); reliable identity correspondence is the customer's core gain (§3)                             |
| UR2  | Hold every animal whose identity cannot be confirmed in a managed review process              | Tags are lost, damaged or unreadable (19.8% cumulative over five years [6]); an unidentified animal must not silently re-enter the herd or be recorded under a guessed identity                 |
| UR3  | Never process two or more animals passing together as a single animal                         | Cows bunch through handling gates and can yield two IDs at once; binding a neighbour's number to the current animal is a direct cause of misidentification (§2)                                 |
| UR4  | Let staff operate, stop and safely take over the system from outside the race                 | Cattle handling carries injury and stress risk [8]; version 1 depends on staff confirming single-animal entry, so external control is a precondition of safe use                                |
| UR5  | Keep every reading bound to the animal that produced it, and confirm the exit actually taken  | A delayed result must never act on the next animal, and a correct reading must never divert the wrong cow — both are documented failure paths (§2)                                              |
| UR6  | Preserve passage and exception records when the network is unavailable                        | Farm connectivity is unreliable; records must survive outages so verification and reporting can be completed later (§3: scattered records)                                                      |
| UR7  | Provide auditable identity, time and outcome records without misreporting legal movements     | Statutory duties include updating the holding register within 36 hours and reporting movements within 3 days [4], [5]; internal passage through the race must never be filed as a farm movement |
| UR8  | Handle the agreed throughput without unacceptable queuing                                     | Keeping passage smooth is a stated customer job (§3); the trial target is 200 head within 90 minutes, counting re-reads and routine reviews                                                     |
| UR9  | Keep operating in the farm environment — wet, dirty, cold, corrosive — after routine cleaning | Robustness, reliability and maintainability in the actual barn are stated product requirements (§1); equipment must suit real conditions, not only the laboratory                               |
| UR10 | Match total cost of ownership with verified economic benefit                                  | Affordability is a stated requirement: price must be justified by value for money, evidenced by measured rather than claimed labour savings (§12)                                               |

UR1 acceptance reports confirmed-read accuracy and coverage separately: high accuracy on confirmed reads does not demonstrate adequate identification while many animals remain unresolved.

---

**字数核对**：正文约 495 词（含表格），符合 ≤1 页上限。  
**MoSCoW**：10/10 全部 Must have；无 Could/Should。  
**追溯**：UR1→§2/§3；UR2→\[6]；UR3→§2；UR4→\[8]；UR5→§2；UR6→§3；UR7→\[4\]\[5]；UR8→§3；UR9→§1；UR10→§12。
