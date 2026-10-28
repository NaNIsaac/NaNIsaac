<div align="center">

<h1>Isaac Yong (용이삭)</h1>

<p><b>X-ray physics · Scientific computing</b><br>M.S. student in Physics, Sogang University</p>

<p><b><a href="https://nanisaac.github.io">Website</a></b> &nbsp;·&nbsp; <b><a href="https://nanisaac.github.io/docs/">Docs</a></b> &nbsp;·&nbsp; <b><a href="https://nanisaac.github.io/notes/">Notes</a></b> &nbsp;·&nbsp; <b><a href="https://nanisaac.github.io/stats/">Stats</a></b> &nbsp;·&nbsp; <b><a href="https://blog.naver.com/sjbpepper">Blog</a></b> &nbsp;·&nbsp; <b><a href="mailto:isaacyong@naver.com">Email</a></b></p>

</div>

<img src="./assets/phase-retrieval.gif" width="100%" alt="The name NaNIsaac recovered from its diffraction intensity by phase retrieval" />

<sub>Only the intensity |F|² goes in. [QoraPhase](https://github.com/NaNIsaac/QoraPhase) recovers the lost phase and the object; <a href="./scripts/name_gif.py">script</a>.</sub>

I study X-ray scattering and diffraction, and build the software around the experiment:
simulation, inverse problems, coherent imaging, and beamtime data analysis.
Longer write-ups live on [my website](https://nanisaac.github.io).

### Research

Research code, results and poster sources live in the
[NaNIsaac Research](https://github.com/NaNIsaac-Research) organization.

- [TraTT](https://github.com/NaNIsaac-Research/TraTT): how acoustic Bragg satellites form while a
  GHz sound wave enters a perfect crystal, from time-dependent Takagi-Taupin dynamical diffraction.
  Poster P2.17, KPS 2026 Fall Meeting, Jeju, October 22, 2026
  ([poster](https://github.com/NaNIsaac-Research/TraTT#readme),
  [docs](https://nanisaac.github.io/docs/tratt/)).
- XRR inverse problem: how much of a thin film one X-ray reflectivity curve determines, and whether
  a generative posterior model is needed. Work in progress
  ([Experiment 001](https://github.com/NaNIsaac/ReflectoLearn/tree/research/identifiability/docs/identifiability)).

### Selected work

| Science | Tools |
|---|---|
| [QoraPhase](https://github.com/NaNIsaac/QoraPhase) ([docs](https://nanisaac.github.io/docs/qoraphase/)) · JAX phase retrieval for CDI and BCDI | [codigest](https://github.com/NaNIsaac/codigest) ([docs](https://nanisaac.github.io/codigest/)) · codebase, diffs and terminal output as LLM context |
| [QoraPhaseCU](https://github.com/NaNIsaac/QoraPhaseCU) · phase retrieval in C++/CUDA, with a measured optimization log | [deai](https://github.com/NaNIsaac/deai) · strip AI co-author trailers from git history |
| [QoraHolo](https://github.com/NaNIsaac/QoraHolo) · holotomography (ODT) reconstruction in C++/CUDA | [hanfix](https://github.com/NaNIsaac/hanfix) · re-run commands typed in the Korean layout |
| [ReflectoLearn](https://github.com/NaNIsaac/ReflectoLearn) ([docs](https://nanisaac.github.io/docs/reflectolearn/)) · differentiable X-ray reflectivity fitting | [clippath](https://github.com/NaNIsaac/clippath) · clipboard screenshot to a file path for terminal agents |
| [QoraFlow](https://github.com/NaNIsaac/QoraFlow) · time-resolved X-ray data at PAL-XFEL | [roi_rectangle](https://github.com/NaNIsaac/roi_rectangle) · rectangular ROIs for NumPy images |
| [TraTT](https://github.com/NaNIsaac-Research/TraTT) · time-dependent Takagi-Taupin diffraction | |
| [xray.ooguy](https://xray.ooguy.com) · offline calculators for old beamline PCs | |

<!-- research:start -->
### Research organization

- `NaNIsaac-Research/ReflectoLearn` [fix(genx_fit): oxide under the film, oxide roughness free in the final stage](https://github.com/NaNIsaac-Research/ReflectoLearn/pull/59) <sub>merged</sub>
- `NaNIsaac-Research/ReflectoLearn` [docs: add a Start here block to the reports index](https://github.com/NaNIsaac-Research/ReflectoLearn/pull/57) <sub>merged</sub>
- `NaNIsaac-Research/TraTT` [docs: add a Start here block to the reports index](https://github.com/NaNIsaac-Research/TraTT/pull/33) <sub>merged</sub>
- `NaNIsaac-Research/TraTT` [docs: call tau_n the characteristic time and label the f0 detuning axis beta/K](https://github.com/NaNIsaac-Research/TraTT/pull/32) <sub>merged</sub>
- `NaNIsaac-Research/TraTT` [docs: use physical names and defined scaled quantities in reader-facing equations](https://github.com/NaNIsaac-Research/TraTT/pull/30) <sub>merged</sub>
- `NaNIsaac-Research/ReflectoLearn` [docs: index the reports and give each hand-written one a summary](https://github.com/NaNIsaac-Research/ReflectoLearn/pull/56) <sub>merged</sub>
- `NaNIsaac-Research/TraTT` [docs: add a reports index and a Reports section to the README](https://github.com/NaNIsaac-Research/TraTT/pull/29) <sub>merged</sub>
- `NaNIsaac-Research/ReflectoLearn` [docs(objective): register experiment 006, the cost of log-type objectives against the Poisson likelihood](https://github.com/NaNIsaac-Research/ReflectoLearn/pull/60) <sub>open</sub>
<!-- research:end -->

<!-- upstream:start -->
### Upstream

- `pydata/xarray` [DOC: Link windowed operations tutorial from computation guide](https://github.com/pydata/xarray/pull/11720) <sub>merged</sub>
<!-- upstream:end -->

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
