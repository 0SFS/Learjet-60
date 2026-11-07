# Learjet 60 LOD3 reconstruction

Status: first construction pass; dimensions beyond overall envelope are estimates.

## Current model audit

The source has 25,176 triangles, twelve embedded JPEGs, 42 original materials,
69 mesh instances and no animation clips. Its nodes use anonymous names and
legacy alternate still/slow/blurred fan and wheel meshes. These are unsuitable
as a documented animation rig without further work.

- No verified independently hinged rudder, elevators, ailerons, flap or spoiler
  assemblies. A painted seam does not establish an operable control surface.
- Gear is stowed in the visible exterior. No validated gear extension sequence,
  wheel steering, suspension, door linkage or wheel rotation is provided.
- There is no JSBSim profile. Missing yaw response cannot be diagnosed from
  the mesh alone: yaw requires aerodynamic rudder forces in the flight model;
  a visible rotating rudder is a separate presentation requirement.
- Source geometry measures 12.798 m span and 18.105 m length, compared with
  published envelope references of 13.35 m and 17.89 m. Uniform scaling cannot
  correct both. Shape fidelity needs orthographic comparison, not eyeballing.
- Source renders include overlapping alternate fan states. Their duplicate
  geometry has no documented runtime visibility contract.
- Original material definitions assign metallic=1 broadly, including paint.
  This is unsuitable for dielectric paint and many cabin surfaces.
- The white override removed painted stripes and registration. It is a solid
  material replacement, not a faithful repaint preserving surface markings.
- Cabin, pilots and seats consume geometry despite no verified cockpit-view
  requirements. Exterior LOD3 should spend geometry on silhouette and mechanisms.
- Twelve texture images and numerous materials need a draw-call/texture budget;
  source counts alone do not demonstrate runtime optimization.
- No verified collision proxy, pilot eye, FDM datum alignment, light attachments,
  aerodynamic hinge stations, swept-volume clearances or contact geometry.
- No evidence of validated intake/exhaust depths, reverser motion, access doors,
  pressure windows, probes, antenna configuration or small external equipment.

These are asset/validation deficiencies, not evidence about its creator's intent.

## References and missing information

[Transport Canada operational evaluation](https://tc.canada.ca/en/aviation/commercial-air-services/operational-evaluation-reports/bombardier-learjet-60-60xr)
confirms hydraulic gear, flap and spoiler operation, and electrically actuated
lateral/directional trim tabs. Use the original 60 configuration; XR documents
must be labeled rather than silently treated as identical.

[EASA TCDS, historical Issue 03](https://www.caa.co.uk/Documents/Download/3934/ca692457-336e-4190-840e-cd26cf498935/2822)
provides engines, loading limits, flap detents and wheel sizes. It does not
provide a complete geometric rig. Refer to the companion JSBSim plan for values.

[Manufacturer pilot manual, externally hosted](https://pilots4rent.com/Lear/LR-60XR-PM.pdf)
is a candidate for mechanism descriptions and three-view verification, not
redistributable project artwork. Do not copy its illustrations into the model.

Missing measurements to resolve before a realism claim:

| Assembly | Information still required |
| --- | --- |
| Fuselage | Station cross-sections, nose/cockpit contour, window/door dimensions |
| Wing | Root/tip chords, sweep, twist, airfoil thickness distributions, winglets |
| Empennage | Tail outlines, incidence, stabilizer trim axis and operating range |
| Controls | Hinge endpoints, balance/trim tabs, travel limits and actuator paths |
| Gear | Axle stations/track, trunnion axes, retraction directions, door sequence, travel |
| Engines | Nacelle stations/sections, pylon outline, reverser bucket geometry and linkage |
| Details | Delta fins, lights, probes, antennas, drains, static wicks and serial-specific options |
| Runtime | Animation property bindings, collision proxy, CG/reference transform and cockpit eye |

Record each input as sourced, measured from a reference, or estimated, with units
and configuration. Unknown values remain estimates; do not infer engineering
measurements from the downloaded decorative mesh.

## Construction and acceptance

Create original procedural geometry without importing Sketchfab vertices or
textures. Preserve the existing HD asset separately. Initial blockout establishes
metre units, a white fuselage, swept wings, T-tail and separate named rudder,
elevators, ailerons, flaps, spoilers and gear pivots. Its provisional outlines
and mechanism axes are explicitly unvalidated.

Aim initially for at most 6,000 triangles and four shared materials; refine that
budget from measured silhouette quality. Keep moving parts separate, merge static
parts by material, omit hidden cabin detail and use shared wheels. Validate
manifold exterior parts, normals, symmetry, measured dimensions and each mechanism
at both endpoints and intermediate positions. Gear must fit its wells without
intersections; surfaces must leave real gaps. Add spoilerons, trim/balance tabs,
reversers, gear doors and small features only after reference verification.

Completion requires reference comparisons from front/side/top, deployed/stowed
clearance renders, actual host animation checks and measured geometry/material
counts. A successful export or a plausible blockout is not a realistic finished
LOD3. This phase does not establish flight dynamics.
