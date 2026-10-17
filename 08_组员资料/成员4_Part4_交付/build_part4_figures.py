#!/usr/bin/env python3
"""Part 4 (Member 4) deliverable figures for ID-Coo report.

Fig 1: Physical layout of the handling race and diversion system (functional).
Fig 2: Functional control, safety and data interfaces.

Style follows the team's build_figures.py conventions (light theme, dark ink).
Output: high-resolution PNGs in the figures folder beside this script.
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon, Circle

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
os.makedirs(OUT, exist_ok=True)

INK = "#1f2430"
MUTED = "#5b6472"
GRID = "#b9c0cb"
BLUE = "#e3edf9"; BLUE_S = "#185FA5"
TEAL = "#dcefe7"; TEAL_S = "#0F6E56"
AMBER = "#fbe9d6"; AMBER_S = "#8a5308"
PINK = "#fbe4ec"; PINK_S = "#993556"
GREY = "#f1efe8"; GREY_S = "#5F5E5A"


def new_ax(w_in, h_in):
    fig, ax = plt.subplots(figsize=(w_in, h_in))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100 * h_in / w_in)
    ax.axis("off")
    return fig, ax


def box(ax, x, y, w, h, fill, edge, title, lines=None, tfs=9.5, bfs=7.6,
        lw=1.1, title_color=None):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0,rounding_size=1.2",
                                linewidth=lw, edgecolor=edge, facecolor=fill,
                                zorder=2))
    tc = title_color or edge
    if lines:
        ax.text(x + w / 2, y + h - 3.2, title, ha="center", va="top",
                fontsize=tfs, fontweight="bold", color=tc, zorder=3)
        ax.text(x + w / 2, y + h - 8.2, "\n".join(lines), ha="center", va="top",
                fontsize=bfs, color=INK, zorder=3, linespacing=1.45)
    else:
        ax.text(x + w / 2, y + h / 2, title, ha="center", va="center",
                fontsize=tfs, fontweight="bold", color=tc, zorder=3)


def gate(ax, x, y, h, label, color=GREY_S, label_dx=0.0, label_dy=2.2):
    """Vertical gate bar with label above (offset configurable)."""
    ax.add_patch(FancyBboxPatch((x - 1.1, y), 2.2, h,
                                boxstyle="round,pad=0,rounding_size=0.5",
                                linewidth=1.0, edgecolor=INK, facecolor=color,
                                zorder=4))
    ax.text(x + label_dx, y + h + label_dy, label, ha="center", va="bottom",
            fontsize=8.2, fontweight="bold", color=INK, zorder=5)


def arrow(ax, x1, y1, x2, y2, color=INK, lw=1.4, style="-|>", ls="-", ms=13):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style,
                                 mutation_scale=ms, linewidth=lw, color=color,
                                 linestyle=ls, zorder=3,
                                 shrinkA=0, shrinkB=0))


def us_point(ax, x, y, label, dx=0, dy=2.6):
    ax.add_patch(Circle((x, y), 1.35, facecolor="#ffffff", edgecolor=AMBER_S,
                        linewidth=1.2, zorder=5))
    ax.text(x, y, "U", ha="center", va="center", fontsize=6.4,
            fontweight="bold", color=AMBER_S, zorder=6)
    ax.text(x + dx, y + dy, label, ha="center", va="bottom", fontsize=6.6,
            color=MUTED, zorder=6)


# ---------------------------------------------------------------- Figure 1
def figure1():
    fig, ax = new_ax(10.4, 5.4)
    W = 100 * 5.4 / 10.4  # ~51.9 y-units

    # Race baseline (the single-file alley floor)
    ax.add_patch(FancyBboxPatch((3, 21.5), 66, 4.5,
                                boxstyle="round,pad=0,rounding_size=0.8",
                                facecolor=GREY, edgecolor=GRID, lw=0.8, zorder=1))
    ax.text(35.5, 23.75, "single-file race (adjustable width)", ha="center",
            va="center", fontsize=6.8, color=MUTED, zorder=2, style="italic")

    # Cattle holding area
    box(ax, 3, 18, 11, 11.5, BLUE, BLUE_S, "Cattle\nholding\narea",
        tfs=8.6)

    # Gate G0
    gate(ax, 17.2, 19, 10, "G0")

    # Buffer section A
    box(ax, 21, 18, 13, 12, TEAL, TEAL_S, "Section A",
        ["single-animal", "buffer"], tfs=9.2, bfs=7.2)
    us_point(ax, 27.5, 33, "U-A", dx=0, dy=2.2)

    # Gate G1
    gate(ax, 37.2, 19, 10, "G1")
    us_point(ax, 37.2, 34.4, "U-IN", dx=-4.2, dy=0.8)

    # Detection section B
    box(ax, 41, 18, 15, 12, BLUE, BLUE_S, "Section B", tfs=9.2)
    ax.text(48.5, 23.2, "detection · read zone", ha="center", va="top",
            fontsize=7.2, color=INK, zorder=3)
    us_point(ax, 43.4, 33, "U-B1", dx=0, dy=2.2)
    us_point(ax, 53.6, 33, "U-B2", dx=0, dy=2.2)
    # RFID antenna marker inside B
    ax.add_patch(FancyBboxPatch((46.1, 18.5), 4.8, 2.5,
                                boxstyle="round,pad=0,rounding_size=0.5",
                                facecolor="#ffffff", edgecolor=PINK_S,
                                lw=1.1, zorder=5))
    ax.text(48.5, 19.75, "LF RFID\nantenna", ha="center", va="center",
            fontsize=5.8, color=PINK_S, zorder=6, linespacing=1.15)

    # Gate G2
    gate(ax, 59.2, 19, 10, "G2")

    # Diversion area with gate D
    ax.add_patch(Polygon([(63.5, 23.75), (70.5, 27.4), (70.5, 20.1), (63.5, 23.75)],
                         closed=True, facecolor=AMBER, edgecolor=AMBER_S,
                         lw=1.2, zorder=3))
    ax.text(66.6, 23.75, "D", ha="center", va="center", fontsize=9.5,
            fontweight="bold", color=AMBER_S, zorder=4)
    ax.text(63.0, 18.8, "diversion area\ngate D", ha="center", va="top",
            fontsize=6.4, color=MUTED, zorder=4, linespacing=1.25)

    # Normal return (top branch)
    ax.add_patch(FancyBboxPatch((72.5, 30.5), 24.5, 8.2,
                                boxstyle="round,pad=0,rounding_size=1.0",
                                facecolor=TEAL, edgecolor=TEAL_S, lw=1.1,
                                zorder=2))
    ax.text(84.75, 34.6, "Normal return\nchannel", ha="center", va="center",
            fontsize=8.4, fontweight="bold", color=TEAL_S, zorder=3,
            linespacing=1.3)
    us_point(ax, 72.2, 34.6, "U-N", dx=-4.4, dy=1.0)

    # Exception branch (bottom)
    ax.add_patch(FancyBboxPatch((72.5, 9.5), 24.5, 8.2,
                                boxstyle="round,pad=0,rounding_size=1.0",
                                facecolor=PINK, edgecolor=PINK_S, lw=1.1,
                                zorder=2))
    ax.text(84.75, 13.6, "Exception branch\n(review pen)", ha="center",
            va="center", fontsize=8.4, fontweight="bold", color=PINK_S,
            zorder=3, linespacing=1.3)
    us_point(ax, 73.6, 13.6, "U-Q", dx=-5.4, dy=0.9)

    # Pen entry gate H
    gate(ax, 71.2, 10.5, 6.2, "H", color=PINK_S, label_dx=-2.2, label_dy=1.8)

    # Flow arrows along the race
    arrow(ax, 14.2, 23.75, 16.0, 23.75)
    arrow(ax, 18.4, 23.75, 20.8, 23.75)
    arrow(ax, 34.2, 23.75, 36.0, 23.75)
    arrow(ax, 38.4, 23.75, 40.8, 23.75)
    arrow(ax, 56.2, 23.75, 58.0, 23.75)
    # D to exits
    arrow(ax, 70.6, 25.2, 72.4, 32.6, color=TEAL_S, lw=1.5)
    arrow(ax, 70.6, 22.0, 72.4, 14.6, color=PINK_S, lw=1.5)

    # Direction-of-travel note
    ax.text(3, 47.5, "Direction of travel:", fontsize=7.0, color=MUTED,
            ha="left", va="center")
    arrow(ax, 21.5, 47.5, 30.5, 47.5, lw=1.1)

    # Legend
    lx = 3
    ax.text(lx, 7.8, "G0–G2  interlocked separating gates      "
                     "D  diversion gate (guide boundary only — never pushes the animal)",
            fontsize=6.8, color=MUTED, ha="left", va="center")
    ax.text(lx, 5.2, "H  review-pen entry gate      "
                     "U-*  ultrasonic occupancy / passage points (planning configuration)",
            fontsize=6.8, color=MUTED, ha="left", va="center")
    ax.text(lx, 2.4, "Antenna mounted outside the head/ear zone. Not to scale — "
                     "final dimensions set by on-farm survey.",
            fontsize=6.8, color=MUTED, ha="left", va="center", style="italic")

    fig.savefig(os.path.join(OUT, "fig_R10_layout.png"), dpi=220,
                bbox_inches="tight", facecolor="white")
    plt.close(fig)


# ---------------------------------------------------------------- Figure 2
def figure2():
    """Functional interfaces with process, protection and data paths separated."""
    fig, ax = plt.subplots(figsize=(10.4, 6.3))
    ax.set_xlim(0, 10.4)
    ax.set_ylim(0, 6.3)
    ax.axis("off")

    def node(x, y, w, h, title, detail, fill, edge,
             title_size=12.5, detail_size=10.2, dashed=False):
        patch = FancyBboxPatch(
            (x, y), w, h, boxstyle="round,pad=0,rounding_size=0.12",
            linewidth=1.25, edgecolor=edge, facecolor=fill, zorder=2,
            linestyle=(0, (4, 2)) if dashed else "-",
        )
        ax.add_patch(patch)
        ax.text(x + w/2, y + h - 0.18, title, ha="center", va="top",
                fontsize=title_size, fontweight="bold", color=edge, zorder=3)
        detail_y = y + (h/2 - 0.08 if h > 2 else 0.17)
        detail_va = "center" if h > 2 else "bottom"
        ax.text(x + w/2, detail_y, detail, ha="center", va=detail_va,
                fontsize=detail_size, color=INK, zorder=3, linespacing=1.28)

    def link(start, end, color=INK, dashed=False, both=False, width=1.5):
        ax.add_patch(FancyArrowPatch(
            start, end, arrowstyle="<->" if both else "-|>",
            mutation_scale=13, linewidth=width, color=color, zorder=1,
            linestyle=(0, (4, 2)) if dashed else "-",
            shrinkA=0, shrinkB=0,
        ))

    # Field inputs and process sequencing: none of these three ordinary
    # signals is presented as a validated safety device.
    input_x, input_w = 0.35, 2.55
    for y, title, detail in (
        (5.00, "Ultrasonic sensing", "occupancy · health"),
        (3.97, "LF RFID reader", "tag number · read time"),
        (2.94, "Gate feedback", "position · fault"),
    ):
        node(input_x, y, input_w, 0.92, title, detail, BLUE, BLUE_S,
             title_size=12.2, detail_size=9.8)
        link((2.90, y + 0.46), (3.40, y + 0.46), color=BLUE_S)

    node(3.40, 2.94, 2.25, 2.98, "Passage PLC",
         "event ID & tag check\nroute · motion request",
         TEAL, TEAL_S, title_size=14.0, detail_size=10.4)
    node(8.05, 4.72, 2.00, 1.20, "Gate drives", "G0–G2 · D · H",
         GREY, GREY_S, title_size=13.5, detail_size=10.8)
    link((5.65, 5.32), (8.05, 5.32), color=INK, width=1.65)
    ax.text(6.85, 5.56, "motion requests", ha="center", va="bottom",
            fontsize=10.0, color=MUTED)

    # Separate safety-related path: its functions and performance are set by
    # the site risk assessment.  It never passes through farm data software.
    node(6.00, 2.94, 1.58, 0.92, "Safety devices",
         "E-stop · guards", PINK, PINK_S,
         title_size=10.2, detail_size=9.1)
    node(8.05, 2.94, 2.00, 0.92, "Safety control",
         "stop / inhibit", PINK, PINK_S,
         title_size=11.4, detail_size=9.6)
    link((7.58, 3.40), (8.05, 3.40), color=PINK_S, width=1.65)
    link((9.05, 3.86), (9.05, 4.72), color=PINK_S, width=1.65)
    ax.text(8.74, 4.32, "enable / inhibit", ha="right", va="center",
            fontsize=9.2, color=PINK_S)

    # Data and operator workflow.  The dashed LIS box is a future option,
    # not a claimed version-1 connection.
    node(3.40, 0.55, 2.25, 1.03, "Local log + HMI",
         "audit · review", BLUE, BLUE_S,
         title_size=12.0, detail_size=9.8)
    node(6.15, 0.55, 1.80, 1.03, "Farm software",
         "v1 export", GREY, GREY_S,
         title_size=10.8, detail_size=9.8)
    node(8.40, 0.55, 1.65, 1.03, "Future LIS",
         "authorised only", "#ffffff", GREY_S,
         title_size=11.0, detail_size=9.2, dashed=True)
    link((4.53, 2.94), (4.53, 1.58), color=BLUE_S, both=True)
    ax.text(4.77, 2.25, "events / operator I/O", ha="left",
            va="center", fontsize=9.4, color=BLUE_S)
    link((5.65, 1.06), (6.15, 1.06), color=INK)
    ax.text(5.90, 1.78, "export", ha="center", va="bottom",
            fontsize=9.2, color=MUTED)
    ax.text(9.23, 1.78, "later / separate interface", ha="center", va="bottom",
            fontsize=8.9, color=MUTED)

    ax.text(0.35, 0.18,
            "Functional concept only · Protective devices and required performance follow site risk assessment.",
            fontsize=9.4, color=MUTED, ha="left", va="center", style="italic")

    fig.savefig(os.path.join(OUT, "fig_R10_block.png"), dpi=240,
                bbox_inches="tight", pad_inches=0.10, facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    figure1()
    figure2()
    print("written:", os.listdir(OUT))
