"""Chapter 7 submission: all non-star problems."""

from __future__ import annotations

import random

Cooperate = 0
Defect = 1


def valid_action(act):
    return act == Cooperate or act == Defect


class BankAccount0:
    def __init__(self, initial_balance):
        self.balance = initial_balance

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            return self.balance
        return "Insufficient funds"


class BankAccount:
    def __init__(self, initial_balance):
        self.__balance = initial_balance

    def withdraw(self, amount):
        if self.__balance >= amount:
            self.__balance -= amount
            return self.__balance
        return "Insufficient funds"

    def deposit(self, amount):
        self.__balance += amount
        return self.__balance


class BankAccount2:
    def __init__(self, initial_balance, password):
        self.__balance = initial_balance
        self.__password = password

    def _check_password(self, password):
        if password != self.__password:
            return "Incorrect password"
        return None

    def withdraw(self, amount, password):
        err = self._check_password(password)
        if err is not None:
            return err
        if self.__balance >= amount:
            self.__balance -= amount
            return self.__balance
        return "Insufficient funds"

    def deposit(self, amount, password):
        err = self._check_password(password)
        if err is not None:
            return err
        self.__balance += amount
        return self.__balance


class Counter:
    def __init__(self):
        self.__counter = 0

    def increment(self):
        self.__counter += 1

    def count(self):
        return self.__counter


class ClockTimer:
    def __init__(self, hour, minute, second):
        self.hour = hour
        self.minute = minute
        self.second = second

    def tick(self):
        self.second += 1
        if self.second == 60:
            self.second = 0
            self.minute += 1
            if self.minute == 60:
                self.minute = 0
                self.hour = (self.hour + 1) % 24


class Fib:
    def fib(self, n):
        if n == 0:
            return 0
        if n == 1:
            return 1
        return self.fib(n - 1) + self.fib(n - 2)


class CountedFib:
    def __init__(self):
        self.__counter = Counter()

    def fib(self, n):
        self.__counter.increment()
        if n == 0:
            return 0
        if n == 1:
            return 1
        return self.fib(n - 1) + self.fib(n - 2)

    def count(self):
        return self.__counter.count()


class MemoFib:
    def __init__(self, limit=1000):
        self.__counter = Counter()
        self.__memo = [None] * limit
        self.__memo[0] = 0
        self.__memo[1] = 1

    def fib(self, n):
        if self.__memo[n] is not None:
            return self.__memo[n]
        self.__counter.increment()
        self.__memo[n] = self.fib(n - 1) + self.fib(n - 2)
        return self.__memo[n]

    def count(self):
        return self.__counter.count()


class Player:
    def name(self):
        pass

    def play(self):
        pass

    def update(self, my_action, op_action):
        pass


class CooperatePlayer(Player):
    def name(self):
        return "CooperatePlayer"

    def play(self):
        return Cooperate


class DefectPlayer(Player):
    def name(self):
        return "DefectPlayer"

    def play(self):
        return Defect


class RandomPlayer(Player):
    def name(self):
        return "RandomPlayer"

    def play(self):
        return Cooperate if random.randrange(2) == 0 else Defect


class TitForTatPlayer(Player):
    def __init__(self):
        self.__op_last_action = Cooperate

    def name(self):
        return "TitForTatPlayer"

    def play(self):
        return self.__op_last_action

    def update(self, my_action, op_action):
        self.__op_last_action = op_action


def play_one_game(player_a, player_b):
    act_a = player_a.play()
    act_b = player_b.play()
    if not valid_action(act_a):
        raise ValueError("invalid action from player_a")
    if not valid_action(act_b):
        raise ValueError("invalid action from player_b")
    reward = [
        [2, 0],  # cooperate
        [3, 1],  # defect
    ]
    reward_a = reward[act_a][act_b]
    reward_b = reward[act_b][act_a]
    print(f"{player_a.name()} v.s. {player_b.name()}")
    print("actions:")
    print("rewards:")
    print((act_a, reward_a, act_b, reward_b))
    player_a.update(act_a, act_b)
    player_b.update(act_b, act_a)
    return act_a, reward_a, act_b, reward_b


P = 1.0 / 8.0


def play_games(player_a, player_b):
    sums = [0, 0]
    history = ["", ""]
    while True:
        act_a, reward_a, act_b, reward_b = play_one_game(player_a, player_b)
        sums[0] += reward_a
        sums[1] += reward_b
        history[0] += str(act_a)
        history[1] += str(act_b)
        if random.random() < P:
            return sums, history


def _test_accounts() -> None:
    a = BankAccount0(10000)
    b = BankAccount(10000)
    c = BankAccount2(10000, "secret")
    assert a.withdraw(5000) == 5000
    assert b.withdraw(5000) == 5000
    assert b.deposit(4000) == 9000
    assert c.withdraw(4000, "secret") == 6000
    assert c.deposit(5000, "wrong") == "Incorrect password"


def _test_counter_and_clock() -> None:
    counter = Counter()
    counter.increment()
    counter.increment()
    assert counter.count() == 2
    timer = ClockTimer(22, 54, 14)
    timer.tick()
    assert (timer.hour, timer.minute, timer.second) == (22, 54, 15)
    for _ in range(45):
        timer.tick()
    assert (timer.hour, timer.minute, timer.second) == (22, 55, 0)


def _test_fib_classes() -> None:
    f = Fib()
    assert f.fib(10) == 55
    g = CountedFib()
    assert g.fib(3) == 2
    assert g.count() > 0
    m = MemoFib()
    assert m.fib(10) == 55
    count1 = m.count()
    assert m.fib(10) == 55
    assert m.count() == count1


def _test_prisoners_dilemma() -> None:
    random.seed(0)
    pc = CooperatePlayer()
    pd = DefectPlayer()
    pr = RandomPlayer()
    tft = TitForTatPlayer()
    assert tft.play() == Cooperate
    tft.update(Cooperate, Defect)
    assert tft.play() == Defect
    # game behavior smoke tests
    play_one_game(pc, pd)
    play_one_game(pc, pr)
    play_one_game(pd, pr)


if __name__ == "__main__":
    _test_accounts()
    _test_counter_and_clock()
    _test_fib_classes()
    _test_prisoners_dilemma()
    print("week7 tests passed")
