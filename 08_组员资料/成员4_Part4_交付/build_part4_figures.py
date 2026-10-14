#!/usr/bin/env python3
"""Part 4 (Member 4) deliverable figures for ID-Coo report.

Fig 1: Physical layout of the handling race and diversion system (functional).
Fig 2: Control and data functional block diagram.

Style follows the team's build_figures.py conventions (light theme, dark ink).
Output: PNG at 220 dpi into the same folder as this script.
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
    fig, ax = new_ax(10.4, 5.6)
    W = 100 * 5.6 / 10.4  # ~53.8 y-units

    # ---- input column (left)
    inputs = [
        ("Ultrasonic sensors", ["distance, status,", "update time,", "diagnostics"], BLUE, BLUE_S, 40.0),
        ("LF RFID reader", ["tag ID, read time,", "device status"], BLUE, BLUE_S, 27.5),
        ("Gate position feedback", ["open / closed,", "locked, fault"], BLUE, BLUE_S, 15.0),
    ]
    for title, lines, fill, edge, y in inputs:
        box(ax, 2, y, 21, 10.5, fill, edge, title, lines, tfs=8.8, bfs=7.0)

    # safety devices (red-ish / pink) feeding safety chain directly
    box(ax, 2, 2.5, 21, 9.5, PINK, PINK_S, "Safety devices",
        ["e-stop, obstruction,", "guards"], tfs=8.8, bfs=7.0)

    # ---- PLC (centre)
    ax.add_patch(FancyBboxPatch((30.5, 14.0), 24, 30.5,
                                boxstyle="round,pad=0,rounding_size=1.4",
                                facecolor="#ffffff", edgecolor=INK, lw=1.6,
                                zorder=2))
    ax.text(42.5, 41.6, "Process controller (PLC)", ha="center", va="center",
            fontsize=9.6, fontweight="bold", color=INK, zorder=3)
    box(ax, 33, 22.5, 19, 15.0, TEAL, TEAL_S, "Passage state machine\n& event decision",
        ["event ID per animal", "de-duplication, limited", "re-reads, diversion", "decision, interlocks"],
        tfs=8.6, bfs=6.9)
    ax.text(42.5, 16.6, "sensor I/O · drive requests", ha="center", va="center",
            fontsize=6.8, color=MUTED, zorder=3, style="italic")

    # ---- safety chain (right top)
    box(ax, 62, 33.5, 20, 11.0, AMBER, AMBER_S, "Independent safety\ncontrol",
        ["evaluates protection", "state alone"], tfs=8.8, bfs=7.0)
    box(ax, 85, 33.5, 13, 11.0, GREY, GREY_S, "Gate drives",
        ["G0–G2, D, H"], tfs=8.6, bfs=7.0)

    # ---- data / UI (right bottom)
    box(ax, 62, 15.0, 36, 11.0, BLUE, BLUE_S, "Local records & farmer interface",
        ["event log, status view,", "manual actions"], tfs=8.8, bfs=7.0)
    box(ax, 62, 2.5, 36, 9.0, GREY, GREY_S, "Farm software / LIS",
        ["audited export (v1);", "direct link after authorisation"], tfs=8.6, bfs=7.0)

    # ---- arrows
    for _, _, y in [(0, 0, 45.2), (0, 0, 32.7), (0, 0, 20.2)]:
        arrow(ax, 23.2, y, 30.3, 29.5 + (y - 32.7) * 0.55)
    # safety devices -> safety control (hardwired), routed below the PLC
    ax.add_patch(FancyArrowPatch((23.2, 7.2), (62.0, 38.5),
                                 arrowstyle="-|>", mutation_scale=13,
                                 linewidth=1.4, color=PINK_S, zorder=3,
                                 linestyle=(0, (4, 2)), shrinkA=0, shrinkB=0,
                                 connectionstyle="angle,angleA=0,angleB=90,rad=0"))
    ax.text(40.0, 5.2, "hard-wired safety loop", fontsize=6.6, color=PINK_S,
            ha="center", va="center", style="italic")
    # PLC -> safety control (drive requests)
    arrow(ax, 54.7, 36.0, 61.8, 38.5, lw=1.5)
    ax.text(58.2, 40.8, "drive\nrequests", fontsize=6.4, color=MUTED,
            ha="center", va="center", linespacing=1.25)
    # safety control -> drives
    arrow(ax, 82.2, 39.0, 84.8, 39.0, lw=1.5)
    ax.text(83.5, 42.4, "drive\nenable", fontsize=6.4, color=MUTED,
            ha="center", va="center", linespacing=1.25)
    # PLC -> local records
    arrow(ax, 54.7, 24.0, 61.8, 20.5, lw=1.5)
    # local records -> farm software
    arrow(ax, 80, 14.8, 80, 11.7, lw=1.5)

    ax.text(2, 0.4, "Process control may request motion; only the independent safety "
                    "chain permits a drive. Software cannot bypass the safety loop. "
                    "Concept structure — not a construction circuit diagram.",
            fontsize=6.8, color=MUTED, ha="left", va="bottom", style="italic")

    fig.savefig(os.path.join(OUT, "fig_R10_block.png"), dpi=220,
                bbox_inches="tight", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    figure1()
    figure2()
    print("written:", os.listdir(OUT))
