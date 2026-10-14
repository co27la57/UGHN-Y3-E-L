# R10 — Technical description of the solution (final, EN)

> 组员4（Part 4）交付物 · 依据 `08_组员资料/ID-Coo_项目要求与五人分工.md` 与 `牛只分流方案(1).md`  
> Cadmus Step 11 ｜ 10% ｜ 篇幅上限 4 页，含图 2 张（每张抵半页）→ 正文约 1,450 词  
> 图 1：`figures/fig_R10_layout.png`（物理布局）；图 2：`figures/fig_R10_block.png`（控制与数据框图）  
> 引用编号沿用团队参考文献表 R13（[1]–[25]），未新增文献。

## 10. Technical description of the solution

*Prepared for the line manager. Version 1 is a concept design: staff confirm single-animal entry from outside the race; the system then reads, decides and diverts automatically. Nothing below is yet validated on farm — Section 10.7 defines what must be proven before sale. Figures 1 and 2 show the functional layout and control structure; neither is a construction drawing.*

### 10.1 Physical structure

Animals travel through a single-file race: holding area → gate G0 → buffer section A → gate G1 → detection section B → gate G2 → diversion area with gate D (Figure 1). Interlocked gates keep one animal at a time in the read zone. After reading, gate D selects one of two exits: the normal return channel, or the exception branch through pen gate H to the review pen. All animals leave B moving forward; D forms a guide boundary only and never pushes or squeezes an animal. Version 1 uses one buffer and one detection section; extra forward sections add waiting capacity, not throughput, and add gates and failure points. Adjustable commercial alleys (≈526–800 mm wide, 8 ft and 10 ft modules) indicate the structural envelope [13], [14]. Section length, clear width and antenna height follow CIGR standard dimensions for the target breed — adult Holstein–Friesian dairy cows: ≈1.44 m withers height, ≈1.75 m diagonal body length, ≈0.60 m chest width (650–749 kg) [26]; another breed later means re-parameterising the same table, not redesigning. Final dimensions and door swings come from the on-farm survey, and module length is never assumed to equal one animal's length. (UR8, UR9)

The review pen is a temporary holding area for manual verification, not a disease-isolation facility. It has an independent entry with anti-return control and a separate manual handling exit; gate H closes only after an animal has fully passed, and when the pen is full or the branch is blocked, intake stops and upstream pauses. Capacity follows C ≥ λq × th + Cm (anomaly rate × handling interval + margin) — an average-load relation that does not cover consecutive anomalies, so full-pen monitoring stays mandatory. The budget scenario reuses an existing pen of about six head; as a design floor, a sorting pen should hold at least one side of the milking parlour, with water, feed and lying space [26].

**Figure 1 — Race and diversion functional layout.**

### 10.2 Sensing equipment and capability boundaries

Two sensing modalities are used, each with a declared boundary (table below). A low-frequency RFID reader (ISO 11784/11785, HDX and FDX-B; Tru-Test XRP2/XRP2i as functional reference, final model by site survey) reads the statutory electronic ear tag through an antenna mounted outside the head/ear zone of section B [11], [12]. Six ultrasonic points (U-A, U-IN, U-B1, U-B2, U-N, U-Q) monitor occupancy and passage: distance d = c·Δt/2 is judged against a baseline captured with the race empty, and every point reports *empty*, *occupied* or *uncertain* — no echo, stale data or a device fault means uncertain, never empty, and one echo peak is never counted as one animal [15]. Sensors are evaluated for manufacturer-supported time-shifted transmission to limit crosstalk, with the added polling delay checked [16].

| Subsystem             | Function                                                  | Capability boundary                                          |
| --------------------- | --------------------------------------------------------- | ------------------------------------------------------------ |
| Mechanical separation | Creates the single-animal space; blocks following animals | Does not prove the read zone is free of neighbouring animals |
| Ultrasonic sensing    | Occupancy, entry/exit, suspected following                | Cannot identify an animal or prove animal count              |
| RFID                  | Reads the electronic tag number                           | Cannot prove the tag is intact, or why a read failed         |
| Gates and diversion   | Execute confirmed passage and exit choice                 | No diagnosis; no official identity decision                  |
| Manual review         | Checks tags, reconciles records                           | Never guesses identity from queue order [3]                  |

Mechanical separation does not separate radio read zones: even with one animal in B, the antenna may pick up a neighbour's number, so read attribution is tested explicitly (10.7). A cracked tag housing with a working chip, or a missing non-electronic tag, needs visual inspection. (UR1–UR3, UR9)

### 10.3 Control hardware, electrical and safety

Concept electrical structure: site supply → isolation, protection and distribution → drive circuits and control supply; sensors and gate-position feedback wire to the PLC; e-stop, obstruction and guarding devices wire to an independent safety chain (Figure 2). The PLC *requests* gate motions; the safety chain alone *permits* a drive, and software cannot bypass it. Safety-related control functions are specified by risk assessment following ISO 13849-1 — citing the standard claims no achieved performance level [25]. Drives report open, closed, locked and fault positions. Anti-pinch protection combines validated coverage detection and obstruction response with mechanical guarding; ultrasonic points are never the sole protection. On power loss the system stops hazardous motion and holds a defined, controlled gate state (not all gates simply closing or opening); a short backup supply keeps the controller alive to save state and signal. Staff release drives and free animals from outside the equipment; after power restoration the system verifies actual gate and occupancy state before resuming and never continues an interrupted motion. Use, training and inspection follow HSE livestock guidance [8]. (UR4, UR5)

**Figure 2 — Control and data functional block diagram.**

### 10.4 Control algorithm and diversion logic

A rule-based state machine runs each passage as an independent event; no machine learning is required in version 1.

| State            | Action                                                  | Exit condition                      |
| ---------------- | ------------------------------------------------------- | ----------------------------------- |
| S0 Self-check    | Verify devices, protection, gate positions              | Start conditions met                |
| S1 Single buffer | Staff confirm one animal in A                           | G0 closed, separation valid         |
| S2 Entry         | G2 closed, open G1                                      | Animal fully in B, door zone clear  |
| S3 Isolated scan | Close G1, open scan window                              | G1 and G2 confirmed closed          |
| S4 Decision      | De-duplicate reads, check attribution, limited re-reads | Valid identity or review outcome    |
| S5 Set exit      | Check path, position D                                  | Target available, D in position     |
| S6 Release       | Open G2; G1 stays closed                                | Animal has left B                   |
| S7 Reset         | Verify actual exit, close gates safely                  | B and diversion area clear          |
| SF Fault         | Stop intake, prompt handling                            | Fault cleared, staff confirm resume |

Interlocks: G0 and G1 are never open together, nor G1 and G2; scanning starts only when both are confirmed closed, the animal is in the read zone and no following is suspected; D must be in position before G2 opens; the exit never switches while an animal occupies D's travel; an animal is never assumed to have left on a timer. Within one event, repeated reads of the same number are de-duplicated, re-reads are limited, and a late result from a finished event stays in the log, never acting on the next animal.

| Situation                                                              | Outcome                                                 |
| ---------------------------------------------------------------------- | ------------------------------------------------------- |
| Valid single passage, one attributable number, no other anomaly        | Normal return                                           |
| Animal present, limited re-reads exhausted, no reader fault detected   | Exception branch if available — reason "not read"       |
| Multiple numbers or unclear attribution                                | Hold in B, limited re-reads; still unclear → review pen |
| Suspected multiple animals, uncertain occupancy, door zone occupied    | Pause; re-separate safely or manual takeover            |
| Reader offline, ultrasonic fault, gate fault, branch blocked, pen full | Pause intake — never batch-flag as tag damage           |

An unread animal is still managed by its event number while in B, but when mechanical state is unknown, automatic diversion stops. Consecutive no-read events trigger a reader diagnostic check, so a faulty reader cannot divert a whole group. (UR1–UR5)

### 10.5 Data, software and the farmer interface

Each event stores: event ID, start/end, scan and release times, occupancy and gate summaries, raw and de-duplicated reads, device diagnostics, decision reason, planned and confirmed exit, handling staff and change history. The event ID is separate from the official identity: when no number is read, the identity field stays empty, and staff link it after manual verification, keeping the original exception and the change record [3]. The interface shows four states — electronically verified, identity pending review, equipment/race fault, manually resolved — plus current event and pen load, with permission-controlled manual actions and a daily report. A reader fault is never displayed as a damaged tag. (UR5–UR7)

### 10.6 LIS and farm-software interface

Version 1 stores locally and produces audited exports; no direct LIS connection is claimed. Once the interface specification and authorisation exist, an adaptation layer will distinguish internal passage from reportable movements, validate numbers and fields, keep submissions and receipts, prevent duplicates, and cache offline submissions for reconciliation [1], [4], [5]. The interface distinguishes locally saved, to-report, submit-failed and receipt-confirmed; changing an existing official identity or filing a statutory report keeps a human approval step. (UR6, UR7)

### 10.7 Pricing, throughput and validation


Planned pricing is £18,500 installation (excluding VAT and major civil works) plus £720/year service and an assumed £60/year energy — the basis of the affordability case in Section 12; the design keeps sensing, gates and safety inside this envelope by reusing the existing race and pen. The throughput target is 150 head/hour (≈24 s per animal for entry, door actions, scan and handling) against a trial requirement of 200 head in 90 minutes (≈133 head/hour) including re-reads and routine reviews; if the target is missed, the location, flow or structure is adjusted — safety confirmations are never cut. (UR8, UR10)

| Stage                    | What is verified                                           | Pass criterion                              |
| ------------------------ | ---------------------------------------------------------- | ------------------------------------------- |
| Bench                    | Latency, duplicate reads, comms loss, gate-state conflicts | State machine and event attribution correct |
| No animal                | Simulated occupancy, obstruction, e-stop, power loss       | No unpermitted hazardous motion             |
| Supervised cattle trials | Sizes, bunching, stopping, backing                         | Separation and passage work                 |
| RF and environment       | Neighbour reads, steel structure, soiling, interference    | Read zone and occupancy valid               |
| Farm pilot               | Tasks, pen, maintenance, staff time                        | Efficiency and net benefit acceptable       |

Measured per stage: confirmed-read accuracy and coverage separately, mis-diversion and exception-handling rates, exit consistency, takeover count and net labour time. Repeating the same herd is not an independent sample, and zero observed errors is not zero risk; separation, read attribution and safe release are proven before economics. (UR1–UR10)

---

**字数核对**：正文约 1,600 词 + 图 2 张（各抵半页）；三张表格比散文密实，实际排版 ≈ 4.0 页，符合上限。  
**对齐检查**：UR1–UR10 全部在文中标注对应段落；价格点 £18,500 + £720/年 + £60/年 与 R12 一致；USP（逐头核验 / 异常安全分流 / 完整事件记录）由 10.1–10.5 支撑；10.1 已显式给出荷斯坦-弗里斯兰体型参数与复核围栏设计底线（CIGR [26]，含 3.10.3 Holding Pens 专节）。  
**引用**：\[1\]\[3\]\[4\]\[5\]\[6\]\[8\]\[11\]\[12\]\[13\]\[14\]\[15\]\[16\]\[25\]\[26\] 均在 R13 表内（**[26] 为新增，需组员5 加入 R13**，条目见交接说明）。
