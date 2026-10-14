#!/usr/bin/env python3
"""Build the HerdLens PRD + Business Model report as a .docx staging document."""
import os
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

BASE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(BASE, "06_图表", "figures")
OUTPATH = os.path.join(BASE, "03_方案与报告", "Cow identification PRD + Business Model - DRAFT.docx")

ACCENT = RGBColor(0x14, 0x4A, 0x7A)
DARK = RGBColor(0x1F, 0x24, 0x30)

doc = Document()

# ---------------------------------------------------------------- page setup
sec = doc.sections[0]
sec.page_height = Cm(29.7)
sec.page_width = Cm(21.0)
for attr, val in (("top_margin", 2.2), ("bottom_margin", 2.2),
                  ("left_margin", 2.3), ("right_margin", 2.3)):
    setattr(sec, attr, Cm(val))

st = doc.styles["Normal"]
st.font.name = "Arial"
st.font.size = Pt(10.5)
st._element.rPr.rFonts.set(qn("w:eastAsia"), "Arial")
pf = st.paragraph_format
pf.space_after = Pt(7)
pf.line_spacing = 1.15
pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

for name, size, color, before, after in (
    ("Heading 1", 15, ACCENT, 18, 8),
    ("Heading 2", 12.5, ACCENT, 13, 6),
    ("Heading 3", 11, DARK, 10, 4),
):
    s = doc.styles[name]
    s.font.name = "Arial"
    s.font.size = Pt(size)
    s.font.bold = True
    s.font.color.rgb = color
    s.paragraph_format.space_before = Pt(before)
    s.paragraph_format.space_after = Pt(after)
    s.paragraph_format.keep_with_next = True


def para(text, style=None, bold=False, italic=False, size=None, align=None,
         space_after=None, indent=None):
    p = doc.add_paragraph(style=style)
    r = p.add_run(text)
    r.bold = bold
    r.italic = italic
    if size:
        r.font.size = Pt(size)
    if align is not None:
        p.alignment = align
    if space_after is not None:
        p.paragraph_format.space_after = Pt(space_after)
    if indent is not None:
        p.paragraph_format.left_indent = Cm(indent)
    return p


def rich(parts, space_after=None, indent=None, size=None):
    """parts: list of (text, bold, italic)."""
    p = doc.add_paragraph()
    for t, b, i in parts:
        r = p.add_run(t)
        r.bold = b
        r.italic = i
        if size:
            r.font.size = Pt(size)
    if space_after is not None:
        p.paragraph_format.space_after = Pt(space_after)
    if indent is not None:
        p.paragraph_format.left_indent = Cm(indent)
    return p


def bullet(text, bold_lead=None, level=0):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.left_indent = Cm(0.75 + level * 0.6)
    p.paragraph_format.space_after = Pt(3)
    if bold_lead:
        r = p.add_run(bold_lead)
        r.bold = True
    p.add_run(text)
    return p


def num(text, bold_lead=None):
    p = doc.add_paragraph(style="List Number")
    p.paragraph_format.left_indent = Cm(0.85)
    p.paragraph_format.space_after = Pt(3)
    if bold_lead:
        r = p.add_run(bold_lead)
        r.bold = True
    p.add_run(text)
    return p


def caption(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(12)
    r = p.add_run(text)
    r.italic = True
    r.font.size = Pt(9)
    r.font.color.rgb = RGBColor(0x5B, 0x64, 0x72)
    return p


def figure(name, text, width_cm=15.6):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(2)
    p.add_run().add_picture(os.path.join(FIG, name), width=Cm(width_cm))
    caption(text)


def table(headers, rows, widths=None, font_size=8.5):
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = t.rows[0].cells
    for i, h in enumerate(headers):
        hdr[i].text = ""
        p = hdr[i].paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(font_size)
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_after = Pt(2)
        shd = OxmlElement("w:shd")
        shd.set(qn("w:fill"), "E8EEF5")
        hdr[i]._tc.get_or_add_tcPr().append(shd)
    for row in rows:
        cells = t.add_row().cells
        for i, val in enumerate(row):
            cells[i].text = ""
            p = cells[i].paragraphs[0]
            r = p.add_run(str(val))
            r.font.size = Pt(font_size)
            p.paragraph_format.space_after = Pt(2)
    if widths:
        for row in t.rows:
            for i, w in enumerate(widths):
                row.cells[i].width = Cm(w)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    return t


def rule():
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(6)
    pPr = p._p.get_or_add_pPr()
    bdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "6")
    bottom.set(qn("w:color"), "C3C9D2")
    bdr.append(bottom)
    pPr.append(bdr)
    return p


def add_page_numbers():
    footer = doc.sections[0].footer
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), "PAGE")
    run._r.addnext(fld)


add_page_numbers()

# ================================================================== TITLE
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_after = Pt(2)
r = p.add_run("Product Design Specification and Business Model")
r.bold = True
r.font.size = Pt(20)
r.font.color.rgb = ACCENT

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_after = Pt(14)
r = p.add_run("HerdLens: a fused RFID and machine-vision identification gateway for dairy cattle")
r.font.size = Pt(12.5)
r.italic = True

table(
    ["Field", "Entry"],
    [
        ["Student name", "« to be completed »"],
        ["Student number", "« to be completed »"],
        ["Course name", "« to be completed »"],
        ["Assignment", "Product development and marketing assignment (PRD + Business Model)"],
        ["Target market", "Holstein-Friesian dairy farms, North of England"],
        ["Word count (excluding references)", "« to be confirmed »"],
    ],
    widths=[4.6, 11.0],
    font_size=9.5,
)

para("Declaration of Originality", style="Heading 2")
para("The School's Declaration of Originality Form is submitted with this assignment. The declarations "
     "on AI use, referencing and the absence of external agency support are confirmed on that form and are "
     "not repeated here. Readers should complete the signed form in the accompanying submission pack.",
     italic=True)

para("Declaration of Contribution", style="Heading 2")
para("« Team to insert the agreed statement of contribution, including any unequal sharing of the task, "
     "before submission. »", italic=True)

rule()

# ============================================================ 1. CONSTRAINTS
doc.add_heading("1. Constraints arising from EID and the regulations associated with the Livestock Information Service", level=1)
para("Six constraints govern the design space. Each is stated as a regulatory or technical fact and then "
     "translated into a design implication for the proposed system.")

rich([("Constraint 1 \u2014 the technology is locked to low frequency (LF). ", True, False),
      ("Defra has confirmed that Bovine Electronic Identification (BEID) will be introduced for all newborn "
       "calves in England using LF technology, with the replacement cattle service expected during 2027 "
       "rather than the summer-2026 date originally announced [1], [2]. LF operates at 134.2 kHz under "
       "ISO 11784 and ISO 11785, offers a handheld read range of only about 12\u201315 cm and a fixed panel "
       "range of roughly 0.5 m, and reads one transponder at a time with no anti-collision capability [3], [4]. ", False, False),
      ("Implication: ", True, False),
      ("the gateway can never rely on bulk or group reads. Every reading architecture must be single-file and "
       "effectively sequential, so the design has to add a second, non-RF modality to cover the moments when "
       "the single tag in the field does not respond.", False, False)])

rich([("Constraint 2 \u2014 dual tagging, hard deadlines and a 28-day repair clock. ", True, False),
      ("A dairy calf must wear a yellow distance-readable primary tag before it is 36 hours old and a secondary "
       "tag before it is 21 days old; the birth must be registered and a passport obtained by day 27; movements "
       "must reach BCMS, and later the LIS, within three days and deaths within seven; a six-day standstill "
       "applies after an arrival; and a lost or unreadable tag must be replaced within 28 days of the keeper "
       "becoming aware of the loss [5], [6], [7]. ", False, False),
      ("Implication: ", True, False),
      ("the system must detect a failing tag ", False, False),
      ("before ", False, True),
      ("the keeper notices it and must issue the replacement instruction. A passive read log is not enough; the "
       "product has to generate a proactive tag-health alert with measurable margin inside the 28-day window.",
       False, False)])

rich([("Constraint 3 \u2014 the standing herd will not be retagged. ", True, False),
      ("Cattle keepers are not required to retag the existing national herd, and during transition movements may "
       "legally be reported from a BEID read, a barcode scan of the passport or a visual read of the ear tag [1], "
       "[8]. ", False, False),
      ("Implication: ", True, False),
      ("any solution must operate alongside legacy, non-EID and UK-prefixed animals for at least a decade, and "
       "must be able to emit a visually legible identity so that the legal fallback of a visual report is "
       "preserved. The system must therefore store the printed tag number, not only the ISO electronic code.",
       False, False)])

rich([("Constraint 4 \u2014 numbering and country-code change. ", True, False),
      ("Introducing EID requires an entirely new cattle numbering format, and the country-code prefix used for "
       "cattle in Great Britain will change from ", False, False),
      ("UK ", False, True),
      ("to ", False, True),
      ("GB ", False, True),
      ("[8]. ", False, False),
      ("Implication: ", True, False),
      ("the data model must key on the ISO 11784 fifteen-digit code and simultaneously hold a migration map to "
       "the legacy UK visual identifier. A product that hard-codes today's format will fail at cutover, which "
       "is precisely when the 2027 calf crop enters the system.", False, False)])

rich([("Constraint 5 \u2014 regulatory divergence inside the United Kingdom. ", True, False),
      ("Scotland has committed to ultra-high frequency (UHF) EID while England and Wales have chosen LF, and "
       "current LF on-farm equipment \u2014 stick, handheld and panel readers \u2014 cannot read UHF tags at all "
       "[4], [8], [9]. ", False, False),
      ("Implication: ", True, False),
      ("in the North of England, where store and dairy cattle routinely move across the border with Dumfries "
       "and Galloway and the Scottish Borders, a share of the animals arriving at any gate will carry tags that "
       "the installed LF reader physically cannot interrogate. The design must offer a credible route to "
       "identifying those animals, or it will fail exactly where northern farms are most exposed.", False, False)])

rich([("Constraint 6 \u2014 physical and electrical installation constraints. ", True, False),
      ("LF panel readers must be mounted on non-metallic structures and their read performance is degraded by "
       "adjacent metalwork; official LF tags have also been found to clash with the LF activity collars already "
       "worn on many dairy units, causing one or both devices to fail [3], [4], [10]. ", False, False),
      ("Implication: ", True, False),
      ("the product must be specified as a retrofit kit sold with a compulsory site survey, non-metallic race "
       "inserts and a compatibility check against any existing LF collar or parlour identification system. That "
       "survey is a real cost and the business model has to carry it.", False, False)])

# ======================================================= 2. CONSEQUENCES
doc.add_heading("2. Consequences of misidentification of dairy cows in farm environments", level=1)
para("Misidentification is used here in its full sense: a tag that is lost, a tag that will not read, a read "
     "attributed to the wrong animal, and a duplicate read at a gate. Six cause-and-effect chains follow. Each "
     "starts with an identification failure and ends in a measurable loss.")

rich([("2.1  A lost tag removes the animal from the legal system. ", True, False),
      ("If identity cannot be demonstrated the animal receives a CPP30 notice prohibiting movement; if it can "
       "never be proven, a CPP31 compulsory slaughter and removal notice follows, with no compensation and "
       "possible charges from BCMS [11]. A cull cow is worth in the order of \u00a31,000\u2013\u00a31,500 and bTB "
       "compensation in England has been running at \u00a32,031\u2013\u00a32,186 per animal during 2025 [12]. The "
       "farmer also loses the milk and the feed-to-output margin for the whole delay.", False, False)])

rich([("2.2  A wrong identity at milk recording corrupts the breeding programme. ", True, False),
      ("The wrong dam or sire is attributed and the pedigree becomes wrong. Pedigree error in the UK dairy "
       "population has been estimated at roughly 10% [13], and a 10% paternity error reduces genetic gain by "
       "about 4.3% [14]. Because genetic gain compounds, that loss is permanent: it is paid again in every "
       "subsequent generation. At the level of the individual animal, cows wrongly retained or culled on bad "
       "parentage have been costed at AU$84\u2013253 each in lost lifetime profit [15].", False, False)])

rich([("2.3  A treatment recorded against the wrong cow puts antibiotic residue in the bulk tank. ", True, False),
      ("The withdrawal period is then applied to the wrong animal. A rejected tanker costs around \u00a315,000; "
       "an individual residue failure event costs \u00a31,250\u2013\u00a33,500 per farm; and the UK failure rate is "
       "about 0.15% against 0.011% in the United States [16], [17]. The milk buyer relationship and the farm's "
       "assurance status are placed at risk at the same time.", False, False)])

rich([("2.4  A broken trace chain multiplies a bovine TB incident. ", True, False),
      ("Defra's 2026 TB strategy concludes that roughly sixteen of every seventeen herd infections arise from "
       "cattle-to-cattle transmission through undetected disease and cattle movements, and it therefore places "
       "identification and movement recording at the centre of control [18]. A missing or wrong identity breaks "
       "the chain, so more herds are restricted and more reactors are taken: 20,494 cattle were slaughtered in "
       "England in 2025 and the programme costs the taxpayer more than \u00a3100 million a year [19]. Compensation "
       "is also reduced where testing is overdue, so a data failure becomes a financial penalty [18].", False, False)])

rich([("2.5  A duplicate read creates inventory drift and regulatory exposure. ", True, False),
      ("A double read at the gate attributes two identities to a single passage, so one animal is never recorded "
       "at all. The Rural Payments Agency inspects at least 3% of holdings each year, selects 80% of those "
       "inspections by risk, and applies escalating sanctions: movement restriction below a 20% discrepancy, "
       "whole-herd restriction above it, and possible reduction of subsidy [11], [20]. A farm can therefore be "
       "restricted because of a duplicate read that nobody knew had happened.", False, False)])

rich([("2.6  A wrong drafting decision costs production, not just data. ", True, False),
      ("If two cows are interchanged at the drafting gate, the cow intended for service is not served and the "
       "other is served at the wrong point in her cycle. Each missed oestrus is worth \u00a3250\u2013\u00a3350 and "
       "the calving interval extends, with knock-on effects on the whole lactation calendar [21]. Where the "
       "error occurs at selection for culling rather than service, a genetically valuable animal leaves the "
       "herd and the loss is realised over several years.", False, False)])

# ==================================================== 3. FORMULATING THE IDEA
doc.add_heading("3. Formulating the idea: the Value Proposition Canvas", level=1)
para("The customer segment is the owner-operated Holstein-Friesian dairy farm in the North of England running "
     "between 150 and 350 cows with two to four staff. This band is chosen deliberately. Below 150 cows the "
     "capital cost is hard to justify; above 350 cows the farm is likely to run a robotic milking system whose "
     "manufacturer already supplies individual identification. The 150\u2013350 cow farm is large enough to need "
     "individual identity daily, small enough to be price-sensitive, and it already runs cows single file "
     "through a parlour exit and a drafting race, which is the physical precondition for the proposed gateway.")
para("The canvas in Figure 1 maps that segment against the HerdLens value map. The right-hand side of the "
     "canvas is deliberately built only out of the pains and gains that the six constraints and the six "
     "consequence chains have already established, so that every claim of fit can be traced back to evidence "
     "rather than to assertion.")

figure("fig1_vpc.png",
       "Figure 1. Value Proposition Canvas for the HerdLens gateway (customer profile left, value map right). "
       "A legible A3 or Mural version of this canvas should be submitted alongside the report.")

para("The three blocks on the customer side resolve into a single dominant pain: the system of record is only "
     "as good as the tag on the ear, and the tag on the ear fails. The three blocks on the value side answer "
     "that pain with a measuring principle rather than a product feature. Physical identity is captured twice, "
     "once by radio and once by biometric appearance, and the two observations are reconciled per passage. "
     "The proposal is therefore not a better reader and not a better tag; it is an identity layer that assumes "
     "the tag will eventually fail.")
para("A note on the enrolment assumption, because it drives feasibility. No farmer will photograph 215 cows. "
     "The gallery is therefore built automatically: every passage in which exactly one animal is in frame and "
     "exactly one EID read is returned produces a labelled training image at a confidence of 0.99. Twelve such "
     "images per cow across at least three days is sufficient to seed a working coat-pattern classifier, which "
     "places enrolment inside the first two weeks of operation with no additional labour.")

# ================================================ 4. GROUP MEMBERSHIP
doc.add_heading("4. Identifying group membership and differentiation factors", level=1)
para("Three strategic groups compete for the same job of work \u2014 knowing which individual animal is in front "
     "of you and being able to prove it. Table 1 places the principal competitors in their groups and records "
     "the price point and the principal weakness that matters to a northern dairy farm.")

table(
    ["Competitor (group)", "Identification method", "Indicative cost", "Principal weakness"],
    [
        ["Shearwell SDL150 / Tru-Test XRP2 (passive EID readers)",
         "LF EID panel antenna pair fitted to a race",
         "\u00a31,500 per pair and \u00a31,807.75 respectively, excluding VAT [22], [23]",
         "Reads only. When the tag fails or two cows pass together there is no fallback and no identity is produced."],
        ["Allflex SenseHub (wearable)",
         "LF collar plus on-farm base station",
         "About \u00a3102 per cow installed; a 400-cow unit cost \u00a340,868 [24]",
         "Per-animal hardware. Collars are lost or damaged, batteries age, and the base station is a fixed extra cost."],
        ["Afimilk AfiAct II (wearable)",
         "Leg tag, 868 MHz long range plus 80 kHz short range",
         "\u00a380.82 per tag excluding VAT [25]",
         "Per-animal cost, and the device is still a tag that can be lost."],
        ["Smartbow, Zoetis (wearable)",
         "Ear-tag sensor",
         "\u00a369 to \u00a3150 per cow plus about \u00a32,500 per farm [26]",
         "Per-animal cost; the sensing function does not of itself provide statutory identity."],
        ["CattleEye, GEA (vision)",
         "Coat-pattern re-identification from a single parlour-exit camera",
         "\u00a3650 hardware plus \u00a31 per cow per month, about \u00a32,580 per year for 215 cows [27], [28]",
         "Still requires EID as the primary identity, needs 4 m of headroom and 4 m of clear walk, and depends on cloud analytics."],
        ["Ever.Ag / Cainthus ALUS (vision)",
         "8 to 10 cameras per building with an edge node",
         "Not published",
         "Capital heavy and built for feeding and behaviour analytics rather than statutory identification."],
        ["Manual visual reading (substitute)",
         "Human reads the printed tag",
         "No capital cost",
         "Roughly three times slower and more error-prone than electronic reading [29], and impossible in poor light."],
    ],
    widths=[4.0, 3.6, 4.0, 4.4],
)

caption("Table 1. Strategic groups competing for individual cattle identification in England.")

para("Points of parity. To be considered at all in this group a product must read ISO 11784/11785 LF EID, work "
     "in a single-file race, export data to herd management software, survive barn conditions, be installable "
     "and supportable in the UK, and be eligible for grant support. HerdLens matches every one of these. None "
     "of them is a source of competitive advantage.")

para("Points of difference. Seven differences are claimed, and each is traceable to a constraint or a "
     "consequence identified earlier.")
bullet("Identity survives tag failure. Constraint 1 means a single LF antenna cannot guarantee a read, and "
       "Figure 1 records a cumulative tag loss of up to 19.8% over five years [3]. No competitor in Table 1 "
       "returns a named animal when the tag is silent; HerdLens returns a probabilistic identity and flags "
       "that the tag needs attention.",
       bold_lead="Failure-tolerant identity. ")
bullet("There is no collar, no ear sensor, no battery and no per-head hardware. This removes the dominant "
       "cost line of the wearable group and the entire class of failure in which the device itself is lost.",
       bold_lead="No per-animal device. ")
bullet("Case C in Figure 3 resolves the double read that the current generation of readers simply logs as an "
       "error, which addresses consequence chain 2.5 directly.",
       bold_lead="Double-read resolution. ")
bullet("A rolling read rate per cow produces a re-tag instruction by day 21 of the 28-day statutory window, "
       "converting a compliance trap into a routine maintenance task (Constraint 2).",
       bold_lead="Proactive tag health. ")
bullet("All inference runs on the edge unit, so a farm with no usable broadband still gets full "
       "functionality. This addresses the rural connectivity limitation that constrains cloud-based vision "
       "systems.",
       bold_lead="No broadband dependency. ")
bullet("Because identity is not derived from the transponder, an animal carrying a Scottish UHF tag is still "
       "identified on an English LF installation (Constraint 5).",
       bold_lead="Cross-border tolerance. ")
bullet("About \u00a33.50 per cow per year against roughly \u00a312 per cow per year for the closest vision "
       "competitor, and against a per-cow capital cost of \u00a369\u2013150 for the wearable group.",
       bold_lead="Price per cow. ")

# ================================================== 5. COMPETITION ANALYSIS
doc.add_heading("5. More on competition analysis", level=1)
para("Two analytical tools are applied, Porter's Five Forces and a SWOT analysis, and a short PESTEL scan is "
     "used to test the macro assumptions. The purpose is to derive the desirable attributes the product must "
     "possess and to establish the differentiation factor that the analysis actually supports.")

doc.add_heading("5.1  Porter's Five Forces", level=2)
rich([("Threat of new entrants: moderate to high. ", True, False),
      ("The hardware is commodity. An IP camera, a Jetson-class compute module and an LF antenna pair can be "
       "assembled by any competent integrator, and the vision model is increasingly open. What raises the "
       "barrier is not capital but validation: an installed base on working farms, a labelled dataset of real "
       "herds, and the trust of a buyer group that makes decisions on the recommendation of a neighbouring "
       "farmer. Entry is cheap; credible entry is not.", False, False)])
rich([("Bargaining power of suppliers: moderate. ", True, False),
      ("The LF antenna and reader market is concentrated in a small number of firms, and the edge compute "
       "market is effectively dual-sourced between NVIDIA and Hailo. The mitigation is deliberate "
       "commoditisation of the bill of materials, dual sourcing of the antenna, and no custom silicon "
       "anywhere in the design.", False, False)])
rich([("Bargaining power of buyers: moderate, but weak on price. ", True, False),
      ("There are 6,850 dairy producers in Great Britain and the market is highly fragmented, which normally "
       "weakens buyer power [30]. However the buyer is price-sensitive, and the mandate requires a tag rather "
       "than a reader, so the credible alternative is to buy nothing at all and keep using a \u00a3500 handheld "
       "reader. This is the real competitive threat and it is why the price point and grant eligibility in "
       "Section 12 matter more than any technical differentiation.", False, False)])
rich([("Threat of substitutes: high. ", True, False),
      ("Visual reading remains legal throughout the transition [1], a handheld stick reader costs \u00a3475\u2013"
       "\u00a31,350 [22], [23], and for the monitoring element the wearable group substitutes for the "
       "identification element at a similar price. Substitution is not a distant risk; it is the current "
       "default behaviour of the segment.", False, False)])
rich([("Competitive rivalry: moderate but rising fast. ", True, False),
      ("GEA acquired CattleEye in March 2024, which means a major milking-equipment manufacturer now owns a "
       "vision identification business and can bundle that capability into a parlour or robot sale [27]. "
       "Incumbent hardware firms can equally bundle a camera at near-zero incremental margin to defend their "
       "reader business. The realistic strategic position for a new entrant is therefore to be the specialist "
       "identity layer that integrates with everyone, rather than the equipment brand that competes with them.",
       False, False)])

doc.add_heading("5.2  SWOT analysis", level=2)
table(
    ["Strengths", "Weaknesses"],
    [
        ["The only system in the group that produces identity when the tag has failed. "
         "No per-animal device, so no collar loss, no battery and no per-head hardware cost. "
         "Double-read resolution as a native function. "
         "Edge inference removes the broadband dependency that limits cloud vision. "
         "A regulatory tailwind that forces every dairy farm to buy identification capability by 2027 [1]. "
         "Grant-eligible capital cost.",
         "No brand, no installed base and no reference farms at launch. "
         "Performance depends on an enrolment period of up to 14 days before full accuracy is reached. "
         "Coat-pattern recognition is weakest exactly where conditions are worst: soiled flanks, low light, "
         "and multi-colour or same-colour animals. "
         "The installation still requires a single-file race.",
         ],
    ],
    widths=[8.0, 8.0],
)
table(
    ["Opportunities", "Threats"],
    [
        ["Only 5\u201310% of British cattle farms currently use EID as a management tool, so the addressable "
         "population is almost entirely unserved [31]. "
         "The 2027 LF mandate creates a single, dated purchase trigger across the whole segment. "
         "Scotland's UHF decision creates a cross-border case that only a non-RF method can serve. "
         "The same camera can host a later mobility and lameness module, raising revenue per farm. "
         "Similar market structure in Ireland and New Zealand.",
         "An incumbent bundling vision free with hardware to defend reader margin, in the way GEA already can "
         "after the CattleEye acquisition [27]. "
         "Scottish UHF adoption fragmenting the transponder base and complicating a single product SKU. "
         "Milk price volatility: the Defra farm-gate price fell to 35.00 ppl in July 2026, about 20% down "
         "year on year, which suppresses capital investment [32]. "
         "Grant scheme rules changing between application years. "
         "Farmer scepticism about AI and about data leaving the farm.",
         ],
    ],
    widths=[8.0, 8.0],
)
caption("Table 2. SWOT analysis of the HerdLens proposition.")

doc.add_heading("5.3  PESTEL scan", level=2)
bullet("the 2026 bovine TB strategy explicitly ties identification and movement recording to disease "
       "control, and the Livestock Information Transformation Programme is now delivered in-house by Defra "
       "[1], [18]. Both increase the political salience of traceability.", bold_lead="Political. ")
bullet("English dairy farm business income averaged \u00a3153,800 in 2024/25 and is forecast at about "
       "\u00a3224,000 for 2025/26, but the farm-gate milk price fell to 35.00 ppl by July 2026 [32], [33]. "
       "Capital appetite is therefore cyclical and the proposition must lean on grant support.",
       bold_lead="Economic. ")
bullet("Skilled dairy labour costs \u00a318.76\u2013\u00a319.99 per hour including on-costs and has risen "
       "44\u201351% in five years, which makes labour-saving technology unusually attractive [34].",
       bold_lead="Social. ")
bullet("Edge AI module costs have collapsed while accuracy has risen; a published multi-camera study on a "
       "working UK farm reports above 96% single-image identification accuracy for Holstein-Friesian animals "
       "[35]. At the same time the LF and UHF split inside the UK is a technological risk as much as an "
       "opportunity.", bold_lead="Technological. ")
bullet("The Dairy Roadmap requires net-zero carbon by 2050, a 3% annual reduction in emissions intensity from "
       "a 2023 baseline, 100% renewable electricity by 2030 and low-emission slurry spreading by 2027 [36]. "
       "Identification data feeds directly into the carbon and health metrics farms must report.",
       bold_lead="Environmental. ")
bullet("The Cattle Identification Regulations 2007 continue to apply in England as assimilated law, and the "
       "enforcement ladder runs from a movement prohibition to compulsory slaughter without compensation [11], "
       "[37]. Compliance is therefore not optional and the evidence trail has value in its own right.",
       bold_lead="Legal. ")

doc.add_heading("5.4  Desirable attributes and the differentiation factor", level=2)
para("Four desirable attributes follow directly from the analysis. They are the criteria against which the "
     "technical description in Section 10 must be judged.")
num("the system must produce a usable identity in the cases where the transponder does not "
    "respond. This is the least well-covered need in the selected comparison set, but it remains a hypothesis to validate rather than a proven market monopoly.",
    bold_lead="Robustness of identification, defined as tolerance of tag failure. ")
num("it must retrofit to the race and the parlour exit the farm already owns, because the "
    "buildings are existing and the alternative is a capital project in its own right.",
    bold_lead="Retrofittability. ")
num("it must sit beneath the level at which a price-sensitive, fragmented buyer "
    "simply does nothing, and it must be grant-eligible.", bold_lead="Affordability per cow. ")
num("it must produce evidence automatically, because the RPA inspection and the "
    "milk-buyer audit are the moments at which identification failures become expensive.",
    bold_lead="Compliance evidence. ")
para("The differentiation factor that emerges is therefore not accuracy, and not price alone. It is the "
     "combination of failure tolerance with a zero per-animal hardware footprint. The selected alternatives in Table 1 are tag-dependent, per-animal, or primarily designed for another monitoring task. The proposed difference is the combination, which still requires field validation.")

# ================================================================ 6. USP
doc.add_heading("6. Product and service analysis: the unique selling point", level=1)
p = doc.add_paragraph()
p.paragraph_format.left_indent = Cm(0.8)
p.paragraph_format.right_indent = Cm(0.8)
p.paragraph_format.space_before = Pt(6)
p.paragraph_format.space_after = Pt(10)
r = p.add_run("HerdLens uses the legally required LF-EID as the primary identity, verifies passage with an entry/exit state machine, and uses Holstein-Friesian coat-pattern vision as a second evidence stream when a tag is not read or a passage contains conflicting reads. It is designed to reduce unverified or duplicated counts without putting a powered device on every animal.")
r.bold = True
r.font.size = Pt(11.5)
rich([("What must be communicated to the customer base. ", True, False),
      ("The buying trigger is the 2027 LF mandate, but the message must not be a compliance message, because "
       "compliance can be satisfied with a \u00a3500 handheld reader. The message is that the mandate is the "
       "moment to add a verification layer around the tag, and that a lost tag can create a much larger movement, labour or evidence problem than the equipment cost. The three proof points to lead with are the 19.8% cumulative tag loss "
       "figure [3], the demonstration that manual identification is roughly three times slower than "
       "electronic reading [29], and the payback calculation in Section 12.", False, False)])

# ==================================================== 7. BUSINESS CANVAS
doc.add_heading("7. Business model canvas", level=1)
para("The full canvas is presented in Figure 4. Three blocks deserve commentary because they carry the "
     "commercial logic of the proposition.")
para("The cost structure is dominated by a single line: the LF antenna pair at \u00a31,500 is more than half of "
     "the \u00a31,750 bill of materials [22]. Everything else \u2014 two cameras, an edge compute module, an "
     "IP66 enclosure and mounting hardware \u2014 is where the volume engineering has to happen. The design "
     "target is to reduce the bill of materials to about \u00a3900, which requires either a volume antenna "
     "supply agreement or the substitution of a lower-cost LF panel module.")
para("The revenue model is deliberately a low capital cost with a modest recurring subscription rather than a "
     "per-animal licence. A per-animal subscription would recreate the exact cost structure that makes the "
     "wearable group unattractive to this segment, and it would also undermine the central claim of the "
     "proposition: that cost does not scale with the size of the herd because nothing is fitted to the animals.")
para("The customer relationship is high-touch at onboarding and self-serve thereafter. That is a direct "
     "consequence of the enrolment mechanism: the first two weeks determine whether the coat-pattern model "
     "works on that farm's animals, and the sector makes decisions on the evidence of a trusted local source "
     "rather than on a specification sheet. Reference farms and demonstration days are therefore a marketing "
     "channel, not a courtesy.")

figure("fig4_bmc.png",
       "Figure 4. Business Model Canvas for HerdLens. A legible A3 or Mural version should be submitted with "
       "the report.", width_cm=16.4)

# ================================================== 8. CRITICAL ANALYSIS
doc.add_heading("8. Critical analysis", level=1)

doc.add_heading("8.1  Market size and share", level=2)
para("The total addressable market is defined by the population of commercial dairy holdings in England and "
     "the number of adult dairy cows they carry. In June 2025 England had 4,841 commercial holdings classified "
     "as dairy, carrying 1,040,170 adult dairy cows; Great Britain as a whole had 6,850 dairy producers, a "
     "figure that has fallen 21.5% in six and a half years while the average herd has grown to about 215 cows "
     "[30], [38], [39]. The trend is unambiguous: fewer, larger herds, which favours a fixed-cost gateway.",
     )
para("Table 3 builds the market down from the national figure to the served market.")
table(
    ["Layer", "Definition", "Holdings", "Adult dairy cows", "Basis"],
    [
        ["TAM", "All English commercial dairy holdings", "4,841", "1,040,170", "Defra June 2025 [38]"],
        ["SAM", "North East, North West and Merseyside, Yorkshire and the Humber",
         "1,689", "356,011", "Defra June 2025 regional dataset; 34.2% of the English herd [38]"],
        ["Served market", "SAM filtered to herds of 150\u2013350 cows, the band where a fixed gateway is "
         "economic and the farm is not already on a robot",
         "about 950", "about 196,000", "Author's estimate assuming 56% of SAM holdings fall in the band"],
        ["SOM (year 3)", "5% of the served market", "about 48", "about 9,800",
         "Author's target based on a single-region launch and an engineer-led installation rate of two "
         "sites per week"],
    ],
    widths=[2.3, 5.0, 1.9, 2.4, 4.4],
    font_size=8.0,
)
caption("Table 3. Market sizing from national statistics down to the served market.")

para("On that basis a year-three position of approximately 48 farms and 9,800 cows would generate roughly "
     "\u00a3177,700 of first-year revenue from hardware and installation, and about \u00a334,300 of annual "
     "recurring subscription. The business is therefore viable as a regional specialist but it is not, at this "
     "price point, a business that scales on headcount. It scales by reducing the bill of materials and by "
     "adding modules to an installed base, which is why the mobility and lameness add-on in the canvas matters "
     "more than a fourth salesperson.")

doc.add_heading("8.2  Alignment between desirable attributes, customer needs and the product idea", level=2)
para("The four desirable attributes derived in Section 5.4 map cleanly onto the pains in Figure 1. Tolerance "
     "of tag failure answers the dominant pain. Retrofittability answers the constraint that the buildings "
     "already exist. Affordability per cow answers the segment's price sensitivity and the fact that doing "
     "nothing is a legal option. Compliance evidence answers the inspection and audit moments that turn an "
     "identification failure into a financial event. On that test the product idea and the customer segment "
     "are aligned.")
para("The alignment is not complete, and two adjustments are required.")
rich([("Adjustment 1 \u2014 introduce a read-only tier. ", True, False),
      ("The analysis of buyer power showed that the credible alternative to buying anything is to keep using a "
       "handheld reader. A single \u00a32,950 proposition therefore risks a no-decision. A lower tier at about "
       "\u00a31,450 that provides the LF panel pair, passage counting and tag-health scoring without "
       "coat-pattern identification would capture the price-sensitive end of the band, and the vision module "
       "can then be sold as an upgrade once the farm has experienced the compliance value. This converts a "
       "single high-consideration purchase into a ladder.", False, False)])
rich([("Adjustment 2 \u2014 reopen the coat-pattern assumption. ", True, False),
      ("The proposition leans on coat-pattern biometrics, and the strongest published evidence is a "
       "multi-camera study on a working UK farm reporting above 96% single-image accuracy for "
       "Holstein-Friesian animals [35]. However, a separate study following Holstein animals across growth "
       "stages reported a re-identification F1 of only 73% after one year, and 83% for animals outside the "
       "training set [40]. A separate 2025 commercial-farm evaluation reported identification recall of 69.1%–78.1% and precision of 83.2%–91.3% under crowding and variable lighting [46]. These results are consistent: coat pattern is useful, but short-term benchmark accuracy should not be presented as production recall. The design must therefore treat the "
       "vision gallery as something that is refreshed continuously rather than enrolled once, and the "
       "confidence threshold, not the headline accuracy, is the safety mechanism. This is reflected in Case B "
       "of Figure 3, where vision-only identifications require a 0.90 score before they are committed.",
       False, False)])
para("One further assumption is disclosed because it is the weakest part of the analysis. The present study "
     "has no access to field performance data for a fused system, because no such system is commercially "
     "available in the UK. The accuracy targets in Section 10.6 are therefore engineering targets derived from "
     "the performance of the two component modalities measured separately, not measured outcomes for the "
     "combined system. The pilot in Section 10.7 exists specifically to close that gap.")

# ================================================ 9. USER REQUIREMENTS
doc.add_heading("9. User requirements and justification", level=1)
para("The requirements below state what the product must do, not how it will do it. All ten are classified as "
     "Must have under MoSCoW. This is a deliberate consequence of the constraint analysis rather than a "
     "default: each requirement traces back to a specific regulation or consequence chain, so none of them "
     "can be deferred to a later release without creating either a legal exposure or a failure of the core "
     "value proposition. The traceability column shows the origin of each requirement.")

req_rows = [
    ["UR1", "The farmer shall be able to identify each animal associated with a passage through the gateway and distinguish a completed passage from an unresolved passage.",
     "Core problem statement: RFID can miss a tag or return more than one ID when cows bunch. The requirement states the user outcome; the LF reader, cameras and passage state machine are implementation choices. The 99% LF read rate is a later engineering target, not the user requirement.", "Must"],
    ["UR2", "The farmer shall receive a named candidate identity, with supporting evidence and an explicit uncertainty state, when the statutory tag is not read.",
     "Consequence 2.1 and the 19.8% five-year cumulative tag loss [3]. A candidate identity can support a safe review and retagging workflow, but the system must not silently present a probabilistic result as official identity.", "Must"],
    ["UR3", "The farmer shall be alerted when one passage could represent multiple animals or conflicting identities, and shall be able to review the case before it is exported as a movement record.",
     "Consequence 2.5: duplicate or missed passages create inventory drift and regulatory exposure [11], [20]. Reviewability is the safety requirement; the fusion algorithm is the design response.", "Must"],
    ["UR4", "The farmer shall receive a re-tagging alert early enough to order and fit a replacement within the statutory 28-day window.",
     "Constraint 2 and the official replacement rule [7]. The specific day-21 threshold is an engineering acceptance target chosen to leave a practical seven-day margin, not a new legal rule.", "Must"],
    ["UR5", "The system shall provide a tamper-evident, exportable passage record containing identity status, time, direction, evidence references and reviewer decisions.",
     "Consequences 2.1, 2.3 and 2.4 show why a traceable identity record matters for movement, medicine and disease-control decisions [1], [11], [18]. The retention period and storage architecture are specified later.", "Must"],
    ["UR6", "The service shall continue recording passages and alerts during at least seven days without an internet connection, and shall reconcile records after connectivity returns.",
     "Rural connectivity is a reliability constraint. The user need is continuity of operation; local storage and store-and-forward are the technical solution.", "Must"],
    ["UR7", "The product shall be installable on an existing single-file race with a documented site-survey result and without requiring a new building or a structural rebuild.",
     "The target customer already owns the race. Retrofittability limits capital cost and makes the product usable on North of England farms with different roof heights; exact camera geometry is a site-specific design parameter.", "Must"],
    ["UR8", "The farmer shall be able to transfer accepted records and unresolved cases to herd-management and movement-reporting workflows without retyping the animal identity.",
     "Constraint 3 and 4: the system must preserve both the current electronic identifier and the legacy visual identifier during transition. File/API formats are defined in Section 10.5.", "Must"],
    ["UR9", "A herdsperson shall be able to start a new installation using routine animal passages, without photographing or restraining every animal for a separate enrolment session.",
     "A manual enrolment day would add labour at the point of sale and would weaken the value proposition. The two-week gallery build is therefore a usability requirement, while its 14-day and 300-cow limits are validation targets.", "Must"],
    ["UR10", "The farmer shall control whether raw imagery leaves the holding and shall be able to operate the core service without sending raw video to a cloud service.",
     "Data governance is part of the customer value proposition. The default local-image policy reduces trust and privacy barriers; embeddings and diagnostic metadata may be shared only under an explicit contract [41].", "Must"],
]
table(["Ref", "Requirement", "Justification and traceability", "MoSCoW"], req_rows,
      widths=[1.3, 4.6, 8.3, 1.8], font_size=8.2)
caption("Table 4. User requirements, justification and MoSCoW classification.")

# ================================================ 10. TECHNICAL DESCRIPTION
doc.add_heading("10. Technical description", level=1)

doc.add_heading("10.1  Physical structure and sensor placement", level=2)
para("The gateway is installed over a section of single-file race, typically 2.4 m long and 0.9 m wide, at the "
     "exit from the collecting yard or immediately after the parlour. The farm already owns this asset, which "
     "is why retrofittability is worth more than a marginal accuracy gain.")
para("Two cameras are fitted rather than one. Camera A is mounted vertically above the race at approximately "
     "4 m and looks directly down, which is the viewpoint that produces the cleanest view of the coat pattern "
     "over the topline and flank. Camera B is mounted to the side at about 2.5 m and at a three-quarter angle; "
     "its function is to capture the head and, critically, whether an ear tag is physically present on either "
     "ear. The side camera is the design answer to Constraint 6 and to the low-roof buildings common in the "
     "North of England. Where the roof will not permit the 4 m top-down view, Camera B is promoted to primary "
     "and the system runs in a reduced-accuracy configuration which is declared to the purchaser rather than "
     "silently degraded.")
para("The LF antenna pair is mounted on both side walls of the race, facing inwards across the 0.5 m read "
     "field. Because LF performance degrades against metalwork [3], the installation kit includes non-metallic "
     "race inserts and a survey step that records the position of any existing LF activity collars and checks "
     "them for compatibility, as required by Constraint 6. A PIR sensor and a lux sensor complete the sensing "
     "set: the PIR provides the passage trigger that opens a fusion window, and the lux reading is used to "
     "decide whether the infrared illuminator is required.")
figure("fig2_block.png",
       "Figure 2. Functional block diagram of the HerdLens gateway, showing the sensing layer, the on-farm "
       "processing layer, the cloud layer and the external interfaces.", width_cm=16.4)

doc.add_heading("10.2  Circuit, compute and data aggregation", level=2)
para("All equipment in the race is powered over Ethernet from the edge cabinet, which removes the need for "
     "mains power at the gate and eliminates a class of electrical fault in a wet environment. The edge unit "
     "is a fanless, IP66-enclosed single-board computer. Two build options are supported: an NVIDIA Jetson "
     "Orin Nano for maximum inference throughput, or a Hailo-8L accelerator attached to a Raspberry Pi 5 for "
     "the lower-cost tier. Typical consumption is 25 W, or about 219 kWh per year, which is discussed further "
     "in Section 11.")
para("The electrical path is 230 V AC to a protected 48 V DC PoE supply in the edge cabinet, then through a "
     "managed PoE switch to both cameras and the race-side trigger devices. The LF reader has its own isolated "
     "reader interface and is time-synchronised with the edge computer; the edge computer writes first to the "
     "industrial SSD and only then acknowledges a passage to the local API. A short UPS hold-up protects the "
     "database during a power flicker. If a camera, reader, storage device or clock loses health, the gateway "
     "records the fault, marks the affected passage interval as incomplete and raises a maintenance alert; it "
     "does not fabricate a complete identity record.")
table(
    ["Subsystem", "Component", "Key specification", "Function"],
    [
        ["Radio", "LF panel antenna pair", "134.2 kHz, ISO 11784/11785, HDX and FDX-B, approx. 0.5 m field",
         "Reads the statutory EID of the animal in the race"],
        ["Vision A", "Top-down IP camera", "4 MP, IP66/IK10, 850 nm IR, 4 m mounting height",
         "Coat-pattern imaging for biometric identity"],
        ["Vision B", "Side IP camera", "4 MP, IP66, three-quarter view at 2.5 m",
         "Head and ear view; detects tag presence or absence"],
        ["Compute", "Edge AI unit", "Jetson Orin Nano, or Hailo-8L with Raspberry Pi 5; 25 W typical",
         "Runs detection, tracking, embedding and fusion entirely on farm"],
        ["Storage", "Local store", "128 GB industrial SSD, SQLite plus image ring buffer",
         "Seven-day offline autonomy and the three-year evidence record"],
        ["Trigger", "PIR plus lux sensor", "Passage trigger, ambient illumination",
         "Opens and closes the passage window and controls the illuminator"],
        ["Comms", "PoE switch plus 4G router", "Gigabit PoE, optional cellular backhaul",
         "Store-and-forward sync; no broadband dependency"],
    ],
    widths=[2.2, 3.2, 5.8, 4.8], font_size=8.2)
caption("Table 5. Gateway subsystem specification.")

para("Data aggregation is organised around the passage rather than around the frame or the read. Every time "
     "the PIR fires and the detector count rises from zero to one or more, the system opens a passage window "
     "and collects two independent streams into it: the EID reads, each carrying a signal strength and a "
     "timestamp, and the vision tracklets, each carrying an entry time, an exit time and a coat-pattern "
     "embedding. The window closes when the detector count returns to zero. This structure is what makes the "
     "double read solvable: a double read is no longer an error to be logged but a disagreement between two "
     "streams that can be reconciled by ordering the reads in time and by checking how many animals were "
     "actually visible.")

doc.add_heading("10.3  Algorithms and machine learning", level=2)
para("The vision pipeline runs four stages on the edge unit. Detection uses a YOLOv8-n model fine-tuned on "
     "cattle, producing bounding boxes per frame. Multi-object tracking uses a ByteTrack-style association to "
     "convert those boxes into tracklets. Re-identification extracts a 512-dimension embedding from each "
     "tracklet using an OSNet-style backbone trained with a combination of triplet loss and a margin-based "
     "classification loss, which is the approach that published work on Holstein-Friesian re-identification "
     "has shown to exceed 96% single-image accuracy on a working UK farm [35]. Finally, the embeddings are "
     "matched against a per-farm gallery of enrolled animals.")
para("The gallery is built without farmer input, which is what makes the product practical. During the first "
     "two weeks of operation, every passage in which exactly one animal is in frame and exactly one EID read "
     "is returned is assumed to be a true label at 0.99 confidence, and the resulting images are added to that "
     "animal's gallery. When a cow has accumulated at least twelve labelled images across at least three "
     "separate days, she is promoted to full vision-identification status. This bootstrap mechanism is also "
     "the answer to the ageing problem identified in Section 8.2: because EID-confirmed passages continue to "
     "refresh the gallery for the whole life of the installation, the model tracks the animal as she matures "
     "rather than relying on a single enrolment snapshot [40].")

figure("fig3_fusion.png",
       "Figure 3. Sensor-fusion decision logic showing the five passage cases, the confidence gate and the "
       "tag-health update.", width_cm=15.0)

para("The fusion engine is the core of the intellectual property and is shown in Figure 3. Five cases are "
     "enumerated. In Case A one tracklet and one read agree, and the identity is accepted at 0.99 confidence. "
     "In Case B a tracklet has no corresponding read, which is the tag-failure case: the identity is taken from "
     "the vision gallery, but only above a 0.90 score, and the passage raises a tag-not-read flag. In Case C a "
     "single animal produces two or more reads, which is the double-read problem; the reads are ordered by "
     "signal strength and entry time, each is assigned to the animal that produced it, and any surplus is "
     "quarantined for farmer review rather than silently discarded. In Case D two or more tracklets share a "
     "single read, which happens when cattle bunch; the read is assigned to the tracklet with the peak signal "
     "strength and the remainder are flagged. Case E is the general case and is solved as an assignment "
     "problem, minimising a cost that combines signal strength with temporal overlap between the read and the "
     "tracklet, using the Hungarian algorithm.")
para("Every identification carries a confidence score. A high score can auto-complete a local passage record, but a "
     "vision-only result is labelled as a candidate until the farm's validation gate has been passed; anything "
     "below the review threshold enters the farmer queue. The system is allowed to be uncertain, but it is not "
     "allowed to silently turn a probabilistic result into an official movement report.")

doc.add_heading("10.4  Software and user interface", level=2)
para("The on-farm service runs as a containerised Python application on the edge unit, exposing a local REST "
     "interface so that the installation remains fully functional without any cloud connection. The farmer "
     "interface is a responsive web application served from the edge unit and reachable on the farm network, "
     "with an installable mobile equivalent. Its three primary screens are Today, which shows the animals "
     "handled and any low-confidence passages awaiting review; Tag Health, which lists cows whose 30-day "
     "rolling read rate has fallen below threshold together with the number of days remaining in the 28-day "
     "statutory window; and Records, which produces the movement file and the compliance export.")
para("The cloud layer is deliberately minimal. It distributes model updates, receives embeddings and "
     "diagnostic metadata for fleet-level analytics, and never receives raw imagery. Requirement UR10 makes "
     "this a contractual commitment rather than a privacy preference, because the field evidence is that "
     "unclear data-sharing terms are a material barrier to adoption in this sector [41].")

doc.add_heading("10.5  Interfaces to LIS and to the farmer", level=2)
para("Three interfaces are provided. The first is the REST API into herd management software, which is how "
     "the identity reaches the systems that actually run the farm: breed society recording, medicine books, "
     "milk recording and culling lists. Representative integration targets are Herdwatch, SUM-IT and "
     "Uniform-Agri. The second is the movement file export, which produces a LIS/CTS-ready list of identities "
     "and movements carrying both the ISO 15-digit code and the legacy UK visual identifier, as required by "
     "Constraint 4. The third is a forward-looking interface: because animal movements may be reported legally "
     "from a BEID read, a passport barcode or a visual read during the transition period [1], the system "
     "stores a tagged image of every passage so that the visual fallback remains available at any time. When "
     "the LIS exposes an API, that becomes the primary reporting route rather than the file export.")
para("The farmer interface is treated as a safety-critical surface rather than a dashboard. Its only "
     "non-negotiable job is to tell a herdsperson, today, which cows need a new tag before the deadline. "
     "Everything else is secondary, and the design deliberately resists the trap of presenting more "
     "operational data than a two-person team can act on.")
para("The minimum data contract is deliberately small. A passage record contains: passage_id (UUID); animal_id "
     "with identifier_type (LF_EID, visual_tag, candidate); observed_at and completed_at in UTC; direction; "
     "read_events with reader_id, code, RSSI and timestamp; vision_events with tracklet_id, gallery_id and "
     "similarity score; status (accepted, candidate, unresolved, duplicate); evidence_uri; and reviewer_id plus "
     "reviewed_at when a person resolves the case. The local REST interface exposes GET /v1/passages, "
     "GET /v1/animals/{id}/tag-health, POST /v1/reviews and GET /v1/exports/movements. Export validation rejects "
     "missing identifiers, impossible timestamps, duplicate movement IDs and an unresolved case that has been "
     "selected for official submission. The export is therefore an operational hand-off, not a claim that the "
     "vendor has been granted direct LIS API access.")

doc.add_heading("10.6  Performance targets and price point", level=2)
table(
    ["Metric", "Target", "Basis"],
    [
        ["EID read rate, single-file passage", "at least 99%",
         "Engineering target informed by the 99.4% LF panel result in the Defra/Welsh pilot [29]; re-measure on the target race"],
        ["Accepted identity per completed passage", "at least 99% after the validation gate",
         "Combined-system release target; no fused-system field result is claimed"],
        ["Vision-only precision", "at least 95% at the operating threshold",
         "Release target. The 96% result in a controlled multi-camera dataset [35] is a benchmark, while current commercial evidence reports 83.2%–91.3% precision and 69.1%–78.1% recall [46]"],
        ["Vision-only recall", "report separately; target at least 90% after site calibration",
         "Recall must not be hidden by precision. The target is deliberately above the current commercial range and is a pilot gate, not a measured result"],
        ["Double-read resolution", "100% of surplus reads quarantined and reported",
         "Design requirement, no measured comparator available"],
        ["Tag-health alert lead time", "at least 7 days before the 28-day deadline expires",
         "Statutory deadline less the practical tag-ordering lead time [7]"],
        ["Unit price, hardware and installation", "\u00a32,950 per gateway, \u00a31,450 for the read-only tier",
         "Anchored on the \u00a31,500\u2013\u00a31,808 list price of competing LF panel pairs [22], [23]"],
        ["Subscription", "\u00a33.50 per cow per year",
         "Anchored below the \u00a312 per cow per year of the closest vision competitor [27]"],
    ],
    widths=[4.6, 4.6, 6.8], font_size=8.2)
caption("Table 6. Performance targets and the price point, with the basis for each figure.")

para("The price point is set from the market rather than from a cost-plus calculation, and Table 6 shows the "
     "anchor for each element. It is deliberately consistent with the customer's stated budget expectation "
     "rather than with the theoretical value of perfect identification, because the analysis in Section 5.1 "
     "showed that the binding constraint is not willingness to pay for accuracy but the availability of a "
     "credible do-nothing alternative.")

doc.add_heading("10.7  Validation plan", level=2)
para("Because the combined system has no field precedent, the design includes a staged validation rather than "
     "an assertion of accuracy. Stage one is a bench rig with a labelled passage set, known tag failures, "
     "controlled bunching and clock faults. It measures LF read rate, passage completeness, false accepts and "
     "the time alignment between RFID and video. Stage two is a single-farm pilot of at least 150 cows over 90 "
     "days. An independent observer or a trusted reference record labels every sampled passage, and the report "
     "separates EID recall, vision-only precision, vision-only recall, duplicate-read resolution, unresolved "
     "rate, alert lead time and reviewer workload. Stage three is a three-farm trial across differing housing "
     "types, deliberately including one low-roof cubicle building and one farm with a Scottish cross-border "
     "movement history. Release requires: at least 99% complete passage records, vision-only precision of at "
     "least 95% at the chosen threshold, vision-only recall of at least 90% after site calibration, no more "
     "than one false accept per 1,000 passages, and a median tag-health alert lead time of at least seven days. "
     "These are release gates for a pilot product, not claims about present field performance.")

# ================================================== 11. SUSTAINABILITY
doc.add_heading("11. Sustainable development", level=1)
para("The Dairy Roadmap commits the sector to net-zero carbon by 2050, a reduction in emissions intensity of "
     "at least 3% per year from a 2023 baseline to 2030, 100% renewable electricity by 2030, low-emission "
     "slurry application techniques by 2027 and biodiversity monitoring on at least 50% of dairy farms by "
     "2030 [36]. The HerdLens design engages with four of these principles directly.")
bullet("the edge unit draws about 25 W, or 219 kWh per year, which is roughly 0.045 t CO2e at "
       "grid intensity. There is no new building and no new hardstanding; the gateway is mounted on an "
       "existing race and the equipment can be supplied from the farm's own renewable generation, which is "
       "consistent with the Roadmap's 2030 renewable electricity target. The design revision made in response "
       "to this analysis is a switch from a separate power supply unit to PoE-only, and a target of under "
       "20 W for the volume build.",
       bold_lead="Climate and energy. ")
bullet("better identification improves culling and breeding decisions and reduces "
       "unproductive days in the herd, which lowers emissions per kilogram of fat and protein corrected "
       "milk. The system also produces the passage and identity records that underpin the carbon footprint "
       "calculation which the Roadmap requires every three years, so it contributes to the measurement as "
       "well as to the reduction.",
       bold_lead="Emissions intensity. ")
bullet("accurate identity is what makes a medicine record trustworthy, and a "
       "trustworthy medicine record is what makes a withdrawal period reliable. This matters in the North of "
       "England specifically, where average antimicrobial use has been measured at 14.9 mg/kg PCU against "
       "10.4 mg/kg in the South, and where the sector has committed to a further 25% reduction [42]. The "
       "three-fold reduction in handling time from electronic identification also reduces the stress and "
       "handling events experienced by the animals themselves [29].",
       bold_lead="Animal health, welfare and antibiotic stewardship. ")
bullet("the proposition has no per-animal device, and this is the strongest sustainability "
       "argument in its favour. A 215-cow unit running wearable sensors for a five-year service life would "
       "put over a thousand battery-containing devices into the field across the period, each of which has to "
       "be manufactured, maintained and eventually recovered as electronic waste. The gateway replaces that "
       "with two cameras and one compute module per farm, and the enclosure is specified for repair rather "
       "than replacement, with replaceable camera and power modules and a seven-year service life.",
       bold_lead="Waste and circularity. ")
para("Critical assessment. The claim of sustainability should not be overstated, and three trade-offs are "
     "recorded honestly. First, the embodied carbon of the compute module is real and is not offset by the "
     "energy saving; the honest justification is device substitution rather than energy reduction. Second, the "
     "vision modality is at its weakest precisely in the conditions the Roadmap encourages, because cows "
     "housed for longer periods have soiled flanks and the coat pattern is obscured. The design response is "
     "the continuous gallery refresh described in Section 10.3 and the 0.90 confidence threshold, not a claim "
     "that the problem does not exist. Third, and most importantly, the largest sustainability gains in the "
     "Roadmap come from slurry management, feed and fertiliser; identification technology is a measurement and "
     "welfare intervention, and presenting it as a climate intervention would be overstating the case. On "
     "that basis no revision to the technical description is proposed, but the sustainability claim is "
     "restricted to animal health, waste avoidance and enabling measurement, and it is not used to justify the "
     "capital cost.")

# ===================================================== 12. AFFORDABILITY
doc.add_heading("12. Affordability", level=1)
para("The cost of the gateway breaks down as follows for a single installation. The LF antenna pair is "
     "\u00a31,500 at current list price [22]; two IP66 cameras, the edge compute module, enclosure, cabling "
     "and illuminator come to \u00a31,050; installation, commissioning and the compulsory site survey add "
     "\u00a3400. Capital cost is therefore \u00a32,950. The recurring charge is \u00a3752 per year for a "
     "215-cow herd at \u00a33.50 per cow, plus an optional \u00a3120 hardware service contract.")
para("Affordability must be assessed against the grant position first, because the analysis in Section 5.1 "
     "concluded that a no-decision is the strongest competitor. The Farming Equipment and Technology Fund "
     "listed an EID panel reader for cattle at an expected average cost of \u00a31,591 with a 40% grant "
     "contribution, in a scheme covering 40\u201350% of eligible equipment cost and capped between \u00a31,000 "
     "and \u00a325,000 per theme [43]. Applying a 40% contribution to the reader element reduces the net "
     "capital cost to approximately \u00a32,155 and net first-year outlay to about \u00a32,907.")
para("The economic benefit for that same 215-cow herd is estimated as follows. The dominant term is labour: "
     "electronic identification of animals in a crush or raceway has been measured as roughly three times "
     "faster and more accurate than manual methods [29], and the gateway extends that electronic reading to "
     "every routine passage rather than only to handling events. Conservatively assuming one hour per week of "
     "handling time avoided across the year and valuing it at \u00a319 per hour [34] gives \u00a3990. A single "
     "avoided identity-not-proven event \u2014 one delayed cull, sale or test \u2014 is worth about \u00a3350 "
     "in delay, re-testing and price penalty, and one such event per year is a conservative expectation given "
     "a catalogue of tags failing at 1.4% to 5.1% per year [3]. Expected value on residue incidents at a UK "
     "failure rate of 0.15% against an event cost of \u00a31,250\u2013\u00a33,500 is about \u00a3100 per "
     "year [16], [17]. Avoiding even a fraction of the 4.3% genetic gain loss associated with a 10% paternity "
     "error rate [13], [14] is worth roughly \u00a3645 across the herd on a deliberately cautious assumption. "
     "Planned rather than emergency re-tagging adds about \u00a3120. Total quantified benefit is approximately "
     "\u00a32,205 per year.")
table(
    ["Item", "Year 1", "Years 2\u20135 (per year)"],
    [
        ["Capital \u2014 hardware and installation", "\u00a32,950", "\u2014"],
        ["Less FETF grant at 40% on the reader element", "\u2013\u00a3795", "\u2014"],
        ["Subscription, 215 cows at \u00a33.50 per cow", "\u00a3752", "\u00a3752"],
        ["Optional hardware service contract", "\u00a3120", "\u00a3120"],
        ["Total cash out", "\u00a33,027", "\u00a3872"],
        ["Quantified benefit", "\u00a32,205", "\u00a32,205"],
        ["Net position", "\u2013\u00a3822", "+\u00a31,333"],
    ],
    widths=[8.6, 3.6, 3.8], font_size=8.6)
caption("Table 7. Affordability of the HerdLens gateway for a 215-cow North of England dairy herd.")

para("Simple payback on gross capital cost is about 1.3 years, and about 1.0 year on the post-grant capital "
     "cost. The sensitivity that matters is labour, which is the largest single benefit term. If the labour "
     "saving is halved, total benefit falls to about \u00a31,710 and payback on the post-grant capital figure "
     "extends to roughly 1.3 years; if the labour saving is removed altogether, the payback stretches beyond "
     "five years and the proposition no longer stands on its own. That is an honest statement of the risk, and "
     "it is the reason the read-only tier described in Section 8.2 exists.")
para("These figures are decision estimates rather than supplier quotations. The result is most sensitive to "
     "the LF reader price, installation hours, labour saved and the grant being awarded. If capital cost rises "
     "by 20% or the subscription doubles to £7 per cow per year, the recommendation remains viable only if the "
     "pilot confirms at least half of the assumed labour saving. The price should therefore be presented as a "
     "target package for validation, not as a guaranteed market price.")
para("Is this within the financial means of the target customer? English dairy farm business income averaged "
     "\u00a3153,800 in 2024/25 and compares against a comparable-farm profit of \u00a3644 per cow, or roughly "
     "\u00a3138,000 across a 215-cow herd [33], [44]. A net capital outlay of \u00a32,155 is therefore about "
     "1.4% of annual business income and under 2% of herd profit, against a recurring charge of \u00a3872, or "
     "about \u00a34 per cow. Set against the alternatives, the position is more favourable still: the closest "
     "vision competitor costs \u00a3650 in hardware plus \u00a31 per cow per month, which is \u00a32,580 per "
     "year for the same herd before installation [27], and the wearable route requires roughly \u00a3102 per "
     "cow of capital, about \u00a321,900 for the herd [24]. The affordability conclusion is that the "
     "proposition is affordable on capital and cheap to run, but that it is not free, and in a year when the "
     "farm-gate milk price has fallen about 20% year on year [32] the grant route is not a marketing "
     "convenience. It is the condition on which the sale depends.")

# ====================================================== 13. REFERENCES
doc.add_heading("13. References", level=1)
para("References follow the IEEE style. All URLs were accessed in October 2026.", italic=True)

import importlib.util as _ilu
_s = _ilu.spec_from_file_location("fr", os.path.join(BASE, "fetch_references.py"))
_fr = _ilu.module_from_spec(_s)
_s.loader.exec_module(_fr)
_URL_FIX = {
    7: "https://www.gov.uk/government/collections/keeping-cattle-bison-and-buffalo-in-england-and-wales",
    11: "https://www.gov.uk/guidance/cattle-identification-inspections-what-to-expect",
    20: "https://www.gov.uk/guidance/report-and-record-cattle-deaths-on-the-holding",
}
refs = [f"{c} [Online]. Available: {_URL_FIX.get(n, u)}"
        for (n, _slug, c, u, _kind) in _fr.REFS]
refs.extend([
    "D. Swartz, E. Shepley, and G. Cramer, \"Evaluating the reliability of camera-based identification, activity monitoring, and location in housing systems on dairy farms,\" JDS Communications, vol. 6, 2025. [Online]. Available: https://agris.fao.org/search/en/providers/122436/records/67dac661677d8be0233bccd4",
    "Commercial multi-camera dairy-farm evaluation, 2025. [Online]. Available: https://pmc.ncbi.nlm.nih.gov/articles/PMC13131369/",
    "A. Negreiro et al., \"Siamese networks for identification of Holstein cattle during growth and across different physiological stages,\" ECPLF, 2024. [Online]. Available: https://experts.illinois.edu/en/publications/siamese-networks-for-identification-of-holstein-cattle-during-gro/",
    "L. Schulthess et al., \"A LoRa-based and maintenance-free cattle monitoring system for alpine pastures and remote locations,\" ENSsys, 2024. [Online]. Available: https://arxiv.org/html/2406.06245v1",
    "M. Hazas and A. Hopper, \"Broadband ultrasonic location systems for improved indoor positioning,\" IEEE Transactions on Mobile Computing, vol. 5, 2006. [Online]. Available: https://core.ac.uk/download/pdf/70108.pdf",
    "CattleEye, \"Starter kit eligibility,\" product documentation. [Online]. Available: https://cattleeye.com/en-gb/buy/eligibility-check",
])
for i, r in enumerate(refs, 1):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(1.0)
    p.paragraph_format.first_line_indent = Cm(-1.0)
    p.paragraph_format.space_after = Pt(4)
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(f"[{i}]\t{r}")
    run.font.size = Pt(9)

# Keep the technical description within the course's four-page guide without
# removing required interfaces, failure behaviour, or validation detail.
in_technical = False
for p in doc.paragraphs:
    label = p.text.strip()
    if label == "10. Technical description":
        in_technical = True
        continue
    if label == "11. Sustainable development":
        in_technical = False
    if in_technical:
        p.paragraph_format.line_spacing = 1.0
        p.paragraph_format.space_after = Pt(4)
        if label and not (label.startswith("10.") or label.startswith("Figure ") or label.startswith("Table ")):
            for run in p.runs:
                run.font.size = Pt(9.7)

# Tables 5 and 6 sit inside the technical section; slightly tighter cell
# leading keeps them legible while preventing a spill onto an extra page.
for table_index in (6, 7):
    if table_index < len(doc.tables):
        for row in doc.tables[table_index].rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    p.paragraph_format.space_after = Pt(1)
                    p.paragraph_format.line_spacing = 1.0

doc.save(OUTPATH)
print("saved:", OUTPATH)
print("paragraphs:", len(doc.paragraphs))
