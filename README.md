# THD CP-Lift parts

3D-printable parts for working with JOBO drums on the THD CP-Lift. Each part is a parametric FreeCAD model with STEP files and printing notes.

▶ **Videos:** [YouTube playlist](https://www.youtube.com/playlist?list=PLADhkNYpSGAc)

## Downloads

Each link downloads the file directly. STEP files open in any CAD program or slicer. The FCStd files are the parametric FreeCAD models.

| Part | Print files (STEP) | FreeCAD model | Everything in one zip |
|---|---|---|---|
| **Bottle holder** | [Module](https://github.com/sasha-nordiclab/thd-cp-lift-parts/raw/main/bottle-holder/step/THD_CP_Lift_Holder_Module.step) · [Module, mirrored](https://github.com/sasha-nordiclab/thd-cp-lift-parts/raw/main/bottle-holder/step/THD_CP_Lift_Holder_Module_Mirrored.step) · [Nut bar](https://github.com/sasha-nordiclab/thd-cp-lift-parts/raw/main/bottle-holder/step/THD_CP_Lift_Nut_Bar.step) · [Gasket (TPU)](https://github.com/sasha-nordiclab/thd-cp-lift-parts/raw/main/bottle-holder/step/THD_CP_Lift_Gasket_TPU.step) · [Bottle stand (TPU)](https://github.com/sasha-nordiclab/thd-cp-lift-parts/raw/main/bottle-holder/step/THD_CP_Lift_Bottle_Stand_TPU.step) | [FCStd](https://github.com/sasha-nordiclab/thd-cp-lift-parts/raw/main/bottle-holder/cad/THD_CP_Lift_Bottle_Holder.FCStd) | [v1.0 release zip](https://github.com/sasha-nordiclab/thd-cp-lift-parts/releases/download/bottle-holder-v1.0/bottle-holder-v1.0.zip) |
| **Heater holder** | [Base](https://github.com/sasha-nordiclab/thd-cp-lift-parts/raw/main/heater-holder/step/THD_Heater_Holder_Base.step) · [Cap](https://github.com/sasha-nordiclab/thd-cp-lift-parts/raw/main/heater-holder/step/THD_Heater_Holder_Cap.step) | [FCStd](https://github.com/sasha-nordiclab/thd-cp-lift-parts/raw/main/heater-holder/cad/THD_Heater_Holder.FCStd) | — |
| **Drum mount** (experimental) | [Mount](https://github.com/sasha-nordiclab/thd-cp-lift-parts/raw/main/drum-mount/step/JoboDrumMount_Mount.step) · [Lock](https://github.com/sasha-nordiclab/thd-cp-lift-parts/raw/main/drum-mount/step/JoboDrumMount_Lock.step) | [FCStd](https://github.com/sasha-nordiclab/thd-cp-lift-parts/raw/main/drum-mount/cad/JoboDrumMount.FCStd) | — |

The whole repository as a zip: [main.zip](https://github.com/sasha-nordiclab/thd-cp-lift-parts/archive/refs/heads/main.zip). Screws, nuts and print settings for each part are in its README.

## Parts

| Part | What it does | Status | Folder |
|---|---|---|---|
| **Bottle holder** | An optimised redesign for this machine: holds four standard JOBO bottles in the water bath. It mounts with stainless countersunk screws through the 3 mm bath wall into a printed nut bar. Strength-checked by FEM; see the [design report](bottle-holder/docs/report.md). | ✅ [v1.0 release](https://github.com/sasha-nordiclab/thd-cp-lift-parts/releases/tag/bottle-holder-v1.0) | [`bottle-holder/`](bottle-holder/) |
| **Drum mount** | Holds a JOBO drum on the lift, with a sliding lock and a printed spring. | 🧪 Experimental, work in progress, no release | [`drum-mount/`](drum-mount/) |
| **Heater holder** | A PETG clamp that holds the 220 V bath heater horizontally, 15 mm above the bath floor. The base is glued to the floor, and the cap is screwed down with two M4 countersunk Torx screws that form their own thread in the plastic. | 🧪 New, not print-tested yet, no release | [`heater-holder/`](heater-holder/) |

## Shared pump model and accessories

The [ROTEK A01VP repository](https://github.com/sasha-nordiclab/ROTEK-A01VP) holds the parametric reference model of the Rotek circulation pump and compatible accessories, starting with a TPU vibration-damping holder. The same pump is used in the JOBO Repair Parts project. The [FreeCAD model](https://github.com/sasha-nordiclab/ROTEK-A01VP/blob/main/cad/TPU_Pump_Holder.FCStd) contains both the pump and the holder.

<table align="center">
  <tr><td align="center"><img src="bottle-holder/docs/img/view_1_bottle_side.png" width="400" alt="Bottle holder"><br><b>Bottle holder</b></td><td align="center"><img src="bottle-holder/docs/img/exploded.png" width="400" alt="Exploded view"><br><b>Exploded view</b></td></tr>
</table>

## Common notes

- **Material:** PETG for everything that goes near the water bath.
- **Profile used for the times in each README:** 0.4 mm nozzle, 0.6 mm line width, 0.2 mm layers, 5 walls, OrcaSlicer on a Bambu Lab A1.
- **Models:** made with a FreeCAD 26.3 development build. Older FreeCAD releases may not open them; the STEP files work in any CAD or slicer.
- **Changing sizes:** every model is driven by a spreadsheet (`params` or `Params`). Change the values there and recompute.

## License

[CC BY-NC-SA 4.0](LICENSE). You may share and adapt these designs with attribution, not for commercial use, and under the same license.
