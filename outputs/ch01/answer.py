"""第1章 章末課題: 非スター問題をまとめて解く."""


def print_multiplication_table(size: int = 9) -> None:
    for i in range(1, size + 1):
        row = []
        for j in range(1, size + 1):
            row.append(f"{i * j:3d}")
        print("".join(row))


def print_training_menu(sets: int = 3) -> None:
    for _ in range(sets):
        print("トレーニング始め!")
        print("腕立て")
        print("腹筋")
        print("腕立て")
        print("腹筋")
        print("(5分休憩)")


def print_triangle2(size: int) -> None:
    for i in range(size, 0, -1):
        print("*" * i)


def print_arrow(size: int) -> None:
    width = 2 * size + 1
    for i in range(size):
        stars = 2 * i + 1
        spaces = (width - stars) // 2
        print(" " * spaces + "*" * stars)
    print("*" * width)
    for i in range(size - 1):
        spaces = size - i - 1
        print(" " * spaces + "*")


def print_frame(size: int) -> None:
    for r in range(size):
        row = []
        for c in range(size):
            row.append("#" if r in (0, size - 1) or c in (0, size - 1) else " ")
        print("".join(row))


def print_shelf(size: int) -> None:
    for r in range(size):
        row = []
        for c in range(size):
            if r in (0, size - 1):
                row.append("#")
            elif r % 2 == 1 and c in (1, size - 2):
                row.append("#")
            else:
                row.append(" ")
        print("".join(row))


def print_door(size: int) -> None:
    for r in range(size):
        row = []
        for c in range(size):
            if r in (0, size - 1):
                row.append("#")
            elif c in (0, size - 1):
                row.append("#")
            elif r == 1:
                row.append("#")
            elif r == size // 2 and 1 < c < size - 2:
                row.append("#")
            elif 1 < r < size - 1 and c in (2, size - 3):
                row.append("#")
            else:
                row.append(" ")
        print("".join(row))


def main() -> None:
    print("=== 九九 ===")
    print_multiplication_table()
    print()

    print("=== 筋トレ3セット ===")
    print_training_menu()
    print()

    print("=== 三角2 ===")
    print_triangle2(4)
    print()

    print("=== 矢印 ===")
    print_arrow(3)
    print()

    print("=== 外枠 ===")
    print_frame(7)
    print()

    print("=== 本棚 ===")
    print_shelf(9)
    print()

    print("=== 扉 ===")
    print_door(9)


if __name__ == "__main__":
    main()
