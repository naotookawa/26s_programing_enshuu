import numpy as np

from submarine_py import Client, Field
from submarine_py.rl.action_space import (
    ACTION_SIZE,
    decode_action,
    encode_attack,
    encode_move,
    legal_action_mask,
    random_legal_action,
)
from submarine_py.rl.config import SHIP_TYPES


def test_encode_decode_all_actions():
    assert ACTION_SIZE == 100
    for y in range(5):
        for x in range(5):
            action = decode_action(encode_attack(x, y))
            assert action.kind == "attack"
            assert (action.x, action.y) == (x, y)
    for ship_type in SHIP_TYPES:
        for y in range(5):
            for x in range(5):
                action = decode_action(encode_move(ship_type, x, y))
                assert action.kind == "move"
                assert action.ship_type == ship_type
                assert (action.x, action.y) == (x, y)


def test_legal_action_mask():
    field = Field()
    client = Client(field, {"w": [0, 0], "c": [2, 2], "s": [4, 4]})
    mask = legal_action_mask(field, client.ships)
    assert mask.shape == (100,)
    assert mask.dtype == np.bool_
    assert mask[encode_attack(1, 1)]
    assert not mask[encode_attack(4, 0)]
    assert mask[encode_move("w", 0, 4)]
    assert not mask[encode_move("w", 1, 1)]
    assert not mask[encode_move("w", 2, 2)]
    del client.ships["s"]
    mask = legal_action_mask(field, client.ships)
    assert not mask[encode_move("s", 4, 0)]
    assert mask[random_legal_action(mask)]
