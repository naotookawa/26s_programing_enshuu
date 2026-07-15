"""Chapter 6 submission up to section 6.2."""

from __future__ import annotations

EmptyTree = "EmptyTree"


def make_node(num, left_node, right_node):
    return [num, left_node, right_node]


def make_leaf(num):
    return make_node(num, EmptyTree, EmptyTree)


def value(tree):
    return tree[0]


def left(tree):
    return tree[1]


def right(tree):
    return tree[2]


def is_empty(tree):
    return tree == EmptyTree


def count_node(tree):
    if is_empty(tree):
        return 0
    return 1 + count_node(left(tree)) + count_node(right(tree))


def max_value(tree):
    if is_empty(tree):
        raise ValueError("tree must not be empty")
    result = value(tree)
    if not is_empty(left(tree)):
        result = max(result, max_value(left(tree)))
    if not is_empty(right(tree)):
        result = max(result, max_value(right(tree)))
    return result


def depth(tree):
    if is_empty(tree):
        return 0
    return 1 + max(depth(left(tree)), depth(right(tree)))


def preorder(tree):
    if is_empty(tree):
        return []
    return [value(tree)] + preorder(left(tree)) + preorder(right(tree))


def inorder(tree):
    if is_empty(tree):
        return []
    return inorder(left(tree)) + [value(tree)] + inorder(right(tree))


def add_node(tree, x):
    if is_empty(tree):
        return make_leaf(x)
    if x < value(tree):
        return make_node(value(tree), add_node(left(tree), x), right(tree))
    return make_node(value(tree), left(tree), add_node(right(tree), x))


def make_binary_search_tree(a):
    tree = EmptyTree
    # ループ不変条件:
    # tree は，これまでに a[0:i] までの要素を挿入した二分探索木である。
    for x in a:
        tree = add_node(tree, x)
    return tree


def make_question_node(question, yes_branch, no_branch):
    return {"kind": "question", "question": question, "yes": yes_branch, "no": no_branch}


def question_text(qnode):
    return qnode["question"]


def question_yes(qnode):
    return qnode["yes"]


def question_no(qnode):
    return qnode["no"]


def make_answer_node(answer):
    return {"kind": "answer", "answer": answer}


def answer_text(anode):
    return anode["answer"]


def is_question_node(node):
    return node["kind"] == "question"


def display(node):
    if is_question_node(node):
        print("Q: " + question_text(node) + " ? [yn]")
        yn = input()
        if yn.lower()[0] == "y":
            display(question_yes(node))
        else:
            display(question_no(node))
    else:
        print("---")
        print("Answer: " + answer_text(node))


def calc(tree):
    if is_empty(left(tree)) and is_empty(right(tree)):
        return value(tree)
    op = value(tree)
    l = calc(left(tree))
    r = calc(right(tree))
    if op == "+":
        return l + r
    if op == "-":
        return l - r
    if op == "*":
        return l * r
    if op == "/":
        return l / r
    raise ValueError(f"unknown operator: {op}")


def _test_tree_basics() -> None:
    t0 = make_leaf(2)
    t1 = make_node(1, make_leaf(3), make_leaf(5))
    t2 = make_node(3, t1, t0)

    assert count_node(t0) == 1
    assert count_node(t1) == 3
    assert count_node(t2) == 5
    assert max_value(t2) == 5
    assert depth(t0) == 1
    assert depth(t1) == 2
    assert depth(t2) == 3
    assert preorder(t1) == [1, 3, 5]
    assert inorder(t1) == [3, 1, 5]


def _test_bst() -> None:
    t = make_binary_search_tree([3, 1, 6, 1, 7, 9, 2, 0, 5])
    assert inorder(t) == [0, 1, 1, 2, 3, 5, 6, 7, 9]
    assert count_node(t) == 9


def _test_qa_and_calc() -> None:
    q = make_question_node(
        "Hungry",
        make_answer_node("cup noodle"),
        make_answer_node("take a nap"),
    )
    assert is_question_node(q) is True
    assert question_text(q) == "Hungry"
    assert answer_text(question_yes(q)) == "cup noodle"
    assert answer_text(question_no(q)) == "take a nap"

    t = make_node("+", make_node("*", make_leaf(3), make_leaf(5)), make_leaf(2))
    assert calc(t) == 17


if __name__ == "__main__":
    _test_tree_basics()
    _test_bst()
    _test_qa_and_calc()

    sample = make_binary_search_tree([3, 1, 6, 1, 7, 9, 2, 0, 5])
    print("inorder =", inorder(sample))
    print("calc =", calc(make_node("+", make_node("*", make_leaf(3), make_leaf(5)), make_leaf(2))))
