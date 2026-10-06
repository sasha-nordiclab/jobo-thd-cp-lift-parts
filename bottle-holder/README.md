# THD CP-Lift bottle holder

An optimised redesign of the bottle holder, reworked for the THD CP-Lift. It holds **four standard JOBO bottles** in the water bath.

- It mounts with stainless steel countersunk screws through the 3 mm bath wall. A printed nut bar on the outside of the bath holds the nuts.
- Each module holds two bottles. Print one **Module**, one **Module mirrored**, two **Nut bars** (PETG) and four **Seals** (TPU).

▶ **Videos:** [YouTube playlist](https://www.youtube.com/playlist?list=PLADhkNYpSGAc)

| | Per module |
|---|---|
| Size | 120.4 × 159.5 × 73.5 mm |
| Bottle opening | 93.4 × 71.4 mm, corner radius 4 mm (×2) |
| Mounting | 2 × M4 × 20 countersunk Torx screws (304 stainless) + 2 nuts in a nut bar |
| Material | PETG |
| Mass / print time | ≈ 126 g / ≈ 3 h (solid, see [Printing](#printing)) |

## Files

| Path | What |
|---|---|
| `cad/THD_CP_Lift_Bottle_Holder.FCStd` | Parametric FreeCAD model: bodies `Module` and `Nut bar`, plus their mirrors |
| `step/THD_CP_Lift_Holder_Module.step` | Module, for slicing or other CAD |
| `step/THD_CP_Lift_Holder_Module_Mirrored.step` | Mirrored module |
| `step/THD_CP_Lift_Nut_Bar.step` | Nut bar; print two, the same part fits both modules |
| `step/THD_CP_Lift_Seal_TPU.step` | Seal for each bath hole; print four in TPU 95A |
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

**Per module you need:**
- 2 × **M4 × 20 countersunk Torx screws**, 304 stainless (ISO 14581, 90° head Ø 8.4 mm). They fit the Ø 9.2 mm countersink.
- 2 × **M4 nuts** ISO 4032, stainless.
- 1 × **printed nut bar**.
- 2 × **TPU seals** (under the nut bar).

The screws go in from the bottle side, through the holder and the bath's Ø 6.6 mm holes. The nuts sit in the hex pockets of the nut bar on the outside of the bath.

**The stack along the screw:**

| Part of the stack | mm |
|---|---|
| Head top to the holder's mounting face | 4.0 |
| Bath wall | 3.0 |
| Nut bar under the nut | 8.9 |
| Nut ISO 4032, flush in its pocket | 3.2 + 0.2 |
| Screw tip past the nut | 0.9 |
| **Total** | **20** |

The nut bar is sized to the screw. `bolt_len` in the spreadsheet sets the screw length, and the bar thickness follows (12.3 mm for M4 × 20, at least 5.4 mm). The tip then ends just past the nut and does not stick out behind the bath; `bolt_tip` shows the overhang.

- **Sealing the bath holes.** A printed TPU 95A seal goes on each screw on the outside of the bath, under the nut bar, so water does not leak out through the holes.
  - The Ø 15.9 × 1.4 mm flange fills an Ø 16 × 1.0 mm groove on the bath side of the nut bar.
  - Tightening squeezes the flange by 0.4 mm. The groove walls stop it from spreading outwards, so the TPU is pushed inwards and closes its Ø 4.2 mm bore onto the M4 screw.
  - The Ø 6.3 mm sleeve goes into the bath's Ø 6.6 mm hole from outside.
  - The holder itself has no groove, so its strength check is unchanged. The bath pressure is tiny (0.01–0.02 bar).
  - Print the seals flange down, 100 % infill.
- The bath holes are a standard M6 clearance (6.6 mm). The M4 screws have play in them, but the countersunk heads and the nut bar hold everything in place.
- The rear face of the holder is tilted 7.5° to sit flat on the bath wall.
- Each bottle's side rib catches the ledge under the front of the frame, so a floating bottle cannot lift out.
- The nut bar has a through slot between the nuts, so material stays only where the nuts press; `slot_w` and `slot_off` set it.
- Print the nut bar flat, bath side down, with the pockets facing up: about 40 min and 17 g. It is 20 mm wide to carry the seal grooves.

## Adapting it to other bottles

Open the model in FreeCAD and edit the spreadsheet `params`. Everything else, including the nut bar, follows these five values:

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
- **Nut bar:** bath wall, nut size, bar thickness and width, plus the screw length `bolt_len`.

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
