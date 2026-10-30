# Research evidence and reproduction

This page is a **navigation and audit record**, not a claim that a new experiment
was executed for this profile edit. It points to recorded results and their
generators as they existed on **2026-10-31**. Follow the source repositories
for updated results and exact environments.

## How to read the statuses

- **Calculated / synthetic:** mathematical or generated-data experiments, not
  experimental confirmation.
- **Public measured data:** instrument counts are public and there is a script
  to analyze them. Any verdict applies to the dataset and stated conditions.
- **Private measured comparison:** methodology and summaries are public but
  measurements/reference arrays cannot be independently checked from GitHub.
- **Not reproduced / unresolved:** a failed or incomplete validation is part of
  the research record, **not** a success claim.

Commands below are **recorded reconstruction routes from the source repositories**.
They were inspected, but **not rerun during this profile update**. Run report
generators in a separate checkout/worktree: some commands overwrite versioned
reports or write local working directories.

## 1. TraTT — time-dependent diffraction (calculation)

**Claim recorded:** For a linear acoustic turn-on, a scan over 11,211
\(S,T\) pairs in the reduced model found a largest first-satellite
center-intensity overshoot of **0.603**, at \(S=3.8\) and
\(T/t_{tr}=4\), on the boundary of the scanned rise-time range.
Selected full Takagi–Taupin solutions agree to **8.65 × 10⁻⁵**
under the report's comparison; this is **not** a global bound.

- [Primary finding F8 and explicit limits](https://github.com/NaNIsaac-Research/TraTT/blob/main/docs/FINDINGS.md)
- [Saved scan arrays](https://github.com/NaNIsaac-Research/TraTT/blob/main/explore/nb/e67_overshoot.npz)
  and [summary JSON](https://github.com/NaNIsaac-Research/TraTT/blob/main/explore/nb/e67_overshoot.json)
- [Source of the scan](https://github.com/NaNIsaac-Research/TraTT/blob/main/explore/nb/e67_overshoot_map.py)
  and [figure generator](https://github.com/NaNIsaac-Research/TraTT/blob/main/explore/make_overshoot_figure.py)
- [Result figure](https://github.com/NaNIsaac-Research/TraTT/blob/main/figures/overshoot.png)

Rebuild the figure from the checked-in scan, in the TraTT repository:

```sh
uv run --group figures python explore/make_overshoot_figure.py
```

**Boundary:** A numerical acoustic-wave/ideal-crystal calculation; selected
full-solver checks, one geometry/order/envelope; no time-resolved measured
crystal scan has been compared. The largest value occurs at a scan boundary.

## 2. ReflectoLearn — XRR fit basins (pre-registered synthetic study)

**Claim recorded:** **935** local refinements started at previously recorded
R2a/X2e endpoints under registered bounded optimizers. The registered
endpoint-to-basin condition H-BM1 is **supported** in R2a and X2e within
those confirmed runs; after refinement, **5 distinct R2a basins and
1 X2e basin** have reported \(S_1^* \ge 10^4\) counts.
Most R2a minima (651 of 656) land on at least one parameter bound.

- [Pre-registration](https://github.com/NaNIsaac-Research/ReflectoLearn/blob/main/docs/fisher_global/PREREG-BASIN.md)
- [Full result, computation budget, exclusions and failures](https://github.com/NaNIsaac-Research/ReflectoLearn/blob/main/docs/fisher_global/reports/RESULTS-BASIN.md)
- [935-row recorded summary](https://github.com/NaNIsaac-Research/ReflectoLearn/blob/main/docs/fisher_global/basin_full_summary.jsonl)
  and [verdict JSON](https://github.com/NaNIsaac-Research/ReflectoLearn/blob/main/docs/fisher_global/basin_verdict.json)
- [Full trace release and checksum inventory](https://github.com/NaNIsaac-Research/ReflectoLearn/releases/tag/research-data-1)
- [Research experiment index](https://github.com/NaNIsaac-Research/ReflectoLearn/blob/main/docs/research/README.md)

Rebuild the **report and verdict from the saved compact summary**, without
rerunning the ~50.9 CPU-hour optimization, in a separate ReflectoLearn checkout:

```sh
uv run python experiments/005_fisher_global/basin_summary.py unpack
uv run python experiments/005_fisher_global/basin_report.py
```

`unpack` reconstructs inputs without per-stage optimizer traces. To inspect
those traces, use the release's `basin_full.zip` instead.

**Boundary:** Noise-free synthetic inputs and bounded local optimization;
not a search for every global minimum or proof of structural uniqueness.
Several registered propositions remain unresolved, and no measured-film
inference is validated by this experiment.

## 3. ReflectoLearn — variability of public XRR counts

**Claim recorded:** One publicly released synchrotron XRR dataset contains
**100 repeated scans**, each on an identical **839-point** q grid.
The median index of dispersion was **φ = 1.34**; **64.2 %** of points
had φ > 1.2, compared with **8.5 %** expected under the stated Poisson
benchmark. This is a property of those observed raw counts, not a
successful film-thickness fit.

- [Primary H-cal2 report and statistical definition](https://github.com/NaNIsaac-Research/ReflectoLearn/blob/main/docs/fisher_global/reports/RESULTS-HCAL2.md)
- [Pre-registration and amendment 1](https://github.com/NaNIsaac-Research/ReflectoLearn/blob/main/docs/fisher_global/PREREG.md)
- [Analysis code](https://github.com/NaNIsaac-Research/ReflectoLearn/blob/main/experiments/005_fisher_global/hcal2.py)
- [Public data source: Zenodo 10.5281/zenodo.18548583](https://doi.org/10.5281/zenodo.18548583)

**Material qualification:** The **literal initial pre-check** would have
excluded every point because a normalization field varied between scans.
Amendment 1 changed the exclusion rule **after pre-checks and before the
dispersion statistic was computed**. The supported verdict therefore
**depends on that amendment**; under the literal original rule there is no
verdict. This must accompany any numerical summary.

**Boundary:** One sample, one fast-scan instrument and one exposure time.
The physical source of the excess variance is not identified. Do not
generalize this dispersion result to all XRR instruments or datasets.

## 4. QoraPhase — phase retrieval: synthetic vs. measured

### Reproducible *synthetic* demonstration

The project README reports a noiseless **64×64** generated object with a
best-of-eight relative object error of **7.9 × 10⁻⁷** under its stated
recipe; this is not a benchmark on unknown measured objects.

- [Figure and reported result](https://github.com/NaNIsaac/QoraPhase/blob/main/README.md)
- [Generation script](https://github.com/NaNIsaac/QoraPhase/blob/main/examples/readme_figure.py)

Rebuild the original synthetic example in a QoraPhase environment:

```sh
python examples/readme_figure.py
```

### Public measured CDI (independently accessible input, unsuccessful reproduction)

[CXIDB 3 and CXIDB 28](https://github.com/NaNIsaac/QoraPhase/blob/main/docs/benchmarks/cxidb.md)
are genuine public detector patterns. The documented runs **did not reproduce
the images from the corresponding papers**. Several recipes fit diffraction
intensities with low Fourier residual while independent starts disagree.

- [CXIDB processing script](https://github.com/NaNIsaac/QoraPhase/blob/main/benchmarks/cxidb.py):
  downloads public inputs and checks recorded SHA-256 values.

```sh
uv run --python 3.14+gil --with h5py python benchmarks/cxidb.py --entry 3
```

This is a resource-intensive reconstruction route, **not** a passing
published-result test.

### Private laboratory 3D BCDI (comparison, not public reproduction)

The [measured comparison report](https://github.com/NaNIsaac/QoraPhase/blob/main/docs/benchmarks/measured.md)
documents the best Fourier residual **0.310** from 10 QoraPhase matched
starts and **0.315** for the lab's saved reference after applying its support;
20 separately rerun MATLAB results are described as well. These residuals
are not measures of image truth or proof that the engines agree on a unique
reconstruction.

- [Comparison script and input contract](https://github.com/NaNIsaac/QoraPhase/blob/main/benchmarks/measured.py)
- [Lab MATLAB rerun driver](https://github.com/NaNIsaac/QoraPhase/blob/main/benchmarks/measured_driver.m)

The prepared intensity, MATLAB reference and scan are **not published**.
External reproduction is therefore blocked by access, not solved by putting
the script online. Do not publish those files without the data owner's
authorization.

## Next experiments that could genuinely strengthen this profile

1. **QoraPhase:** independently reproduce *one published* public CXIDB
   reconstruction, with specified preprocessing, multiple starts, a
   preregistered image/PRTF comparison, and code/environment frozen. Report
   failure if the criterion is not met.
2. **ReflectoLearn:** validate a deposited measured film with independently
   known thickness/roughness/SLD and instrument parameters; preregister
   success and uncertainty-calibration criteria.
3. **TraTT:** compare the time-dependent satellite prediction with a
   publishable transient diffraction dataset and report instrument
   resolution, model assumptions, and deviations.

**No new scientific validation was performed for this index.** These are
traceable records, executable or inspectable entrypoints, and documented
missing evidence—not a claim of successful reproduction in this chat.
