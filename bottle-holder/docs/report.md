# THD CP-Lift bottle holder — design report

Revision: 2026-10-06. Covers the bottle holder, its mounting (nut bar, TPU gasket, screws) and the checks behind each decision.

![Assembled module, seen from the bath side](img/assembled.png)

## 1. Summary

**What it is.** A printed holder for **four standard JOBO bottles** in the water bath of the THD CP-Lift.
- It is made of two modules: a **Module** and its mirror image. Each holds two bottles.
- Each module screws through the 3 mm bath wall with two stainless countersunk screws.
- On the outside of the bath, a printed **nut bar** holds the nuts and a **TPU gasket** seals the holes.

**Key numbers per module:**

| | |
|---|---|
| Size | 120.4 × 159.5 × 73.5 mm |
| Holder | 102.6 cm³, ≈ 126 g PETG, ≈ 3 h 05 min (solid) |
| Nut bar | 101.5 × 14 × 11.3 mm, ≈ 11 g PETG, ≈ 32 min |
| Gasket | 1 mm TPU 95A, ≈ 1 g |
| Hardware | 2 × M4 × 20 countersunk Torx (304 stainless), 2 × M4 nut ISO 4032 |
| Strength (load / allowable, ≤ 1 passes) | floating bottles **0.31** ✅; knocks by a full bottle 1.08–1.75 (see §5) |

## 2. How it works

![Exploded view: holder, bath wall, TPU gasket, nut bar, nuts](img/exploded.png)

[Explode animation](img/exploded.mp4)

**Holding the bottles.**
- Each bottle drops through a rounded opening in the top frame.
- Its side rib catches a ledge under the front edge of the frame.
- An empty or half-full bottle floats in the bath. Buoyancy pushes the rib up against the ledge, so the bottle cannot lift out.

**Carrying the load into the bath wall.**
- The holder is a shelf hanging on the bath wall. The bottle loads push the front down or up, and that creates a moment at the wall.
- The moment is carried in two ways: the two screws near the top hold the holder against the wall, and the rear face bears on the wall over its whole height.
- The rear face is one flat surface tilted 7.5°, the same angle as the bath wall, from the bottom of the holder to the top of the frame. The holder therefore bears on the bath wall everywhere and never rocks on an edge.

**The screw joint.** The parts along each screw, from the inside of the bath to the outside:
1. **Screw head.** A countersunk head sits in a 90° Ø 9.2 mm countersink in a teardrop-shaped boss on the holder's rear wall. The boss spreads the screw load downwards, away from the thin wall.
2. **Holder rear wall.** About 4.4 mm of plastic along the screw.
3. **Bath wall.** 3 mm thick, with Ø 6.6 mm holes (M6 clearance). The M4 screw has play there; the clamped joint, not the hole, holds the position.
4. **TPU gasket.** 1 mm thick, the same outline as the nut bar. Its sleeves fill the bath holes from outside, and tightening squeezes it flat against the bath, which seals the holes.
5. **Nut bar.** A PETG bar with hex pockets for the nuts. It spreads the clamp over the bath wall, bridges the Ø 6.6 mm holes and holds the nuts while the screws are turned. A slot between the nuts removes material that carries no load.
6. **Nut.** An M4 ISO 4032 nut, flush in its pocket. The screw tip ends 0.9 mm past it, so nothing sharp sticks out behind the bath.

**Mirrored modules.** The second module is a mirror image, not a copy: its screws sit at mirrored positions. In the CAD file the mirror is generated from the Module, so a change to one updates both. The nut bar and gasket are symmetric, so the same parts fit both modules.

## 3. Parts and hardware

| Part | Qty (4 bottles) | Material | Print |
|---|---|---|---|
| Module | 1 | PETG | frame face down, 5 walls, 100 % zig-zag: ≈ 3 h 05 min, 126 g |
| Module mirrored | 1 | PETG | same |
| Nut bar | 2 | PETG | bath side down, pockets up: ≈ 32 min, 11 g |
| Gasket | 2 | TPU 95A | flat, sleeves up, 100 % |
| Countersunk Torx screw M4 × 20, 304 stainless | 4 | — | — |
| Nut M4 ISO 4032, stainless | 4 | — | — |

The print times are from OrcaSlicer on a Bambu Lab A1: 0.4 mm nozzle, 0.6 mm lines, 0.2 mm layers.

## 4. Assembly

1. Push a gasket onto the outside of the bath wall, with its sleeves in the two holes.
2. Put the nuts into the hex pockets of the nut bar and hold the bar against the gasket.
3. From the bath side, put the holder against the wall and insert the screws through the holder, the bath, the gasket and the bar.
4. Tighten to about **0.5 N·m**: snug with a screwdriver, no force. See §6 for why.
5. Repeat with the mirrored module.
6. After the first warm-up of the bath, check the screws again. PETG settles slightly at 38 °C.

## 5. Strength of the holder (FEM)

**Model.**
- Second-order tetrahedra (Gmsh), solved in CalculiX. PETG: E = 2200 MPa, ν = 0.38.
- **Screws:** the countersink under each head is held fixed. A tightened screw keeps the joint closed (§6), so the seat acts as bonded.
- **Bath wall:** a rigid plate on the tilted mounting plane. The holder's rear face is in frictionless contact with it (CalculiX node-to-surface contact): the wall can push the holder but cannot pull it.
- **Failure criterion:** layered PETG, printed frame-down:

```
FI = sqrt( (σ_vM,in-plane / 40)² + (max(σ_zz, 0) / 20)² + (τ_interlayer / 15)² )    [MPa]
```

  - Strengths are reduced by 0.85 for the 38 °C bath.
  - Safety factor 4 for the sustained load, 2 for knocks.
  - The tables give the load divided by the allowable: **1.0 or less passes**.
- **Knocks:** a full 0.7 kg bottle at 0.5 m/s carries E = 87.5 N·mm. The force follows from the stiffness k at the point of impact: F = √(2 E k).

**Loads and results:**

| Case | Force | Stiffness | Deflection | Load / allowable | Where, failure mode |
|---|---|---|---|---|---|
| Floating bottles, sustained | 2 × 5.9 N up | — | 0.26 mm | **0.31** ✅ | lower rear wall below screw 2; layer peel |
| Full bottle hits the frame from above | 172 N | 169 N/mm | 1.0 mm | 1.08 | rear wall 6 mm beside screw 1; layer peel |
| Full bottle hits the front edge | 136 N | 105 N/mm | 1.3 mm | 1.17 | frame at the front edge; in-plane |
| Full bottle hits the divider sideways | 58 N | 19 N/mm | 3.0 mm | 1.75 | corner of the bottle opening; in-plane |

**What the numbers mean.**
- The sustained load uses less than a third of the allowable, so the holder does not creep in warm water.
- Knocks use part of the safety factor of 2. Even the worst one, 1.75, stays below the material strength: about 0.9 of what warm PETG takes.
- The divider is the softest place: it is a thin wall loaded sideways. A careless sideways knock is the one case to avoid.

**Check of the calculation.** For every case the forces balance:
- applied load + screw reactions + wall reaction = 0;
- the wall reaction points exactly along the wall normal (z/x = 0.1317 = tan 7.5°), as it must without friction.

The floating case stalled at 58 % of the load (one node kept flipping between touching and not touching). Frictionless contact with no initial gap is proportional to the load, so the last converged step was scaled to the full load.

**Correction to earlier results.** An earlier version of the calculation found only 204 nodes on the rear face, out of 10 743: the search tolerance was too tight and the tilt was 7.547° instead of 7.5°. The wall then held the holder on a narrow strip only, so the holder seemed much softer and weaker (hit from above 1.98, floating 0.86). With the whole face in contact, the holder is stiffer. A knock therefore produces a larger force (172 N instead of 43 N), but the stress is lower.

![Floating bottles](img/fem/story_1_buoyancy.png)
![Hit from above](img/fem/story_2_top_impact.png)
![Hit on the front edge](img/fem/story_3_front_impact.png)
![Hit on the divider](img/fem/story_4_divider_impact.png)

The pictures show the deformed shape, strongly exaggerated, over the undeformed outline. Colour shows deflection, from blue (none) to red (most). The arrows mark the load.

![Deflection envelope of all four cases](img/fem/story_5_utilisation.png)

[Animation of the four load cases](img/fem/loads_story.mp4)

All numbers: [`fem_results.json`](fem_results.json). Method in detail: [`strength.md`](strength.md).

## 6. Screw joint

**Screw length.** The stack along the screw:

| Part of the stack | mm |
|---|---|
| Head top to the holder's mounting face (ISO 14581 head, Ø 8.4 mm) | 4.0 |
| Bath wall | 3.0 |
| TPU gasket | 1.0 |
| Nut bar under the nut | 7.9 |
| Nut + pocket clearance | 3.2 + 0.2 |
| Thread past the nut | 0.9 |
| **Total** | **20 → M4 × 20** |

A 10 mm screw ends 2.7 mm past the bath wall, too short even for a bare nut. In the CAD file, `bolt_len` drives the bar thickness and `bolt_tip` shows the thread past the nut.

**Preload and bearing pressure** at 0.5 N·m (nut factor K ≈ 0.2):

| | Value |
|---|---|
| Preload F = T / (K·d) | ≈ 625 N per screw |
| Screw stress (A_s = 8.78 mm²) | 71 MPa: a small fraction of 304 stainless (≈ 450 MPa proof for A2-70) |
| Head on the countersink (Ø 6 → 8.4 mm, 27 mm²) | 23 MPa |
| Nut on the bar (hex 7 mm minus Ø 4.5, 26.5 mm²) | 24 MPa |

About 20 MPa is what PETG takes long-term at bath temperature without creeping. **Tighten gently.** Over-tightening crushes the plastic under the head and the nut and loosens the joint over time. The thickness of the bar does not change this; the pressure is set by the area under the head and the nut.

**Service loads at the screws** from the FEM:

| Case | Screw 1, axial / lateral | Screw 2, axial / lateral |
|---|---|---|
| Floating bottles | 16 / 4 N | 16 / 8 N |
| Hit from above | **201 / 122 N** | 108 / 49 N |
| Hit on the front edge | 9 / 17 N | 29 / 13 N |
| Hit on the divider | 40 / 27 N | 13 / 33 N |

Screw 1 is in the bay at the end wall, screw 2 in the bay at the far wall. The rest of the moment goes into the bath wall as pressure on the rear face: up to 332 N in a hit from above.

All of them are well below the 625 N preload, so the joint never opens. Lateral loads are carried by friction from the preload (μ ≈ 0.3 → ≈ 190 N per screw) and, beyond that, by the screw shank.

## 7. Sealing

| | Value |
|---|---|
| Water pressure at 20 cm depth | 0.002 MPa |
| Gasket contact pressure, 2 × 625 N over ≈ 846 mm² | ≈ 1.5 MPa |
| Ratio | ≈ 700 × |

The gasket is pressed on several hundred times harder than the water pushes. Its sleeves fill the gap between the M4 screw and the Ø 6.6 mm hole.
- Print it in TPU 95A at 100 % infill so it is fully dense and watertight.
- Replace it if it takes a permanent set.

## 8. Printing

- **Material:** PETG for the holder and the nut bar, TPU 95A for the gasket.
- **Holder orientation:** frame face down. The top face is flat, and nothing is steeper than 40° from vertical except the screw countersinks. No supports are needed.
- **Solid parts:** 5 walls of 0.6 mm fill a 3 mm wall exactly. With 100 % rectilinear infill the frame is solid too, which matches the strength check. It was also faster than 40 % cubic: 3 h 05 min against 3 h 17 min.
- **Recesses instead of windows:** the walls are lightened with one-sided recesses (≥ 1.8 mm left, = 3 lines) instead of through windows. That saves 23 min per module at the same mass.

## 9. Design history and decisions

| Step | Why |
|---|---|
| Through diamond windows → tapered one-sided recesses | Same mass, 23 min faster. Each window in a 3 mm wall adds perimeters and travel. |
| Recess depths from the FEM utilisation map | Thin only where the load is low; never below 3 lines (1.8 mm). |
| 4 mm fill along the rear-wall / frame junction | Removed the layer peel at the junction under buoyancy. |
| Teardrop screw bosses | Moved the stiffness step away from the screw; peak under a hit from above −20 %. |
| One flat tilted mounting face | The vertical frame edge used to stick 0.43 mm out of the tilted face. |
| Fully parametric model | One spreadsheet drives every sketch; tested from 50 × 40 to 100 × 80 mm openings. |
| Nut bar with slot, M4 × 20 | Nuts held captive; slot −40 % plastic; bar thickness follows the screw length. |
| Flat TPU gasket with sleeves | Seals the bath holes; no groove in the holder, so its strength is unchanged. |

**Tried and rejected:**
- ribs under the screws (new peaks at the rib ends);
- local pads around the screws;
- a thicker rear wall (9 g for less gain than the teardrop bosses);
- a TPU washer under the nut (makes the joint soft and lets it loosen);
- a sealing groove in the holder (weakens the area round the screw).

## 10. Limits and open points

- Strength was calculated for the default size only. After changing the bottle size, run the calculation again.
- The recessed version has not yet been printed and tested; the layout and the ledge come from a holder that is already in use.
- PETG strengths are typical values, not tested on this printer. Check a first print under load before relying on it.

## 11. Files

| Path | What |
|---|---|
| `../cad/THD_CP_Lift_Bottle_Holder.FCStd` | Parametric model: Module, Nut bar, Gasket, and their mirrors |
| `../step/` | STEP of every printed part |
| `strength.md` | FEM method in detail |
| `../scripts/fem/` | Calculation scripts (CalculiX, Gmsh) |
| `img/` | Images and animations in this report |
