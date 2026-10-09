# JOBO drum mount v0.1 — experimental

An experimental two-part JOBO drum mount for the THD CP-Lift: an 80 × 80 mm mounting plate with locating rings and a sliding lock with a printed spring. Pull the finger ears to release the drum; the lock travel is 3.5 mm.

<p align="center"><img src="https://raw.githubusercontent.com/sasha-nordiclab/thd-cp-lift-parts/drum-mount-v0.1/drum-mount/docs/img/release_v0_1_overview.png" width="440" alt="Drum mount and sliding lock"><img src="https://raw.githubusercontent.com/sasha-nordiclab/thd-cp-lift-parts/drum-mount-v0.1/drum-mount/docs/img/release_v0_1_top.png" width="440" alt="Drum mount and lock from above"></p>

## Download

- [Complete v0.1 ZIP — FreeCAD model, both STEP files, pictures, instructions, and license](https://github.com/sasha-nordiclab/thd-cp-lift-parts/releases/download/drum-mount-v0.1/drum-mount-v0.1.zip)
- [Mount STEP](https://github.com/sasha-nordiclab/thd-cp-lift-parts/releases/download/drum-mount-v0.1/JoboDrumMount_Mount.step) · [Lock STEP](https://github.com/sasha-nordiclab/thd-cp-lift-parts/releases/download/drum-mount-v0.1/JoboDrumMount_Lock.step)
- [Parametric FreeCAD model](https://github.com/sasha-nordiclab/thd-cp-lift-parts/releases/download/drum-mount-v0.1/JoboDrumMount.FCStd)

## Design and assembly

| Part | Approximate size | Function |
|---|---|---|
| Mount | 80 × 80 × 19 mm | Locates the drum with rings, a Ø24 mm centre bore, and a motor pocket |
| Lock | 45 × 34 × 13 mm | Sliding latch with a spring and finger ears; the STEP file contains the final mirrored lock shape |

Three M4 cap screws mount the plate to the lift through Ø4.5 mm holes with Ø8 mm counterbores. Two M3 screws attach the lock through its slots into Ø2.9 mm pilot holes in the mount. The FreeCAD file includes the parametric model and an assembly showing the parts together. All saved sketches have zero free degrees of freedom; the exported lock is one valid solid and matches the `LockMirror` feature.

Both pieces are intended to print flat in PETG without supports. Earlier OrcaSlicer estimates on a Bambu Lab A1 were about 2 h / 60 g for the Mount at 40% cubic infill and about 25 min / 8 g for the Lock. Re-slice the supplied STEP files for current times and material use.

**Work in progress:** the geometry may change, and this mount has not been strength-checked. See the [full printing and assembly notes](https://github.com/sasha-nordiclab/thd-cp-lift-parts/blob/drum-mount-v0.1/drum-mount/README.md). The FCStd file uses a FreeCAD 26.3 development build. Licensed under [CC BY-NC-SA 4.0](https://github.com/sasha-nordiclab/thd-cp-lift-parts/blob/drum-mount-v0.1/LICENSE).
