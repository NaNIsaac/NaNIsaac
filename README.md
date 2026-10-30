<div align="center">

<h1>Isaac Yong (용이삭)</h1>

<p><strong>Physics researcher building scientific software</strong><br>
X-ray diffraction · Inverse problems · Computational imaging</p>

<p>M.S. student in Physics, Sogang University</p>

<p>
  <a href="https://nanisaac.github.io"><strong>Portfolio</strong></a> ·
  <a href="https://github.com/NaNIsaac-Research">Research</a> ·
  <a href="https://nanisaac.github.io/notes/">Notes</a> ·
  <a href="https://blog.naver.com/sjbpepper">Blog</a> ·
  <a href="mailto:isaacyong@naver.com">Contact</a>
</p>

</div>

**I work at the boundary between X-ray experiments and computation.** My central
question is: *What can a diffraction measurement actually tell us, and how can
we check the answer?*

I build physical models, inverse methods, and experiment-facing software to
turn scattering data into images, material parameters, and reproducible
analyses. A convincing reconstruction is not necessarily a unique solution;
understanding noise, ambiguity, and failure modes matters just as much.

<img src="./assets/phase-retrieval.gif" width="100%" alt="Animated reconstruction of the synthetic NaNIsaac lettering from a simulated diffraction pattern" />

<sub>A small illustration of that idea: <a href="https://github.com/NaNIsaac/QoraPhase">QoraPhase</a>
recovers a <strong>synthetic</strong> object from simulated diffraction intensity (the phase
is not supplied). <a href="./scripts/name_gif.py">Generation script</a>. This animation is
not a measured-data validation.</sub>

## Research questions

- **How does a Bragg satellite form in time?** I model X-ray diffraction as a
  GHz acoustic wave enters a crystal using time-dependent Takagi–Taupin theory.
  [TraTT](https://github.com/NaNIsaac-Research/TraTT) ·
  [Findings](https://github.com/NaNIsaac-Research/TraTT/blob/main/docs/FINDINGS.md) ·
  [KPS 2026 Fall poster](https://github.com/NaNIsaac-Research/TraTT#readme).
- **What can one reflectivity curve actually determine?** I study X-ray
  reflectivity (XRR) fitting, uncertainty, identifiability, and wrong
  optimization basins, alongside a differentiable Abeles model and CNN-based
  initialization. [ReflectoLearn](https://github.com/NaNIsaac-Research/ReflectoLearn) ·
  [Research reports](https://github.com/NaNIsaac-Research/ReflectoLearn/blob/main/docs/research/README.md).
- **Can we reconstruct an object when diffraction phase is missing?**
  [QoraPhase](https://github.com/NaNIsaac/QoraPhase) implements iterative
  coherent diffraction imaging (CDI/BCDI) in JAX.
  [Synthetic example](https://github.com/NaNIsaac/QoraPhase/blob/main/docs/reconstruction.png) ·
  [Measured-data limitations](https://github.com/NaNIsaac/QoraPhase/blob/main/docs/benchmarks/measured.md).

The research notebooks, models, figures, and evidence are organized in
[NaNIsaac-Research](https://github.com/NaNIsaac-Research). I distinguish
**calculated or synthetic demonstrations** from results validated on
experimental data.

## Tools around the experiment

- **From detector frames to time traces:**
  [QoraFlow](https://github.com/NaNIsaac/QoraFlow) reduces PAL-XFEL
  pump–probe diffraction data into laser-on/off images and delay-dependent
  observables.
- **Faster and reproducible computation:**
  [QoraPhaseCU](https://github.com/NaNIsaac/QoraPhaseCU) explores C++/CUDA
  phase retrieval; [xray.ooguy](https://xray.ooguy.com) collects beamline
  calculators.
- **Figures that are readable, not just attractive:**
  [qoraplot](https://github.com/NaNIsaac/qoraplot) provides publication-style
  Matplotlib layouts, while [cvdkit](https://github.com/NaNIsaac/cvdkit)
  pairs color-vision-aware palettes with markers and line styles.

## Developer tools

I also work on the infrastructure that makes research and coding less
repetitive: [codigest](https://github.com/NaNIsaac/codigest) packages the
code, diffs, and terminal context you choose for an AI assistant;
[herdr-courier](https://github.com/NaNIsaac/herdr-courier) queues agent messages
without overwriting unfinished human input; and
[hanfix](https://github.com/NaNIsaac/hanfix) fixes terminal commands typed with
the Korean keyboard layout.

[Browse the full repository map](REPOSITORIES.md) ·
[Longer technical notes](https://nanisaac.github.io/docs/)

<details>
<summary><strong>Recent research work and upstream contributions</strong></summary>

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
