# 2026p.pdf メモ

## 第7章 インターフェース
- 対応ページ: 125-132
- 索引上の開始ページ: 125

### p.125
124 7.1 内部状態を持つオブジェクト 問題 変更可能な二分探索木 (BST ree) (optional) 先週作成した二分木のクラスを参考に，変更可能な二分探索木のクラス BSTree を用意せよ． さらに，これらを用いて，自分自身が 2 分探索木であるときに値を追加するメソッド add(x) を作成せよ． 空の木である EmptyTree や is empty の定義は適当に変更して良い． オプション: 二分探索木 tree の任意の節点 node について，節点 node を削除した木を作る関 数 t…

### p.126
125 7.2 インターフェース BankAccount balance password withdraw(amount, password) deposit(amount, password) 詳しくは UML やクラス図などのキーワードで調査してみよう． 7.2 インターフェース オセロやすごろくなどのゲームをプレイするプレイヤを考える．複数のプレイヤにはそれぞれ個性 があり，同じ状況でも異なる選択肢を選択するが，同じゲームをプレイするとする．このような場合 にはゲームをプレイするのに必要なプレイヤの機能…

### p.127
126 7.2 インターフェース Reward = [ 6 [ 2, 0 ], # 自分が協調した 7 [ 3, 1 ], # 自分が裏切った 8 ] 9 プレイヤにはどのような機能があれば良いだろうか ? まずは，協調か裏切りかを返すメソッド play が必須である．さらに結果を集計する便宜を考えて，名前を返すメソッド name を持たせる． 例 と し て 次 の 3 種 類 の プ レ イ ヤ を 考 え る: 必 ず 協 調 す る CooperatePlayer，必 ず 裏 切 る DefectPlay…

### p.128
127 7.2 インターフェース Python3 def play_one_game(player_a, player_b): 1 act_a = player_a.play() 2 act_b = player_b.play() 3 if not valid_action(act_a): # 行動がルールに従っているかを確認 4 raise ValueError 5 if not valid_action(act_b): # 行動がルールに従っているかを確認 6 raise ValueError 7 rewar…

### p.129
128 7.2 インターフェース 関数 play one game に 3 種類のどのプレイヤを渡しても動くことに注目されたい．仮にもし，対戦 するプレイヤの組み合わせごとに play one game random versus cooperate のように別々の関数を 作る必要があるとしたら，耐えられない手間となってしまう．この例では，3 種類のプレイヤがどれも 共通に name と play という一字一句同じ名前のメソッドを持っている点が重要である．外から見て (使う立場で) オブジェクトがどのような振る…

### p.130
129 7.2 インターフェース # print による表示は，ゲームを繰り返す場合は冗長なので除いておく 15 16 return act_a, reward_a, act_b, reward_b 17 今 ま で の プ レ イ ヤ は 相 手 が 誰 で も 気 に し な い(行 動 を 変 え な い) の で ，update(my action, op action) の動作は空で良い．しかしメソッド自体は定義しないと，実行時に上記 9 行目や 10 行目 でエラーとなってしまう． 3 つのクラス全て…

### p.131
130 7.2 インターフェース Python3 class CooperatePlayer(Player): 1 def name(self): 2 return "CooperatePlayer" 3 4 def play(self): 5 return Cooperate 6 親クラスのメソッドは継承されるので update は各クラスで，親クラスのものが使われる．一方， name と play は子クラスで定義されているので，そちらの新しい内容が使われる．これを 上書き (overriding) という．…

### p.132
131 7.3 この章の提出課題 問題 tit-for-tat (TitF orT atPlayer) 繰り返し囚人のジレンマゲームでは， tit-for-tat が有力な戦略とされている．この戦略で は，基本は協調するが，相手が裏切った場合は次のターンで自分も裏切る． この戦略を用いる TitForTatPlayer を作成し，今までに作ったプレイヤ 4 種類に対して，それ ぞれどのように振る舞うかを観察せよ． なおこの問題の主旨は，クラスの理解も兼ねているので，資料の流れに沿って実装すること． テスト部分は概…
