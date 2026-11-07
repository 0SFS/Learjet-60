# Learjet 60 for 0SFS

The HD model is prepared from OUTPISTON's
[Bombardier Learjet 60](https://sketchfab.com/3d-models/bombardier-learjet-60-7573f836dd3a46bdbce8b90b5a40f104).
Only HD is included at this stage; there are no reduced-detail models.

The aircraft is not yet flyable. No existing Learjet 60 JSBSim definition was
found in the upstream JSBSim catalog or the FlightGear sources checked.
[The flight-model plan](docs/proposals/jsbsim-model.md) records the sources,
recommended implementation and validation still needed.

`aircraft.json` is a draft visual definition, not an installable mod manifest.
The current simulator requires a flight profile for every selectable aircraft.
It has no visual-only aircraft state, so this package stays out of the default
modpack until its own flight model is available.

## Files and preparation

- `public/aircraft/learjet-60/Learjet_60_HD.glb`: self-contained, metre-scale HD model.
- `aircraft.json`: draft aircraft definition for the eventual mod.
- `public/aircraft/thumbnails/learjet-60.png`: render of the HD asset.
- `docs/proposals/jsbsim-model.md`: JSBSim research and implementation plan.

Preparation details and third-party attribution accompany the model in its
asset directory. Keep the downloaded ZIP intact; intermediate files and visual
inspection renders belong in ignored `build/`.

The model has 25,176 triangles and twelve embedded JPEG textures. The source
geometry, embedded textures and coordinate frame are preserved; attribution
metadata and a white exterior paint material were added. The aircraft has white
fuselage, wings, tail and nacelles with dark glazing and gear retracted.
The draft uses yaw zero (verified with the Babylon glTF loader). Its zero model
offset is provisional until an FDM reference point and stance are defined.

To reproduce the prepared GLB from the supplied archive:

```sh
cd ~/gh/0sfs/Learjet-60
npm run prepare:hd -- /Users/felg/gh/foss-earth/experiments/bombardier-learjet-60.zip
```

Preparation checks the source SHA-256 and embedded texture count. The imported
model was inspected in Blender and loaded through Babylon's glTF loader; no
in-flight physics or animation has been validated.

## Licensing

The project's code is covered by [AGPL-3.0-only](LICENSE). OUTPISTON's model,
textures and derived renders retain
[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).
Credit OUTPISTON, link the model and licence, and identify modifications.
The asset licence limits use to noncommercial purposes and requires adaptations
to use the same licence. It is not relicensed under the code's AGPL.
