"""Chapter 4 submission.

Starred problem: beautiful life game (color animation)
"""

from __future__ import annotations

from dataclasses import dataclass

import matplotlib
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np


def next_cell_living(living: bool, neighbor_count: int) -> bool:
    """Return the next state of one cell in Conway's Game of Life."""
    if living:
        return neighbor_count in (2, 3)
    return neighbor_count == 3


def next_field(field: list[list[bool]]) -> list[list[bool]]:
    """Return the next field for the whole board."""
    height = len(field)
    width = len(field[0])
    new_field = [[False for _ in range(width)] for _ in range(height)]

    for r in range(height):
        for c in range(width):
            neighbor_count = 0
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr == 0 and dc == 0:
                        continue
                    rr = r + dr
                    cc = c + dc
                    if 0 <= rr < height and 0 <= cc < width and field[rr][cc]:
                        neighbor_count += 1
            new_field[r][c] = next_cell_living(field[r][c], neighbor_count)

    return new_field


def make_field(height: int, width: int, live_cells: list[tuple[int, int]]) -> list[list[bool]]:
    field = [[False for _ in range(width)] for _ in range(height)]
    for r, c in live_cells:
        field[r][c] = True
    return field


def field_to_rgba(field: list[list[bool]], age: int) -> np.ndarray:
    """Convert a life field to an RGBA image with a custom palette.

    Alive cells are rendered with a warm glowing gradient that changes with age.
    """
    height = len(field)
    width = len(field[0])
    img = np.zeros((height, width, 4), dtype=float)

    alive = np.array(field, dtype=bool)
    # Background: deep navy.
    img[..., 0] = 0.04
    img[..., 1] = 0.06
    img[..., 2] = 0.12
    img[..., 3] = 1.0

    # Alive cells: age-tinted gold to coral.
    age_scale = min(age / 20.0, 1.0)
    img[alive, 0] = 0.95
    img[alive, 1] = 0.35 + 0.45 * (1.0 - age_scale)
    img[alive, 2] = 0.15 + 0.25 * age_scale
    img[alive, 3] = 1.0
    return img


def show_color_animation(initial_field: list[list[bool]], step: int = 50, interval: int = 120):
    """Create a matplotlib animation for the life game with custom colors."""
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_axis_off()
    ax.set_title("Beautiful Life Game", pad=12)

    field = initial_field
    image = ax.imshow(field_to_rgba(field, 0), interpolation="nearest")

    def update(frame: int):
        nonlocal field
        if frame > 0:
            field = next_field(field)
        image.set_data(field_to_rgba(field, frame))
        return (image,)

    anim = animation.FuncAnimation(
        fig,
        update,
        frames=step,
        interval=interval,
        blit=True,
        repeat=True,
    )
    return anim


def glider(top: int = 1, left: int = 1) -> list[tuple[int, int]]:
    """Coordinates of a glider pattern."""
    return [
        (top, left + 1),
        (top + 1, left + 2),
        (top + 2, left),
        (top + 2, left + 1),
        (top + 2, left + 2),
    ]


def _test_next_field() -> None:
    a = [
        [False, True, False, False, False],
        [False, False, True, False, False],
        [True, True, True, False, False],
        [False, False, False, False, False],
        [False, False, False, False, False],
    ]
    expected = [
        [False, False, False, False, False],
        [True, False, True, False, False],
        [False, True, True, False, False],
        [False, True, False, False, False],
        [False, False, False, False, False],
    ]
    assert next_field(a) == expected


def _test_animation_helpers() -> None:
    field = make_field(5, 5, glider())
    assert field[1][2] is True
    rgba = field_to_rgba(field, 0)
    assert rgba.shape == (5, 5, 4)


if __name__ == "__main__":
    _test_next_field()
    _test_animation_helpers()

    plt.rcParams["animation.html"] = "jshtml"
    field = make_field(15, 15, glider(1, 1))
    anim = show_color_animation(field, step=50)
    print("animation object:", type(anim).__name__)
