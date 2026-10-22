# Repositories

Index of every repository in the `NaNIsaac` account (68 on 2026-10-23). It lists what each repository is for, how far it is, how it relates to the others and what is next. It does not rank projects: a repository with no recent commits is not ended, and two repositories with similar code are not one project.

Status words come from what was read or run during the 2026-10-23 audit; a row says "not run" or "pending" where that is true. Sensitive details of private repositories are kept in `local-notes`, not here. Archived on 2026-10-23 by explicit decision: `eng_cook_book` and `reflexauto_site`; no other repository is archived.

| Reading the tables | |
|---|---|
| Purpose | original goal of the repository |
| Level | what was verified: releases, tests, CI |
| Role and related | where it sits and what it is related to |
| Unfinished / next | open work, with issue or PR numbers where they exist |

## XRR research and products

| Repository | Visibility | Purpose | Level | Role and related | Unfinished / next |
|---|---|---|---|---|---|
| [ReflectoExp](https://github.com/NaNIsaac/ReflectoExp) | public | Series of experiments (exp01-07) that estimate thickness, roughness and SLD of thin films from XRR curves with neural networks | exp02-07 run; exp07 ablation result exists (simulation only, one seed); exp01 imports a missing module and exp03 a loss that is not defined | XRR research branch. Reflecto, XRefine and ReflectoLearn took code from it (transfer, not succession) | GenX fitter layer order and background not reflected (#9); no measured-data validation |
| [Reflecto](https://github.com/NaNIsaac/Reflecto) | public | Single-layer XRR analysis: exp07 CNN initial values plus a GenX differential-evolution fit, packaged | Working code with an In2O3 measured example; weights included | XRR research branch. `reflectolearn.genx_fit` took this fitter | Background parameter (#2) and oxide position (#3) not reflected; split and multilayer fitting on side branches not merged |
| [XRefine](https://github.com/NaNIsaac/XRefine) | private | PINN-style network with a differentiable Abeles model inside (multilayer, complex SLD, six instrument parameters) and staged DE/hybrid refinement | Code complete; training and evaluation metrics were never committed | XRR research branch. ReflectoLearn took the Abeles code, utilities and refine loss. Not replaced: which fitting strategy is best is not established | No retraining since the forward-model unification; no PINN-loss versus supervised comparison; PRs #1, #3, #4 open |
| [ReflectoLearn](https://github.com/NaNIsaac/ReflectoLearn) | public | XRR library (CNN initial values, differentiable Abeles refinement, MCMC, GenX and stitch ports) plus a research branch on identifiability | Main works; no trained-model metrics (a 40-epoch demo only); Experiment 001 in progress (PR #24) | XRR research branch and the maintained library. Master research index: PR #33 | README sentence about superseding other repositories is Isaac's decision; issues #25, #29, #14, #8, #32 |
| [xrr_combine](https://github.com/NaNIsaac/xrr_combine) | private | Independent beamline CLI that joins XRR scan segments taken with different attenuators | Works (example outputs 297 points); 6 tests added in PR #1 | Standalone practical tool, not a predecessor of the XRR research. ReflectoLearn `stitch.py` ports the same idea (reuse) | Shared boundary point is not checked (warning deferred as a behaviour change); long term: a normalization, conversion and quality-check toolkit |
| [ReflexAuto](https://github.com/NaNIsaac/ReflexAuto) | private | Earlier attempt to sell licences for automatic XRR fitting software; the business plan has ended | Repository holds documentation and example data; product history written in `docs/history.md` (PR #3) | Product history kept; separate from the research repositories (similar function only). Not archived | Location of the engine source and archival of the executable (Isaac) |
| [reflexauto_site](https://github.com/NaNIsaac/reflexauto_site) | private, archived | Promotional site for ReflexAuto that was never deployed | Unfinished; archived by Isaac's decision (2026-10-23), code and history kept | Product-side | None |
| [calculate](https://github.com/NaNIsaac/calculate) | private | Early sketch of TT diffraction in a crystal carrying an acoustic wave (`FTTSolver`) with sideband and satellite-angle notebooks | No code change since 2026-01-15; preserved | Early code of the FTT research line; one RK45 integrator was copied into TraTT `explore/`. The directive calls it the predecessor of xray_ooguy; the lineage lane found evidence against that and asks Isaac (xray_ooguy PR #10 is draft) | None (kept); README correction PR #1 |
| [xray_ooguy](https://github.com/NaNIsaac/xray_ooguy) | public | Offline X-ray calculators and a beamtime log as a single page for beamline PCs | Works; `check.js` passes | Independent tool; its DATA view has its own XRR stitching (median ratio, two or more overlapping points) | README history paragraph awaits Isaac's confirmation (PR #10, draft) |
| [TraTT](https://github.com/NaNIsaac/TraTT) | public | Time-dependent Takagi-Taupin calculation of how acoustic Bragg satellites form (KPS 2026 Fall poster, package `tratt`) | Solver, tests and notebook entries 0-67 on main, 68-88 in PR #16 | Current repository of the FTT research line. Lineage document: PR #17 | Paper scope (Isaac), T2s, T2d (needs PDFs) |

## X-ray and imaging

| Repository | Visibility | Purpose | Level | Role and related | Unfinished / next |
|---|---|---|---|---|---|
| [Ca-STO](https://github.com/NaNIsaac/Ca-STO) | private | Beamtime proposal material and the T_AFD figure for Ca-doped SrTiO3 | pending: imaging lane report | pending | pending |
| [insitu-heating-xrd](https://github.com/NaNIsaac/insitu-heating-xrd) | public | In-situ heating 2D XRD analysis: Eiger HDF5 images to 2θ profiles, heatmaps and peak tracking | pending: imaging lane report | pending | pending |
| [QoraPhase](https://github.com/NaNIsaac/QoraPhase) | public | JAX-native, composable phase retrieval for coherent diffraction imaging (CDI, BCDI) | pending: imaging lane report | pending | pending |
| [QoraPhaseCU](https://github.com/NaNIsaac/QoraPhaseCU) | public | Phase retrieval for coherent diffraction imaging in C++ and CUDA (ER, HIO, RAAR, shrinkwrap) with a measured GPU optimization study | pending: imaging lane report | pending | pending |
| [QoraHolo](https://github.com/NaNIsaac/QoraHolo) | public | Holotomography (optical diffraction tomography) reconstruction in C++ and CUDA: off-axis field retrieval, phase unwrapping, Rytov/Fourier diffraction theorem, Gerchberg-Papoulis | pending: imaging lane report | pending | pending |
| [QoraDFXM](https://github.com/NaNIsaac/QoraDFXM) | public | Dark-field X-ray microscopy (DFXM) image analysis: Python engine, CLI and PySide6 app | pending: imaging lane report | pending | pending |
| [QoraFlow](https://github.com/NaNIsaac/QoraFlow) | public | Data processing toolkit for time-resolved X-ray experiments at PAL-XFEL | pending: imaging lane report | pending | pending |
| [QoraGeom](https://github.com/NaNIsaac/QoraGeom) | public | Detector geometry for X-ray scattering: lab-frame q of a detector pixel | pending: imaging lane report | pending | pending |
| [CXD](https://github.com/NaNIsaac/CXD) | public | Coherent X-ray diffraction analysis: SPEC parsing, Timepix frames, q-space regridding, 3D viewer | pending: imaging lane report | pending | pending |
| [rocking_xrd_sim](https://github.com/NaNIsaac/rocking_xrd_sim) | private | BCDI rocking-scan forward simulator: strained 3D particle to detector frames and ground truth (PLS-II 9C geometry) | pending: imaging lane report | pending | pending |
| [9c-sim](https://github.com/NaNIsaac/9c-sim) | private | Motor limits and sample kinematic chain of the 9C beamline diffractometer | pending: imaging lane report | pending | pending |
| [DiffractoLearn](https://github.com/NaNIsaac/DiffractoLearn) | private | Machine learning tools for X-ray reflectivity analysis | pending: imaging lane report | pending | pending |
| [xrd_tools](https://github.com/NaNIsaac/xrd_tools) | private | Interactive scripts for diffractometer geometry: delta/gamma mapping, 2-theta calibration and Q-space conversion | pending: imaging lane report | pending | pending |
| [roi_rectangle](https://github.com/NaNIsaac/roi_rectangle) | public | Rectangular regions of interest (ROI) for images and NumPy arrays | pending: imaging lane report | pending | pending |
| [h5explorer](https://github.com/NaNIsaac/h5explorer) | private | Explore the structure and metadata of HDF5 files from Python or the command line | pending: imaging lane report | pending | pending |
| [bcdi_mapping](https://github.com/NaNIsaac/bcdi_mapping) | private | Finds facet and streak directions in 3D Bragg CDI rocking-curve data | pending: imaging lane report | pending | pending |
| [cxd_map](https://github.com/NaNIsaac/cxd_map) | public | BCDI 3D diffraction pattern analysis: angular map around the center of mass, DBSCAN streak directions, line profiles | pending: imaging lane report | pending | pending |
| [metadata_loader](https://github.com/NaNIsaac/metadata_loader) | private | Prints the group, dataset and attribute structure of PAL-XFEL HDF5 files | pending: imaging lane report | pending | pending |
| [spec_manager](https://github.com/NaNIsaac/spec_manager) | private | SPEC scan file parser (motors, #UXML metadata) with rocking curve and FWHM vs Q scripts | pending: imaging lane report | pending | pending |

## Independent theory

| Repository | Visibility | Purpose | Level | Role and related | Unfinished / next |
|---|---|---|---|---|---|
| [eml](https://github.com/NaNIsaac/eml) | private | Independent mathematical exploration started after reading Odrzywolek, "All elementary functions from a single binary operator" (arXiv:2603.21852): build arithmetic from `e(x, y) = exp(x) - ln(y)` and the constant 1 by macro expansion in a REPL | REPL, macro expander and 11 stdlib definitions; the other operations of the paper (-1, 2, i, pi, 1/x, x/y, x^y, sqrt, trigonometric) are not implemented; 215 tests (PR #3) | Independent; not merged into sandbox. `sandbox/eml` is a history-preserving copy | Missing operations, strict (pure EML) input mode, `ln 0 = -inf`, tree-based expansion; open tasks and minimum completion in `eml/docs/paper.md` |
| [PHYSICAL_GRAMMAR](https://github.com/NaNIsaac/PHYSICAL_GRAMMAR) | private | Long-term research on the semantics, naming, representation and composition rules of physical quantities; narrowed from quantity naming (QSF) to grounding and a composition grammar | Document-style research package: v0.4 kernel frozen, v0.5 meta layer, BB1 (totals only), 20 counterexamples analysed once, 8 `pgcheck` scripts | Independent long-term research; unrelated to the X-ray repositories | Independent review, matched comparison, annotation cost, BB1 reconstruction, acyclic contract check; seven-step plan in `research/NEXT_STEPS_PLAN.md` |

## Subtitles

| Repository | Visibility | Purpose | Level | Role and related | Unfinished / next |
|---|---|---|---|---|---|
| [trans_sub](https://github.com/NaNIsaac/trans_sub) | private | AI/MCP tool that translates a whole SRT file in context and writes a translated SRT (subtitle work that is still useful today) | Skeleton only: `main.py` imports `srt` and prints a greeting; 9 contract tests for the `srt` library pass; no parsing or translation code | Standalone CLI/MCP tool; general SRT handling is left to an existing library. `sandbox/trans_sub/` is a history-preserving copy | Batching and context, translator interface, validation, checkpoint and retry, CLI, MCP; resume plan in the README (PR #2) |

## 2023 games and physics engine

| Repository | Visibility | Purpose | Level | Role and related | Unfinished / next |
|---|---|---|---|---|---|
| [PlaneFight](https://github.com/NaNIsaac/PlaneFight) | private | Vertical-scrolling shooter in raylib (2023-02) | Menu, play, pause and game-over code exist; builds. Not yet run | Past work; a subtree of games-2023 | Run capture on a desktop session |
| [ScreenSaver](https://github.com/NaNIsaac/ScreenSaver) | private | openFrameworks particle and animation sketches (2023-03, three co-developers) | 746 lines of code; not built (openFrameworks not installed) | Past work; a subtree of games-2023 | openFrameworks tree and a run (heavy install, needs approval) |
| [FlatPhysics](https://github.com/NaNIsaac/FlatPhysics) | public | C++ 2D rigid-body engine with a raylib slingshot prototype (2023-03 to 05, three co-developers) | Engine (circles, boxes, convex and concave polygons, AABB broad phase, SAT, impulses) and game; builds. Not yet run | Engine and prototype; ShootingGame continues it. A subtree of games-2023 | Run capture |
| [ShootingGame](https://github.com/NaNIsaac/ShootingGame) | public | Continuation of the FlatPhysics prototype: slingshot, limited shots, enemy HP (2023-05) | Damage, sound effects and music; builds. Not yet run | Past work; a subtree of games-2023 | Run capture |
| [games-2023](https://github.com/NaNIsaac/games-2023) | public | Collection of the four 2023 projects as git subtrees | README and four folders | Collection and preservation | Add captured images (PR #1) |

## Developer tools

| Repository | Visibility | Purpose | Level | Role and related | Unfinished / next |
|---|---|---|---|---|---|
| [codigest](https://github.com/NaNIsaac/codigest) | public | Turn a codebase, diffs and terminal output into LLM-ready context (CLI and MCP server) | Released: Rust binary rust-v0.12.2 and PyPI 0.12.2; CI green on main (2026-10-21); `cargo test` 214 and Python tests 172 passed (2026-10-23) | Developer tool. Overlaps in function with project_to_markdown (overlap, not succession) | Open: #24 direction check, #25 `requires-python` forces Python 3.15 beta so pip cannot install on 3.12/3.13, term-hook fixes (#18 #19 #22 #23) |
| [clippath](https://github.com/NaNIsaac/clippath) | public | Clipboard image to PNG file path for terminal AI agents on Windows and WSL | Released v0.5.0 (Rust); CI green; `cargo test` 6 and Python tests 8 passed (2026-10-23) | Developer tool | Open: #10 record what was verified for the Rust rewrite and decide the Python 0.4.0 tree; #8 uninstall env flag |
| [deai](https://github.com/NaNIsaac/deai) | public | Remove AI co-author trailers from git history | Released on PyPI as `git-deai` 0.2.0; 11 tests pass | Developer tool used on the other repositories | Open PR: commit `uv.lock` (#6) |
| [hanfix](https://github.com/NaNIsaac/hanfix) | public | Re-run a command typed with the Korean keyboard layout on, translated back to QWERTY | Released v0.2.3 (Rust, Linux/macOS/Windows); CI green; `cargo test` 4 passed (2026-10-23) | Developer tool | None recorded |
| [hangeul](https://github.com/NaNIsaac/hangeul) | public | Korean text toolkit for Python: jamo assemble/disassemble, josa, choseong search, similarity, number reading | Released on PyPI 0.2.0; 52 tests pass | Library | None recorded; English README and Korean README.ko.md already merged |
| [seltools](https://github.com/NaNIsaac/seltools) | private | Wrap-around (circular) access for anything with `len()` and `[]`, plus reusable `Selection` objects; optional Rust iterators | Works: 46 tests pass. Not on PyPI yet (404 on 2026-10-23; the README says so) | Library; `pure-py-engine` uses it for polygon edges | First PyPI release needs Trusted Publisher setup by Isaac; open PRs: tests (#3), vulnerable locks (#2) |
| [pure-py-engine](https://github.com/NaNIsaac/pure-py-engine) | private | 2D rigid-body physics engine in pure Python with a pygame-ce demo | Experiment as stated in its README; 35 tests pass; five check scenes with saved frames | Standalone; uses seltools | Known limits: speculative contacts can stop a body a fraction of a step early; distance joints have no min/max length |
| [IsaacPSTools](https://github.com/NaNIsaac/IsaacPSTools) | private | PowerShell 7 session helpers for a Windows dev machine (`reset`, `reenv`, `sys`, `holders`, `unhold`, `port`, `dev`) | Works; test script passes (25 checks, 2026-10-23); no CI | Loaded from `$PROFILE` by DotFiles setup | Adding or removing tools is confirmed with Isaac first |
| [DotFiles](https://github.com/NaNIsaac/DotFiles) | private | Windows dev machine setup: apps, PowerShell profile, coding-agent rules and git hooks; herdr operating notes | In daily use; Tests workflow failing on main since 2026-10-22 (log not retrievable; likely the private-repository billing limit) | Infrastructure for all repositories | Open: 7 PRs and about 30 issues; README setup steps not yet marked for the README test workflow |
| [gh-garden](https://github.com/NaNIsaac/gh-garden) | private | `gh` extension: what differs between the GitHub account and the machines | Released v0.3.0 (Rust); used in this audit; `cargo test` 1 unit test passed (2026-10-23), fixtures hand-checked per FEEDBACK.md | Developer tool; used by every agent for repository state | Open: #5 an unsaved-commit false positive when a remote-tracking ref is missing |
| [naver-gmail-bridge](https://github.com/NaNIsaac/naver-gmail-bridge) | private | Import new Naver Mail inbox messages into Gmail via IMAP and the Gmail API (Actions, every 15 minutes) | Works; 12 tests pass | Personal automation | Deliberately low priority; open PRs for durable state (#5) and an English README (#6) |
| [eclass-ta](https://github.com/NaNIsaac/eclass-ta) | private | Plan registration of weekly eClass activities for a physics lab course, creating only new activities | Stages 1-2 implemented (inspection, schedule and plan); 25 tests pass. Registration (stages 3-6) is not implemented, per PLAN.md | Personal teaching tool | Needs from Isaac: video completion rule and content IDs (PLAN.md); GitHub description and topics are empty |
| [project_to_markdown](https://github.com/NaNIsaac/project_to_markdown) | private | Dump a project directory as one Markdown file: tree, file table, source blocks | Single script (`main.py`); no tests; no README on main yet | Small utility; functionally overlaps codigest (not a successor) | Open PR adds a README (#2) |

## Site, records and experiments

| Repository | Visibility | Purpose | Level | Role and related | Unfinished / next |
|---|---|---|---|---|---|
| [NaNIsaac](https://github.com/NaNIsaac/NaNIsaac) | public | Profile README of the account, with selected work and the contribution garden | Live; the profile refresh workflow succeeds daily | Public face of the account; this index lives here | The "Now" line still names the 22 October poster |
| [NaNIsaac.github.io](https://github.com/NaNIsaac/NaNIsaac.github.io) | public | Personal site: portfolio, `/lab/` Fourier and X-ray reflectivity demos, `/notes/` | Live on GitHub Pages; started from the `pizn/blogTheme` fork | Public site; the lab demos mirror ReflectoLearn's reference engine | Open: Person metadata consolidation (#1, #2), fixtures note draft (#4) |
| [stats](https://github.com/NaNIsaac/stats) | public | GitHub statistics for the account, collected every six hours and shown on Pages | Live; workflow succeeds | Dashboard under the site | No tests (`collect.py` uses only the standard library) |
| [.github](https://github.com/NaNIsaac/.github) | public | Default community files, `CONVENTIONS.md` and repository tooling (conventions check, merge queue) | In use; `conventions.py` check fixed to survive redirected output (PR #18) | Shared by all repositories | Open: 8 PRs, 3 issues (merge-queue tooling, conventions edge cases) |
| [Life](https://github.com/NaNIsaac/Life) | private | Personal notes in Markdown and git | In use | Private notes; details are not listed here | README usage line repaired (PR #1) |
| [local-notes](https://github.com/NaNIsaac/local-notes) | private | Private planning notes and code-review notes | Notes only; README in a pull request | Private; holds the sensitive detail kept out of this index | Coordination snapshot PR (#2) |
| [oss-contrib-notes](https://github.com/NaNIsaac/oss-contrib-notes) | private | Tracking notes and a `gh` script for open-source contribution issues and PRs | Notes and one script | Supports the upstream forks | Open PRs with upstream status notes (#3, #4) |
| [ponyhead](https://github.com/NaNIsaac/ponyhead) | public | Opt-in parody coding skill that puts the repetitive code back | Works as a skill; 2 tests pass (9,382 subtests) | Hobby project; stated "not for real work" | None recorded |
| [sandbox](https://github.com/NaNIsaac/sandbox) | private | Private place to start small experiments | Holds `eml/` and `trans_sub/` (history-preserving copies; the live repositories are separate) and `daily_plan/` | Starting space; not a destination for other repositories (rules in its README) | Promotion of an experiment to its own repository is Isaac's call |
| [eng_cook_book](https://github.com/NaNIsaac/eng_cook_book) | private, archived | Generates the print PPTX of a kids' English cooking workbook from a Markdown manuscript | Archived 2026-10-23 by explicit decision; code and history kept | Separate from the research work | None |

## Forks of upstream projects

Kept for contributions and experiments. The upstream README and license are untouched.

| Repository | Upstream | Visibility | Own work | Sync |
|---|---|---|---|---|
| [cpython](https://github.com/NaNIsaac/cpython) | [python/cpython](https://github.com/python/cpython) | public | IDLE pull request #159189 closed; branch `idle-syntaxerror-shell` | Behind 306; not cloned |
| [xarray](https://github.com/NaNIsaac/xarray) | [pydata/xarray](https://github.com/pydata/xarray) | public | PR #11720 merged; branch `fix-decode-cf-float32-fillvalue` | Behind 52 |
| [cohere](https://github.com/NaNIsaac/cohere) | [AdvancedPhotonSource/cohere](https://github.com/AdvancedPhotonSource/cohere) | public | No upstream PR; fork main has one own commit (pyproject and beamlines submodule) | Ahead 1, behind 29 |
| [cdiutils](https://github.com/NaNIsaac/cdiutils) | [clatlan/cdiutils](https://github.com/clatlan/cdiutils) | public | PR #112 open | In sync |
| [pyFAI](https://github.com/NaNIsaac/pyFAI) | [silx-kit/pyFAI](https://github.com/silx-kit/pyFAI) | public | No upstream PR; branch `2474_f` unexplained | Behind 4 |
| [xrayutilities](https://github.com/NaNIsaac/xrayutilities) | [dkriegner/xrayutilities](https://github.com/dkriegner/xrayutilities) | public | PR #248 open | In sync |
| [tomopy](https://github.com/NaNIsaac/tomopy) | [tomopy/tomopy](https://github.com/tomopy/tomopy) | public | PR #664 open | In sync |
| [prompt-gallery](https://github.com/NaNIsaac/prompt-gallery) | [Q07K/prompt-gallery](https://github.com/Q07K/prompt-gallery) | public | Two merged PRs (#18, #21) | Behind 118 |

