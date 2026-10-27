"""Tuesday 27 Oct: the full logged day, sunrise to sunset.

Power estimated from short-circuit current: P = Isc / 1.20 A * 20 W.
Gap 12:45-14:30: the recording stopped and the panel was used for the charging tests (R6, R7).
Before 09:24 the meter was on the 10 A range (0.01 A resolution), so those points are coarse.
"""
import csv, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

P_RATED, ISC_STC = 20.0, 1.20
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "data", "2026-10-27_tue.csv")
OUT = os.path.join(HERE, "..", "figures", "tuesday_full_day.png")
INK, INK2, GRID, BG, C = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb", "#1baf7a"

rows = list(csv.DictReader(open(SRC)))
h = [int(r["time"][:2]) + int(r["time"][3:]) / 60 for r in rows]
p = [float(r["isc_A"]) / ISC_STC * P_RATED for r in rows]
coarse = [r["range"] == "10A" for r in rows]

fig, ax = plt.subplots(figsize=(8, 4.2), dpi=200)
fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
gap_i = next(i for i in range(1, len(h)) if h[i] - h[i - 1] > 0.5)
for seg in (range(0, gap_i), range(gap_i, len(h))):
    ax.plot([h[i] for i in seg], [p[i] for i in seg], color=C, lw=2, zorder=3)
ax.scatter([h[i] for i in range(len(h)) if not coarse[i]], [p[i] for i in range(len(h)) if not coarse[i]],
           s=22, color=C, edgecolor=BG, linewidth=1.2, zorder=4)
ax.scatter([h[i] for i in range(len(h)) if coarse[i]], [p[i] for i in range(len(h)) if coarse[i]],
           s=22, facecolor=BG, edgecolor=C, linewidth=1.4, zorder=4)
ax.axvspan(h[gap_i - 1], h[gap_i], color="#f0efec", zorder=0)
ax.text((h[gap_i - 1] + h[gap_i]) / 2, 0.08, "not logged\n(charging tests)", ha="center", fontsize=7.5, color=INK2)
k = p.index(max(p))
ax.annotate(f"peak {p[k]:.2f} W at {rows[k]['time']}", (h[k], p[k]), xytext=(h[k] + 0.4, p[k] + 0.05),
            fontsize=8, color=INK, arrowprops=dict(arrowstyle="-", color=INK2, lw=0.8))
ax.text(7.05, 0.95, "open points: 10 A range (coarse)", fontsize=7.5, color=INK2)
ax.set_xlim(6.8, 17); ax.set_ylim(0, 1.15)
ax.set_xticks(range(7, 18)); ax.set_xticklabels([f"{x}:00" for x in range(7, 18)])
ax.set_ylabel("Estimated power (W)", color=INK2, fontsize=9); ax.set_xlabel("Time (CET)", color=INK2, fontsize=9)
for s in ["top", "right"]: ax.spines[s].set_visible(False)
for s in ["left", "bottom"]: ax.spines[s].set_color(GRID)
ax.tick_params(colors=INK2, labelsize=8); ax.grid(axis="y", color=GRID, lw=0.8); ax.set_axisbelow(True)
fig.suptitle("A full day · Tue 27 Oct 2026 · clear sky", x=0.07, ha="left", fontsize=11, color=INK, y=0.98)
ax.set_title("20 Wp panel behind a west-facing roof window · P ≈ Isc / 1.20 A × 20 W (estimate)",
             loc="left", fontsize=8, color=INK2)
plt.tight_layout(); plt.savefig(OUT, facecolor=BG)
