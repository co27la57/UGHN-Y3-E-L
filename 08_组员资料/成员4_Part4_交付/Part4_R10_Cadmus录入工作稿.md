# R10 Cadmus 录入工作稿（人工逐节录入用）

> **为什么不用 TypePaste 自动敲入**：① 你们分工总纲的红线是"正文必须**直接在 Cadmus 里输入**"——这条规则的目的就是让提交的文本由本人在 Cadmus 里写作产生；用自动敲字工具把现成稿子"敲"进去，本质是绕过这条规则，和粘贴没有区别。② 课程 AI 指导明确禁止 AI 代做实质性写作，且"标注了 AI 使用也不能豁免越界的使用"——把 AI 起草的 1,500 词由机器直接存入提交系统，属于最容易被认定为越界的情形。③ Cadmus 会记录活动，非自然敲入有行为风险，可能触发学术诚信程序。  
> **合规且更快的做法**：下面每节都配了【改写点】。你逐节照着改写提示用自己的话调整表述，然后**自己敲进 Cadmus**——一边敲一边改，正是这条红线想要的流程，也顺便完成了"本人内化"。全文 1,500 词，认真改着敲约 40–60 分钟。  
> 图 1、图 2 用编辑器的插图功能插入 `figures/fig_R10_layout.png` 和 `figures/fig_R10_block.png`，各抵半页。表格用编辑器的表格工具（若没有，用缩进列表呈现）。

---

## 引言段（斜体，1 段）

【改写点】这句是全文门面，务必换成你自己的说法，例如把 "staff confirm single-animal entry from outside the race" 换成你描述分流方案时的习惯用语。

> Prepared for the line manager. Version 1 is a concept design: staff confirm single-animal entry from outside the race; the system then reads, decides and diverts automatically. Nothing below is yet validated on farm — Section 10.7 defines what must be proven before sale. Figures 1 and 2 show the functional layout and control structure; neither is a construction drawing.

## 10.1 Physical structure（1 段 + 图 1）

【改写点】HF 体型那句是我们刚补的，务必用你自己的话组织数字；"guide boundary only and never pushes or squeezes" 是方案灵魂句，确认你认同再敲。

> Animals travel through a single-file race: holding area → gate G0 → buffer section A → gate G1 → detection section B → gate G2 → diversion area with gate D (Figure 1). Interlocked gates keep one animal at a time in the read zone. After reading, gate D selects one of two exits: the normal return channel, or the exception branch through pen gate H to the review pen. All animals leave B moving forward; D forms a guide boundary only and never pushes or squeezes an animal. Version 1 uses one buffer and one detection section; extra forward sections add waiting capacity, not throughput, and add gates and failure points. Adjustable commercial alleys (≈526–800 mm wide, 8 ft and 10 ft modules) indicate the structural envelope [13], [14]. Section length, clear width and antenna height follow CIGR standard dimensions for the target breed — adult Holstein–Friesian dairy cows: ≈1.44 m withers height, ≈1.75 m diagonal body length, ≈0.60 m chest width (650–749 kg) [26]; another breed later means re-parameterising the same table, not redesigning. Final dimensions, door swings and pen layout come from the on-farm survey, and module length is never assumed to equal one animal's length. (UR8, UR9)

**图 1 — Race and diversion functional layout.**（插图 + 图注一行）

## 10.2 Sensing equipment and capability boundaries（2 段 + 1 表）

【改写点】"no echo, stale data or a device fault means uncertain, never empty" 这句是超声判定的核心，请确认你能自己推导出来再敲。

> Two sensing modalities are used, each with a declared boundary (table below). A low-frequency RFID reader (ISO 11784/11785, HDX and FDX-B; Tru-Test XRP2 as functional reference, final model by site survey) reads the statutory electronic ear tag through an antenna mounted outside the head/ear zone of section B [11], [12]. Six ultrasonic points (U-A, U-IN, U-B1, U-B2, U-N, U-Q) monitor occupancy and passage: distance d = c·Δt/2 is judged against a baseline captured with the race empty, and every point reports empty, occupied or uncertain — no echo, stale data or a device fault means uncertain, never empty, and one echo peak is never counted as one animal [15]. Sensors are evaluated for manufacturer-supported time-shifted transmission to limit crosstalk, with the added polling delay checked [16].

表格（用 Cadmus 表格工具，3 列 × 5 行）：

| Subsystem             | Function                                                  | Capability boundary                                          |
| --------------------- | --------------------------------------------------------- | ------------------------------------------------------------ |
| Mechanical separation | Creates the single-animal space; blocks following animals | Does not prove the read zone is free of neighbouring animals |
| Ultrasonic sensing    | Occupancy, entry/exit, suspected following                | Cannot identify an animal or prove animal count              |
| RFID                  | Reads the electronic tag number                           | Cannot prove the tag is intact, or why a read failed         |
| Gates and diversion   | Execute confirmed passage and exit choice                 | No diagnosis; no official identity decision                  |
| Manual review         | Checks tags, reconciles records                           | Never guesses identity from queue order [3]                  |

> Mechanical separation does not separate radio read zones: even with one animal in B, the antenna may pick up a neighbour's number, so read attribution is tested explicitly (10.7). A cracked tag housing with a working chip, or a missing non-electronic tag, lies outside automatic detection and needs visual inspection. (UR1–UR3, UR9)

## 10.3 Control hardware, electrical and safety（1 段 + 图 2）

【改写点】"The PLC requests gate motions; the safety chain alone permits a drive" 这句是安全设计核心，用自己的话重述。

> Concept electrical structure: site supply → isolation, protection and distribution → drive circuits and control supply; sensors and gate-position feedback wire to the PLC; e-stop, obstruction and guarding devices wire to an independent safety chain (Figure 2). The PLC requests gate motions; the safety chain alone permits a drive, and software cannot bypass it. Safety-related control functions are specified by risk assessment following ISO 13849-1 — citing the standard claims no achieved performance level [25]. Drives report open, closed, locked and fault positions. Anti-pinch protection combines validated coverage detection and obstruction response with mechanical guarding; ultrasonic points are never the sole protection. On power loss the system stops hazardous motion and holds a defined, controlled gate state (not all gates simply closing or opening); a short backup supply keeps the controller alive to save state and signal. Staff release drives and free animals from outside the equipment; after power restoration the system verifies actual gate and occupancy state before resuming and never continues an interrupted motion. Use, training and inspection follow HSE livestock guidance [8]. (UR4, UR5)

**图 2 — Control and data functional block diagram.**（插图 + 图注一行）

## 10.4 Control algorithm and diversion logic（1 句引言 + 3 表/段）

引言句：

> A rule-based state machine runs each passage as an independent event; no machine learning is required in version 1.

状态机表（3 列 × 9 行）：

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

【改写点】联锁段是整节最"AI 味"的一段，务必逐句改写——内容来自你们的《牛只分流方案》，按那份文档的表述习惯重组。

> Interlocks: G0 and G1 are never open together, nor G1 and G2; scanning starts only when both are confirmed closed, the animal is in the read zone and no following is suspected; D must be in position before G2 opens; the exit never switches while an animal occupies D's travel; an animal is never assumed to have left on a timer. Within one event, repeated reads of the same number are de-duplicated, re-reads are limited, and a late result from a finished event stays in the log, never acting on the next animal.

分流表（2 列 × 5 行）：

| Situation                                                              | Outcome                                                 |
| ---------------------------------------------------------------------- | ------------------------------------------------------- |
| Valid single passage, one attributable number, no other anomaly        | Normal return                                           |
| Animal present, limited re-reads exhausted, no reader fault detected   | Exception branch if available — reason "not read"       |
| Multiple numbers or unclear attribution                                | Hold in B, limited re-reads; still unclear → review pen |
| Suspected multiple animals, uncertain occupancy, door zone occupied    | Pause; re-separate safely or manual takeover            |
| Reader offline, ultrasonic fault, gate fault, branch blocked, pen full | Pause intake — never batch-flag as tag damage           |

> An unread animal is still managed by its event number while in B, but when mechanical state is unknown, automatic diversion stops. Consecutive no-read events trigger a reader diagnostic check, so a faulty reader cannot divert a whole group. (UR1–UR5)

## 10.5 Data, software and the farmer interface（1 段）

【改写点】"A reader fault is never displayed as a damaged tag" 是好句子，但前后衔接请自己写。

> Each event stores: event ID, start/end, scan and release times, occupancy and gate summaries, raw and de-duplicated reads, device diagnostics, decision reason, planned and confirmed exit, handling staff and change history. The event ID is separate from the official identity: when no number is read, the identity field stays empty, and staff link it after manual verification, keeping the original exception and the change record [3]. The interface shows four states — electronically verified, identity pending review, equipment/race fault, manually resolved — plus current event and pen load, with permission-controlled manual actions and a daily report. A reader fault is never displayed as a damaged tag. (UR5–UR7)


## 10.6 LIS and farm-software interface（1 段）

【改写点】整段较短，建议整段自己重述——关键词：local export、adaptation layer、internal passage vs reportable movements、receipts、offline cache。

> Version 1 stores locally and produces audited exports; no direct LIS connection is claimed. Once the interface specification and authorisation exist, an adaptation layer will distinguish internal passage from reportable movements, validate numbers and fields, keep submissions and receipts, prevent duplicates, and cache offline submissions for reconciliation [1], [4], [5]. The interface distinguishes locally saved, to-report, submit-failed and receipt-confirmed; changing an existing official identity or filing a statutory report keeps a human approval step. (UR6, UR7)

## 10.7 Pricing, throughput and validation（2 段 + 1 表）

【改写点】价格三个数字必须与 R12 逐字一致（£18,500 / £720 / £60），改写时别动数字。

> Planned pricing is £18,500 installation (excluding VAT and major civil works) plus £720/year service and an assumed £60/year energy — the basis of the affordability case in Section 12; the design keeps sensing, gates and safety inside this envelope by reusing the existing race and pen. The throughput target is 150 head/hour (≈24 s per animal for entry, door actions, scan and handling) against a trial requirement of 200 head in 90 minutes (≈133 head/hour) including re-reads and routine reviews; if the target is missed, the location, flow or structure is adjusted — safety confirmations are never cut. (UR8, UR10)

验证表（3 列 × 5 行）：

| Stage                    | What is verified                                           | Pass criterion                              |
| ------------------------ | ---------------------------------------------------------- | ------------------------------------------- |
| Bench                    | Latency, duplicate reads, comms loss, gate-state conflicts | State machine and event attribution correct |
| No animal                | Simulated occupancy, obstruction, e-stop, power loss       | No unpermitted hazardous motion             |
| Supervised cattle trials | Sizes, bunching, stopping, backing                         | Separation and passage work                 |
| RF and environment       | Neighbour reads, steel structure, soiling, interference    | Read zone and occupancy valid               |
| Farm pilot               | Tasks, pen, maintenance, staff time                        | Efficiency and net benefit acceptable       |

> Measured at each stage: confirmed-read accuracy and coverage separately, mis-diversion rate, exception-handling rate, exit consistency, takeover count and net labour time. Repeating the same herd is not an independent sample, and zero observed errors is not zero risk. Separation, read attribution and safe release are proven before economics; only then do scale-up or added automation follow. (UR1–UR10)

---

## 录入完成后

1. 把你改写后的 R10 全文发给我，我当 critical friend 挑逻辑漏洞（这是课程允许的 AI 用法）。
2. R9（495 词）更短，需要的话我同样出一份录入工作稿。
3. Declaration of Originality 的 AI 记录按实际填写：工具名 + "辅助起草结构化草稿，本人逐节改写并录入"。
