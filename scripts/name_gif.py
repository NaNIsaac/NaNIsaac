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
BG, FG = "#0d1117", "#8b949e"
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
frames = [np.abs(np.asarray(qp.align_to(rec(k, seed).object, obj))) for k in STEPS]
print(f"seed {seed}, final Fourier error {rec(STEPS[-1], seed).error:.1e}")

crop = (slice(N // 2 - 20, N // 2 + 20), slice(N // 2 - 70, N // 2 + 70))
fig, axes = plt.subplots(1, 2, figsize=(8, 2.4), gridspec_kw={"width_ratios": [1, 2.9]},
                         facecolor=BG)
for ax in axes:
    ax.set_axis_off()
q = slice(N // 2 - 56, N // 2 + 56)
axes[0].imshow(np.log10(intensity + 1e-5)[q, q], cmap="turbo", vmin=-4)
axes[0].set_title("measured |F|²", color=FG, fontsize=9, family="monospace")
im = axes[1].imshow(frames[0][crop], cmap="gray", vmin=0, vmax=1)
title = axes[1].set_title("", color=FG, fontsize=9, family="monospace")
fig.tight_layout()


def update(i: int) -> None:
    k = min(i, len(STEPS) - 1)
    im.set_data(frames[k][crop])
    title.set_text(f"phase retrieval, {CYCLE * STEPS[k]} iterations, support found from data")


OUT.parent.mkdir(exist_ok=True)
FuncAnimation(fig, update, frames=len(STEPS) + 8).save(
    OUT, writer=PillowWriter(fps=5), dpi=100, savefig_kwargs={"facecolor": BG}
)
print(f"wrote {OUT}")
