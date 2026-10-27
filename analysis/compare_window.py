"""Same hours (14:30-16:30), different days: same panel, same position, only the weather changes.

Power is estimated from short-circuit current: P = Isc / Isc_STC * P_rated
(panel label: P_rated = 20 Wp, Isc_STC = 1.20 A).
"""
import csv, glob, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

P_RATED, ISC_STC = 20.0, 1.20
WINDOW = ["14:30", "14:45", "15:00", "15:15", "15:30", "15:45", "16:00", "16:15", "16:30"]
WEATHER = {"2026-10-25": "Sun 25 Oct · overcast, rain",
           "2026-10-26": "Mon 26 Oct · overcast, dry",
           "2026-10-27": "Tue 27 Oct · clear sky"}
COLORS = {"2026-10-25": "#2a78d6", "2026-10-26": "#eb6834", "2026-10-27": "#1baf7a"}
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
OUT = os.path.join(HERE, "..", "figures", "same_hours_comparison.png")
INK, INK2, GRID, BG = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"

h = [int(t[:2]) + int(t[3:]) / 60 for t in WINDOW]
fig, ax = plt.subplots(figsize=(8, 4.2), dpi=200)
fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
print(f"{'date':<12}{'mean Isc mA':>12}{'energy Wh':>11}")
for path in sorted(glob.glob(os.path.join(DATA, "*.csv"))):
    rows = {r["time"]: (r["date"], float(r["isc_A"])) for r in csv.DictReader(open(path))}
    if not all(t in rows for t in WINDOW):
        continue
    date = rows[WINDOW[0]][0]
    p = [rows[t][1] / ISC_STC * P_RATED for t in WINDOW]
    e = sum((p[k] + p[k + 1]) / 2 * (h[k + 1] - h[k]) for k in range(len(p) - 1))
    print(f"{date:<12}{sum(rows[t][1] for t in WINDOW) / len(WINDOW) * 1000:>12.1f}{e:>11.2f}")
    ax.plot(h, p, color=COLORS.get(date, "#6250d6"), lw=2, marker="o", ms=4.5, mec=BG, mew=1.2, zorder=3)
    ax.text(h[0] - 0.04, p[0], f"{WEATHER.get(date, date)}\n{e:.2f} Wh in window",
            ha="right", va="center", fontsize=7.5, color=INK)
ax.set_xlim(13.3, 16.65); ax.set_ylim(bottom=0)
ax.set_xticks(h[::2]); ax.set_xticklabels(WINDOW[::2])
ax.set_ylabel("Estimated power (W)", color=INK2, fontsize=9); ax.set_xlabel("Time (CET)", color=INK2, fontsize=9)
for s in ["top", "right"]: ax.spines[s].set_visible(False)
for s in ["left", "bottom"]: ax.spines[s].set_color(GRID)
ax.tick_params(colors=INK2, labelsize=8); ax.grid(axis="y", color=GRID, lw=0.8); ax.set_axisbelow(True)
fig.suptitle("Same hours, different days · 14:30–16:30", x=0.07, ha="left", fontsize=11, color=INK, y=0.98)
ax.set_title("20 Wp panel, same position behind a west-facing roof window · P ≈ Isc / 1.20 A × 20 W (estimate)",
             loc="left", fontsize=8, color=INK2)
plt.tight_layout(); plt.savefig(OUT, facecolor=BG)
