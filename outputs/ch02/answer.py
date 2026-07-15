"""第2章 章末課題: 変数を含む電卓 (calcvar)."""


def make_term(token: str):
    if token == "x":
        return lambda x: x
    value = int(token)
    return lambda x: value


def calculator(a: int, op: str, b: int) -> int:
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    if op == "/":
        return a // b
    raise ValueError(f"unsupported operator: {op}")


def parse_one(s: str):
    lf = make_term(s[0])
    op = s[1]
    rf = make_term(s[2])
    return lambda x: calculator(lf(x), op, rf(x))


def parse_term(s: str):
    if s[0] == "(":
        lf, lsize = parse_term(s[1:])
        op_index = 1 + lsize
        op = s[op_index]
        rf, rsize = parse_term(s[op_index + 1 :])
        close_index = op_index + 1 + rsize

        def func(x):
            return calculator(lf(x), op, rf(x))

        return func, close_index + 1

    i = 0
    while i < len(s) and s[i] not in "+-*/()":
        i += 1
    return make_term(s[:i]), i


def parse(s: str):
    f, size = parse_term(s)
    if size != len(s):
        raise ValueError("unexpected trailing characters")
    return f


if __name__ == "__main__":
    f = parse("((x+3)+3)")
    print(f(0))
    print(f(1))
    f = parse("((x+3)*(x-3))")
    print(f(1))
