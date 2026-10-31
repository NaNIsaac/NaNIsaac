<div align="center">

<h1>Isaac Yong (용이삭)</h1>

<p><strong>X-ray physics · Inverse problems · Scientific software</strong><br>
M.S. student in Physics, Sogang University</p>

<p>
  <a href="https://nanisaac.github.io"><strong>Portfolio</strong></a> ·
  <a href="https://github.com/NaNIsaac-Research">Research</a> ·
  <a href="https://nanisaac.github.io/notes/">Notes</a> ·
  <a href="https://blog.naver.com/sjbpepper">Blog</a> ·
  <a href="mailto:isaacyong@naver.com">Contact</a>
</p>

</div>

When X-rays scatter from a crystal or a thin film, a detector records
intensities—not a ready-made image of the structure or a list of layer
thicknesses. Those have to be worked out from the measurements, and sometimes
more than one answer appears plausible.

**I build the software for that work:** predicting diffraction patterns,
fitting X-ray reflectivity curves, reconstructing images, and turning raw
beamline data into quantities we can compare. Most of my research code is
Python (NumPy, JAX, PyTorch); I also explore C++20/CUDA in QoraPhaseCU.

## Selected work

- **[TraTT](https://github.com/NaNIsaac-Research/TraTT): diffraction while sound enters a crystal.**
  A sound wave can produce extra peaks beside the main Bragg peak. I simulate
  how those peaks form before the wave has crossed the crystal, using
  time-dependent Takagi–Taupin equations.
  [Calculated findings](https://github.com/NaNIsaac-Research/TraTT/blob/main/docs/FINDINGS.md) ·
  [KPS 2026 Fall poster](https://github.com/NaNIsaac-Research/TraTT/blob/main/figures/poster/poster_preview.jpg).
- **[ReflectoLearn](https://github.com/NaNIsaac-Research/ReflectoLearn): film structure from X-ray reflection.**
  An X-ray reflectivity curve contains information about film thickness,
  roughness, and scattering strength. I use a neural-network starting guess
  and a physics-based fit, then study when that estimate goes wrong or cannot
  be distinguished from another structure.
  [Findings and limits](https://github.com/NaNIsaac-Research/ReflectoLearn/blob/main/docs/FINDINGS.md).
- **[QoraPhase](https://github.com/NaNIsaac/QoraPhase): images from diffraction intensities.**
  Diffraction measurements lose the wave's phase. This JAX package iteratively
  estimates the missing phase and the object that produced the pattern.
  [Synthetic demonstration](https://github.com/NaNIsaac/QoraPhase/blob/main/docs/reconstruction.png) ·
  [Measured-data limitations](https://github.com/NaNIsaac/QoraPhase/blob/main/docs/benchmarks/measured.md).
- **[QoraFlow](https://github.com/NaNIsaac/QoraFlow): raw detector frames to time traces.**
  At PAL-XFEL, a laser excites the sample and X-rays probe it after different
  delays. The pipeline groups detector shots by laser state and delay, corrects
  the images, and tracks changes in a selected diffraction peak.
  [Processing steps](https://github.com/NaNIsaac/QoraFlow/blob/main/docs/pipeline.md) ·
  [Simulated example](https://github.com/NaNIsaac/QoraFlow/blob/main/docs/pipeline_example.png).

## What has actually been tested

These are recorded calculations and benchmarks with specific limits—not
claims that every program has been validated on an experimental sample.

| Work | Recorded result | What this does **not** prove |
| --- | --- | --- |
| [TraTT](https://github.com/NaNIsaac-Research/TraTT/blob/main/docs/FINDINGS.md) | Calculated acoustic-satellite overshoot mapped over **11,211** parameter pairs; selected full Takagi–Taupin checks agree with the reduced model. | No comparison to a measured transient dataset. |
| [ReflectoLearn](https://github.com/NaNIsaac-Research/ReflectoLearn/blob/main/docs/fisher_global/reports/RESULTS-BASIN.md) | **935** bounded local-fit refinements. Six incorrect parameter regions require at least **10⁴ counts** to distinguish from the reference in the studied conditions (5 in test group R2a, 1 in X2e). | Does not search every possible solution or establish accuracy on a measured film. |
| [Public XRR counts](https://github.com/NaNIsaac-Research/ReflectoLearn/blob/main/docs/fisher_global/reports/RESULTS-HCAL2.md) | **100** repeated public scans: median dispersion index **1.34** versus a Poisson benchmark near 1 (**draft; not independently verified**). | One experimental setup; the supported verdict requires a post-pre-check amendment. Under the original exclusion rule there is **no verdict**; the excess-noise source is unknown. |
| [QoraPhase](https://github.com/NaNIsaac/QoraPhase/blob/main/docs/benchmarks/cxidb.md) | Synthetic images were reconstructed; on two public coherent-diffraction datasets (CXIDB), the published images were **not reproduced**. | Matching diffraction intensity does not prove the reconstructed image is correct. |

**[Read the evidence and reproduction guide](EVIDENCE.md)** — sources, commands,
data-access limits, and the next validation needed for each claim.

<p align="center">
  <img src="./assets/phase-retrieval.gif" width="760"
       alt="Synthetic phase retrieval animation reconstructing the NaNIsaac lettering from simulated diffraction intensity" />
</p>
<p align="center"><sub>Not measured data: a simulated diffraction intensity
reconstructed with <a href="https://github.com/NaNIsaac/QoraPhase">QoraPhase</a>.
<a href="./scripts/name_gif.py">Reproduce the animation</a>.</sub></p>

## Other software I maintain

- **Numerical performance:** [QoraPhaseCU](https://github.com/NaNIsaac/QoraPhaseCU)
  explores C++20/CUDA phase retrieval; [xray.ooguy](https://xray.ooguy.com)
  provides beamline calculators.
- **Scientific figures:** [qoraplot](https://github.com/NaNIsaac/qoraplot)
  supplies Matplotlib publication layouts;
  [cvdkit](https://github.com/NaNIsaac/cvdkit) pairs color-vision-aware palettes
  with markers and line styles.
- **Developer workflows:** [codigest](https://github.com/NaNIsaac/codigest)
  packages selected code/diffs/terminal output as AI context;
  [herdr-courier](https://github.com/NaNIsaac/herdr-courier) is designed to keep
  agent prompts from interrupting typed human input; [hanfix](https://github.com/NaNIsaac/hanfix)
  repairs terminal commands typed under the Korean keyboard layout.

[Technical notes](https://nanisaac.github.io/docs/) ·
[Repository index (last audited 2026-10-23)](REPOSITORIES.md)

<details>
<summary><strong>Recent research and upstream contributions</strong></summary>

<!-- research:start -->
### Research organization

- `NaNIsaac-Research/ReflectoLearn` [docs: index research findings and evidence](https://github.com/NaNIsaac-Research/ReflectoLearn/pull/62) <sub>merged</sub>
- `NaNIsaac-Research/TraTT` [docs: add a findings page and a Findings section to the README](https://github.com/NaNIsaac-Research/TraTT/pull/35) <sub>merged</sub>
- `NaNIsaac-Research/ReflectoLearn` [docs(identifiability): redraw the experiment 001 figure from the saved results](https://github.com/NaNIsaac-Research/ReflectoLearn/pull/61) <sub>merged</sub>
- `NaNIsaac-Research/TraTT` [docs: redraw the Entry 67 overshoot figure with residuals and full-TT checks](https://github.com/NaNIsaac-Research/TraTT/pull/34) <sub>merged</sub>
- `NaNIsaac-Research/ReflectoLearn` [docs(objective): register experiment 006, the cost of log-type objectives against the Poisson likelihood](https://github.com/NaNIsaac-Research/ReflectoLearn/pull/60) <sub>merged</sub>
- `NaNIsaac-Research/ReflectoLearn` [fix(genx_fit): oxide under the film, oxide roughness free in the final stage](https://github.com/NaNIsaac-Research/ReflectoLearn/pull/59) <sub>merged</sub>
- `NaNIsaac-Research/ReflectoLearn` [docs: add a Start here block to the reports index](https://github.com/NaNIsaac-Research/ReflectoLearn/pull/57) <sub>merged</sub>
- `NaNIsaac-Research/ReflectoLearn` [docs(findings): add structured Hypothesis fields for ICC research tab](https://github.com/NaNIsaac-Research/ReflectoLearn/pull/63) <sub>open</sub>
<!-- research:end -->

<!-- upstream:start -->
### Upstream

- `pydata/xarray` [DOC: Link windowed operations tutorial from computation guide](https://github.com/pydata/xarray/pull/11720) <sub>merged</sub>
<!-- upstream:end -->

</details>

<sub>Pepper (후추), my black-and-tan Shiba Inu, takes care of the contribution garden.</sub>

<picture>
  <source media="(prefers-color-scheme: dark)"
          srcset="./assets/pepper/pepper-harvest-dark.svg" />
  <source media="(prefers-color-scheme: light)"
          srcset="./assets/pepper/pepper-harvest-light.svg" />
  <img src="./assets/pepper/pepper-harvest-light.svg"
       width="100%"
       alt="Pepper harvesting GitHub contributions" />
</picture>

<sub>Formerly "SJB7777". Renamed to "NaNIsaac" on October 14, 2026, at 00:06:41 KST.</sub>
