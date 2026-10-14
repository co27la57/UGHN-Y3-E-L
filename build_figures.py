#!/usr/bin/env python3
"""Generate figures for the HerdLens PRD + Business Model coursework."""
import os
import math
import textwrap
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "06_图表", "figures")
os.makedirs(OUT, exist_ok=True)

INK = "#1f2430"
MUTED = "#5b6472"
GRID = "#b9c0cb"
GREY = "#f1efe8"
BLUE = "#e3edf9"; BLUE_S = "#185FA5"
TEAL = "#dcefe7"; TEAL_S = "#0F6E56"
AMBER = "#fbe9d6"; AMBER_S = "#8a5308"
PINK = "#fbe4ec"; PINK_S = "#993556"
GREY_S = "#5F5E5A"


class Layout:
    """All coordinates are fractions of the axes (0-1)."""

    def __init__(self, w_in, h_in):
        self.w = w_in
        self.h = h_in

    def chars(self, w_frac, fs, pad_in=0.16):
        avail_pt = (w_frac * self.w - 2 * pad_in) * 72
        return max(8, int(avail_pt * 0.95 / (fs * 0.505)))

    def line_adv(self, fs, spacing=1.34):
        return (fs * spacing / 72) / self.h

    def wrap(self, text, w_frac, fs, pad_in=0.16):
        return textwrap.wrap(text, width=self.chars(w_frac, fs, pad_in)) or [""]

    @staticmethod
    def n_lines(lines, chars):
        return sum(max(1, math.ceil(len(l) / chars)) for l in lines if l) or 1


def rounded(ax, x, y, w, h, fill, edge, lw=0.9, r=0.010, z=2):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle=f"round,pad=0,rounding_size={r}",
                                linewidth=lw, edgecolor=edge, facecolor=fill, zorder=z))


def box(ax, L, x, y, w, h, fill, edge, title, lines, tfs=9.0, bfs=7.4,
        tcolor=None, pad=0.011, center_title=False):
    rounded(ax, x, y, w, h, fill, edge)
    tcolor = tcolor or edge
    tx = x + w / 2 if center_title else x + pad
    anc = "center" if center_title else "left"
    ax.text(tx, y + h - pad - 0.008, title, ha=anc, va="top", fontsize=tfs,
            fontweight="bold", color=tcolor, zorder=3)
    cy = y + h - pad - 0.008 - L.line_adv(tfs) - 0.004
    for ln in lines:
        if not ln:
            cy -= L.line_adv(bfs) * 0.5
            continue
        for wl in L.wrap(ln, w, bfs, pad_in=pad):
            ax.text(x + pad, cy, wl, ha="left", va="top", fontsize=bfs,
                    color=INK, zorder=3)
            cy -= L.line_adv(bfs)
        cy -= L.line_adv(bfs) * 0.22


def stacked_panel(ax, L, x, y, w, h, fill, edge, title, blocks, tfs=10.5,
                  bbfs=7.4, title_fs=8.8):
    rounded(ax, x, y, w, h, fill, edge, lw=1.1, r=0.012, z=1)
    ax.text(x + 0.013, y + h - 0.014, title, ha="left", va="top",
            fontsize=tfs, fontweight="bold", color=edge, zorder=3)
    head = L.line_adv(tfs) + 0.022
    pad_in = 0.012
    top = y + h - head
    bottom = y + pad_in
    avail = top - bottom

    inner_w = w - 2 * pad_in
    body_chars = L.chars(inner_w, bbfs, pad_in=0.10)
    bodies = [L.n_lines(bl, body_chars) for _, bl, _, _ in blocks]
    tline = L.line_adv(title_fs, 1.2)
    overhead = tline + 0.014
    min_h = overhead + 2 * L.line_adv(bbfs) * 0.5
    total_body = sum(bodies) or 1
    extra = avail - len(blocks) * min_h
    extra = max(0.0, extra)

    cy = top
    for (bt, blines, bf, be), nb in zip(blocks, bodies):
        bh = min_h + extra * (nb / total_body)
        by = cy - bh
        rounded(ax, x + pad_in, by, inner_w, bh, bf, be, lw=0.7, r=0.007, z=2)
        ax.text(x + pad_in + 0.008, by + bh - 0.008, bt, ha="left", va="top",
                fontsize=title_fs, fontweight="bold", color=be, zorder=3)
        ty = by + bh - 0.008 - tline - 0.003
        for ln in blines:
            for wl in L.wrap(ln, inner_w, bbfs, pad_in=0.10):
                ax.text(x + pad_in + 0.008, ty, "\u2022 " + wl, ha="left", va="top",
                        fontsize=bbfs, color=INK, zorder=3)
                ty -= L.line_adv(bbfs)
            ty -= L.line_adv(bbfs) * 0.20
        cy = by - 0.006


def arrow(ax, x1, y1, x2, y2, color=MUTED, lw=1.1, ls="-", ms=10):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                                 mutation_scale=ms, linewidth=lw, color=color,
                                 linestyle=ls, zorder=4, shrinkA=1, shrinkB=1))


def canvas(caption, w, h):
    fig, ax = plt.subplots(figsize=(w, h), dpi=200)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    fig.patch.set_facecolor("white")
    fig.subplots_adjust(left=0.004, right=0.996, top=0.996, bottom=0.004)
    ax.text(0.5, 0.978, caption, ha="center", va="top", fontsize=9, color=MUTED)
    return fig, ax


# ----------------------------------------------------------------- Figure 1 VPC
def fig_vpc():
    L = Layout(13.6, 7.6)
    fig, ax = canvas("Figure 1. Value Proposition Canvas for HerdLens.", 13.6, 7.6)

    cust = [
        ("Customer Jobs", [
            "Tag calves on time (36 h primary / 21 d secondary) and register the birth by day 27",
            "Report movements in 3 days and deaths in 7 days; keep the holding register current",
            "Know which individual cow needs AI, treatment, foot trimming or culling",
            "Keep milk recording, breeding and medicine records accurate",
            "Prove traceability at TB tests, milk-buyer audits and RPA inspections",
            "Replace lost or unreadable tags inside the 28-day legal window",
        ], GREY, GREY_S),
        ("Pains", [
            "EID tags fall out or stop working: up to 19.8% cumulative loss over five years [3]",
            "LF reads one animal at a time, so two cows at a gate give a missed or a double read",
            "A cow whose tag has failed is invisible until the day she is actually needed",
            "Manual identification in a crush is about three times slower than electronic reading",
            "Wearables cost about GBP 102 per cow, need base stations and get torn off",
            "Camera systems still require EID, 4 m headroom and 4 m of clear, unobstructed walk",
            "Rural broadband is far too poor to depend on cloud video analytics",
        ], PINK, PINK_S),
        ("Gains", [
            "Never lose an animal's identity, whatever happens to the tag",
            "Faster, calmer handling with less time spent in the race",
            "Compliance evidence produced automatically rather than written up afterwards",
            "Confident culling and breeding decisions backed by reliable records",
            "One fixed system and no device on any animal",
            "Grant-eligible capital cost that pays back inside two years",
        ], TEAL, TEAL_S),
    ]
    val = [
        ("Products and Services", [
            "HerdLens Gate: an LF EID antenna pair, two IP66 cameras and an edge AI unit, retrofitted to the race the farm already owns",
            "HerdLens Cloud: identity engine, tag-health scoring, audit trail and API",
            "HerdLens App: review queue, re-tag list and movement-file export",
            "Installation, site survey and 14-day automatic herd enrolment",
        ], BLUE, BLUE_S),
        ("Pain Relievers", [
            "Coat-print biometrics return a named identity when the EID tag does not read",
            "Vision counting and tracking split a double read into two correct animals",
            "Tag-health score raises a re-tag alert well inside the 28-day deadline",
            "Dual-view camera plan (4 m top-down plus 2.5 m side) suits low-roof North England buildings",
            "All inference runs on the farm, so no broadband is required",
            "No collar, no ear sensor, no battery and no per-animal hardware to lose",
        ], BLUE, BLUE_S),
        ("Gain Creators", [
            "A single source of identity truth for the whole holding",
            "A ready-made, time-stamped and image-backed movement and passage record",
            "Scottish UHF and untagged cross-border animals still identified by vision",
            "The same camera can host a later mobility and lameness module",
            "Data feeds the carbon, health and welfare metrics the farm must already report",
        ], BLUE, BLUE_S),
    ]
    stacked_panel(ax, L, 0.012, 0.012, 0.470, 0.945, "#fbfbfd", MUTED,
                  "Customer Profile  \u2014  North of England dairy farmer", cust)
    stacked_panel(ax, L, 0.518, 0.012, 0.470, 0.945, "#fbfbfd", BLUE_S,
                  "Value Map  \u2014  HerdLens", val)
    fig.savefig(os.path.join(OUT, "fig1_vpc.png"), facecolor="white")
    plt.close(fig)


# --------------------------------------------------------- Figure 2 block diagram
def fig_block():
    L = Layout(12.8, 7.6)
    fig, ax = canvas("Figure 2. HerdLens functional block diagram.", 12.8, 7.6)

    col = 0.205
    x1, x2, x3, x4 = 0.012, 0.255, 0.520, 0.790
    x4w = 0.198
    box(ax, L, x1, 0.720, col, 0.220, BLUE, BLUE_S, "1. LF EID antenna pair",
        ["134.2 kHz, ISO 11784/11785 HDX and FDX-B",
         "0.5 m read field, mounted on both sides of the race"])
    box(ax, L, x1, 0.480, col, 0.215, BLUE, BLUE_S, "2. Camera A (top-down)",
        ["4 m, 4 MP IP66, coat-pattern view", "850 nm IR illuminator"])
    box(ax, L, x1, 0.240, col, 0.215, BLUE, BLUE_S, "3. Camera B (side)",
        ["2.5 m, head and ear-tag view", "Fitted when roof height is under 4 m"])
    box(ax, L, x1, 0.040, col, 0.175, GREY, GREY_S, "4. Auxiliary sensors",
        ["PIR passage trigger", "Ambient lux and temperature"])

    box(ax, L, x2, 0.700, col, 0.240, TEAL, TEAL_S, "5. Edge AI unit",
        ["Jetson Orin Nano, or Hailo-8L / Raspberry Pi 5",
         "YOLOv8-n detection and ByteTrack tracking",
         "OSNet coat-pattern embedding, 512 dimensions"])
    box(ax, L, x2, 0.420, col, 0.250, TEAL, TEAL_S, "6. Fusion engine",
        ["Passage-window builder, one event per animal",
         "Hungarian assignment of reads to tracklets",
         "Confidence scoring and tag-health scoring"])
    box(ax, L, x2, 0.040, col, 0.350, GREY, GREY_S, "7. Local store",
        ["SQLite record plus image ring buffer",
         "Seven days of full offline autonomy",
         "Raw imagery never leaves the holding"])

    box(ax, L, x3, 0.755, col, 0.185, AMBER, AMBER_S, "8. HerdLens Cloud",
        ["Encrypted store-and-forward sync", "Embeddings and metadata only",
         "Model updates and fleet analytics"])
    box(ax, L, x3, 0.480, col, 0.240, AMBER, AMBER_S, "9. HerdLens App and API",
        ["Farmer review queue and re-tag list",
         "REST API into herd management software"])
    box(ax, L, x3, 0.040, col, 0.410, AMBER, AMBER_S, "10. External interfaces",
        ["Herd management software (Herdwatch, SUM-IT, Uniform-Agri)",
         "LIS / CTS-ready movement file",
         "Future LIS API integration",
         "Milk-buyer and assurance scheme reporting"])

    box(ax, L, x4, 0.720, x4w, 0.180, PINK, PINK_S, "Farmer", ["Web dashboard", "Mobile PWA"])
    box(ax, L, x4, 0.390, x4w, 0.180, PINK, PINK_S, "Assurance", ["RPA inspection", "Milk-buyer audit"])
    box(ax, L, x4, 0.040, x4w, 0.180, PINK, PINK_S, "Government", ["LIS / BCMS", "bTB tracing"])

    for y in (0.830, 0.588, 0.348, 0.128):
        arrow(ax, x1 + col + 0.006, y, x2 - 0.006, y)
    arrow(ax, x2 + col / 2, 0.698, x2 + col / 2, 0.672)
    arrow(ax, x2 + col / 2, 0.418, x2 + col / 2, 0.392)
    arrow(ax, x2 + col + 0.006, 0.830, x3 - 0.006, 0.840)
    arrow(ax, x2 + col + 0.006, 0.560, x3 - 0.006, 0.600)
    arrow(ax, x2 + col + 0.006, 0.180, x3 - 0.006, 0.180)
    arrow(ax, x3 + col + 0.006, 0.810, x4 - 0.006, 0.810)
    arrow(ax, x3 + col + 0.006, 0.600, x4 - 0.006, 0.480)
    arrow(ax, x3 + col + 0.006, 0.200, x4 - 0.006, 0.130)

    fig.savefig(os.path.join(OUT, "fig2_block.png"), facecolor="white")
    plt.close(fig)


# ------------------------------------------------------ Figure 3 fusion logic
def fig_fusion():
    L = Layout(12.0, 8.4)
    fig, ax = canvas("Figure 3. Sensor-fusion decision logic for one passage event.", 12.0, 8.4)

    box(ax, L, 0.220, 0.878, 0.560, 0.062, GREY, GREY_S,
        "Step 1  \u2014  Passage event opened (PIR trigger, detector count 0 \u2192 1+)", [],
        tfs=9.2, center_title=True)
    arrow(ax, 0.500, 0.876, 0.500, 0.856)

    box(ax, L, 0.030, 0.716, 0.455, 0.138, BLUE, BLUE_S, "Step 2  \u2014  Collect evidence",
        ["EID reads (N_eid) with RSSI and timestamps",
         "Vision tracklets (N_trk) with entry and exit times"], tfs=9.0)
    box(ax, L, 0.515, 0.716, 0.455, 0.138, BLUE, BLUE_S, "Step 2b  \u2014  Gallery refresh",
        ["High-confidence matches add labelled images",
         "Enrolment target: 12+ images per cow over 3+ days"], tfs=9.0)
    arrow(ax, 0.490, 0.785, 0.510, 0.785)
    arrow(ax, 0.500, 0.714, 0.500, 0.692)

    rows = [
        ("Case A", "1 tracklet, 1 EID read", "Accept at 0.99 confidence and refresh the coat gallery.", TEAL, TEAL_S),
        ("Case B", "1 tracklet, no EID read", "Vision re-identification only. Above 0.90 assign the identity and raise a 'tag not read' flag.", AMBER, AMBER_S),
        ("Case C", "1 tracklet, 2 or more EID reads", "Double read: order the reads by RSSI and entry time, assign each to the correct animal, quarantine any surplus.", PINK, PINK_S),
        ("Case D", "2 or more tracklets, 1 EID read", "Split the passage: assign the read to the tracklet with peak RSSI and flag the remainder.", AMBER, AMBER_S),
        ("Case E", "2 or more tracklets, 2 or more EID reads", "Hungarian assignment on a cost of RSSI strength multiplied by temporal overlap.", TEAL, TEAL_S),
    ]
    top = 0.688
    rh = 0.054
    for i, (tag, cond, action, f, e) in enumerate(rows):
        y = top - (i + 1) * rh
        rounded(ax, 0.030, y + 0.005, 0.940, rh - 0.010, f, e, lw=0.8, r=0.006)
        ax.text(0.042, y + rh / 2 - 0.004, tag, ha="left", va="center",
                fontsize=8.6, fontweight="bold", color=e, zorder=3)
        ax.text(0.118, y + rh / 2 - 0.004, cond, ha="left", va="center",
                fontsize=8.0, color=INK, zorder=3)
        ax.text(0.360, y + rh / 2 - 0.004, action, ha="left", va="center",
                fontsize=7.5, color=INK, zorder=3)
    arrow(ax, 0.500, 0.414, 0.500, 0.394)

    box(ax, L, 0.030, 0.252, 0.455, 0.140, GREY, GREY_S, "Step 4  \u2014  Confidence gate",
        ["Below 0.90: route the passage to the farmer review queue",
         "At or above 0.90: commit the identity to the record"], tfs=9.0)
    box(ax, L, 0.515, 0.252, 0.455, 0.140, GREY, GREY_S, "Step 5  \u2014  Tag-health update",
        ["30-day rolling read rate maintained per cow",
         "Re-tag list issued by day 21 of the 28-day statutory window"], tfs=9.0)
    arrow(ax, 0.490, 0.322, 0.510, 0.322)

    box(ax, L, 0.150, 0.100, 0.700, 0.118, BLUE, BLUE_S,
        "Step 6  \u2014  Outputs",
        ["Cow identity and timestamp written to the local record; movement file and API sync queued; image retained as compliance evidence"],
        tfs=9.0, center_title=True)
    arrow(ax, 0.500, 0.250, 0.500, 0.220)

    fig.savefig(os.path.join(OUT, "fig3_fusion.png"), facecolor="white")
    plt.close(fig)


# ----------------------------------------------------------------- Figure 4 BMC
def fig_bmc():
    L = Layout(15.4, 9.8)
    fig, ax = canvas("Figure 4. Business Model Canvas for HerdLens.", 15.4, 9.8)

    cw = 0.188
    gap = 0.009
    xs = [0.012 + i * (cw + gap) for i in range(5)]

    r1t, r1h = 0.940, 0.330
    r2t, r2h = 0.588, 0.228
    r3t, r3h = 0.335, 0.290

    def blk(x, ytop, w, h, title, lines, tfs=8.6, bfs=7.35):
        box(ax, L, x, ytop - h, w, h, "white", GRID, title, lines, tfs=tfs, bfs=bfs,
            tcolor=INK, pad=0.009)

    blk(xs[0], r1t, cw, r1h + r2h + 0.015, "Key Partners", [
        "Shearwell Data and Datamars: LF antenna and reader modules",
        "NVIDIA and Hailo: edge compute modules",
        "Herd software vendors (Herdwatch, SUM-IT, Uniform-Agri)",
        "Regional agricultural engineers for install and service",
        "AHDB, NMR and milk buyers for validation and reach",
        "Defra FETF: the 40-50% grant route to market",
    ])
    blk(xs[1], r1t, cw, r1h, "Key Activities", [
        "Edge AI model development and per-farm fine-tuning",
        "Hardware integration and IP66 enclosure design",
        "Farm site survey and retrofit installation",
        "Automatic herd enrolment pipeline",
        "Regulatory watch on LIS, BEID and grant schemes",
    ])
    blk(xs[1], r2t, cw, r2h, "Key Resources", [
        "Self-supervised Holstein re-identification model",
        "Passage-window fusion algorithm",
        "Installed fleet generating labelled on-farm data",
        "UK field engineering team",
        "FETF-eligible product listing",
    ])
    blk(xs[2], r1t, cw, r1h + r2h + 0.015, "Value Propositions", [
        "The only system that still names the cow when the EID tag is lost, damaged or double-read",
        "No device on any animal: no collar, no battery, no per-head hardware",
        "Two cows at the gate are resolved, not logged as an error",
        "Tag-health alerts inside the 28-day statutory window",
        "Works with no farm broadband: all inference at the edge",
        "Retrofits to the race the farm already owns",
        "About GBP 3.50 per cow per year against GBP 12 for camera subscriptions",
    ], tfs=8.8, bfs=7.4)
    blk(xs[3], r1t, cw, r1h, "Customer Relationships", [
        "Engineer-led installation and enrolment",
        "Annual herd compliance review",
        "Self-serve app with a named regional contact",
        "Reference farms and demonstration days",
    ])
    blk(xs[3], r2t, cw, r2h, "Channels", [
        "Direct field sales at dairy shows and discussion groups",
        "Vet practices and nutritionists as referral partners",
        "Agricultural engineer resellers",
        "Milk buyer and assurance scheme channels",
    ])
    blk(xs[4], r1t, cw, r1h + r2h + 0.015, "Customer Segments", [
        "North of England Holstein-Friesian farms, 150-350 cows",
        "Owner-operated with two to four staff",
        "Already run cows single file through a parlour exit or drafting race",
        "Facing the 2027 LF EID mandate",
        "Currently treat EID as a compliance chore, not a management tool",
        "Later: Scottish UHF herds, Irish and New Zealand pastoral dairy",
    ])

    bw = cw * 2.5 + gap * 1.5
    blk(xs[0], r3t, bw, r3h, "Cost Structure", [
        "Hardware bill of materials about GBP 1,750 per gate (the GBP 1,500 antenna pair is the largest line; target GBP 900 at volume)",
        "Installation and commissioning labour GBP 200 per site",
        "Cloud and connectivity GBP 0.40 per cow per year",
        "R&D: computer vision engineers and on-farm data collection",
        "Sales, service and warranty provisioning",
    ])
    blk(xs[0] + bw + gap, r3t, bw, r3h, "Revenue Streams", [
        "One-off hardware and installation GBP 2,950, or GBP 2,155 net of a 40% FETF grant",
        "SaaS subscription GBP 3.50 per cow per year, so GBP 752 for a 215-cow herd",
        "Optional hardware service contract GBP 120 per year",
        "Future module add-ons: mobility and lameness scoring, body condition",
        "Anonymised benchmarking data sold to milk buyers and breed societies",
    ])

    fig.savefig(os.path.join(OUT, "fig4_bmc.png"), facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    fig_vpc(); fig_block(); fig_fusion(); fig_bmc()
    print("figures written to", OUT)
    for f in sorted(os.listdir(OUT)):
        print(" ", f, os.path.getsize(os.path.join(OUT, f)))
