# THD CP-Lift bottle holder

A 3D-printable holder for 600 ml square chemistry bottles. It screws to the wall of a THD CP-Lift and holds the bottles in the water bath.

Each module holds two bottles. Print one **Module** and one **Module mirrored**; together they hold four bottles.

| | Per module |
|---|---|
| Size | 120.4 × 159.5 × 73.5 mm |
| Bottle opening | 93.4 × 71.4 mm, corner radius 4 mm (×2) |
| Mounting | 2 × M4 countersunk screws |
| Material | PETG |
| Mass / print time | ≈ 126 g / ≈ 3 h (solid, see [Printing](#printing)) |

## Files

| Path | What |
|---|---|
| `cad/THD_CP_Lift_Bottle_Holder.FCStd` | Parametric FreeCAD model: one body `Module` plus its mirror `Module mirrored` |
| `step/THD_CP_Lift_Holder_Module.step` | Module, for slicing or other CAD |
| `step/THD_CP_Lift_Holder_Module_Mirrored.step` | Mirrored module |
| `docs/strength.md` | How the part was checked and why it looks the way it does |
| `scripts/fem/` | The strength calculation (CalculiX), for the default size |

## Printing

- **Orientation:** frame face down on the bed. The top face is flat, and nothing is steeper than 40° except the small screw countersinks. No supports are needed.
- **Profile:** PETG, 0.4 mm nozzle, 0.6 mm line width, 0.2 mm layers, 5 walls.
- **Infill:** **100 %, rectilinear (zig-zag).**
  - The walls are 1.8–3 mm thick and the strength check assumes solid plastic.
  - 5 walls of 0.6 mm fill the 3 mm walls exactly, and 100 % infill makes the 3.6 mm frame solid.
  - On thin-walled parts like this, 100 % rectilinear was faster than 40 % cubic.
- **Result:** in OrcaSlicer on a Bambu Lab A1, about 3 h 05 min and 126 g per module.

## Mounting

- Two M4 countersunk screws per module (ISO 10642 / DIN 7991). Insert them from the bottle side; the countersink is 90°, Ø 9.2 mm.
- Choose the screw length to suit your wall. Tighten the screws; the strength check assumes a clamped joint.
- The rear face is tilted 7.5° to sit flat on the lift wall.
- Each bottle's side rib catches the ledge under the front of the frame, so a floating bottle cannot lift out.

## Adapting it to other bottles

Open the model in FreeCAD and edit the spreadsheet `params`. Everything else follows these five values:

| Parameter | Default | Meaning |
|---|---|---|
| `open_x` | 93.4 | bottle opening, rear to front |
| `open_y` | 71.4 | bottle opening, side to side |
| `open_r` | 4 | opening corner radius |
| `web_h` | 70.5 | depth of the side walls below the frame |
| `lip_h` | 18 | depth of the front wall |

What follows automatically:
- the bay pitch, module length, frame, recesses, screw positions and the mirror;
- recesses switch themselves off when their zone gets too small;
- the screws keep clear of the walls.

**Other parameter groups in `params`:**
- **Build:** wall and frame thickness, gaps.
- **Mount:** wall tilt, screw positions, bosses.
- **Lightening:** recess depths (0 = none).

Do not edit the **Derived** cells.

These sizes were rebuilt and checked: 50 × 40 / 35 mm, 60 × 45 / 45 mm, 75 × 60 / 60 mm, 100 × 80 / 80 mm, and 2.4 mm walls. In every case the result is one valid solid with clear screw holes. **Strength was calculated only for the default size**; check yours before relying on it.

The model was made with a FreeCAD 26.3 development build. Older FreeCAD releases may not open it; the STEP files work anywhere.

## Strength

Checked by finite elements (CalculiX) with real supports:
- the screw heads clamp the countersinks;
- the rear wall can push on the lift wall but not pull;
- the material is treated as layered PETG, so layers can peel apart.

Loads:
- floating empty bottles, sustained, safety factor 4;
- a full 0.7 kg bottle knocked into the part at 0.5 m/s, safety factor 2.

| Load case | Load / allowable |
|---|---|
| Floating bottles (sustained) | 0.86 ✅ |
| Bottle hits the frame from above | 1.98 |
| Bottle hits the front edge | 1.15 |
| Bottle hits the divider sideways | 1.73 |

- A value of 1.0 or less passes with the full safety factor.
- Values up to about 2 mean a careless knock is close to the material's limit. They occur at the top screw (layers peeling) and at the corner of the opening.
- The front ledge and overall layout come from a holder that is already in use.

Details, the design changes and rejected variants are in [docs/strength.md](docs/strength.md).

## License

[CC BY-NC-SA 4.0](../LICENSE): you may share and adapt this design with attribution, not for commercial use, and under the same license.
