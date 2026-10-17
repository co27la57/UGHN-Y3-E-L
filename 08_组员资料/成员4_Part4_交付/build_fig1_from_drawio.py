#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild Figure 1 (race & diversion layout) from the drawio source.

Source: figures/fig_R10_layout.drawio (page 1500x820, y-down).
All coordinates, colours, stroke widths and texts are taken from that file
so the PNG and the .drawio stay in sync.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Ellipse, Polygon
from matplotlib.font_manager import FontProperties

# ---- palette (from drawio) ----
INK      = "#1F2430"   # main line / text
MUTED    = "#5B6472"   # secondary text
GATE     = "#5F5E5A"   # gate bar fill
FLOOR    = "#F1EFE8"   # race floor fill
FLOOR_E  = "#B9C0CB"   # race floor edge
BLUE     = "#E3EDF9"; BLUE_E  = "#185FA5"
GREEN    = "#DCEFE7"; GREEN_E = "#0F6E56"
PINK     = "#FBE4EC"; PINK_E  = "#993556"
AMBER    = "#FBE9D6"; AMBER_E = "#8A5308"
WHITE    = "#FFFFFF"

PAGE_W, PAGE_H = 1500, 820
DPI = 200                      # 15in x 8.2in -> 3000 x 1640 px

fig = plt.figure(figsize=(PAGE_W / 100.0, PAGE_H / 100.0), dpi=DPI)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, PAGE_W)
ax.set_ylim(PAGE_H, 0)         # drawio y-down coordinates
ax.axis("off")
fig.patch.set_facecolor("white")

def pt(px):
    """drawio px -> matplotlib pt (96 dpi reference)."""
    return px * 0.75

def rbox(x, y, w, h, fc, ec, lw, z=3, radius=None):
    r = radius if radius is not None else max(6, min(w, h) * 0.07)
    p = FancyBboxPatch((x + r, y + r), w - 2 * r, h - 2 * r,
                       boxstyle=f"round,pad={r},rounding_size={r}",
                       linewidth=pt(lw), edgecolor=ec, facecolor=fc, zorder=z,
                       mutation_aspect=1)
    ax.add_patch(p)
    return p

def txt(x, y, s, size, color=INK, bold=False, italic=False, ha="center", va="center", z=5, lh=1.25):
    ax.text(x, y, s, fontsize=pt(size), color=color, ha=ha, va=va, zorder=z,
            fontweight="bold" if bold else "normal",
            fontstyle="italic" if italic else "normal",
            linespacing=lh, family="DejaVu Sans")

def arrow(x1, y1, x2, y2, color=INK, lw=2.6, z=4, ms=13):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), zorder=z,
                arrowprops=dict(arrowstyle="-|>", mutation_scale=ms,
                                linewidth=pt(lw), color=color,
                                shrinkA=0, shrinkB=0))

# ---------------- 1. race floor (behind everything) ----------------
rbox(230, 310, 790, 60, FLOOR, FLOOR_E, 1.0, z=1, radius=8)

# ---------------- 2. top labels ----------------
txt(50, 39.5, "Direction of travel", 18, MUTED, ha="left")
arrow(265, 40, 375, 40, INK, 2.4, ms=15)
txt(425 + 435 / 2, 39.5, "Single-file race · adjustable width", 17, MUTED, italic=True)

# ---------------- 3. race chain ----------------
rbox(50, 225, 180, 200, BLUE, BLUE_E, 2.4)
txt(140, 300, "Cattle\nholding\narea", 23, BLUE_E, bold=True)

ax.add_patch(Rectangle((265, 235), 30, 180, facecolor=GATE, edgecolor=INK,
                       linewidth=pt(2.2), zorder=3))
txt(280, 213, "G0", 22, INK, bold=True)

rbox(330, 225, 205, 200, GREEN, GREEN_E, 2.4)
txt(432.5, 272, "Section A", 24, GREEN_E, bold=True)
txt(432.5, 336, "single-animal\nbuffer\nstaff-confirmed\nin v1", 17, INK)

ax.add_patch(Rectangle((570, 235), 30, 180, facecolor=GATE, edgecolor=INK,
                       linewidth=pt(2.2), zorder=3))
txt(601, 213, "G1", 22, INK, bold=True)

rbox(635, 225, 255, 200, BLUE, BLUE_E, 2.4)
txt(762.5, 272, "Section B", 24, BLUE_E, bold=True)
txt(762.5, 322, "detection ·\nread zone", 17, INK)

rbox(700, 365, 125, 43, WHITE, PINK_E, 1.8, radius=8)
txt(762.5, 386.5, "LF RFID\nantenna", 16, PINK_E)

ax.add_patch(Rectangle((925, 235), 30, 180, facecolor=GATE, edgecolor=INK,
                       linewidth=pt(2.2), zorder=3))
txt(956, 213, "G2", 22, INK, bold=True)

# ---------------- 4. diverter D (triangle pointing west/left) ----------------
ax.add_patch(Polygon([(1005, 327.5), (1100, 280), (1100, 375)], closed=True,
                     facecolor=AMBER, edgecolor=AMBER_E,
                     linewidth=pt(2.5), zorder=3))
txt(1048, 327.5, "D", 27, AMBER_E, bold=True)

# ---------------- 5. exits ----------------
rbox(1140, 155, 310, 160, GREEN, GREEN_E, 2.4)
txt(1295, 235, "Normal return\nchannel", 24, GREEN_E, bold=True)

ax.add_patch(Rectangle((1090, 475), 28, 132, facecolor=PINK_E, edgecolor=INK,
                       linewidth=pt(2.2), zorder=3))
txt(1104, 453, "H", 22, INK, bold=True)

rbox(1140, 455, 310, 160, PINK, PINK_E, 2.4)
txt(1295, 512, "Exception branch", 23, PINK_E, bold=True)
txt(1295, 548, "review pen", 17, INK)

# ---------------- 6. ultrasonic points ----------------
for cx, cy, label, lx, ly in [
    (430, 162, "U-A", 430, 115),
    (615, 130, "U-IN", 615, 83),
    (710, 162, "U-B1", 710, 115),
    (825, 162, "U-B2", 825, 115),
    (1100, 132, "U-N", 1100, 84),
    (1235, 425, "U-Q", 1235, 380),
]:
    ax.add_patch(Ellipse((cx, cy), 44, 44, facecolor=WHITE, edgecolor=AMBER_E,
                         linewidth=pt(2.4), zorder=3))
    txt(cx, cy, "U", 22, AMBER_E, bold=True)
    txt(lx, ly, label, 17, MUTED)

# ---------------- 7. flow arrows ----------------
for x1, x2 in [(230, 265), (295, 330), (535, 570), (600, 635), (890, 925), (955, 1005)]:
    arrow(x1, 325, x2, 325, INK, 2.6)
arrow(1100, 301, 1140, 272, GREEN_E, 3.1, ms=15)     # D -> normal return
arrow(1052.5, 375, 1090, 541, PINK_E, 3.1, ms=15)    # D -> H
arrow(1118, 541, 1140, 541, PINK_E, 3.1, ms=15)      # H -> review pen
arrow(1295, 615, 1295, 662, PINK_E, 2.6, ms=13)      # manual handling exit

txt(1310, 634, "separate manual\nhandling exit", 14, MUTED, ha="left")

# ---------------- 8. legend ----------------
txt(50, 691, "G0–G2  separating gates with process interlocks     "
             "D  guiding diversion boundary; never pushes the animal",
    16, MUTED, ha="left")
txt(50, 726, "H  review-pen entry gate     "
             "U-*  ultrasonic occupancy / passage points (planning configuration)",
    16, MUTED, ha="left")
txt(50, 769, "Antenna mounted outside the head/ear zone. "
             "Not to scale; final dimensions follow the on-farm survey.",
    16, MUTED, ha="left", italic=True)

OUT = "/Users/Admin/Documents/大三上/E&L/Coursework 1 - resources-20261009/08_组员资料/成员4_Part4_交付/figures/fig_R10_layout.png"
fig.savefig(OUT, dpi=DPI, facecolor="white")
print("saved:", OUT)
