# 付録B 最終課題: 潜水艦ゲーム (p.191-200)

<!--
source_pages: 191-200
source_md_pages: 192-201
chapter_id: 付録B
title: 最終課題: 潜水艦ゲーム
keywords: 最終課題: 潜水艦ゲーム, 目標, 準備, 動作確認と対戦, 独自の思考プレイヤー作り方, サンプルプログラムを読む, ヒント, Python パッケージの読み方, フォルダ構成, よく使うモジュール, pytest, argparse, logging, 関数と引数, 2025 年度の変更
-->

## この章の構成

- B.1 目標 (p.191)
- B.2 準備 (p.191)
- B.3 動作確認と対戦 (p.192-193)
- B.4 独自の思考プレイヤー作り方 (p.194)
- B.4.1 サンプルプログラムを読む (p.194)
- B.4.2 ヒント (p.194)
- B.5 Python パッケージの読み方 (p.195-199)
- B.5.1 フォルダ構成 (p.195)
- B.5.2 よく使うモジュール (p.195-198)
- pytest (p.196)
- argparse (p.196)
- logging (p.197-198)
- B.5.3 関数と引数 (p.199)
- B.6 2025 年度の変更 (p.200)

## B.1 目標 (p.191)

## B.2 準備 (p.191)

<!-- source: pdf_page=191; md_page_heading=p.192 -->

付録 B 最終課題: 潜水艦ゲーム この章では，潜水艦ゲームの思考部分の作成という課題ついて紹介する． B.1 目標
- 必須
  - ランダムプレイヤー (random player.py) より，はっきり強いプレイヤーを作る
  - 何かしら自分の考えた戦略によって行動する
  - いろいろな大きさのマップに対応する (最大 40 マス程度と仮定して良い)
- 努力目標
  - なるべく強くする
  - simple player.py (後日 UTOL に掲載) に勝ち越す B.2 準備 タ ー ミ ナ ル で ，git, python が 使 え る こ と を 確 認 す る ．Mac の 場 合 は ど れ も 標 準 で 使 え る ． Microsoft Windows の場合は，第 9 章のファイルからの実行 (9.A 節) で紹介した手順により，git と python (または python3) コマンドが使えているはず． 続いてインストールを行う 1. 配布物一式をダウンロードして, 適当な場所で展開する． 

**Terminal**

```bash
$ git clone https://github.com/tkaneko/submarine-py.git
$ cd submarine-py
```

2. 必要に応じて1）git checkout main で main というブランチ (後述) を選択 

**Terminal**

```bash
$ git checkout main
```

3. ソースコードの変更準備として，local-changes というブランチ (保存場所) を新たに作成する． (必須ではないが推奨) 1） フォルダにファイルが見当たらない場合は必要

## B.3 動作確認と対戦 (p.192-193)

<!-- source: pdf_page=192; md_page_heading=p.193 -->

B.3 動作確認と対戦 

**Terminal**

```bash
$ git checkout -b local-changes
```

4. インストール ターミナルを 1 つ開いて, パッケージをインストールする．オプションの -e とそ れにつづくドット . が今後の開発で重要．2） 

**Terminal**

```bash
$ uv pip install --user -e .
```

あるいは 

**Terminal**

```bash
$ pip3 install --user -e .
```

Help:Virtualenv の準備が必要な場合 新しい Python (3.12 以降) では，パッケージのインストールの前に virtualenv の準備が必 須である．そのようなエラーが出た際には，以下のコマンドで準備をし，もう一度インス トールすると良い． $ python3 -m venv venv な お uva を 導 入 済 み の 場 合 は ，uv venv と source .venv/bin/activate b, uv pip install -e . などが同等のコマンドである． a https://docs.astral.sh/uv/ b あるいは source .venv/Scripts/activate B.3 動作確認と対戦 まず，人間が AI と対戦するまでを，動作確認しよう．その後で，README.md の説明を読むと良い． 1. サーバ起動 同ターミナルで以下を実行する 

**Terminal**

```bash
$ python3 sample/server.py
```

これによりサーバープログラムが起動し, プレイヤープログラムからの接続を待つ. 2） 標準コードを編集した場合に再インストール無しで反映されるかどうかが変わる．変更しなければ動作に差はない．

<!-- source: pdf_page=193; md_page_heading=p.194 -->

B.3 動作確認と対戦 2. プレイヤーの接続 ターミナルをもう 1 つ (別のウィンドウまたはタブを ) 開いて, 以下を実行 する 

**Terminal**

```bash
$ python3 sample/random_player.py localhost 2000
```

これによりランダムに動く AI プログラムをサーバープログラムと接続する. 3. ターミナルをさらにもう つ (別のウィンドウまたはタブを) 開いて, 以下を実行する． 

**Terminal**

```bash
$ python3 sample/manual_player.py localhost 2000
```

これは，ターミナルからのキーボード入力を通じて , 人がゲームをプレイするプログラムで ある. Terminal 0 1 2 3 4 1 ------------------------ 2 0 3 ------------------------ 4 1 5 ------------------------ 6 2 7 ------------------------ 8 3 9 ------------------------ 10 4 11 ------------------------ 12 please input x, y in ([0, 4] x [0, 4]) 13 w 14 x = 0 15 y = 0 16 c 17 x = 4 18 y = 4 19 s 20 x = 2 21 y = 2 22 0 1 2 3 4 23 ------------------------ 24 0 w3 25 ------------------------ 26 1 27 ------------------------ 28 2 s1 29 ------------------------ 30 3 31

## B.4 独自の思考プレイヤー作り方 (p.194)

### B.4.1 サンプルプログラムを読む (p.194)

### B.4.2 ヒント (p.194)

<!-- source: pdf_page=194; md_page_heading=p.195 -->

B.4 独自の思考プレイヤー作り方 ------------------------ 32 4 c2 33 ------------------------ 34 Help:うまく動かない時の調査
- 3 つのターミナルを注視し，エラーメッセージが出ている場合は，よく読む．一つが異常 終了すると，巻き添えで全てが止まることがあるので，どれが最初かを推理する．たとえ ば，起動時の引数が足りない場合などはエラーメッセージから追跡できる．
- ファイアーウォールが通信を止めている場合がある． (安全な環境 e.g., インターネットか ら切り離した状態で ) ファイアーウォールを一旦停止して，動かしてみる．これで動く場 合は，ファイアーウォールの設定を工夫して，ファイアーウォール動作状態で動くように する．サーバが接続を待ち受ける許可を出したり， port 番号 (上記の例では 2000 番) での 通信を許可するなどが必要と思われる．
- IPv4 v.s. IPv6: random player.py は IPv4 を前提に書かれているが，サーバ側は OS の 設定に依存するため IPv6 で接続を待つことがある． B.4 独自の思考プレイヤー作り方 sample/random player.py などを参考に, 自動で行動するプレイヤーを作成する. B.4.1 サンプルプログラムを読む 1. README.md を読んで, 全体の概要をつかむ.（ゲームのルール, ディレクトリの構造など） ．ウェブ ブラウザで https://github.com/tkaneko/submarine-py/blob/main/README.md を読んでも 良い． 2. doc/client doc.md, doc/document.md を読んで, 通信の流れなどの仕様を理解する. 3. src/submarine py/player base.py, sample/random player.py や sample/manual player.py の を 軽 く 読 ん で 見 る ．共 通 のPlayer class を 継 承 し て い る こ と ，子 ク ラ ス で 実 装 が 必 要 な method が何かを把握する 4. 自分の AI プレイヤー sample/xxxx player.py を作る B.4.2 ヒント
- 人とランダムプレイヤーでゲームを遊んでみる.
- 人間同士で遊んでみる . 紙でも遊べるが, このプログラムを利用する方が簡便 . ゲームの特徴を理 解して, 人間ならまずどういう作戦を立てられるかを検討する.
- プレイヤープログラムがサーバーから情報 (json) を受け取るのは, 「自分の行動終了後」及び「相

## B.5 Python パッケージの読み方 (p.195-199)

### B.5.1 フォルダ構成 (p.195)

### B.5.2 よく使うモジュール (p.195-198)

<!-- source: pdf_page=195; md_page_heading=p.196 -->

B.5 Python パッケージの読み方 手の行動終了後」で, このタイミングで Player クラスの update メソッドが実行される.
- random player.py はゲームのルールに違反しないように実装されているが , もしゲームのルール に違反した行動をサーバーに送信するとその時点で敗北扱いになる . それを防ぐために，自分の 行動をサーバーに送信する前に, ルール違反がないかどうかをチェックするようにすること . その ための補助メソッドが player base.py に存在するので, 適宜活用すると良い. B.5 Python パッケージの読み方 既存ソフトウェアを信頼できるという前提なら，重要なところに時間を使うこと，常識的に理解で きそうな部分は「流し」て，どこが本質か手早く見分けられると良い．そのような読み方の手がかり をいくつか紹介する． B.5.1 フォルダ構成 潜 水 艦 ゲ ー ム の プ ロ ジ ェ ク ト は ，典 型 的 な Python パ ッ ケ ー ジ に 倣 っ て ，右 図 の よ う な デ ィ レ ク ト リ 構 造 を 持 つ ．ル ー ト 直 下 の pyproject.toml (と setup.py) が，パッケージ の内容と pip install 時の動作を定める．授業 では，詳細の説明は割愛する．3） src/submarine py が ， submarine py パ ッ ケージの本体である．その中の， init /.py が import submarine_py したときに提供される機 能を定義し，各機能の実装は，同フォルダの他の ファイルに置かれる．たとえば init /.py 内 の from .ship import Ship という行は，同じ フォルダの ship.py から Ship という機能を使 う (ここでは提供する) という意味である． . ├── pyproject.toml ├── README.md ├── sample │ ├── random_player.py │ └── ... ├── setup.py ├── src │ ├── submarine_py │ │ ├── __init__.py │ │ ├── field.py │ │ └── ... └── tests ├── test_client.py └── ... B.5.2 よく使うモジュール 大規模ソフトウェアでしばしば必要になる機能について， Python での標準的な実現方法で，かつ， このゲームで利用されているものを紹介する． 3） https://packaging.python.org/ja/latest/tutorials/packaging-projects/

#### pytest (p.196)

#### argparse (p.196)

<!-- source: pdf_page=196; md_page_heading=p.197 -->

B.5 Python パッケージの読み方 pytest 潜水艦ゲームのパッケージでは， python -m pytest などで，テストを実行することができる．テ スト用のコードは，フォルダ tests 以下に格納されている．また pytest.ini の設定により，自動で doctest も実行される． argparse プログラムの起動時に引数を与えて，動作を調整する方法を 9.6.2 項 で紹介した．標準ライブラリ argparse は，より高度な機能を提供する．以下のサンプルは， 2 つの整数を引数 a, b としてとり，そ の和を返す．またオプションで --scale があたえられたら，それを乗ずる． 

**Python3**

```python
import argparse
def task(a, b, scale):
    return (a + b) * scale
if __name__ == ' __main__' :
    parser = argparse.ArgumentParser(
    description="argparse sample ",
```

) 行目は定型なので，実用上はコピーペーストして適宜編集すれば良い． いくつかの実行例を示す． 

**Terminal**

```bash
$ python samples/argparse-sample.py
```

**Terminal**

```bash
$ python samples/argparse-sample.py
```

--scale 必須の引数が不足している場合はエラーになる．自動生成された，簡易的な使い方が示される．

#### logging (p.197-198)

<!-- source: pdf_page=197; md_page_heading=p.198 -->

B.5 Python パッケージの読み方 

**Terminal**

```bash
$ python samples/argparse-sample.py
```

usage: argparse-sample.py [-h] [--scale SCALE] a b ヘルプ --help の対応は自動生成される．これにより詳細な説明を加えることもできる (配布プログ ラムを参照)． 

**Terminal**

```bash
$ python samples/argparse-sample.py --help
```

usage: argparse-sample.py [-h] [--scale SCALE] a b つである必要があるので，変数の値を表示する際には f' text {a}' という formatted string5）という文法を用いている． 

**Python3**

```python
import logging
def sample_logs():
```

logging.debug("I' m looking for chocolate ") 4） https://click.palletsprojects.com/en/stable/ 5） https://docs.python.org/3/tutorial/inputoutput.html#formatted-string-literals

<!-- source: pdf_page=198; md_page_heading=p.199 -->

B.5 Python パッケージの読み方 a = [3, 1, 4] 7 logging.info(f"sample for printing value of a variable: {a}") 8 logging.warning("I feel a bit hungry ") 9 logging.error("Where is my phone? ") 10 logging.critical("No more energy to act ") 11 12 13 if __name__ == ' __main__' : 14 level = logging.DEBUG 15 # level = logging.WARNING 16 logging.basicConfig(level=level) 17 sample_logs() 18 このソースコードを実行すると以下の表示を得る． 

**Terminal**

```bash
$ python3 logging-sample.py
```

DEBUG:root:I' m looking for chocolate ここで変数 level を次のように変更すると，この 1 行の変更のみで，表示が簡潔になる 

**Python3**

```python
level = logging.WARNING
```

**Terminal**

```bash
$ python3 logging-sample.py
```

WARNING:root:I feel a bit hungry 必ず必要な表示以外は，print に代えて logging を用い， 重要さに応じてdebug, info, warning, error, critical を使い分けると良い．そのようにしておくと，デバッグ中は詳細を表示するなどを 簡単に切り替えることができる．また，方法は割愛するが，記録先をファイルに切り替える，時刻を 付記するなども簡単に実現できる． /lightbulb 潜水艦ゲームでの logging このプロジェクトでは，起動時に引数 --verbose を与えると logging.debug まですべての情 報を表示し，それ以外は logging.info までを出力するように書かれている．

### B.5.3 関数と引数 (p.199)

<!-- source: pdf_page=199; md_page_heading=p.200 -->

B.5 Python パッケージの読み方 B.5.3 関数と引数 ソースコードをより読みやすく，また管理を容易にするために， Python の機能をいくつか紹介 する． 以下の例で 関数 add and scale(a, b, c) は (a + b) · c を返す． 

**Python3**

```python
def add_and_scale(a: int, b: int, scale: int = 1) -> int:
```

''' return sum of a and b, optionally multiply it by scale と解釈される． 

**実行例**

```text
>>> add_and_scale(1, 2)
>>> add_and_scale(1, 2, 100)
>>> add_and_scale(' 1' , ' 2' ) # 異なる型でも，...
>>> add_and_scale(' 1' , ' 2' , 10)
12121212121212121212
```

関数呼び出しの際に，変数名を指定すること，また (その場合に) 記述の順序を入れ替えることがで きる． 

**実行例**

```text
>>> add_and_scale(a=1, b =2, scale =10)
>>> add_and_scale(scale=10, a =1, b =2)
```

## B.6 2025 年度の変更 (p.200)

<!-- source: pdf_page=200; md_page_heading=p.201 -->

B.6 2025 年度の変更 B.6 2025 年度の変更 2025 年度は以下の変更が行われた:
- Python package としてインストール可能に
- サーバ sample/server.py が Python に移植され，Ruby のコードは不要となった
- ゲーム開始前のプロトコルを拡張し，ゲームのマップの大きさなどを指定可能とした． 詳しくは python3 sample/server.py --help で指定可能なオプションの一覧を参照
