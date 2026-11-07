# Learjet 60 JSBSim model

Status: research and proposed implementation, 1 November 2026. No aircraft or
engine XML has been implemented or flight-tested for this package.

## Decision

Build a dedicated Learjet 60 baseline with
[JSBSim's AeromatiC++ generator](https://github.com/JSBSim-Team/jsbsim/tree/master/utils/aeromatic%2B%2B),
using two turbine engines mounted on the aft fuselage. Label its flight model
experimental until performance is checked. Generator defaults are estimates,
not measured Learjet coefficients.

The upstream-derived local JSBSim aircraft and engine catalogs contain no
Learjet 60 or PW305A. Web searches did not locate an exact reusable model.
This is a search result, not proof that none exists elsewhere.

| Candidate | Assessment |
| --- | --- |
| [FlightGear Learjet 35A](https://wiki.flightgear.org/Learjet_35-A) | Uses YASim, a different FDM. It is also a different aircraft. Its CC BY-NC-SA 3.0 terms need preserving if any material is reused. |
| [JSBSim Global 5000](https://github.com/JSBSim-Team/jsbsim/blob/master/aircraft/global5000/global5000.xml) | Aeromatic-derived ALPHA twin business jet. Useful XML structure, but its 87,700 lb maximum weight and 93 ft span make its flight coefficients unsuitable for direct reuse. |
| AeromatiC++ | Recommended starting point for a new configuration with recorded inputs and explicit estimates. |

If copying upstream source, retain its authorship and applicable licence; the
local AeromatiC++ source headers specify LGPL-2.1-or-later. No upstream flight
model has been copied into this package.

## Configuration and reference inputs

Start with the original Model 60's standard weight configuration. Keep optional
weight increases separate rather than mixing configurations. The
[EASA IM.A.212 Issue 03 TCDS, pp. 7–11, hosted by the UK CAA](https://www.caa.co.uk/Documents/Download/3934/ca692457-336e-4190-840e-cd26cf498935/2822)
provides these historical reference inputs:

| Input | Value |
| --- | --- |
| Engines | Two PW305A; 4,600 lbf static sea-level takeoff thrust each |
| Standard maximum ramp / takeoff weight | 23,000 / 22,750 lb |
| Maximum landing / zero-fuel weight | 19,500 / 16,500 lb |
| Optional maximum takeoff weights | 23,100 or 23,500 lb, with the relevant modifications |
| Usable wing fuel, combined | 2,898 lb at fuselage station 391.7 in |
| Usable fuselage fuel | 5,012 lb at fuselage station 427.1 in |
| Flap detents and corresponding VFE | 8° / 250 KIAS; 20° / 200 KIAS; 40° / 165 KIAS |

These are inputs for simulation research. Check a current TCDS and the matching
configuration's AFM before treating them as final. EASA's current download is
[here](https://www.easa.europa.eu/en/downloads/7238/en); the research used the
readable 2012 Issue 03 copy above.

For initial geometry, the manufacturer-authored
[Learjet 60 XR fact sheet](https://www.aviation-broker.com/fileadmin/user_upload/flugzeuge/midsize_jets/bombadier_60_xr/learjet_60_xr_factsheet.pdf)
lists length 17.89 m, span 13.35 m, overall height 4.44 m and wing area 24.57 m².
This historical PDF remains indexed but its URL can redirect to a newer broker
page. Verify these inputs against a matching Model 60 reference before generation.
Its XR performance figures are comparison candidates, not an original-60
calibration dataset. Basic operating weight includes operating items and must
not silently be used as JSBSim empty weight.

[Transport Canada's evaluation](https://tc.canada.ca/en/aviation/commercial-air-services/operational-evaluation-reports/bombardier-learjet-60-60xr)
distinguishes the 60 and 60XR configurations. The
[Learjet/NASA wing-design paper abstract](https://ntrs.nasa.gov/citations/19950057595)
describes aircraft-specific transonic improvements; it supplies no complete
coefficient database or downloadable paper in that record.

## Implementation and validation

1. Record the chosen weight configuration, datum and CG envelope. Source empty
   mass and loading; mark inertia, empty CG and aerodynamic derivatives as
   estimated wherever measured data is absent. Do not derive aerodynamics from
   this decorative mesh.
2. Generate `aircraft/learjet60/learjet60.xml` and a reusable PW305A engine mod.
   Use two direct turbine thrusters, explicit fuel feeds, and documented estimates
   for thrust lapse, fuel flow and spool response. Include flaps, retractable
   gear, brakes, steering, spoilers and reversers as supported by the evidence.
3. Check loading in the exact JSBSim artifact installed by `fly`. Verify engine
   indexing, approximately 4,600 lbf per engine under matching static conditions,
   fuel conservation, control signs and stable ground equilibrium.
4. Check repeatable trim across weights and CG, approach, climb and cruise;
   exercise stalls and asymmetric engine response. Compare takeoff, climb,
   cruise fuel flow and landing with matching-condition reference data. Record
   errors and unresolved assumptions instead of equating successful loading
   with correct performance.
5. Align the HD model with the FDM reference point and ground stance. Confirm
   cockpit, contact locations and gear visibility in the runtime; the current
   static visual asset does not establish gear animation or aerodynamic geometry.

## 0SFS integration when physics is ready

Create the aircraft's `public/0sfs-mod.json` with its family, HD definition,
`fdmProfiles`, `jsbsimFiles`, attribution and PW305A dependency. Put the engine
in its own mod, as the organization architecture requires. Add the aircraft to
`default-modpack` and both new mods as `file:` dependencies of `fly`, update its
lockfile, then run `node scripts/link-packs.mjs` from `fly`.

For now, `aircraft.json` is a draft visual definition. The current mod loader
registers aircraft definitions even if their FDM profile is absent, and flight
selection then dereferences that profile. Consequently there is no installable
manifest or default-modpack entry yet. This avoids presenting an aircraft that
fails on selection or silently uses another airframe's physics.
