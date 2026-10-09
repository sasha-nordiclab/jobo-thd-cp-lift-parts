# THD heater holder v1.0 — ABS clamp

A two-part clamp for the 220 V THD bath heater. The base is glued to the bath floor; an M4-screwed cap holds the rubber heater head horizontally with its axis 15 mm above the floor. The parts are designed as symmetric, fully parametric FreeCAD bodies.

<p align="center"><img src="https://raw.githubusercontent.com/sasha-nordiclab/thd-cp-lift-parts/heater-holder-v1.0/heater-holder/docs/img/release_v1_0_overview.png" width="440" alt="ABS heater clamp, cap lifted above base"><img src="https://raw.githubusercontent.com/sasha-nordiclab/thd-cp-lift-parts/heater-holder-v1.0/heater-holder/docs/img/release_v1_0_side.png" width="440" alt="Heater clamp bore and screw holes"></p>

## Download

- [Complete v1.0 ZIP — FreeCAD model, STEP files, build script, pictures, instructions, and license](https://github.com/sasha-nordiclab/thd-cp-lift-parts/releases/download/heater-holder-v1.0/heater-holder-v1.0.zip)
- [Base STEP](https://github.com/sasha-nordiclab/thd-cp-lift-parts/releases/download/heater-holder-v1.0/THD_Heater_Holder_Base.step) · [Cap STEP](https://github.com/sasha-nordiclab/thd-cp-lift-parts/releases/download/heater-holder-v1.0/THD_Heater_Holder_Cap.step)
- [Parametric FreeCAD model](https://github.com/sasha-nordiclab/thd-cp-lift-parts/releases/download/heater-holder-v1.0/THD_Heater_Holder.FCStd)

## Design

- Base: 46 × 20 mm glue footprint, 14.7 mm high, with a half-round bed and two blind octagonal pilot holes.
- Cap: a 46 × 20 × 12.6 mm block with a half-round bore, two octagonal clearance holes, and flush 90° countersinks.
- Two M4 × 25 ISO 14581 countersunk Torx screws, at ±14.5 mm from the heater axis, form threads in the base pilot holes. The split has a 0.6 mm gap before tightening.
- Rounded R1.5 outer corners and chamfered end faces help with ABS printing. The base and cap STEP exports were regenerated from the current CAD solids and checked for valid single-solid geometry. All seven sketches have zero free degrees of freedom.

## Printing and status

Use ABS (the model was prepared for AzureFilm ABS Plus), 0.4 mm nozzle, 0.6 mm line width, 0.2 mm layers, and 100% rectilinear infill. Print each part on an end face with a brim. OrcaSlicer estimates on a Bambu Lab A1 are about 36 min / 10.2 g for the base and 32 min 30 s / 7.9 g for the cap. These are slicer estimates; this design has **not been print-tested**.

See the [full model and assembly notes](https://github.com/sasha-nordiclab/thd-cp-lift-parts/blob/heater-holder-v1.0/heater-holder/README.md). The FCStd file uses a FreeCAD 26.3 development build. Licensed under [CC BY-NC-SA 4.0](https://github.com/sasha-nordiclab/thd-cp-lift-parts/blob/heater-holder-v1.0/LICENSE).
