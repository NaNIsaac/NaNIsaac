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

**I write numerical models, inverse solvers, and data pipelines for X-ray experiments.**
My work ranges from predicting diffraction patterns to reconstructing objects,
fitting reflectivity curves, and reducing detector data. Most projects are in
Python (NumPy, JAX, PyTorch); I also work on C++/CUDA implementations.

## Selected work

- **[TraTT](https://github.com/NaNIsaac-Research/TraTT) — dynamical diffraction.**
  Time-dependent Takagi–Taupin simulations of Bragg satellites as a GHz acoustic wave
  enters a crystal. [Calculated findings](https://github.com/NaNIsaac-Research/TraTT/blob/main/docs/FINDINGS.md) ·
  [KPS 2026 Fall poster](https://github.com/NaNIsaac-Research/TraTT#readme).
- **[ReflectoLearn](https://github.com/NaNIsaac-Research/ReflectoLearn) — X-ray reflectivity inference.**
  CNN starting estimates and differentiable Abeles fitting, alongside research on
  parameter identifiability, count statistics, and wrong optimization basins.
  [Findings and limits](https://github.com/NaNIsaac-Research/ReflectoLearn/blob/main/docs/FINDINGS.md).
- **[QoraPhase](https://github.com/NaNIsaac/QoraPhase) — coherent diffraction imaging.**
  Iterative phase retrieval in JAX for 2D/3D CDI and BCDI.
  [Synthetic reconstruction](https://github.com/NaNIsaac/QoraPhase/blob/main/docs/reconstruction.png) ·
  [Measured-data comparison and limitations](https://github.com/NaNIsaac/QoraPhase/blob/main/docs/benchmarks/measured.md).
- **[QoraFlow](https://github.com/NaNIsaac/QoraFlow) — experimental data reduction.**
  PAL-XFEL pump–probe diffraction frames to laser-on/off averages and delay-resolved
  ROI intensity and peak shifts.
  [Reduction steps](https://github.com/NaNIsaac/QoraFlow/blob/main/docs/pipeline.md) ·
  [Synthetic example](https://github.com/NaNIsaac/QoraFlow/blob/main/docs/pipeline_example.png).

<p align="center">
  <img src="./assets/phase-retrieval.gif" width="760"
       alt="Synthetic phase retrieval animation reconstructing the NaNIsaac lettering from simulated diffraction intensity" />
</p>
<p align="center"><sub>Not measured data: a simulated diffraction intensity
reconstructed with <a href="https://github.com/NaNIsaac/QoraPhase">QoraPhase</a>.
<a href="./scripts/name_gif.py">Reproduce the animation</a>.</sub></p>

## Beyond the research code

- **Numerical performance:** [QoraPhaseCU](https://github.com/NaNIsaac/QoraPhaseCU)
  explores C++20/CUDA phase retrieval; [xray.ooguy](https://xray.ooguy.com)
  provides beamline calculators.
- **Scientific figures:** [qoraplot](https://github.com/NaNIsaac/qoraplot)
  supplies Matplotlib publication layouts;
  [cvdkit](https://github.com/NaNIsaac/cvdkit) pairs color-vision-aware palettes
  with markers and line styles.
- **Developer workflows:** [codigest](https://github.com/NaNIsaac/codigest)
  packages selected code/diffs/terminal output as AI context;
  [herdr-courier](https://github.com/NaNIsaac/herdr-courier) queues agent prompts
  without overwriting human input; [hanfix](https://github.com/NaNIsaac/hanfix)
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
- `NaNIsaac-Research/TraTT` [docs: add a Start here block to the reports index](https://github.com/NaNIsaac-Research/TraTT/pull/33) <sub>merged</sub>
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
