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

<p align="center">
  <img src="./assets/phase-retrieval.gif" width="760"
       alt="Synthetic phase retrieval animation reconstructing the NaNIsaac lettering from simulated diffraction intensity" />
</p>
<p align="center"><sub>Not measured data: a simulated diffraction intensity
reconstructed with <a href="https://github.com/NaNIsaac/QoraPhase">QoraPhase</a>.
<a href="./scripts/name_gif.py">Reproduce the animation</a>.</sub></p>

X-ray measurements record intensities, not structures directly. I develop
numerical models and software to extract structural information from diffraction,
reflectivity and coherent imaging data.

My work spans inverse problems, time-dependent scattering and beamline data
processing, primarily in Python (NumPy, JAX and PyTorch).

## Selected research

- **[TraTT](https://github.com/NaNIsaac-Research/TraTT) — transient acoustic diffraction.**
  Simulates Bragg satellites during acoustic-wave propagation using
  time-dependent Takagi–Taupin equations.
  [Calculated findings](https://github.com/NaNIsaac-Research/TraTT/blob/main/docs/FINDINGS.md) ·
  [KPS 2026 Fall poster](https://github.com/NaNIsaac-Research/TraTT/blob/main/figures/poster/poster_preview.jpg).
- **[ReflectoLearn](https://github.com/NaNIsaac-Research/ReflectoLearn) — XRR inverse problems.**
  Combines neural-network initialization with physics-based fitting and
  investigates parameter ambiguity and identifiability.
  [Findings and limits](https://github.com/NaNIsaac-Research/ReflectoLearn/blob/main/docs/FINDINGS.md).
- **[QoraPhase](https://github.com/NaNIsaac/QoraPhase) — phase retrieval.**
  A JAX package for iterative reconstruction of objects from diffraction
  intensities with missing phase information.
  [Synthetic demonstration](https://github.com/NaNIsaac/QoraPhase/blob/main/docs/reconstruction.png) ·
  [Measured-data limitations](https://github.com/NaNIsaac/QoraPhase/blob/main/docs/benchmarks/measured.md).
- **[QoraFlow](https://github.com/NaNIsaac/QoraFlow) — XFEL data processing.**
  Groups pump–probe detector frames by laser state and delay, applies corrections
  and extracts time traces from diffraction peaks.
  [Processing steps](https://github.com/NaNIsaac/QoraFlow/blob/main/docs/pipeline.md) ·
  [Simulated example](https://github.com/NaNIsaac/QoraFlow/blob/main/docs/pipeline_example.png).

## Software and open source

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

Results and limitations are recorded in the
[evidence and reproduction guide](EVIDENCE.md).

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

- `tendlane/pepperpaw` [fix: report a ghost left in an input box, refuse a message ending in a backslash](https://github.com/tendlane/pepperpaw/pull/47) <sub>merged</sub>
- `tendlane/pepperpaw` [feat: deliver messages waiting for one pane as a single prompt](https://github.com/tendlane/pepperpaw/pull/46) <sub>merged</sub>
- `tendlane/pepperpaw` [fix: name a Codex pane by its own session, not the pane that started the shared app-server](https://github.com/tendlane/pepperpaw/pull/45) <sub>merged</sub>
- `tendlane/pepperpaw` [feat: locate panes with ppw where](https://github.com/tendlane/pepperpaw/pull/44) <sub>merged</sub>
- `tendlane/pepperpaw` [fix: verify courier submission and expose receiver outcomes](https://github.com/tendlane/pepperpaw/pull/43) <sub>merged</sub>
- `tendlane/pepperpaw` [Add ppw: list, read and answer questions from providers](https://github.com/tendlane/pepperpaw/pull/41) <sub>merged</sub>
- `tendlane/pepperpaw` [Configure task notices and execution checks in [ledger]](https://github.com/tendlane/pepperpaw/pull/40) <sub>merged</sub>
- `tendlane/pepperpaw` [Spec message delivery; split the queue record into message and delivery](https://github.com/tendlane/pepperpaw/pull/37) <sub>merged</sub>
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

<sub>Previously SJB7777 (renamed October 2026).</sub>
