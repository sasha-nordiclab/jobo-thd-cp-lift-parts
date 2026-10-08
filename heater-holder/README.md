# THD heater holder — PETG clamp

A two-part clamp that holds the 220 V THD bath heater horizontally on the bath floor. The base is glued to the floor. The cap is pulled down onto the soft rubber head of the heater by two M4 screws. The clamp has no snap, so thermal swell of the head or the plastic does not matter.

## Model

**Working model:** [THD_Heater_Holder.FCStd](cad/THD_Heater_Holder.FCStd), rebuilt from scratch with `python3 scripts/build.py` (fdmkit over RPC). All sizes are in the `params` spreadsheet.

- Body **Heater**: a reference mock-up. The rod is Ø16 × 110, the rubber head Ø20 × 20.
- Body **Base**: glued to the floor, with a half-round bed for the head.
- Body **Cap**: a half ring with two ears.
- **Screw** is an M4 × 16 ISO 14581 (countersunk Torx) from the Fasteners workbench. **Screw_Mirror** is an `App::Link` to it.

### How the model is built

Each part is built from features centred on the heater axis, plus one side (+Y): the ear, the screw hole and the pilot hole. A single PartDesign **Mirrored** across the XZ plane then makes the −Y side. To change a hole or an ear, edit the +Y feature; the mirror follows.

| Base | Cap |
|---|---|
| `b_block`: the block, symmetric | `k_ring`, `k_trim`, `k_bore`: the half ring, symmetric |
| `b_bed`: the half-round bed | `k_ear`: the +Y ear, with the R`k_er` round |
| `b_pilot`: the +Y octagonal pilot hole | `k_oct`, `k_hole`: the +Y octagon and the countersink (PartDesign Hole) |
| `b_mirror`: mirrors the pilot to −Y | `k_mirror`: mirrors the ear and its holes to −Y |
| `b_bed_chamfer`, `b_top_chamfer`: end-face chamfers | `k_bed_chamfer`, `k_top_chamfer`: end-face chamfers |

Every sketch is fully constrained, and every size comes from the `params` spreadsheet. Change a value there and recompute. Checked with a 24 mm head, a 25 mm head length, an 18 mm axis height, and 54 mm wide ears.

### Coordinates

- z = 0 is the bath floor, which is also the base's glue face.
- The heater axis runs along X at `ax_z` = 15 mm.
- x = 0 is the joint between head and rod. The head is at x −20…0, the rod at x 0…110.

### Clamp

| | |
|---|---|
| Length along the axis | `c_len` = the full head length, 20 mm |
| Bore | Ø19.8 (`c_fit` 0.2 undersize), split at the axis with a `k_gap` 0.6 mm gap |
| Base | a solid block, 46 × 20 mm on the floor and 14.7 mm high, with a half-round bed |
| Cap | a half ring, 3 mm wall, with two flat 6 mm ears |
| Screws | 2 × M4 × 16 ISO 14581, 304 stainless, at ±16.5 mm. The heads sit flush in 90° countersinks (Ø9.6) |
| Thread | the screws form their own thread in octagonal blind pilot holes in the base: 3.5 mm across flats, 12 mm deep. The screw bites into the flats, and the corners take the chips. Engagement is 9.4 mm |

Tightening the screws closes the gap, so the rubber head is squeezed by about 0.8 mm in height.

The heater bottom is 5 mm above the floor and the rod bottom 7 mm, so water flows under the rod.

## Files

- [cad/THD_Heater_Holder.FCStd](cad/THD_Heater_Holder.FCStd) is the parametric model.
- [`step/`](step/) holds the STEP files of the base and the cap.
- [scripts/build.py](scripts/build.py) rebuilds the model in a running FreeCAD through fdmkit.

## Print

PETG, profile "0.20mm NordicLab 0.6 Ballance", 100 % zig-zag, Bambu A1:

| Part | Orientation | Time | Mass |
|---|---|---|---|
| Base | on its end face x = −20 (profile on the bed) | 32 min 9 s | 12.9 g |
| Cap | on its end face x = −20 (profile on the bed) | 21 min 50 s | 5.3 g |

Every edge of both end faces has a chamfer: 1.2 mm along the print vertical at 30° from vertical, so 0.69 mm on the face (`e_h`, `e_a`). On the bed face it prevents elephant foot. The outer top edges of the cap ears are rounded with R1.5 (`k_er`); they run along the print vertical.

All screw holes are octagons, with a flat facing up in the end-face print: a short bridge (< 2 mm) on top and 45° sides. The cap clearance holes are 4.5 mm across flats. The upper part of the 90° countersink is 45° from vertical, which is slightly over the 40° limit, but it is only about 2.5 mm deep.
