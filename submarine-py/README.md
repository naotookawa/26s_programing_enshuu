# submarine-py

人間または自作 AI が対戦できる、Python 製の潜水艦ゲームです。
サーバーが 2 つのプレイヤープログラムをソケットで受け付け、各ターンの移動・攻撃・勝敗判定を行います。

Python でプレイヤーを作る場合は `submarine_py.Player` を継承できます。
通信仕様に沿った JSON を送受信できれば、Python 以外の言語でもプレイヤーを実装できます。

## 主な内容

- 2 人対戦用のゲームサーバー
- ランダムに行動するサンプル AI
- ターミナルで操作できる手動プレイヤー
- 自作プレイヤー用の基底クラスと補助クラス
- サーバー・クライアント間の JSON 通信仕様

## ルール概要

各プレイヤーは自分のフィールドに 3 隻の艦を配置します。
座標は `[x, y]` で表し、標準フィールドは `5 x 5` です。

| 記号 | 艦種 | HP |
| --- | --- | ---: |
| `w` | 戦艦 | 3 |
| `c` | 巡洋艦 | 2 |
| `s` | 潜水艦 | 1 |

ゲームの流れは次の通りです。

1. 各プレイヤーが 3 隻の初期位置をサーバーに送ります。
2. 先攻から交互に、移動または攻撃を 1 回行います。
3. 移動では、自分の艦 1 隻を縦または横に任意のマス数だけ動かせます。ただし、自分の他の艦と同じマスには移動できません。
4. 攻撃では、自分のいずれかの艦がいるマス、またはその周囲 1 マスを攻撃できます。斜め方向も周囲に含みます。
5. 攻撃が命中すると対象艦の HP が 1 減り、HP が 0 になった艦は沈没します。
6. 相手の艦をすべて沈めたプレイヤーが勝ちです。不正な行動を送った場合は敗北します。

より詳しい JSON 仕様は [doc/document.md](doc/document.md) を参照してください。

## ディレクトリ構成

| パス | 内容 |
| --- | --- |
| [src/submarine_py](src/submarine_py) | ゲーム本体の Python パッケージ |
| [sample](sample) | サーバー、ランダム AI、手動プレイヤーのサンプル |
| [doc](doc) | 通信仕様と内部実装の説明 |
| [tests](tests) | pytest によるテスト |
| [pyproject.toml](pyproject.toml) | パッケージ設定と依存関係 |

## セットアップ

Python 3.10 以上を想定しています。

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

`src` レイアウトのため、インストールせずに `sample/*.py` を直接実行すると `ModuleNotFoundError: No module named 'submarine_py'` になります。
通常は上記の編集可能インストールを行ってから実行してください。

## すぐに対戦する

ターミナルを 3 つ開いて、サーバー 1 つとプレイヤー 2 つを起動します。

サーバー:

```bash
python sample/server.py --host localhost --port 2000
```

ランダム AI プレイヤー 1:

```bash
python sample/random_player.py localhost 2000
```

ランダム AI プレイヤー 2:

```bash
python sample/random_player.py localhost 2000
```

片方を人間が操作したい場合は、どちらかのランダム AI の代わりに次を起動します。

```bash
python sample/manual_player.py localhost 2000
```

手動プレイヤーでは、最初に `w`, `c`, `s` の初期座標を入力し、自分の手番ごとに `m` で移動、`a` で攻撃を選びます。

## サーバーの主なオプション

```bash
python sample/server.py --help
```

よく使うオプションは次の通りです。

| オプション | 意味 |
| --- | --- |
| `--host` | 待ち受けるホスト名または IP アドレス |
| `--port` | 待ち受けるポート番号 |
| `--games` | 連続して実行するゲーム数 |
| `--quiet` | フィールド表示を抑えて実行 |
| `--verbose` | 通信ログを詳しく表示 |
| `--field-width` | フィールドの横幅 |
| `--field-height` | フィールドの高さ |
| `--rounded-field` | 四隅を通行不可マスにする |

## 自作プレイヤーを作る

Python で AI を作る場合は `submarine_py.Player` を継承し、次の 3 つのメソッドを実装します。

| メソッド | 役割 |
| --- | --- |
| `name()` | プレイヤー名を返す |
| `place_ship()` | `{"w": [x, y], "c": [x, y], "s": [x, y]}` の形式で初期配置を返す |
| `action()` | `self.move(...)` または `self.attack(...)` を JSON 文字列にして返す |

最小構成の例です。

```python
import json
from submarine_py import Player, play_game


class MyPlayer(Player):
    def name(self):
        return "my-player"

    def place_ship(self):
        return {
            "w": [0, 0],
            "c": [1, 0],
            "s": [2, 0],
        }

    def action(self):
        return json.dumps(self.attack([0, 1]))


if __name__ == "__main__":
    play_game("localhost", 2000, MyPlayer())
```

実用的な実装例は [sample/random_player.py](sample/random_player.py) を参照してください。
`action()` の中では、主に次の情報や補助メソッドを使えます。

- `self.field`: フィールド情報
- `self.ships`: 自分の生存艦
- `self.last_msg`: サーバーから最後に受け取った観測情報
- `self.move(ship_type, to)`: 移動アクションの辞書を作る
- `self.attack(to)`: 攻撃アクションの辞書を作る
- `self.in_attack_range(to)`: 攻撃可能な座標か判定する
- `self.overlap(position)`: 自分の艦がいる座標か判定する

## 通信仕様

サーバーとプレイヤーは 1 行ごとのテキストと JSON で通信します。
自作クライアントを別言語で作る場合は、次のドキュメントを読んでください。

- [doc/document.md](doc/document.md): JSON メッセージ仕様
- [doc/client_doc.md](doc/client_doc.md): クライアント側ライブラリの説明
- [doc/server_doc.md](doc/server_doc.md): サーバー側実装の説明

## テスト

```bash
python -m pytest
```

`pytest.ini` で doctest も有効になっているため、通常のテストに加えて docstring 内の例も検証されます。

### LOG例
warning: No `requires-python` value found in the workspace. Defaulting to `>=3.13`.
┌────┬─────┬─────┬─────┬─────┬─────┐
│    │  0  │  1  │  2  │  3  │  4  │
├────┼─────┼─────┼─────┼─────┼─────┤
│  0 │     │     │     │     │     │
├────┼─────┼─────┼─────┼─────┼─────┤
│  1 │     │     │     │     │     │
├────┼─────┼─────┼─────┼─────┼─────┤
│  2 │     │     │     │     │     │
├────┼─────┼─────┼─────┼─────┼─────┤
│  3 │     │     │     │     │     │
├────┼─────┼─────┼─────┼─────┼─────┤
│  4 │     │     │     │     │     │
└────┴─────┴─────┴─────┴─────┴─────┘
please input x, y in ([0, 4] x [0, 4])
w
x = 0
y = 0
c
x = 0
y = 0
position overlapping
x = 0
y = 3
s
x = 2
y = 2
t=1 waiting
opponent moved s by <<<
opponent ships: w:3 c:2 s:1 
┌────┬─────┬─────┬─────┬─────┬─────┐
│    │  0  │  1  │  2  │  3  │  4  │
├────┼─────┼─────┼─────┼─────┼─────┤
│  0 │ w3  │     │     │     │     │
├────┼─────┼─────┼─────┼─────┼─────┤
│  1 │     │     │     │     │     │
├────┼─────┼─────┼─────┼─────┼─────┤
│  2 │     │     │ s1  │     │     │
├────┼─────┼─────┼─────┼─────┼─────┤
│  3 │ c2  │     │     │     │     │
├────┼─────┼─────┼─────┼─────┼─────┤
│  4 │     │     │     │     │     │
└────┴─────┴─────┴─────┴─────┴─────┘

t=2 your turn
select your action: move (m) or attack (a) ?  a
x = 3
y = 3
you attacked [3, 3] hit w near []
opponent ships: w:2 c:2 s:1 

t=3 waiting
opponent attacked [3, 4] near []
opponent ships: w:2 c:2 s:1 
┌────┬─────┬─────┬─────┬─────┬─────┐
│    │  0  │  1  │  2  │  3  │  4  │
├────┼─────┼─────┼─────┼─────┼─────┤
│  0 │ w3  │     │     │     │     │
├────┼─────┼─────┼─────┼─────┼─────┤
│  1 │     │     │     │     │     │
├────┼─────┼─────┼─────┼─────┼─────┤
│  2 │     │     │ s1  │     │     │
├────┼─────┼─────┼─────┼─────┼─────┤
│  3 │ c2  │     │     │     │     │
├────┼─────┼─────┼─────┼─────┼─────┤
│  4 │     │     │     │  !  │     │
└────┴─────┴─────┴─────┴─────┴─────┘

t=4 your turn
select your action: move (m) or attack (a) ?  a
x = 0
y = 4
you attacked [0, 4] hit s near []
opponent ships: w:2 c:2 

t=5 waiting
opponent moved c by v
opponent ships: w:2 c:2 
┌────┬─────┬─────┬─────┬─────┬─────┐
│    │  0  │  1  │  2  │  3  │  4  │
├────┼─────┼─────┼─────┼─────┼─────┤
│  0 │ w3  │     │     │     │     │
├────┼─────┼─────┼─────┼─────┼─────┤
│  1 │     │     │     │     │     │
├────┼─────┼─────┼─────┼─────┼─────┤
│  2 │     │     │ s1  │     │     │
├────┼─────┼─────┼─────┼─────┼─────┤
│  3 │ c2  │     │     │     │     │
├────┼─────┼─────┼─────┼─────┼─────┤
│  4 │     │     │     │     │     │
└────┴─────┴─────┴─────┴─────┴─────┘

t=6 your turn
select your action: move (m) or attack (a) ?  m
select your ship: warship(w), cruiser(c), or submarine(s)
w
x = 3
y = 0
opponent ships: w:2 c:2 

t=7 waiting
opponent attacked [2, 0] near ['w']
opponent ships: w:2 c:2 
┌────┬─────┬─────┬─────┬─────┬─────┐
│    │  0  │  1  │  2  │  3  │  4  │
├────┼─────┼─────┼─────┼─────┼─────┤
│  0 │     │     │  !  │ w3  │     │
├────┼─────┼─────┼─────┼─────┼─────┤
│  1 │     │     │     │     │     │
├────┼─────┼─────┼─────┼─────┼─────┤
│  2 │     │     │ s1  │     │     │
├────┼─────┼─────┼─────┼─────┼─────┤
│  3 │ c2  │     │     │     │     │
├────┼─────┼─────┼─────┼─────┼─────┤
│  4 │     │     │     │     │     │
└────┴─────┴─────┴─────┴─────┴─────┘

t=8 your turn
select your action: move (m) or attack (a) ?  a
x = a
y = 1
out of field
x = 2
y = 1
you attacked [2, 1] hit c near []
opponent ships: w:2 c:1 

t=9 waiting
opponent moved c by vvv
opponent ships: w:2 c:1 
┌────┬─────┬─────┬─────┬─────┬─────┐
│    │  0  │  1  │  2  │  3  │  4  │
├────┼─────┼─────┼─────┼─────┼─────┤
│  0 │     │     │     │ w3  │     │
├────┼─────┼─────┼─────┼─────┼─────┤
│  1 │     │     │     │     │     │
├────┼─────┼─────┼─────┼─────┼─────┤
│  2 │     │     │ s1  │     │     │
├────┼─────┼─────┼─────┼─────┼─────┤
│  3 │ c2  │     │     │     │     │
├────┼─────┼─────┼─────┼─────┼─────┤
│  4 │     │     │     │     │     │
└────┴─────┴─────┴─────┴─────┴─────┘

t=10 your turn
select your action: move (m) or attack (a) ?  a
x = 3
y = 3
you attacked [3, 3] hit w near ['c']
opponent ships: w:1 c:1 

t=11 waiting
opponent moved w by ^^
opponent ships: w:1 c:1 
┌────┬─────┬─────┬─────┬─────┬─────┐
│    │  0  │  1  │  2  │  3  │  4  │
├────┼─────┼─────┼─────┼─────┼─────┤
│  0 │     │     │     │ w3  │     │
├────┼─────┼─────┼─────┼─────┼─────┤
│  1 │     │     │     │     │     │
├────┼─────┼─────┼─────┼─────┼─────┤
│  2 │     │     │ s1  │     │     │
├────┼─────┼─────┼─────┼─────┼─────┤
│  3 │ c2  │     │     │     │     │
├────┼─────┼─────┼─────┼─────┼─────┤
│  4 │     │     │     │     │     │
└────┴─────┴─────┴─────┴─────┴─────┘

t=12 your turn
select your action: move (m) or attack (a) ?  a
x = 3
y = 2
you attacked [3, 2] near ['w']
opponent ships: w:1 c:1 

t=13 waiting
opponent attacked [2, 2] hit s near []
opponent ships: w:1 c:1 
┌────┬─────┬─────┬─────┬─────┬─────┐
│    │  0  │  1  │  2  │  3  │  4  │
├────┼─────┼─────┼─────┼─────┼─────┤
│  0 │     │     │     │ w3  │     │
├────┼─────┼─────┼─────┼─────┼─────┤
│  1 │     │     │     │     │     │
├────┼─────┼─────┼─────┼─────┼─────┤
│  2 │     │     │  !  │     │     │
├────┼─────┼─────┼─────┼─────┼─────┤
│  3 │ c2  │     │     │     │     │
├────┼─────┼─────┼─────┼─────┼─────┤
│  4 │     │     │     │     │     │
└────┴─────┴─────┴─────┴─────┴─────┘

t=14 your turn
select your action: move (m) or attack (a) ?  a
x = 3
y = 1
you attacked [3, 1] hit w near []
opponent ships: c:1 

t=15 waiting
opponent moved c by ^^^
opponent ships: c:1 
┌────┬─────┬─────┬─────┬─────┬─────┐
│    │  0  │  1  │  2  │  3  │  4  │
├────┼─────┼─────┼─────┼─────┼─────┤
│  0 │     │     │     │ w3  │     │
├────┼─────┼─────┼─────┼─────┼─────┤
│  1 │     │     │     │     │     │
├────┼─────┼─────┼─────┼─────┼─────┤
│  2 │     │     │     │     │     │
├────┼─────┼─────┼─────┼─────┼─────┤
│  3 │ c2  │     │     │     │     │
├────┼─────┼─────┼─────┼─────┼─────┤
│  4 │     │     │     │     │     │
└────┴─────┴─────┴─────┴─────┴─────┘

t=16 your turn
select your action: move (m) or attack (a) ?  m
select your ship: warship(w), cruiser(c), or submarine(s)
c
x = 0
y = 4
opponent ships: c:1 

t=17 waiting
opponent attacked [1, 1] near []
opponent ships: c:1 
┌────┬─────┬─────┬─────┬─────┬─────┐
│    │  0  │  1  │  2  │  3  │  4  │
├────┼─────┼─────┼─────┼─────┼─────┤
│  0 │     │     │     │ w3  │     │
├────┼─────┼─────┼─────┼─────┼─────┤
│  1 │     │  !  │     │     │     │
├────┼─────┼─────┼─────┼─────┼─────┤
│  2 │     │     │     │     │     │
├────┼─────┼─────┼─────┼─────┼─────┤
│  3 │     │     │     │     │     │
├────┼─────┼─────┼─────┼─────┼─────┤
│  4 │ c2  │     │     │     │     │
└────┴─────┴─────┴─────┴─────┴─────┘

t=18 your turn
select your action: move (m) or attack (a) ?  a
x = 1
y = 1
you can't attack [1, 1]
x = 3
y = 0
you attacked [3, 0] near ['c']
opponent ships: c:1 

t=19 waiting
opponent attacked [1, 1] near []
opponent ships: c:1 
┌────┬─────┬─────┬─────┬─────┬─────┐
│    │  0  │  1  │  2  │  3  │  4  │
├────┼─────┼─────┼─────┼─────┼─────┤
│  0 │     │     │     │ w3  │     │
├────┼─────┼─────┼─────┼─────┼─────┤
│  1 │     │  !  │     │     │     │
├────┼─────┼─────┼─────┼─────┼─────┤
│  2 │     │     │     │     │     │
├────┼─────┼─────┼─────┼─────┼─────┤
│  3 │     │     │     │     │     │
├────┼─────┼─────┼─────┼─────┼─────┤
│  4 │ c2  │     │     │     │     │
└────┴─────┴─────┴─────┴─────┴─────┘

t=20 your turn
select your action: move (m) or attack (a) ?  a
x = 2
y = 2
you can't attack [2, 2]
x = a
y = 2
out of field
x = 1
y = 1
you can't attack [1, 1]
x = 2
y = 1
you attacked [2, 1] hit c near []
opponent ships: 

t=21 you win
