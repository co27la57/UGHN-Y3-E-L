# 10. Technical description of the solution

> This is the Section 10 text in `ID-Coo_报告提交框架_EN_R9完成_R10四页版.docx`. The Word report is the submission version; reference numbers follow its IEEE list [1]–[26]. The five detailed matrices remain in `Part4_R10_Technical_Description_EN.md` as development notes.

## 10.1 Physical structure

ID-Coo uses a single-file race: holding area → gate G0 → buffer A → gate G1 → detection section B → gate G2. Gate D then directs the cow either back to the herd or, through gate H, into the review pen (Figure 1). Both exits lead forward; D guides rather than pushes the animal.

Version 1 has one buffer and one detection section. More upstream sections would add waiting space, not speed to the read-and-divert cycle, while adding gates and faults. Adjustable alleys about 526–800 mm wide, with 8 ft and 10 ft modules, indicate a structural envelope [16], [17]. A backing stop may help with reversal but cannot replace the separating gate.

CIGR gives a 650–749 kg Holstein–Friesian cow a withers height of 1.44 m, body length of 1.75 m and chest width of 0.60 m [18]. A field study of 1,054 cows reports a mean withers height of 1.411 m and trunk length of 1.708 m [19]. These guide section length, clear width and antenna height. A farm survey must confirm final dimensions and gate swings; a standard module does not necessarily hold one cow. Other breeds require a fresh dimensional check.

The race requires non-slip drainage, no sharp projections, guarded tracks and hinges, safe head and leg clearances, and continuous exit boundaries [20]. Staff operate from outside; head restraint is optional. (UR4, UR8, UR9)

The review pen temporarily holds cows for manual identity checks; it is not for disease isolation. It needs an anti-return entrance, separate handling exit and outside operating space. Gate H closes only after the cow passes. A full pen or blocked branch stops intake.

Capacity follows C ≥ λq × th + Cm (exception rate × handling interval + margin). Because this is an average-load relation, the pen also needs full-pen monitoring. The budget assumes reuse of an existing pen for roughly six cattle. CIGR generally recommends capacity for one parlour side but excepts sorting at the parlour exit. Holding pens should provide water, feed and lying space [18]; the site survey must confirm capacity and facilities.

![Figure 1 — Race and diversion functional layout](figures/fig_R10_layout.png)

*Figure 1 — Race and diversion functional layout.*

## 10.2 Sensing equipment and capability boundaries

An LF RFID reader scans LF EID tags where fitted using ISO 11784/11785, HDX and FDX-B. Cattle without an LF EID tag follow manual identity verification or an alternative workflow; an absent read alone does not diagnose tag damage [1]. Tru-Test XRP2/XRP2i is a functional reference; the final reader and antenna position outside B's head-and-ear zone depend on the site survey [4], [21].

Six planned ultrasonic points (U-A, U-IN, U-B1, U-B2, U-N, U-Q) monitor occupancy and passage; top-down mounting is assessed first for U-B1/U-B2. Distance, d = c × Δt / 2, is compared with an empty-race baseline. Each point reports *empty*, *occupied* or *uncertain*. No echo, stale data or a fault means *uncertain*; one echo cannot prove that only one cow is present [22].

Manufacturer-supported staggered transmission will be evaluated to limit crosstalk [23]. Six points are provisional; blind spots at entry or diversion require additional coverage.

An antenna may read a neighbouring tag even when one cow occupies B. The trial must therefore establish read attribution rather than infer it from a closed gate (Section 10.7). Cracked but readable tags and missing non-electronic tags still need visual inspection. (UR1–UR3, UR9)

## 10.3 Control hardware, electrical and safety

Figure 2 shows functional interfaces, not construction wiring. Voltage, drive rating, cable protection and earthing depend on the chosen equipment and site. The PLC sends motion requests directly to the gate drives. Separately, safety-related control monitors risk-assessed protection devices and can stop or inhibit the drives independently; software and data interfaces cannot bypass it. Site-selected enclosures, connectors and cables must withstand wash-down, ingress and corrosion; operation is checked after routine cleaning. (UR9)

Safety functions and required performance levels follow a site risk assessment using ISO 13849-1 [24]; no achieved level is claimed. Mechanical guards and validated obstruction responses protect the gates. Ultrasonic points alone cannot provide anti-pinch protection.

On power loss, hazardous movement stops and each gate holds a defined state; a short backup saves the event and signals the fault. Staff can release cattle from outside. On restart, the controller verifies gate positions and occupancy rather than resuming interrupted motion. Training and inspection follow HSE guidance [25]. (UR4, UR5)

![Figure 2 — Functional control, safety and data interfaces](figures/fig_R10_block.png)

*Figure 2 — Functional control, safety and data interfaces.*

## 10.4 Control algorithm and diversion logic

A rule-based state machine handles each passage separately; version 1 needs no machine learning. Staff confirm one cow in A, after which the controller admits her to B, reads the tag, sets the exit and confirms the route taken.

Process interlocks keep G0/G1 and G1/G2 from opening together. Scanning requires both B gates closed, a cow in the read zone and no suspected follower. D must be positioned before G2 opens and cannot move while its path is occupied. Sensors and gate feedback confirm exit; a timer alone cannot.

Late reads remain with their original event and cannot redirect the next cow. Process interlocks do not prove safe first entry, so version 1 retains staff confirmation and counts that time in its economics. Automatic entry requires prior validation of separation, anti-pinch protection and exception handling.

An unread cow retains an event ID while in B. Uncertain mechanical state stops automatic diversion; consecutive no-reads trigger reader diagnostics before a whole group can be misdirected. (UR1–UR5)

## 10.5 Data, software and the farmer interface

Each event records its ID, timing, occupancy and gate state, raw and de-duplicated reads, device status, decision reason, planned and actual exit, operator and edit history.

Event ID and official identity remain separate. If no tag is read, identity stays blank until staff verify it; the original exception and later link remain auditable. If official visual identifiers also fail, staff follow the official procedure rather than invent a number.

The farmer interface distinguishes electronically verified, pending identity review, equipment/race fault and manually resolved. It shows the active event, pen load, open cases and maintenance record, with access-controlled manual actions. A reader fault never appears as a damaged-tag diagnosis. (UR5–UR7)

## 10.6 LIS and farm-software interface

Version 1 stores records locally and exports them for audit; direct LIS access is not assumed. If specifications and authorisation become available, an adapter will separate internal passages from reportable movements, validate fields, retain submissions and receipts, prevent duplicates, and reconcile after outages [1], [8], [26].

The interface shows locally saved, pending, failed and receipt-confirmed states. Changes to official identity and statutory submissions require human approval. (UR6, UR7)

## 10.7 Pricing, throughput and validation

The planned installed price is £18,500 excluding VAT and major civil works, plus £720/year service and an assumed £60/year electricity (Section 12). It assumes reuse of the existing race and review pen, while covering sensors, gates and safety equipment. Payback is recalculated using final quotations, service and energy costs, and measured net labour savings. (UR10)

Target throughput is 150 head/hour (about 24 seconds per cow for entry, gates, reading and handling). The trial requires 200 cows in 90 minutes (about 133 head/hour), including retries and reviews. If unmet, the site or flow changes; safety checks do not. (UR8, UR10)

Trials report confirmed-read accuracy against a provisional ≥99.5% target and coverage separately, plus wrong diversions, exceptions, actual versus planned exits, takeovers and net labour time. Repeated passages by one herd are not independent animals; zero observed errors is not zero risk. Safe separation, read attribution and release precede economic validation. (UR1–UR10)
