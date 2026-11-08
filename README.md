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

## Selected research

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

## Phase retrieval in motion

<p align="center">
  <img src="./assets/phase-retrieval.gif" width="760"
       alt="Synthetic phase retrieval animation reconstructing the NaNIsaac lettering from simulated diffraction intensity" />
</p>
<p align="center"><sub>Not measured data: a simulated diffraction intensity
reconstructed with <a href="https://github.com/NaNIsaac/QoraPhase">QoraPhase</a>.
<a href="./scripts/name_gif.py">Reproduce the animation</a>.</sub></p>

## Software and open source

Beyond the research models, I build tools for scientific computing and for
working with code. These projects are independent of any one experiment.

### Scientific software

- **[QoraPhaseCU](https://github.com/NaNIsaac/QoraPhaseCU)** explores
  C++20/CUDA implementations of phase retrieval, alongside the JAX work.
- **[xray.ooguy](https://xray.ooguy.com)** provides interactive calculators
  for X-ray and beamline work.
- **[qoraplot](https://github.com/NaNIsaac/qoraplot)** provides Matplotlib
  layouts for publication figures; **[cvdkit](https://github.com/NaNIsaac/cvdkit)**
  combines color-vision-aware palettes with marker and line styles.

### Developer tools

- **[codigest](https://github.com/NaNIsaac/codigest)** packages selected code,
  diffs and terminal output into context for coding agents.
- **[herdr-courier](https://github.com/NaNIsaac/herdr-courier)** is designed to
  prevent agent prompts from interrupting human typing.
- **[hanfix](https://github.com/NaNIsaac/hanfix)** repairs terminal commands
  entered with the Korean keyboard layout.

[Technical notes](https://nanisaac.github.io/docs/) ·
[Repository index (2026-10-23 snapshot)](REPOSITORIES.md)

## Evidence and reproducibility

The research repositories include calculations, benchmarks and explicit
validation boundaries. A few recorded results are summarized below;
the [evidence and reproduction guide](EVIDENCE.md) documents the sources,
commands and remaining checks.

<details>
<summary><strong>Recorded results and limitations</strong></summary>

| Work | Recorded result | What this does **not** prove |
| --- | --- | --- |
| [TraTT](https://github.com/NaNIsaac-Research/TraTT/blob/main/docs/FINDINGS.md) | Calculated acoustic-satellite overshoot mapped over **11,211** parameter pairs; selected full Takagi–Taupin checks agree with the reduced model. | No comparison to a measured transient dataset. |
| [ReflectoLearn](https://github.com/NaNIsaac-Research/ReflectoLearn/blob/main/docs/fisher_global/reports/RESULTS-BASIN.md) | **935** bounded local-fit refinements. Six incorrect parameter regions require at least **10⁴ counts** to distinguish from the reference in the studied conditions (5 in test group R2a, 1 in X2e). | Does not search every possible solution or establish accuracy on a measured film. |
| [Public XRR counts](https://github.com/NaNIsaac-Research/ReflectoLearn/blob/main/docs/fisher_global/reports/RESULTS-HCAL2.md) | **100** repeated public scans: median dispersion index **1.34** versus a Poisson benchmark near 1 (**draft; not independently verified**). | One experimental setup; the supported verdict requires a post-pre-check amendment. Under the original exclusion rule there is **no verdict**; the excess-noise source is unknown. |
| [QoraPhase](https://github.com/NaNIsaac/QoraPhase/blob/main/docs/benchmarks/cxidb.md) | Synthetic images were reconstructed; on two public coherent-diffraction datasets (CXIDB), the published images were **not reproduced**. | Matching diffraction intensity does not prove the reconstructed image is correct. |

</details>

<details>
<summary><strong>Recent research and upstream contributions</strong></summary>

<!-- research:start -->
### Research organization

- `NaNIsaac-Research/ReflectoLearn` [refactor: take the forward physics from reflectosim](https://github.com/NaNIsaac-Research/ReflectoLearn/pull/65) <sub>merged</sub>
- `NaNIsaac-Research/TraTT` [docs: drop private paths and internal workspace references from tracked text](https://github.com/NaNIsaac-Research/TraTT/pull/37) <sub>merged</sub>
- `NaNIsaac-Research/TraTT` [docs: paper-form summary (background, method, results, limits)](https://github.com/NaNIsaac-Research/TraTT/pull/36) <sub>merged</sub>
- `NaNIsaac-Research/ReflectoLearn` [docs(findings): add structured Hypothesis fields for ICC research tab](https://github.com/NaNIsaac-Research/ReflectoLearn/pull/63) <sub>merged</sub>
- `NaNIsaac-Research/ReflectoLearn` [docs: index research findings and evidence](https://github.com/NaNIsaac-Research/ReflectoLearn/pull/62) <sub>merged</sub>
- `NaNIsaac-Research/TraTT` [docs: add a findings page and a Findings section to the README](https://github.com/NaNIsaac-Research/TraTT/pull/35) <sub>merged</sub>
- `NaNIsaac-Research/ReflectoLearn` [docs(identifiability): redraw the experiment 001 figure from the saved results](https://github.com/NaNIsaac-Research/ReflectoLearn/pull/61) <sub>merged</sub>
- `NaNIsaac-Research/ReflectoLearn` [docs: paper draft on identifiability and search reach in XRR fits](https://github.com/NaNIsaac-Research/ReflectoLearn/pull/66) <sub>open</sub>
<!-- research:end -->

<!-- upstream:start -->
### Upstream

- `clatlan/cdiutils` [Fix int32 overflow in SpaceConverter.get_transformation_matrix](https://github.com/clatlan/cdiutils/pull/112) <sub>merged</sub>
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
