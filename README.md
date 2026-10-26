# Desk-Scale Solar + Battery System: Measuring Real PV Output

I'm a first-year Energy Systems Engineering student at Deggendorf Institute of Technology (THD) in Germany. I built this small off-grid system to see with my own instruments what the textbook says about solar PV: how much a real panel produces through a real day, how much the weather changes that, and why a system needs storage.

A 20 Wp solar panel, a PWM charge controller and a 12 V AGM battery, built and measured over three days (25–27 Oct 2026) in Passau, Germany. The panel's short-circuit current was logged every 15 minutes to estimate how much energy it produces through a real day.

![Wiring diagram](figures/wiring_diagram.png)

## System

| # | Part | Key specs |
|---|---|---|
| 1 | Nicesolar monocrystalline panel | 20 Wp ±5%, Voc 22.0 V, Vmp 18.0 V, Isc 1.20 A, Imp 1.11 A (STC) |
| 2 | AstroAI AM33D multimeter | V DC, A DC (10 A and 200 mA ranges) |
| 3 | Greencell Cube battery | 12 V, 7.2 Ah, AGM VRLA |
| 4 | Nicesolar PWM charge controller | 12/24 V, 10 A, USB output, set to lead-acid (b01) |
| 5 | Inline fuse | 5 A on battery + |
| 6 | USB fan | load |

**Connection order:** battery → panel → load. Disconnect in reverse.

## Method

1. **Open-circuit voltage (Voc)** measured once with the multimeter as a voltmeter.
2. **Short-circuit current (Isc)** logged continuously: the multimeter on a current range (10 A, or 200 mA for weak light) shorts the panel, and a laptop camera recorded the display. Readings were taken from the video every 15 minutes.
3. **Isc is proportional to irradiance**, so power is estimated as:

```
P(t) ≈ Isc(t) / Isc,STC × 20 W          (Isc,STC = 1.20 A)
G(t) ≈ Isc(t) / Isc,STC × 1000 W/m²
Energy = ∫ P dt   (trapezoidal rule)
```

Equivalent view: P = FF × Voc × Isc, with fill factor FF = (18.0 × 1.11) / (22.0 × 1.20) ≈ 0.76.

**Setup:** panel fixed behind the glass of a west-facing roof window (azimuth 284°), not moved during logging.

## Results

### Same hours, different days (14:30–16:30)

Same panel, same position, same clock window: only the weather changes. Both days were overcast; the difference is the rain. Weather from the Apple Weather app (Passau, recorded conditions).

![Same-hours comparison](figures/window_comparison.png)

| Day | Weather | Mean Isc | Energy 14:30–16:30 |
|---|---|---|---|
| Sun 25 Oct | Overcast, rain from late morning to ~17:00 (high 10 °C) | 9.4 mA | 0.32 Wh |
| Mon 26 Oct | Overcast, dry, 0% rain (high 12 °C) | 35.0 mA | 1.17 Wh (≈ 3.6× Sunday) |
| Tue 27 Oct | | | |

### Everything logged

![Production curve](figures/production_curve.png)

| Day | Logged | Peak | Energy (logged window) |
|---|---|---|---|
| Sun 25 Oct | 11:15–16:30 | 0.05 A at 12:45 (≈ 0.83 W, ≈ 42 W/m²) | ≈ 2.0 Wh |
| Mon 26 Oct | 14:30–17:00 | 62 mA at 14:30 (≈ 1.03 W, ≈ 52 W/m²) | ≈ 1.2 Wh |
| Tue 27 Oct | | | |

**Spot readings**

| ID | Measurement | Value |
|---|---|---|
| R1 | Battery voltage at rest | 12.94 V |
| R2 | Battery voltage on controller display | 12.7 V |
| R3 | Battery voltage with fan running | 12.68 V |
| R4 | Panel Voc (overcast, behind glass) | 21.8 V (99% of rated) |
| R5 | Panel Isc (same conditions) | 0.04 A (3% of rated) |

## Observations

The comparison window is 14:30–16:30 because that is the span both days cover (Sunday's log ends at 16:30; Monday's starts at 14:30).

- Under heavy overcast, **voltage stayed at 99% of rated while current fell to ~3%**: light intensity drives current, not voltage.
- On the overcast day the peak came around midday: diffuse light makes the window's orientation matter less.
- Battery voltage dropped 0.26 V under the fan load (internal resistance).

## What I learned

- **Voltage is not the story, current is.** I expected a dark, rainy day to "turn the panel off". The voltage barely moved; the current, and with it the power, collapsed to a few percent.
- **Compare like with like.** Comparing the same clock hours on different days isolates the weather. Same panel, same window, same hours: Monday gave about 3.6× the energy of Sunday.
- **Solar output swings from one day to the next, so storage matters.** On an overcast day a 20 W panel made about 2 Wh. A battery turns that uneven daytime supply into energy I can use whenever I need it. At grid scale, that is exactly the role of storage and flexibility in a renewable energy system.
- **Range choice is a trade-off.** The 10 A range is safe for full sun but only resolves 0.01 A; the 200 mA range resolves 0.1 mA but saturates in bright light. I used 200 mA for weak light and 10 A when the sun could get strong.

## Next steps

- Log a full clear day from sunrise to sunset (Tuesday 27 Oct).
- Measure real power under load (voltage and current at the same time) instead of estimating it from Isc.
- Repeat with the panel outside and facing south, and compare with the window results.

## Limitations

- Power is **estimated** from Isc, not measured at the maximum power point; real output in weak light is slightly lower.
- 10 A range resolution is 0.01 A, so low-light readings are coarse (switched to the 200 mA range on 25 Oct from 14:51).
- Panel is behind window glass (~10–15% loss) and faces west, not south.

## Reproduce

```bash
pip install matplotlib
python analysis/plot_production.py   # all logged data -> figures/production_curve.png
python analysis/compare_window.py    # 14:30-16:30 per day -> figures/window_comparison.png
```

Data: `data/*.csv` (columns: `date, time, isc_A, range, source`).

## Credits

Built and measured by Mohamed Eniw, B.Eng. Energy Systems Engineering student, Deggendorf Institute of Technology (THD).
The analysis script and figures were prepared with the help of an AI assistant (Claude); all measurements were taken by hand.
