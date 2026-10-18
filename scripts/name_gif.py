# /// script
# requires-python = ">=3.12"
# dependencies = ["qoraphase"]
# ///
"""Regenerate assets/name-cdi.gif: the name recovered from its diffraction intensity.

uv run scripts/name_gif.py
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter

import qoraphase as qp

N, CYCLE = 192, 30
STEPS = [1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 18, 22, 26, 30]
BG, FG, ACCENT, TRACK = "#0d1117", "#8b949e", "#58a6ff", "#21262d"
OUT = Path(__file__).parents[1] / "assets" / "name-cdi.gif"

fig = plt.figure(figsize=(4, 0.9), dpi=56)
fig.text(0.5, 0.5, "NaNIsaac", ha="center", va="center", fontsize=26,
         weight="bold", family="DejaVu Sans Mono")
fig.canvas.draw()
txt = 1 - np.asarray(fig.canvas.buffer_rgba())[..., 0] / 255
plt.close(fig)
rows, cols = np.nonzero(txt > 0.05)
txt = txt[rows.min() : rows.max() + 1, cols.min() : cols.max() + 1]
h, w = txt.shape
obj = np.zeros((N, N))
obj[N // 2 - h // 2 : N // 2 - h // 2 + h, N // 2 - w // 2 : N // 2 - w // 2 + w] = txt

intensity = np.abs(np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(obj), norm="ortho"))) ** 2


def rec(cycles: int, seed: int) -> qp.Reconstruction:
    # No support given: it starts from the autocorrelation and is shrinkwrapped.
    recipe = qp.Recipe(qp.repeat(cycles, qp.RAAR(CYCLE, beta=0.9), qp.Shrinkwrap()), qp.ER(50))
    return qp.reconstruct(intensity, recipe=recipe, seed=seed)


seed = min(range(12), key=lambda s: float(rec(STEPS[-1], s).error))
# Runs are deterministic per seed, so rerunning to k cycles gives the frame at k.
runs = [rec(k, seed) for k in STEPS]
frames = [np.abs(np.asarray(qp.align_to(r.object, obj))) for r in runs]
errors = [float(r.error) for r in runs]
print(f"seed {seed}, final Fourier error {errors[-1]:.1e}")

crop = (slice(N // 2 - 20, N // 2 + 20), slice(N // 2 - 70, N // 2 + 70))
total = CYCLE * STEPS[-1]
fig = plt.figure(figsize=(8, 2.6), facecolor=BG)
grid = fig.add_gridspec(2, 2, width_ratios=[1, 2.9], height_ratios=[6, 1], hspace=0.25)
ax_f, ax_r, ax_p = fig.add_subplot(grid[:, 0]), fig.add_subplot(grid[0, 1]), fig.add_subplot(grid[1, 1])
for ax in (ax_f, ax_r, ax_p):
    ax.set_axis_off()
q = slice(N // 2 - 56, N // 2 + 56)
ax_f.imshow(np.log10(intensity + 1e-5)[q, q], cmap="turbo", vmin=-4)
ax_f.set_title("measured |F|²", color=FG, fontsize=9, family="monospace")
im = ax_r.imshow(frames[0][crop], cmap="gray", vmin=0, vmax=1)
ax_r.set_title("phase retrieval, support found from data", color=FG, fontsize=9, family="monospace")
ax_p.set_xlim(0, total)
ax_p.set_ylim(0, 1)
ax_p.barh(0.3, total, height=0.35, color=TRACK)
bar = ax_p.barh(0.3, 0, height=0.35, color=ACCENT)[0]
label = ax_p.text(0, 0.85, "", color=FG, fontsize=8.5, family="monospace", va="center")
score = ax_p.text(total, 0.85, "", color=FG, fontsize=8.5, family="monospace", va="center", ha="right")
fig.subplots_adjust(left=0.02, right=0.98, top=0.88, bottom=0.04, wspace=0.06)


def update(i: int) -> None:
    k = min(i, len(STEPS) - 1)
    im.set_data(frames[k][crop])
    bar.set_width(CYCLE * STEPS[k])
    label.set_text(f"iteration {CYCLE * STEPS[k]:>3} / {total}")
    score.set_text(f"Fourier error {errors[k]:.1e}")


OUT.parent.mkdir(exist_ok=True)
FuncAnimation(fig, update, frames=len(STEPS) + 8).save(
    OUT, writer=PillowWriter(fps=5), dpi=100, savefig_kwargs={"facecolor": BG}
)
print(f"wrote {OUT}")
