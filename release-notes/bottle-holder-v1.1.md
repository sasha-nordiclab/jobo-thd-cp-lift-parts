# THD CP-Lift bottle holder v1.1

The current two-module frame holds four standard JOBO bottles in the THD CP-Lift water bath. **This release includes both mirrored frame modules**, the matching nut bar and gasket, four-bottle assembly model, and TPU bottle stands.

<p align="center"><img src="https://raw.githubusercontent.com/sasha-nordiclab/thd-cp-lift-parts/bottle-holder-v1.1/bottle-holder/docs/img/release_v1_1_overview.png" width="440" alt="Current four-bottle frame"><img src="https://raw.githubusercontent.com/sasha-nordiclab/thd-cp-lift-parts/bottle-holder-v1.1/bottle-holder/docs/img/release_v1_1_top.png" width="440" alt="Frame openings viewed from above"></p>

## Download

- [Complete v1.1 ZIP — FreeCAD model, all STEP files, documentation, pictures, and license](https://github.com/sasha-nordiclab/thd-cp-lift-parts/releases/download/bottle-holder-v1.1/bottle-holder-v1.1.zip)
- [Module STEP](https://github.com/sasha-nordiclab/thd-cp-lift-parts/releases/download/bottle-holder-v1.1/THD_CP_Lift_Holder_Module.step) · [Mirrored module STEP](https://github.com/sasha-nordiclab/thd-cp-lift-parts/releases/download/bottle-holder-v1.1/THD_CP_Lift_Holder_Module_Mirrored.step)
- [Nut bar STEP](https://github.com/sasha-nordiclab/thd-cp-lift-parts/releases/download/bottle-holder-v1.1/THD_CP_Lift_Nut_Bar.step) · [TPU gasket STEP](https://github.com/sasha-nordiclab/thd-cp-lift-parts/releases/download/bottle-holder-v1.1/THD_CP_Lift_Gasket_TPU.step) · [TPU bottle stand STEP](https://github.com/sasha-nordiclab/thd-cp-lift-parts/releases/download/bottle-holder-v1.1/THD_CP_Lift_Bottle_Stand_TPU.step)
- [Parametric FreeCAD model](https://github.com/sasha-nordiclab/thd-cp-lift-parts/releases/download/bottle-holder-v1.1/THD_CP_Lift_Bottle_Holder.FCStd)

## Changes since v1.0

- Updated the two frame modules with the bed-side chamfer and rounded outside corner. The openings remain 93.4 × 71.4 mm with R4 corners; each module is about 120.4 × 159.5 × 74.7 mm.
- Corrected the M4 hole layout: the pair across the module joint is 27.8 mm centre to centre. The matching nut bar and gasket STEP files are included.
- Added the TPU bottle stand to the downloadable set. Four stands support the bottles above the bath floor and leave water paths underneath.
- Updated the complete FreeCAD assembly. All 25 sketches are fully constrained, and the five STEP files were checked against their corresponding final CAD solids.

## Printing and assembly

| Part | Quantity | Material | Orientation and slicer estimate |
|---|---:|---|---|
| Module + mirrored module | 1 + 1 | PETG | Frame face down; 5 walls, 100% rectilinear; about 3 h 05 min and 126 g each |
| Nut bar | 2 | PETG | Bath side down, nut pockets up; about 32 min and 11 g each |
| Gasket | 2 | TPU 95A | Flat, sleeves up |
| Bottle stand | 4 | TPU 95A | Glue face down; about 1 h 16 min and 11 g each |

Use four M4 × 20 countersunk Torx screws (ISO 14581, stainless 304) and four M4 nuts (ISO 4032). The holder mounts through the 3 mm bath wall; the gasket sits between the wall and each nut bar. See the [assembly and printing instructions](https://github.com/sasha-nordiclab/thd-cp-lift-parts/blob/bottle-holder-v1.1/bottle-holder/README.md).

The [FEM design report](https://github.com/sasha-nordiclab/thd-cp-lift-parts/blob/bottle-holder-v1.1/bottle-holder/docs/report.md) describes the earlier frame. FEM was **not rerun** after the latest hole layout and chamfer changes. The model was made with a FreeCAD 26.3 development build; STEP files can be used without that version. Licensed under [CC BY-NC-SA 4.0](https://github.com/sasha-nordiclab/thd-cp-lift-parts/blob/bottle-holder-v1.1/LICENSE).
