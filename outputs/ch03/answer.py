"""Chapter 3 submission.

Includes:
- score(a): olympic-style sum excluding min and max, with loop invariant comments
- integral_trapezoid / integral_simpson: starred integral problem solved in Python
"""

from __future__ import annotations

import math


def score(a: list[float]) -> float:
    """Return the sum after removing one minimum and one maximum.

    The assignment guarantees at least 3 judges.
    """
    total = 0
    current_min = a[0]
    current_max = a[0]

    # ループ不変条件:
    # total は，これまで見た要素の合計である。
    # current_min と current_max は，これまで見た要素の最小値・最大値である。
    for x in a:
        total += x
        if x < current_min:
            current_min = x
        if x > current_max:
            current_max = x

    return total - current_min - current_max


def integral_trapezoid(f, a: float, b: float, n: int) -> float:
    """Approximate integral of f on [a, b] using the trapezoidal rule."""
    h = (b - a) / n
    total = 0.5 * (f(a) + f(b))

    # ループ不変条件:
    # total は，端点を半分ずつ含めた，これまで加算済みの台形和である。
    for i in range(1, n):
        total += f(a + i * h)

    return total * h


def integral_simpson(f, a: float, b: float, n: int) -> float:
    """Approximate integral of f on [a, b] using Simpson's rule.

    n must be even.
    """
    if n % 2 != 0:
        raise ValueError("Simpson's rule requires an even number of subintervals")

    h = (b - a) / n
    total = f(a) + f(b)

    # ループ不変条件:
    # total は，シンプソン公式の重みを反映した途中までの和である。
    for i in range(1, n):
        weight = 4 if i % 2 == 1 else 2
        total += weight * f(a + i * h)

    return total * h / 3.0


def _test_score() -> None:
    assert score([3, 2, 5]) == 3
    assert score([10, 1, 3, 7]) == 10
    assert score([8, 8, 8]) == 8
    assert score([1.5, 2.5, 10.0, 4.0]) == 6.5


def _test_integral() -> None:
    def f_quad(x: float) -> float:
        return x * x

    def f_line(x: float) -> float:
        return 2.0 * x + 1.0

    # x^2 の 0 から 1 の積分は 1/3
    trap = integral_trapezoid(f_quad, 0.0, 1.0, 1000)
    simp = integral_simpson(f_quad, 0.0, 1.0, 1000)
    assert abs(trap - (1.0 / 3.0)) < 1e-3
    assert abs(simp - (1.0 / 3.0)) < 1e-10

    # 1次式はシンプソン公式で正確に求まる
    assert abs(integral_simpson(f_line, 0.0, 2.0, 20) - 6.0) < 1e-12


if __name__ == "__main__":
    _test_score()
    _test_integral()

    print("score([3, 2, 5]) =", score([3, 2, 5]))
    print("score([10, 1, 3, 7]) =", score([10, 1, 3, 7]))
    print("trapezoid x^2 on [0, 1] =", integral_trapezoid(lambda x: x * x, 0.0, 1.0, 1000))
    print("simpson x^2 on [0, 1] =", integral_simpson(lambda x: x * x, 0.0, 1.0, 1000))
