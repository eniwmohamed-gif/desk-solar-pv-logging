"""Turn logged short-circuit current (Isc) into estimated power, daily energy and a production chart.

Method: Isc is proportional to irradiance, so P(t) ~= Isc(t) / Isc_STC * P_rated.
Panel label (STC: 1000 W/m2, AM1.5, 25 C): P_rated = 20 Wp, Isc_STC = 1.20 A.
"""
import csv, glob, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

P_RATED, ISC_STC, G_STC = 20.0, 1.20, 1000.0
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
OUT = os.path.join(HERE, "..", "figures", "production_curve.png")
COLORS = ["#2a78d6", "#eb6834", "#1baf7a"]  # one fixed hue per day

def load(path):
    rows = list(csv.DictReader(open(path)))
    t = [int(r["time"][:2]) + int(r["time"][3:]) / 60 for r in rows]
    isc = [float(r["isc_A"]) for r in rows]
    return rows[0]["date"], t, isc

def energy_wh(t, p):
    return sum((p[k] + p[k + 1]) / 2 * (t[k + 1] - t[k]) for k in range(len(p) - 1))

fig, ax = plt.subplots(figsize=(8, 4.2), dpi=200)
print(f"{'date':<12}{'peak A':>8}{'peak W':>8}{'peak W/m2':>11}{'energy Wh':>11}")
for i, path in enumerate(sorted(glob.glob(os.path.join(DATA, "*.csv")))):
    date, t, isc = load(path)
    p = [x / ISC_STC * P_RATED for x in isc]
    k = p.index(max(p))
    e = energy_wh(t, p)
    print(f"{date:<12}{isc[k]:>8.3f}{p[k]:>8.2f}{isc[k]/ISC_STC*G_STC:>11.0f}{e:>11.1f}")
    ax.plot(t, p, color=COLORS[i % 3], lw=2, marker="o", ms=4, label=f"{date}  ({e:.1f} Wh)")
ax.set_xlabel("Time (CET)"); ax.set_ylabel("Estimated power (W)"); ax.set_ylim(bottom=0)
ax.grid(axis="y", color="#e4e3df"); ax.spines[["top", "right"]].set_visible(False)
ax.legend(frameon=False, fontsize=8)
ax.set_title("Estimated PV output, 20 Wp panel behind a west-facing roof window", loc="left", fontsize=10)
plt.tight_layout(); plt.savefig(OUT)
