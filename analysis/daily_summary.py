"""Summary of every logged day: peak current, estimated peak power and irradiance, energy over the logged span."""
import csv, glob, os

P_RATED, ISC_STC, G_STC = 20.0, 1.20, 1000.0
DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")

print(f"{'date':<12}{'logged':>14}{'peak':>16}{'peak W':>8}{'W/m2':>7}{'energy Wh':>11}")
for path in sorted(glob.glob(os.path.join(DATA, "*.csv"))):
    rows = list(csv.DictReader(open(path)))
    t = [int(r["time"][:2]) + int(r["time"][3:]) / 60 for r in rows]
    isc = [float(r["isc_A"]) for r in rows]
    p = [x / ISC_STC * P_RATED for x in isc]
    k = p.index(max(p))
    e = sum((p[i] + p[i + 1]) / 2 * (t[i + 1] - t[i]) for i in range(len(p) - 1))
    span = f"{rows[0]['time']}-{rows[-1]['time']}"
    peak = f"{isc[k]*1000:.0f} mA @ {rows[k]['time']}"
    print(f"{rows[0]['date']:<12}{span:>14}{peak:>16}{p[k]:>8.2f}{isc[k]/ISC_STC*G_STC:>7.0f}{e:>11.1f}")
