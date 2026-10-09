# JOBO drum mount for the THD CP-Lift

> [!WARNING]
> **Experimental, work in progress.** This part is still being developed and has no release yet. The geometry may change, and it has not been strength-checked. Print and use it at your own risk.

⬇️ **Download:** [Mount](https://github.com/sasha-nordiclab/thd-cp-lift-parts/raw/main/drum-mount/step/JoboDrumMount_Mount.step) · [Lock](https://github.com/sasha-nordiclab/thd-cp-lift-parts/raw/main/drum-mount/step/JoboDrumMount_Lock.step) · [FreeCAD model](https://github.com/sasha-nordiclab/thd-cp-lift-parts/raw/main/drum-mount/cad/JoboDrumMount.FCStd)

A two-part mount that holds a JOBO drum on the THD CP-Lift:
- **Mount** — an 80 × 80 mm plate with locating rings, a Ø 24 mm centre bore and a pocket for the motor.
- **Lock** — a sliding latch with a printed spring. To release the drum, pull the finger ears; the spring pushes the latch back. Travel is 3.5 mm.

| Part | Size | Print (PETG, see below) |
|---|---|---|
| Mount | 80 × 80 × 19 mm | ≈ 2 h, 60 g (40 % infill) / 85 g (solid) |
| Lock | 45 × 34 × 13 mm | ≈ 25 min, 8 g |

## Files

| Path | What |
|---|---|
| `cad/JoboDrumMount.FCStd` | Parametric FreeCAD model: bodies `Mount` and `Lock`, the final `LockMirror` feature, and an assembly that shows how they fit |
| `step/JoboDrumMount_Mount.step` | Mount |
| `step/JoboDrumMount_Lock.step` | Lock, exported from `LockMirror` |

## Printing

- Both parts print flat on their largest face, with no supports.
- PETG, 0.4 mm nozzle, 0.6 mm line width, 0.2 mm layers, 5 walls.
- The times above are from OrcaSlicer on a Bambu Lab A1. The Mount at 40 % cubic is enough for normal use; print it solid if you want it stiffer.

## Assembly

- **Mount to the lift:** three screws through Ø 4.5 mm holes with Ø 8 mm counterbores, 4.4 mm deep. M4 cap screws fit.
- **Lock to the Mount:** two screws through the Lock's slots into Ø 2.9 mm pilot holes in the Mount. M3 screws tap into them.

## Parameters

All sizes are in the spreadsheet `Params`. Cells starting with `D_` are derived; do not edit them.

| Parameter | Default | Meaning |
|---|---|---|
| `PLATE_W`, `PLATE_T`, `PLATE_R` | 80, 5, 3 | plate width, thickness, corner radius |
| `RING_OD`, `RING_ID`, `RING_H` | 39, 34, 7 | locating ring |
| `RING2_OD`, `RING2_H` | 26, 3 | inner ring |
| `BORE_D` | 24 | centre bore |
| `RECESS_D`, `FRAME_H` | 50, 12 | drum recess diameter, frame height |
| `MOTOR_OFS`, `MOTOR_POCKET_R` | 31.5, 11 | motor pocket position and radius |
| `HOLE_OFS`, `HOLE_D`, `HOLE_CB_D`, `HOLE_CB_DEPTH` | 30, 4.5, 8, 4.4 | mounting holes |
| `SLOT_W`, `LOCK_CLR`, `LOCK_TRAVEL` | 35, 0.3, 3.5 | lock slot width, clearance, travel |
| `SPRING_T`, `SPRING_PRE` | 1.3, 0.5 | spring strip thickness, preload |
| `LOCK_SCREW_PITCH`, `LOCK_SCREW_HOLE_D` | 25, 2.9 | lock screws |

## License

[CC BY-NC-SA 4.0](../LICENSE).
