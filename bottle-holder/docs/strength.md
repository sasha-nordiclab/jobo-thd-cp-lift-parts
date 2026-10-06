# Strength check and design decisions

The goal was a holder that is strong where it needs to be, prints fast, and uses plastic only where the load needs it. This page explains how the default size was checked and why the part looks the way it does.

## Model

**Mesh and solver.** Second-order tetrahedra (Gmsh, `-order 2`, `Mesh.SecondOrderLinear 1`, maximum element size 2.5 mm). The solver is CalculiX, linear elastic, with PETG at E = 2200 MPa and ν = 0.38.

**Screws.** The screws are tightened, so the joint stays closed while the load changes the screw force by less than the preload.
- The countersink surface under each screw head is fixed.
- The 6 mm bore has clearance and carries nothing.
- Check after solving: the largest screw force is 201 N axial and 122 N lateral (hit from above). Both are below the 625 N preload and the ≈ 190 N friction it provides, so the joint stays closed.

**Bath wall.** The rear face is in frictionless one-sided contact with the bath wall: the wall can push the part but not pull it.
- The wall is a rigid hexahedral plate on the tilted mounting plane.
- CalculiX solves the contact itself: node-to-surface, linear penalty 2·10⁴ MPa/mm, `ADJUST=0.002` to close round-off gaps.
- All 10 743 nodes of the rear face take part.
- The impacts are solved at 100 N and scaled to the impact force; the floating case at its real load. Frictionless contact with no initial gap is proportional to the load, so the scaling is exact.
- The floating case stalls at 58 % of the load (one node flips between touching and not touching). The last converged step is scaled to the full load.

**Check of every solve.** Applied load + screw reactions + wall reaction = 0, and the wall reaction points along the wall normal (z/x = tan 7.5°).

An earlier version used its own active-set loop and found only 204 face nodes: the tolerance was too tight and the plane was tilted 7.547° instead of 7.5°. The holder then bore on a narrow strip only, which made it look softer and weaker. The numbers below replace those results.

**Failure criterion.** The part is printed frame-down, so the layers lie normal to the model Z axis, and the criterion follows them:

```
FI = sqrt( (σ_vM,in-plane / 40)² + (max(σ_zz, 0) / 20)² + (τ_interlayer / 15)² )    [MPa]
```

- The strengths are typical PETG values: 40 MPa in plane, 20 MPa layer tension, 15 MPa layer shear.
- They are reduced by 0.85 for a 38 °C bath.
- The safety factors are 4 for the sustained load and 2 for impacts.
- The tables report FI divided by the allowable: 1.0 or less passes.

## Loads

| Case | Load |
|---|---|
| Floating bottles | 2 × 5.9 N upwards on the front ledge: an empty 600 ml bottle in water; sustained load |
| Hit from above | A full bottle (0.7 kg) at 0.5 m/s straight down on the front of the frame |
| Hit on the front edge | The same bottle into the front face |
| Hit on the divider | The same bottle sideways into the divider |

Each impact is turned into a force by its energy. With E = ½ m v² = 87.5 N·mm, the force is F = √(2 E k), where k is the stiffness at the point of impact. A stiffer part therefore takes a larger force: stress grows like √k, so "more material" helps less than expected.

## Results (default size)

| Case | Force | Load / allowable | Where |
|---|---|---|---|
| Floating bottles | 11.8 N | **0.31** ✅ | layer peel in the lower rear wall below screw 2 |
| Hit from above | 172 N (k = 169 N/mm) | 1.08 | layer peel in the rear wall beside screw 1 |
| Hit on the front edge | 136 N (k = 105 N/mm) | 1.17 | frame at the front edge |
| Hit on the divider | 58 N (k = 19 N/mm) | 1.75 | corner of the bottle opening |

With the whole rear face in contact, the holder is much stiffer under a hit from above (169 instead of 8 N/mm). A knock therefore produces a larger force, but a lower stress.

On the old strip-contact model, a finer mesh (maximum element size 1.8 mm) raised the peaks by 10–12 %. Expect a similar margin here.

The design changes below were compared on the old strip-contact model. Their ranking holds, but the absolute numbers are from that model.

## What changed against the previous version, and why

| Change | Effect |
|---|---|
| Diamond through-windows replaced by one-sided tapered recesses | Same mass, **23 min faster** to print. Each window in a 3 mm wall adds perimeters and travel moves. |
| Recesses only where the calculated load is low | End wall and far wall 1.8 mm thick, divider 2.4 mm, lower half of the rear wall 1.8 mm. The load in the recess zones is ≤ 0.56 of the allowable. The walls are multiples of the 0.6 mm line width and never thinner than 3 lines. |
| Recess sides tapered at 50° | They overhang no more than 40° from vertical when printed. |
| 4 mm fill along the rear-wall / frame junction | Floating case 1.04 → 0.84 for 0.2 g. |
| Screw bosses extended 22 mm downwards as a teardrop | Hit from above 2.59 → 1.98 for 0.4 g. The boss edge was the stress raiser. |

## Tried and rejected

| Variant | Result |
|---|---|
| Ribs under the screws | Worse: a new peak at the rib end (hit from above 3.26) |
| Local pads around the screws, 1.2 / 2.0 mm | Hit from above 3.05 / 2.29; the floating case got worse |
| Whole rear wall 1 mm thicker | Hit from above 2.05 for 9 g; the teardrop bosses do better for 0.4 g |
| One-sided screw seat without preload | The part becomes a mechanism; wrong for a tightened screw |

## Running the calculation

The scripts in `scripts/fem/` are written for the default size: screw positions and load patches are coordinates in `fem_run.py` and `fem2.py`. They need the Gmsh and CalculiX that ship with FreeCAD. Set `CCX` if CalculiX is not at the macOS default path.

```sh
gmsh module.step -3 -order 2 -setnumber Mesh.SecondOrderLinear 1 -clmax 2.5 -clmin 0.8 -format inp -o module.inp
CASES=BUOY,HIT_TOP,HIT_FRONT,HIT_DIVIDER python3 scripts/fem/fem6.py module.inp result   # 10-30 min per case
```

Export `module.step` from the `Module` body with its placement reset to identity. The model coordinates are those of the body.
