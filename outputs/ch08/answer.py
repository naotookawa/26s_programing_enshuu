"""Chapter 8 submission: all non-star Python problems."""

from __future__ import annotations

import abc
import doctest
import random


def rectarea(a, b):
    """Return the area of a rectangle.

    >>> rectarea(7, 5)
    35
    """
    return a * b


class BankAccount:
    """Bank account with encapsulated balance.

    >>> a = BankAccount(10000)
    >>> a.withdraw(5000)
    5000
    >>> a.deposit(4000)
    9000
    >>> a.withdraw(6000)
    3000
    """

    def __init__(self, initial_balance):
        self.__balance = initial_balance

    def withdraw(self, amount):
        """Withdraw money and return the new balance.

        >>> a = BankAccount(10000)
        >>> a.withdraw(4000)
        6000
        >>> a.withdraw(7000)
        'Insufficient funds'
        """
        if self.__balance >= amount:
            self.__balance -= amount
            return self.__balance
        return "Insufficient funds"

    def deposit(self, amount):
        self.__balance += amount
        return self.__balance


class Player(abc.ABC):
    """Player of repeated prisoners' dilemma game."""

    @abc.abstractmethod
    def name(self):
        """Return player's name."""

    @abc.abstractmethod
    def play(self):
        """Return Cooperate or Defect."""

    def update(self, my_action, op_action):
        pass


Cooperate = 0
Defect = 1


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


def valid_action(act):
    return act == Cooperate or act == Defect


def play_one_game(player_a, player_b):
    """Play one prisoner's dilemma game.

    >>> random.seed(0)
    >>> play_one_game(CooperatePlayer(), DefectPlayer())
    ('CooperatePlayer', 'DefectPlayer', (0, 0, 1, 3))
    """
    act_a = player_a.play()
    act_b = player_b.play()
    if not valid_action(act_a):
        raise ValueError("invalid action from player_a")
    if not valid_action(act_b):
        raise ValueError("invalid action from player_b")

    reward = [[2, 0], [3, 1]]
    reward_a = reward[act_a][act_b]
    reward_b = reward[act_b][act_a]
    player_a.update(act_a, act_b)
    player_b.update(act_b, act_a)
    return player_a.name(), player_b.name(), (act_a, reward_a, act_b, reward_b)


P = 1.0 / 8.0


def play_games(player_a, player_b):
    """Play repeated prisoner's dilemma games.

    >>> random.seed(0)
    >>> play_games(CooperatePlayer(), DefectPlayer())[0]  # doctest: +ELLIPSIS
    [0, ...]
    """
    sums = [0, 0]
    history = ["", ""]
    while True:
        _, _, (act_a, reward_a, act_b, reward_b) = play_one_game(player_a, player_b)
        sums[0] += reward_a
        sums[1] += reward_b
        history[0] += str(act_a)
        history[1] += str(act_b)
        if random.random() < P:
            return sums, history


class Subject(abc.ABC):
    """Abstract subject."""

    def __init__(self):
        self.observers = []

    def attach(self, observer):
        self.observers.append(observer)

    def detach(self, observer):
        self.observers.remove(observer)

    def notify(self):
        for observer in list(self.observers):
            observer.update()


class Observer(abc.ABC):
    """Abstract observer class."""

    @abc.abstractmethod
    def update(self):
        pass


class ClockTimer(Subject):
    """a class manages time (self.hour, self.minute, and self.second)"""

    def __init__(self, hour, minute, second):
        super().__init__()
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
        self.notify()


class ConsoleClock(Observer):
    """display time in console"""

    def __init__(self, subject):
        self.subject = subject
        subject.attach(self)

    def update(self):
        print(f"{self.subject.hour:02d}:{self.subject.minute:02d}:{self.subject.second:02d}")


class MultiClock(Observer):
    """Another observer that records snapshots."""

    def __init__(self, subject):
        self.subject = subject
        self.history = []
        subject.attach(self)

    def update(self):
        self.history.append((self.subject.hour, self.subject.minute, self.subject.second))


class CountdownClock(Observer):
    """Count down with alarms.

    >>> timer = ClockTimer(22, 54, 12)
    >>> cd = CountdownClock(timer, 3)
    >>> timer.tick()
    >>> timer.tick()
    >>> timer.tick()
    !!!
    """

    def __init__(self, subject, remaining):
        self.subject = subject
        self.remaining = remaining
        self.alarmed = False
        subject.attach(self)

    def update(self):
        if self.alarmed:
            return
        self.remaining -= 1
        if self.remaining <= 0:
            self.alarmed = True
            print("!!!")


def _test_rectarea():
    assert rectarea(7, 5) == 35


def _test_bankaccount():
    a = BankAccount(10000)
    assert a.withdraw(5000) == 5000
    assert a.deposit(4000) == 9000
    assert a.withdraw(6000) == 3000


def _test_players():
    random.seed(0)
    assert CooperatePlayer().play() == Cooperate
    assert DefectPlayer().play() == Defect
    assert valid_action(RandomPlayer().play())


def _test_subject_observer():
    timer = ClockTimer(22, 54, 12)
    cc = ConsoleClock(timer)
    mc = MultiClock(timer)
    timer.tick()
    timer.tick()
    assert mc.history == [(22, 54, 13), (22, 54, 14)]
    timer.detach(cc)
    timer.tick()
    assert mc.history[-1] == (22, 54, 15)


def _test_countdown():
    timer = ClockTimer(22, 54, 12)
    cd = CountdownClock(timer, 3)
    timer.tick()
    timer.tick()
    assert cd.alarmed is False
    timer.tick()
    assert cd.alarmed is True


if __name__ == "__main__":
    doctest.testmod(verbose=True)
    _test_rectarea()
    _test_bankaccount()
    _test_players()
    _test_subject_observer()
    _test_countdown()
    print("week8 tests passed")
