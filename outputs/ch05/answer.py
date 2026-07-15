"""Chapter 5 submission: problems up to section 5.4."""

from __future__ import annotations

import math


def factorial(n: int) -> int:
    if n == 1:
        return 1
    return n * factorial(n - 1)


def count_multiples(n: int, m: int) -> int:
    if n == 0:
        return 0
    if n % m == 0:
        return 1 + count_multiples(n - 1, m)
    return count_multiples(n - 1, m)


def gcd(a: int, b: int) -> int:
    if b == 0:
        return a
    return gcd(b, a % b)


EPSILON = 0.0001


def sqrt(x: float, a: float, b: float) -> float:
    m = (a + b) / 2.0
    if abs(m * m - x) < EPSILON:
        return m
    if m * m > x:
        return sqrt(x, a, m)
    return sqrt(x, m, b)


def sigmoid_inverse(y: float, a: float, b: float) -> float:
    def sigmoid(x: float) -> float:
        return 1.0 / (1.0 + math.exp(-x))

    m = (a + b) / 2.0
    if abs(sigmoid(m) - y) < 1e-11:
        return round(m, 10)
    if sigmoid(m) > y:
        return sigmoid_inverse(y, a, m)
    return sigmoid_inverse(y, m, b)


def binary_search(a: list[int], x: int, l: int, r: int) -> int:
    if l + 1 == r:
        return l if a[l] == x else -1
    m = (l + r) // 2
    if a[m] > x:
        return binary_search(a, x, l, m)
    return binary_search(a, x, m, r)


def fib(n: int) -> int:
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fib(n - 1) + fib(n - 2)


def mdigit(m: int, n: int) -> list[str]:
    def build(prefix: str, remaining: int) -> list[str]:
        if remaining == 0:
            return [prefix]
        result = []
        for d in range(m):
            result += build(prefix + str(d), remaining - 1)
        return result

    return build("", n)


def koch(x0: float, y0: float, x1: float, y1: float, n: int) -> list[list[float]]:
    if n == 0:
        return [[x0, y0]]

    sx = (2 * x0 + x1) / 3.0
    sy = (2 * y0 + y1) / 3.0
    tx = (x0 + 2 * x1) / 3.0
    ty = (y0 + 2 * y1) / 3.0
    ux = (tx - sx) / 2.0 - math.sqrt(3.0) * (ty - sy) / 2.0 + sx
    uy = math.sqrt(3.0) * (tx - sx) / 2.0 + (ty - sy) / 2.0 + sy

    return (
        koch(x0, y0, sx, sy, n - 1)
        + koch(sx, sy, ux, uy, n - 1)
        + koch(ux, uy, tx, ty, n - 1)
        + koch(tx, ty, x1, y1, n - 1)
    )


def merge(a: list[int], b: list[int]) -> list[int]:
    c = []
    i = 0
    j = 0
    # ループ不変条件:
    # c は a[0:i] と b[0:j] を昇順に併合した配列である。
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            c.append(a[i])
            i += 1
        else:
            c.append(b[j])
            j += 1
    c += a[i:]
    c += b[j:]
    return c


def first_half(a: list[int]) -> list[int]:
    return a[: (len(a) + 1) // 2]


def second_half(a: list[int]) -> list[int]:
    return a[(len(a) + 1) // 2 :]


def mergesort(a: list[int]) -> list[int]:
    if len(a) <= 1:
        return a[:]
    return merge(mergesort(first_half(a)), mergesort(second_half(a)))


def _test_factorial() -> None:
    assert factorial(1) == 1
    assert factorial(5) == 120


def _test_count_multiples() -> None:
    assert count_multiples(10, 3) == 3
    assert count_multiples(20, 5) == 4


def _test_gcd() -> None:
    assert gcd(12, 18) == 6
    assert gcd(18, 12) == 6


def _test_sqrt() -> None:
    assert abs(sqrt(3, 0, 10) - 1.7320508075688772) < 1e-3


def _test_sigmoid_inverse() -> None:
    assert sigmoid_inverse(0.5, -10, 10) == 0.0
    assert abs(sigmoid_inverse(0.2, -10, 10) + 1.3862943611) < 1e-9


def _test_binary_search() -> None:
    a = [1, 3, 5, 7]
    assert binary_search(a, 1, 0, len(a)) == 0
    assert binary_search(a, 3, 0, len(a)) == 1
    assert binary_search(a, 5, 0, len(a)) == 2
    assert binary_search(a, 7, 0, len(a)) == 3
    assert binary_search(a, 2, 0, len(a)) == -1


def _test_fib() -> None:
    assert fib(0) == 0
    assert fib(1) == 1
    assert fib(5) == 5


def _test_mdigit() -> None:
    assert mdigit(3, 2) == ["00", "01", "02", "10", "11", "12", "20", "21", "22"]


def _test_koch() -> None:
    a = koch(0.0, 0.0, 100.0, 0.0, 1)
    assert len(a) == 4
    assert abs(a[0][0] - 0.0) < 1e-9
    assert abs(a[-1][0] - 100.0 * 2.0 / 3.0) < 1e-9


def _test_merge_sort() -> None:
    assert merge([1, 3, 5], [2, 4]) == [1, 2, 3, 4, 5]
    assert first_half([0, 1, 2, 3, 4]) == [0, 1, 2]
    assert second_half([0, 1, 2, 3, 4]) == [3, 4]
    assert mergesort([8, 3, 4, 1, 5, 9, 6, 7, 2]) == [1, 2, 3, 4, 5, 6, 7, 8, 9]


if __name__ == "__main__":
    _test_factorial()
    _test_count_multiples()
    _test_gcd()
    _test_sqrt()
    _test_sigmoid_inverse()
    _test_binary_search()
    _test_fib()
    _test_mdigit()
    _test_koch()
    _test_merge_sort()

    print("factorial(5) =", factorial(5))
    print("count_multiples(10, 3) =", count_multiples(10, 3))
    print("gcd(12, 18) =", gcd(12, 18))
    print("sqrt(3, 0, 10) =", sqrt(3, 0, 10))
    print("sigmoid_inverse(0.2, -10, 10) =", sigmoid_inverse(0.2, -10, 10))
    print("binary_search([1,3,5,7], 5, 0, 4) =", binary_search([1, 3, 5, 7], 5, 0, 4))
    print("fib(5) =", fib(5))
    print("mdigit(3,2) =", mdigit(3, 2))
    print("koch depth1 points =", len(koch(0.0, 0.0, 100.0, 0.0, 1)))
    print("mergesort(...) =", mergesort([8, 3, 4, 1, 5, 9, 6, 7, 2]))
