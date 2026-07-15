# 付録C 最終課題: 強化学習Gymnasium (p.201-208)

<!--
source_pages: 201-208
source_md_pages: 202-209
chapter_id: 付録C
title: 最終課題: 強化学習Gymnasium
keywords: 最終課題: 強化学習Gymnasium, インストール, 動作確認, ランダムプレイ, 賢い行動をさせる, 初めの一歩(案), 強化学習, 環境の選択
-->

## この章の構成

- C.1 インストール (p.201)
- C.2 動作確認 (p.201)
- C.3 ランダムプレイ (p.202)
- C.4 賢い行動をさせる (p.202-208)
- C.4.1 初めの一歩(案) (p.203)
- C.4.2 強化学習 (p.203)
- C.4.3 環境の選択 (p.203-208)

## C.1 インストール (p.201)

## C.2 動作確認 (p.201)

<!-- source: pdf_page=201; md_page_heading=p.202 -->

付録 C 最終課題: 強化学習 Gymnasium この章では，最終課題のオプションの一つである， Gymnasium について紹介する．歴史とし ては OpenAI Gym として始まり， OpenAI から Farama Foundation に開発が引き継がれ，名称も gymnasium に変化した． 強 化 学 習 は ，試 行 錯 誤 を 通 じ て 学 ぶ 方 法 で ，い ま 注 目 さ れ て い る 分 野 の 一 つ で あ る ．例: https://www.youtube.com/watch?v=TmPfTpjtdgg Gymnasium は ，さ ま ざ ま な 問 題(環 境) を 統 一 的 に 扱 う た め の ，イ ン タ ー フ ェ ー ス の 一 つ ． https://gymnasium.farama.org/ C.1 インストール 

**Terminal**

```bash
$ pip3 install --user ' gymnasium[classic-control,toy-text]'
```

Note旧版利用の場合 かつては gym という名称で配布されていた $ pip3 install --user gym C.2 動作確認 python3 を起動して import gymnasium as gym できれば成功． 

**Python3**

```python
import gymnasium as gym
env = gym.make(' CartPole-v1' , render_mode =' human' )
```

env.reset() 絵が出る．

## C.3 ランダムプレイ (p.202)

## C.4 賢い行動をさせる (p.202-208)

<!-- source: pdf_page=202; md_page_heading=p.203 -->

C.3 ランダムプレイ Note旧版利用の場合 import gym 1 env = gym.make(' CartPole-v0' ) 2 env.reset() 3 env.render() 4 C.3 ランダムプレイ 動作確認として，ランダムにプレイするエージェントの動作を確認する．初めに，環境 env を作 成する．`CartPole-v1` 以外にもさまざまな環境が用意されている (難しすぎるものもあるので注意 )． エージェントの行動は，step の引数として伝える．行動の選択肢は，env.action space で得られる． env.make 時に render_mode=' human' と指定しておくと render() で GUI 上に描画される．描画は 把握に有用だが必須ではない． 

**Python3**

```python
env = gym.make(' CartPole-v1' , render_mode =' human' )
```

env.reset() C.4 賢い行動をさせる env.reset() や env.step() を呼び出す毎に，状態と報酬を返り値として得られる．(上記のランダ ムプレイでは捨てているが)，それらを適切に活用することで，賢い行動を出来るようになる． 詳細は公式文書を参照: https://gymnasium.farama.org/1） 1） 旧版 https://www.gymlibrary.dev/

### C.4.1 初めの一歩(案) (p.203)

### C.4.2 強化学習 (p.203)

### C.4.3 環境の選択 (p.203-208)

<!-- source: pdf_page=203; md_page_heading=p.204 -->

C.4 賢い行動をさせる C.4.1 初めの一歩 (案) FrozenLake-v12）で (よい確率で3）) ゴールに到達するエージェントを作成せよ． これは API に慣れる (特に observation を活用する) 練習なので，(学習せずに)，行動選択方法を直 接プログラムに書き込んで良い． C.4.2 強化学習 経験から学習するには， 強化学習を用いると良い．ニューラルネットワークを使うことが最近の流 行だが，はじめは，表 (tabular) の Q 学習または Policy Gradient を勧める．詳しくは教科書を参照 : http://incompleteideas.net/book/the-book-2nd.html 他の人のコードを参考にした場合は，出典と参考にした内容について，提出物内できちんと説明す ること． C.4.3 環境の選択 さまざまな環境が用意されていて 4），それぞれ難易度が異なる．とくに入力が画像で与えられるも のは，はじめは避けること．(画像認識の訓練を GPU で行う経験を積んだのちに取り組む方が無難) 2） https://gymnasium.farama.org/environments/toy_text/frozen_lake/ 3） 床は滑る/回転するので，良い行動を選択していても運が悪いと穴に落ちる． 4） ゲーム以外でも，たとえば GUI の操作 https://github.com/Farama-Foundation/miniwob-plusplus

<!-- source: pdf_page=204; md_page_heading=p.205 -->

参考文献 参考文献 [1] 森畑明昌 「 Python によるプログラミング入門 アルゴリズムと情報科学の基礎を学ぶ」 ，東京大 学出版会，2019 年 [2] Peter Van Roy and Seif Haridi, "Concepts, Techniques, and Models of Computer Programming" MIT Press, 2004, https://ieeexplore.ieee.org/servlet/opac?bknumber=6267353 [3] 計算機プログラムの構造と解釈 http://sicp.iijlab.net/fulltext/ [GHJV95] Erich Gamma, Richrad Helm, Ralph Johnson, and John Vlissides. Design Patterns . Addison-Wesley, 1995. [4] Edmonds, J. (2008). How to Think About Algorithms. Cambridge: Cambridge University Press. doi:10.1017/CBO9780511808241 [5] 秋葉 拓哉，岩田 陽一，北川 宜稔， 「プログラミングコンテストチャレンジブック」第二版，マイ ナビ，2012 年, https://book.mynavi.jp/ec/products/detail/id=22672

<!-- source: pdf_page=205; md_page_heading=p.206 -->

索引 init , 112 argparse, 196 assert, 43, 44, 62 base64, 157 binary search, 90 commit, 182 composition, 121 deepcopy, 81 design patterns, 144 dict, 160 docstring, 138 doctest, 138 dunder, 117 elif, 30 else, 30 encapsulation, 116 evaluate, 21 expression, 21 Fibonacci numbers, 91 for, 13 formatted string, 197 Google Colaboratory, 10 help, 137 identity, 115 if, 16, 30 IndexError, 49 inheritance, 129 inorder, 106 jupyter, 9 koch, 93 logging, 197 matplotlib, 74 memoization, 122 merge sort, 95 module, 155 NameError, 48 node, 103 npz, 166 numpy, 164 overriding, 130 package, 155 postorder, 106 preorder, 106 print, 10, 11 pull, 187 push, 187 pytest, 43 recursion, 86 return, 25 slice, 96 staged, 183 statement, 10 this, 135 type, 137 ulimit, 101 UML, 125 unittest, 43 upstream, 187 utf-8, 11, 157 value, 21 variable, 23 205

<!-- source: pdf_page=206; md_page_heading=p.207 -->

variant, 137 virtual, 141 while, 96 値, 21 値渡し, 81 インスタンス, 112, 116 インターフェース, 125 インデント, 13 上書き, 130 オブジェクト, 115 改行, 12 仮想関数, 141 型, 21 カプセル化, 116 関数, 24 クラス, 111 クラス図, 125 継承, 129 コッホ曲線, 93 コンストラクタ, 135 再帰, 86 参照, 80 式, 21 条件分岐, 16 真偽値, 27 スタック領域, 101 制御変数, 13 整数, 12 節点, 103 漸化式, 86 代入, 50 抽象化, 23 抽象メソッド, 140 定数, 17 デザイン・パターン, 144 テストケース, 44 内部状態, 115 二項演算子, 22 二次元配列, 66 二重ループ, 15 二分木, 103 二分探索, 90 二分探索木条件, 107 根, 103 バイト列, 156 ハッシュ, 160 引数, 25 評価, 21 符号化方式, 156 フレーム, 100 ブロック, 13 文, 10, 11 変数, 23 末尾再帰, 87 メソッド, 112, 116 メモ化, 122 メンバ関数, 135 メンバ初期化子, 135 メンバ変数, 135 文字列, 28 ユニットテスト, 43 206

<!-- source: pdf_page=207; md_page_heading=p.208 -->

ライフゲーム, 73 リスト内包表記, 65 ループ不変条件, 52 例外, 135 連想配列, 160 207
