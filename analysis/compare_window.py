"""Compare the same clock window (14:30-16:30) across days: same panel, same position, only the weather changes."""
import csv, glob, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

P_RATED, ISC_STC = 20.0, 1.20
WINDOW = ["14:30", "14:45", "15:00", "15:15", "15:30", "15:45", "16:00", "16:15", "16:30"]
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
OUT = os.path.join(HERE, "..", "figures", "window_comparison.png")
COLORS = ["#2a78d6", "#eb6834", "#1baf7a"]

h = [int(t[:2]) + int(t[3:]) / 60 for t in WINDOW]
fig, ax = plt.subplots(figsize=(8, 4.2), dpi=200)
print(f"{'date':<12}{'mean Isc mA':>12}{'energy Wh':>11}")
for i, path in enumerate(sorted(glob.glob(os.path.join(DATA, "*.csv")))):
    rows = {r["time"]: (r["date"], float(r["isc_A"])) for r in csv.DictReader(open(path))}
    if not all(t in rows for t in WINDOW):
        continue
    date = rows[WINDOW[0]][0]
    p = [rows[t][1] / ISC_STC * P_RATED for t in WINDOW]
    e = sum((p[k] + p[k + 1]) / 2 * (h[k + 1] - h[k]) for k in range(len(p) - 1))
    print(f"{date:<12}{sum(rows[t][1] for t in WINDOW) / len(WINDOW) * 1000:>12.1f}{e:>11.2f}")
    ax.plot(h, p, color=COLORS[i % 3], lw=2, marker="o", ms=4, label=f"{date}  ({e:.2f} Wh)")
ax.set_xticks(h[::2]); ax.set_xticklabels(WINDOW[::2]); ax.set_ylim(bottom=0)
ax.set_xlabel("Time (CET)"); ax.set_ylabel("Estimated power (W)")
ax.grid(axis="y", color="#e4e3df"); ax.spines[["top", "right"]].set_visible(False)
ax.legend(frameon=False, fontsize=8)
ax.set_title("Same hours (14:30-16:30), different days", loc="left", fontsize=10)
plt.tight_layout(); plt.savefig(OUT)
