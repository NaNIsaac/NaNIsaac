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

## Organizations

<table align="center">
  <tr>
    <td align="center" width="240">
      <a href="https://github.com/NaNIsaac-Research"><img src="https://github.com/NaNIsaac-Research.png?size=160" width="80" alt="NaNIsaac-Research" /><br><strong>NaNIsaac-Research</strong></a><br>
      <sub>X-ray research code<br>TraTT · ReflectoLearn</sub>
    </td>
    <td align="center" width="240">
      <a href="https://github.com/tendlane"><img src="https://github.com/tendlane.png?size=160" width="80" alt="tendlane" /><br><strong>tendlane</strong></a><br>
      <sub>AI coding agents, side by side<br>pepperpaw</sub>
    </td>
    <td align="center" width="240">
      <a href="https://github.com/neurin-ocha"><img src="https://github.com/neurin-ocha.png?size=160" width="80" alt="neurin-ocha" /><br><strong>느린 오차</strong></a><br>
      <sub>Music: songs and lyric videos<br>coverlyric</sub>
    </td>
  </tr>
</table>

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
- **[pepperpaw](https://github.com/tendlane/pepperpaw)** (the
  `herdr-courier` package) is designed to prevent agent prompts from interrupting human typing.
- **[hanfix](https://github.com/NaNIsaac/hanfix)** repairs terminal commands
  entered with the Korean keyboard layout.

[Technical notes](https://nanisaac.github.io/docs/) ·
[Repository index](REPOSITORIES.md)

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

- `NaNIsaac-Research/TraTT` [docs(poster): i-QMS final, editable PowerPoint copy, review fixes and A-C overshoot traces](https://github.com/NaNIsaac-Research/TraTT/pull/47) <sub>merged</sub>
- `NaNIsaac-Research/TraTT` [docs(poster): i-QMS merged formation section and an overshoot section](https://github.com/NaNIsaac-Research/TraTT/pull/46) <sub>merged</sub>
- `NaNIsaac-Research/TraTT` [docs(poster): i-QMS rocking curve at L = 296 um and a 4:3 depth-time map](https://github.com/NaNIsaac-Research/TraTT/pull/44) <sub>merged</sub>
- `NaNIsaac-Research/TraTT` [docs(poster): physical notation, one sign convention, v4 story and a plain layout](https://github.com/NaNIsaac-Research/TraTT/pull/43) <sub>merged</sub>
- `NaNIsaac-Research/TraTT` [fix: README figures on an opaque white background](https://github.com/NaNIsaac-Research/TraTT/pull/42) <sub>merged</sub>
- `NaNIsaac-Research/TraTT` [ci(publish): run the shared publish gates before the tratt upload](https://github.com/NaNIsaac-Research/TraTT/pull/41) <sub>merged</sub>
- `NaNIsaac-Research/ReflectoLearn` [feat(predict): negative intensity option, recorded with the prediction](https://github.com/NaNIsaac-Research/ReflectoLearn/pull/67) <sub>merged</sub>
- `NaNIsaac-Research/TraTT` [docs: one scientific report replaces PAPER.md; prior-art reading of the referee list (Entry 91)](https://github.com/NaNIsaac-Research/TraTT/pull/40) <sub>merged</sub>
<!-- research:end -->

<!-- upstream:start -->
### Upstream

- `neurin-ocha/coverlyric` [feat(web): zoom the part's waveform with bar lines; keep named parts to compare](https://github.com/neurin-ocha/coverlyric/pull/80) <sub>merged</sub>
- `neurin-ocha/coverlyric` [feat(web): loop the hand-set part with the render's seam; move its ends by a bar or a beat](https://github.com/neurin-ocha/coverlyric/pull/79) <sub>merged</sub>
- `neurin-ocha/coverlyric` [docs: point links at the neurin-ocha organization](https://github.com/neurin-ocha/coverlyric/pull/78) <sub>merged</sub>
- `tendlane/pepperpaw` [feat(agents): show lanes stopped on purpose from a configured stops command](https://github.com/tendlane/pepperpaw/pull/69) <sub>merged</sub>
- `neurin-ocha/coverlyric` [fix(project): a save gives up after 10 s when the lock is held](https://github.com/neurin-ocha/coverlyric/pull/76) <sub>merged</sub>
- `neurin-ocha/coverlyric` [feat(mcp): print the client setting with --config; usage notes in the server instructions](https://github.com/neurin-ocha/coverlyric/pull/74) <sub>merged</sub>
- `neurin-ocha/coverlyric` [feat(tall): Shorts hook caption, top crop, one loop blend, English words lit whole](https://github.com/neurin-ocha/coverlyric/pull/73) <sub>merged</sub>
- `neurin-ocha/coverlyric` [feat: coverlyric mcp, and the page on a project folder](https://github.com/neurin-ocha/coverlyric/pull/71) <sub>merged</sub>
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
