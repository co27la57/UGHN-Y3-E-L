# R10 — Technical description of the solution (final, EN)

> 组员4（Part 4）交付物 · 依据 `08_组员资料/ID-Coo_项目要求与五人分工.md` 与 `牛只分流方案(1).md`  
> Cadmus Step 11 ｜ 10% ｜ 篇幅上限 4 页，含图 2 张（每张抵半页）→ 正文实际约 1,740 词（缺口补丁后，见缺口核查记录）  
> 图 1：`figures/fig_R10_layout.png`（物理布局）；图 2：`figures/fig_R10_block.png`（控制与数据框图）  
> 引用编号：团队 R13 表 [1]–[25] + 新增 [26] CIGR、[27] Cerqueira 2013（需组员5 收录，条目见交接说明）。

## 10. Technical description of the solution

*Prepared for the line manager. Version 1 is a concept design: staff confirm single-animal entry from outside the race; the system then reads, decides and diverts automatically. Nothing is yet validated on farm — Section 10.7 defines what must be proven before sale. Neither figure is a construction drawing.*

### 10.1 Physical structure

Animals travel through a single-file race: holding area → gate G0 → buffer section A → gate G1 → detection section B → gate G2 → diversion area with gate D (Figure 1). After reading, gate D selects one of two exits: the normal return channel, or the exception branch through pen gate H to the review pen. All animals leave B moving forward; D forms a guide boundary only and never pushes or squeezes an animal. Version 1 uses one buffer and one detection section; extra forward sections add waiting capacity, not throughput, and add gates and failure points. Adjustable commercial alleys (≈526–800 mm wide, 8 ft and 10 ft modules) indicate the structural envelope [13], [14]; an alley stop may assist backing control but never replaces the separating gate. Section length, clear width and antenna height follow CIGR dimensions for the target breed — adult Holstein–Friesian cows stand ≈1.4 m at the withers (CIGR 1.44 m at 650–749 kg [26]; field mean 1.41 m from 1,054 cows [27]), with body length ≈1.71–1.75 m and chest width ≈0.60 m [26], [27]; another breed means re-parameterising the same tables, not redesigning. Final dimensions and door swings come from the on-farm survey; module length is never assumed to equal one animal's length. The structure is designed for handling welfare — anti-slip drainage, no sharp projections, guarded tracks and hinges, head-neck and leg clearances, a continuous exit boundary and operating positions outside the pen [9]; head restraint stays a reference option, as the design does not assume head fixing. (UR8, UR9)

The review pen is a temporary holding area for manual verification, not a disease-isolation facility. It has an independent anti-return entry and a separate manual handling exit; gate H closes only after an animal has fully passed; when the pen is full or the branch blocked, intake stops and upstream pauses. Staff operate the pen gate from outside, with safe handling space. Capacity follows C ≥ λq × th + Cm (anomaly rate × handling interval + margin) — an average-load relation, so full-pen monitoring stays mandatory for consecutive anomalies. The budget scenario reuses an existing pen of about six head; as a floor, a sorting pen should hold at least one side of the milking parlour, with water, feed and lying space [26].

**Figure 1 — Race and diversion functional layout.**

### 10.2 Sensing equipment and capability boundaries

Two sensing modalities are used, each with a declared boundary (table below). A low-frequency RFID reader (ISO 11784/11785, HDX and FDX-B; Tru-Test XRP2/XRP2i as functional reference, final model by site survey) reads the statutory electronic ear tag through an antenna mounted outside the head/ear zone of section B [11], [12]. Six ultrasonic points (U-A, U-IN, U-B1, U-B2, U-N, U-Q; top-down mounting evaluated first for U-B1/U-B2) monitor occupancy and passage: distance d = c·Δt/2 is judged against an empty-race baseline, and every point reports *empty*, *occupied* or *uncertain* — no echo, stale data or a fault means uncertain, never empty, and one echo peak is never one animal [15]. Sensors are evaluated for manufacturer-supported time-shifted transmission to limit crosstalk [16]. The six points are a planning configuration: where diversion-area or entry coverage is insufficient, points are added — blind spots are never left for budget reasons.

| Subsystem             | Function                                                  | Capability boundary                                          |
| --------------------- | --------------------------------------------------------- | ------------------------------------------------------------ |
| Mechanical separation | Creates the single-animal space; blocks following animals | Does not prove the read zone is free of neighbouring animals |
| Ultrasonic sensing    | Occupancy, entry/exit, suspected following                | Cannot identify an animal or prove animal count              |
| RFID                  | Reads the electronic tag number                           | Cannot prove the tag is intact, why a read failed, or that one number means one animal |
| Gates and diversion   | Execute confirmed passage and exit choice                 | No diagnosis; no official identity decision                  |
| Manual review         | Checks tags, reconciles records                           | Never guesses identity from queue order [3]                  |

Mechanical separation does not separate radio read zones — even with one animal in B, the antenna may pick up a neighbour's number, so read attribution is tested explicitly (10.7); a cracked housing with a working chip, or a missing non-electronic tag, needs visual inspection. (UR1–UR3, UR9)

### 10.3 Control hardware, electrical and safety

Concept interfaces are listed below (Figure 2); voltages, drive power, cable protection and earthing follow the selected equipment and site design — this is not a construction circuit diagram. The PLC *requests* gate motions; the safety chain alone *permits* a drive, and software cannot bypass it. Safety-related control functions are specified by risk assessment following ISO 13849-1 — citing the standard claims no achieved performance level [25]. Anti-pinch protection combines validated coverage detection and obstruction response with mechanical guarding; ultrasonic points are never the sole protection. On power loss, hazardous motion stops and gates hold a defined state — never simply all-closed or all-open; a short backup keeps the controller alive to save state and signal. Staff free animals from outside; after restoration the system verifies actual gate and occupancy state and never resumes an interrupted motion. Use, training and inspection follow HSE guidance [8]. (UR4, UR5)

| Interface | Signal or data |
| --- | --- |
| Ultrasonic — PLC | Distance, status, update time, diagnostics |
| RFID — PLC | Number, receive time, device status |
| Gate position — PLC | Open, closed, locked, fault |
| Safety devices — safety chain | E-stop, obstruction, guard status |
| PLC — drives | Open, close, stop requests |
| Data system — farm software | Verified export or authorised interface |

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

Interlocks: G0 and G1 are never open together, nor G1 and G2; scanning starts only when both are confirmed closed, the animal is in the read zone and no following is suspected; D must be in position before G2 opens; the exit never switches while an animal occupies D's travel; an animal is never assumed to have left on a timer. Late results from a finished event stay in the log and never act on the next animal. These interlocks alone do not guarantee a single first entry — first entry and following separation are validated separately. Staff confirmation of single-animal entry is removed only after automatic separation, anti-pinch and exception handling are validated; version 1 economics include staff time.

| Situation                                                              | Outcome                                                 |
| ---------------------------------------------------------------------- | ------------------------------------------------------- |
| Valid single passage, one attributable number, no other anomaly        | Normal return — tag appearance not checked              |
| Animal present, limited re-reads exhausted, no reader fault detected   | Exception branch if available — reason "not read"       |
| Multiple numbers or unclear attribution                                | Hold in B, limited re-reads; still unclear → review pen |
| Suspected multiple animals, uncertain occupancy, door zone occupied    | Pause; re-separate safely or manual takeover            |
| Reader offline, ultrasonic fault, gate fault, branch blocked, pen full | Pause intake — never batch-flag as tag damage           |

An unread animal is still managed by its event number in B, but when mechanical state is unknown, automatic diversion stops; consecutive no-reads trigger a reader diagnostic, so a faulty reader cannot divert a whole group. (UR1–UR5)

### 10.5 Data, software and the farmer interface

Each event stores: event ID, start/end, scan and release times, occupancy and gate summaries, raw and de-duplicated reads, device diagnostics, decision reason, planned and confirmed exit, handling staff and change history. The event ID is separate from official identity: with no read, the identity field stays empty and staff link it after manual verification, keeping the original exception and change record [3]; where both official visual identifiers are insufficient, the official procedure is followed — a substitute official number is never created. The interface shows four states — electronically verified, identity pending review, equipment/race fault, manually resolved — plus current event and pen load, with permission-controlled manual actions and a daily report of open events and maintenance records. A reader fault is never displayed as a damaged tag. (UR5–UR7)

### 10.6 LIS and farm-software interface

Version 1 stores locally and produces audited exports; no direct LIS connection is claimed. Once the interface specification and authorisation exist, an adaptation layer will separate internal passage from reportable movements, validate numbers and fields, keep submissions and receipts, prevent duplicates, and cache offline submissions [1], [4], [5]. The interface distinguishes locally saved, to-report, submit-failed and receipt-confirmed; changing an existing official identity or filing a statutory report keeps a human approval step. (UR6, UR7)

### 10.7 Pricing, throughput and validation


Planned pricing is £18,500 installation (excluding VAT and major civil works) plus £720/year service and an assumed £60/year energy — the basis of the affordability case in Section 12; the design keeps sensing, gates and safety inside this envelope by reusing the existing race and pen. The throughput target is 150 head/hour (≈24 s per animal for entry, door actions, scan and handling) against a trial requirement of 200 head in 90 minutes (≈133 head/hour) including re-reads and reviews; if missed, location, flow or structure is adjusted — safety confirmations are never cut. (UR8, UR10)

| Stage                    | What is verified                                           | Pass criterion                              |
| ------------------------ | ---------------------------------------------------------- | ------------------------------------------- |
| Bench                    | Latency, duplicate reads, comms loss, gate-state conflicts | State machine and event attribution correct |
| No animal                | Simulated occupancy, obstruction, e-stop, power loss       | No unpermitted hazardous motion             |
| Supervised cattle trials | Sizes, bunching, stopping, backing                         | Separation and passage work                 |
| RF and environment       | Neighbour reads, steel structure, soiling, interference    | Read zone and occupancy valid               |
| Tag conditions           | Working, dead, missing, cracked-but-readable, neighbour-read tags | Mis-diversion and misses recorded separately |
| Farm pilot               | Tasks, pen, maintenance, staff time                        | Efficiency and net benefit acceptable       |

Measured per stage: confirmed-read accuracy and coverage separately, mis-diversion and exception-handling rates, exit consistency, takeover count and net labour time. Repeating the same herd is not an independent sample and zero observed errors is not zero risk; separation, read attribution and safe release are proven before economics. (UR1–UR10)

---

**字数核对**：正文约 1,740 词 + 表 4 张 + 图 2 张（各抵半页）；紧凑排版 ≈ 4.0–4.2 页，贴近上限。若 Cadmus 实际排版超出 4 页，按交接说明的压缩优先级清单处理（先并接口表、再压事件字段列表）。  
**对齐检查**：UR1–UR10 全部在文中标注对应段落；价格点 £18,500 + £720/年 + £60/年 与 R12 一致；USP（逐头核验 / 异常安全分流 / 完整事件记录）由 10.1–10.5 支撑；10.1 已显式给出 HF 体型参数（[26] 标准 + [27] 1,054 头实测双重支撑）、复核围栏设计底线（CIGR 3.10.3，通用工程惯例）与处理福利结构要求 [9]；10.3 含接口表；10.7 验证计划含耳标状态矩阵。  
**引用**：\[1\]\[3\]\[4\]\[5\]\[6\]\[8\]\[11\]\[12\]\[13\]\[14\]\[15\]\[16\]\[25\]\[26\]\[27\] 中，[1]–[25] 在 R13 表内；**[26]（CIGR）与 [27]（Cerqueira 2013）为新增，需组员5 加入 R13**，条目见交接说明。
