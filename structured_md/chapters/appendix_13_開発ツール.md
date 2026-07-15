# 付録A 開発ツール (p.179-190)

<!--
source_pages: 179-190
source_md_pages: 180-191
chapter_id: 付録A
title: 開発ツール
keywords: 開発ツール, バージョン管理システムと最小限のgit, さいしょの目標, 初期設定, ユーザ情報の設定, リポジトリの初期作成, 既存のリポジトリを複製する場合, 新規リポジトリを作成する場合(参考), ファイルの変更と登録, git add とcommit の関係, 履歴の活用, リモートコンピュータの利用— SSH, 公開鍵暗号システムを用いた認証, 鍵ペアの作成, 公開鍵の登録, ログイン, リモートリポジトリの利用と共同開発, 上流リポジトリの作成, 上流リポジトリの活用, 複数人での開発
-->

## この章の構成

- A.1 バージョン管理システムと最小限のgit (p.179-183)
- A.1.1 さいしょの目標 (p.179)
- A.1.2 初期設定 (p.180)
- ユーザ情報の設定 (p.180)
- リポジトリの初期作成 (p.180)
- 既存のリポジトリを複製する場合 (p.181)
- 新規リポジトリを作成する場合(参考) (p.181)
- A.1.3 ファイルの変更と登録 (p.181-183)
- git add とcommit の関係 (p.182-183)
- A.1.4 履歴の活用 (p.184)
- A.2 リモートコンピュータの利用— SSH (p.184-186)
- A.2.1 公開鍵暗号システムを用いた認証 (p.184-186)
- 鍵ペアの作成 (p.185)
- 公開鍵の登録 (p.185)
- ログイン (p.186)
- A.3 リモートリポジトリの利用と共同開発 (p.187-190)
- A.3.1 上流リポジトリの作成 (p.187)
- A.3.2 上流リポジトリの活用 (p.188)
- A.3.3 複数人での開発 (p.189-190)

## A.1 バージョン管理システムと最小限のgit (p.179-183)

### A.1.1 さいしょの目標 (p.179)

<!-- source: pdf_page=179; md_page_heading=p.180 -->

付録 A 開発ツール A.1 バージョン管理システムと最小限の git 概要 継続的な開発 (関連するファイル群に継続的に変更を加えるような状況) では，過去の履歴を保 存し，バージョン管理システムの使用を勧める (義務とはしない)．さらに，ネットワークで共 有することで，自宅と大学など複数の場所での開発で連携をとったり，グループで共同開発す ることにも可能である．ツール類は日々新しい物が登場するので，良いツールを見極める目を 養う必要がある．ここでは git を中心に紹介する． A.1.1 さいしょの目標 長 期 的 に 開 発 す る ソ ー ス コ ー ド や ，文 書 (markdown, LaTeX, html 等) の管理について， まずは以下の目標を同時に実現しよう
- いつでも過去のバージョンを取り出せる
- 複数のファイルを一貫して管理する
- 通常は最新版だけが見えている
- 記録したくない変更は記録しない Help:避けたいこと
- report-new2.pdf と report-0706- 1.pdf は ど っ ち が 新 し い ん だ っ け? 何を変更したんだっけ?
- いつのまにか bug が発生して，動か ない機能があった 図 A.1 ProGit ( 図 1.5) の説明 — 縦の列の単位でバージョンを管理する．おおむね時刻と対応する．

### A.1.2 初期設定 (p.180)

#### ユーザ情報の設定 (p.180)

#### リポジトリの初期作成 (p.180)

<!-- source: pdf_page=180; md_page_heading=p.181 -->

A.1 バージョン管理システムと最小限の git /lightbulb インストール 各自の PC で使う場合は，インストールが必要な場合もある．
- macOS: 最近は標準で入っている． もしなければ brew install git (homebrew を使っている場合)
- Ubuntu: apt install git
- Microsoft Windows: 9.A 節 で紹介した， gitbash ( https://gitforwindows.org/) ま たは wsl のどちらでも良い．(VSCode を使っていてそのターミナルで git --version な どのコマンドが動作すればそれを使えば十分) /lightbulb GUI 本資料では，git の概念との対応を重視してターミナルでの cui コマンドを紹介する．しかし， 実用的には (基本を習得後は) GUI を使う方が便利であろう．たとえば以下の URL に，様々な 選択肢が紹介されている (有料のものもあるので注意)．VSCode を使っているならそのプラグ イン，初めて試すなら GitHub Desktop が候補と思われる．なお担当教員は，Emacs と Magit を使っているがここでの紹介は割愛する． https://git-scm.com/downloads/guis A.1.2 初期設定 ユーザ情報の設定 各計算機 (あるいそのログインアカウント) ごとに 1 度だけ，ユーザ名と電子メールアドレスを設定 する．共同作業が前提の場合は普段使うアドレスが適するが，一人で使う分にはなんでも良い．後で 変更可． 

**Terminal**

```bash
$ git config --global user.name "Hanako Komaba"
$ git config --global user.email "xxxx@g.ecc.u-tokyo.ac.jp"
```

リポジトリの初期作成 git で管理する単位 (一連のファイルやフォルダ) を プロジェクト と呼ぶ．また，ユーザがプロジェ クト内のファイルを編集する場所を ワーキングディレクトリ と呼ぶ．なお，プロジェクトがフォルダ を含む場合は，そのルートをワーキングディレクトリとする．プロジェクトを管理するための git の 単位を リポジトリ と呼ぶ．最初に紹介する使い方では，ワーキングディレクトリ，リポジトリそれぞ れが 1:1 で対応する．大学の計算機と個人 PC の両方で同じプロジェクトを開発する場合は，1 つのプ ロジェクトに複数のワーキングディレクトリが対応する．

#### 既存のリポジトリを複製する場合 (p.181)

#### 新規リポジトリを作成する場合(参考) (p.181)

### A.1.3 ファイルの変更と登録 (p.181-183)

<!-- source: pdf_page=181; md_page_heading=p.182 -->

A.1 バージョン管理システムと最小限の git 既存のリポジトリを複製する場合 既存のリポジトリを複製して作業を始めるには git clone を用いる．github 等の公開リポジトリか ら，ソースコードを入手する場合もこれに従う 

**Terminal**

```bash
$ git clone URL
```

複 製 元 の リ ポ ジ ト リ をupstream repository (上流), 手元を local repository と呼ぶ． .git/...working directory /destlocal repository source.py ☁/b♀dngupstream repository clone clone 操作後に通常目にするのは， working directory 内のファイル群で，当該リポジトリの最新の ものである．それ以外に，隠しフォルダ .git の中には，過去の履歴や，複製元の URL などが格納さ れている． このように clone したプロジェクトに変更を加える前に，以下のように local-changes というブ ランチ (保存先) を新たに作成するとよい． 

**Terminal**

```bash
$ git checkout -b local-changes
```

ブランチは，自分の変更の歴史を隔離して管理する仕組みである．上流 repository は独自の開発の 歴史を持つので，それと分けることが，ここでの目的． 潜水艦ゲームの導入 (B.2 節) においても，この手順に倣った． 新規リポジトリを作成する場合 (参考) プロジェクトを新規に始める場合，以下のよ うに新規フォルダを作成後に，そのフォルダ内 で git init を行いリポジトリを作成する．こ こではプロジェクト名を project とする． 

**Terminal**

```bash
$ mkdir project
$ cd project
$ git init
```

既にソースコード等をおいたフォルダを対象 として，git リポジトリを作ることもできる．右 図は ProgrammingLab というフォルダの例． 

**Terminal**

```bash
$ cd ProgrammingLab
$ git init
```

その後，管理するファイルを git add で指定し，git commit で最初のバージョンを登録する．こ れらの操作は，次に説明するファイルの変更と登録次の操作と同じ． A.1.3 ファイルの変更と登録 ソースコードを編集・あるいはファイルを追加後に，リポジトリに記録するファイルを git add で 指定する．

#### git add とcommit の関係 (p.182-183)

<!-- source: pdf_page=182; md_page_heading=p.183 -->

A.1 バージョン管理システムと最小限の git 指定するファイルは，既存のものでも新規に 作成したものでも良い．たとえば hello.py な ら，右記の操作を行う． 

**Terminal**

```bash
$ git add hello.py
```

複数のファイルを指定する場合は， 度に登録することも，何度かに分けて登録することもできる． また，間違えて指定した場合に取り消すこともできる． git add 後に，該当ファイルをもう一度編集 した場合は git add を再度行う． 現時点で管理したいファイルをすべて指定したら，最後に commit という操作を行う． Terminal % git commit -m ' msg' 1 `msg` の部分は自分のメモである．たとえば `initial version` などとする． commit によ り，一連のファイルのスナップショットとバー ジョン ID が作成される． /desktop .git/... repository working directory source.py commit add 通常は，add と commit 相当の操作を GUI で 行うことが多い．たとえば，Visual Studio Code では，+ ボタンで add，✓ ボタンで commit を 行う． /lightbulb これまでの成果 ここまでで，自身の変更を加えたバージョンが登録された．今後，現在見えているファイルを どのように変更しても，いつでもこのバージョンに戻したり，内容の差分を調査したりするこ とができる． git add と commit の関係 git commit によりいつでもスナップショットをとることができる．あとから見て分かりやすい状 態で commit すると良い．指針はたとえば，
- 動くコード，test をすべて pass するもの．
- 保存したいコード (臨時で書いた debug 用 print などは，あとから読んだときに邪魔になりがち)
- 前回からの commit からの目的が，単一．

<!-- source: pdf_page=183; md_page_heading=p.184 -->

A.1 バージョン管理システムと最小限の git 3 点目について，はじめは 1 日 1 回作業終了時に commit することから始めて，慣れてきたら，機能 A の実装など区切りの良い単位で細かく commit を行うと良い． git では意図通りの commit を作るためのサポートとして，commit の準備用の staged という中間段 階を用いて，2 段階で commit を行う． /desktop .git/... repository source.py staged working directory source.py add commit 第 1 段階では， commit に入れたい (スナップショットをとりたい ) ファイルを git add で指定す る．これにより，まずワーキングディレクトリのファイルの内容のスナップショットが staged 領域に 作られる．どのファイルがどの状態にあるかは，git status で確認できる． 複数のファイルの編集・変更を登録する場合 は，1 度に add することも， 何度かに分けて登録 することもできる． Terminal % git add files 1 変更内容の確認は，git diff で行う．stage に準備したものかどうかで，コマンドのオプションが 変わる．
- git diff ワーキングディレクトリと stage された内容との差分 (次の commit に 含まれない)
- git diff --cached stage された内容と 最新の commit との差分 (次の commit に 含まれる) 第 2 段階として，意図通りに登録できたことを確認したら， git commit を行う．これにより， staged にあるスナップショットで commit が作成され新しくバージョン ID を付与する．図 A.1 の時 系列が右に一列進むことに相当する． Terminal % git commit -m ' message' 1 注意点として， git add 後に，該当ファイルをもう一度編集した場合，そのままではその変更は commit には含まれない． 2 種類の diﬀ で確認をすればそのような場合にも気づくことができる．な お，編集後に git add を再度行えば，最新の内容が stage される． commit に入れる予定でないファイルや変更 を，間違えて add した場合には，取り消すこと もできる．本資料では，git restore を勧める． Terminal % git restore --staged filename 1

### A.1.4 履歴の活用 (p.184)

## A.2 リモートコンピュータの利用— SSH (p.184-186)

### A.2.1 公開鍵暗号システムを用いた認証 (p.184-186)

<!-- source: pdf_page=184; md_page_heading=p.185 -->

A.2 リモートコンピュータの利用 — SSH A.1.4 履歴の活用 commit を活用して，様々な操作が実行可能である．それぞれの目的のために沢山のコマンドが用意 されているので，当面は必要になったら調べる方針が良い． 過去の commit の一覧を見る． Terminal % git log 1 同 1 行で commit の一覧を見る． Terminal % git log --oneline 1 変更点も含めて読む Terminal % git log -p 1 過去の特定の時点でのファイルの内容の表示 Terminal % git show バージョン文字列: ファイル名 1 同差分の表示 Terminal % git diff バージョン文字列 ファイル名 1 A.2 リモートコンピュータの利用 — SSH 目的 家から大学の計算機上のプログラムを読み書きする．github を使うなど． SSH を用いると， 「ターミナル」で行う操作を(たとえば git コマンドも) 遠隔から行うことができ る．情報系ではほぼ必須の技能である．また，SSH の認証部分は，github など多くのサービスで採用 されている．そのため，認証部分だけでも理解しておくことが望ましい． A.2.1 公開鍵暗号システムを用いた認証 公開鍵暗号システムでは，ユーザ毎が 鍵ペア (公開鍵, 秘密鍵) を作成して用いる．サーバは秘密鍵 の所有者のログインを許可し，所有しないもののログインを拒絶する．加えて，通信データを暗号化 する． 公開鍵 公開して用いる． SSH ログインの場合は，ログイン 先 のサーバに置く．ログイン先のサー

#### 鍵ペアの作成 (p.185)

#### 公開鍵の登録 (p.185)

<!-- source: pdf_page=185; md_page_heading=p.186 -->

A.2 リモートコンピュータの利用 — SSH バが，ログインを試みるものが行った電子署名をこの公開鍵を用いて検証する．サーバでの置き 場所は，標準的には /tildelow /.ssh/authorized keys． 秘密鍵 ユーザの手元で 1 つのファイルを秘密に保つ．ssh でログインを試みる際に，秘密鍵を用いて 署名を作成しサーバに提出する．標準的には /tildelow /.ssh/id method ． (method の部分は方式の名前 で，rsa や ecdsa が入る) 鍵ペアの作成 ssh-keygen コマンドにより，公開鍵 /search と秘 密鍵 /paint-brush のペアを作成する.1）下記の実行例は，手 元のノート PC ( 等) でのユーザ名が hanako の 場合． /desktop /home /tildelow / .ssh/ /search id rsa.pub (id ecdsa.pub) /paint-brush id rsa (id ecdsa) 

**Terminal**

```bash
$ ssh-keygen
```

Generating public/private rsa key pair. Notice 

> **Notice:** 注意 もし，秘密鍵が盗まれると (ノート PC 盗難やウィルス感染を含む )，盗んだ人はログインして あなたの権限を行使できる．その場合，まず間違いなくそこを踏み台に他のサーバを攻撃する ので，被害はユーザ個人に留まらない．そのようら可能性が分かった際は，速やかにログイン 先サーバの管理者に届け出ること．最後の砦がパスフレーズだが，時間がたてば破られてし まう． 鍵 ペ ア 作 成 に お け る 一 次 資 料 と し て はopenssh の マ ニ ュ ア ル https://man.openbsd.org/ ssh-keygen を参照されたい． 公開鍵の登録 /desktop /home /tildelow / .ssh/ /search id rsa.pub (id ecdsa.pub) /paint-brush id rsa (id ecdsa) /server /building/tildelow / .ssh/ /search /search /search authorized keys upload 1） 暗号化と復号の文脈では，公開鍵が錠前 /unlock秘密鍵が ὑ1 とたとえることもあるが，今回は署名と検証に使うので，専用検査 キット /search と特殊インク /paint-brush の意図でたとえた．

#### ログイン (p.186)

<!-- source: pdf_page=186; md_page_heading=p.187 -->

A.2 リモートコンピュータの利用 — SSH 作 成 し た 公 開 鍵 を ，login 先 の サ ー バ に 登 録 す る ．ECCS や github な ど の サ ー ビ ス で は ， Web か ら 行 う こ と が で き る ．ECCS の 場 合 は「SSH サ ー バ 公 開 鍵 ア ッ プ ロ ー ド 」 https: //portal.ecc.u-tokyo.ac.jp/key_upload を用いる． 大学研究室など多くの通常のサーバでは， /tildelow /.ssh/authorized keys が公開鍵を登録するべき場 所となる．管理者に依頼するか， ECCS の場合は自身で端末にログインし，該当ファイルに公開鍵を コピーペーストしても良い．なお， /tildelow /.ssh/authorized keys には複数の鍵を登録できる．テキスト ファイルで，1 行に 1 つの鍵を登録する． ログイン ログインには ssh コマンドを使う @の前がユーザ名，後にホスト名を書く．なお， github 等のサー ビスで ssh の公開鍵の認証を用いる場合は，ここで説明するログインには対応していない．次の節に 進まれたい． 次の例は，ログイン先でのユーザ名が 9876543210 で， ssh01.ecc.u-tokyo.ac.jp にログインす る例である． 

**Terminal**

```bash
$ ssh 9876543210@ssh01.ecc.u-tokyo.ac.jp
```

このとき，秘密鍵を使うためにパスフレーズを聞かれたらタイプする．ログインに成功したら，リ モートでコマンドを実行することができる．下図はログイン後に date コマンドをログイン先で実行 し，実行結果を手元のターミナルで受け取った例である． /desktop /home /keyboard /server /building ssh username @server login ok date Fri Apr 10:15:30 AM JST 2024 ECCS 環境に ssh ログインする方法の詳細は次の URL を参照 https://www.ecc.u-tokyo.ac.jp/ system/outside.html#ssh /lightbulb 発展 何 度 も ロ グ イ ン す る 際 に ，パ ス フ レ ー ズ を い ち い ち 打 た ず に 行 う に は ，ssh-agent や ForwardAgent などの仕組みを調べると良い．またホスト名の短縮表記やユーザ名の省略記法 については，.ssh/config の設定方法を調べると良い．ファイルのコピーは scp, rsync など を調べると良い．

## A.3 リモートリポジトリの利用と共同開発 (p.187-190)

### A.3.1 上流リポジトリの作成 (p.187)

<!-- source: pdf_page=187; md_page_heading=p.188 -->

A.3 リモートリポジトリの利用と共同開発 A.3 リモートリポジトリの利用と共同開発 目的 ノート PC とデスクトップなど複数の環境のどこでも開発する．グループで，作業を共有する． 研究室で，卒論やソースコードを教員に見せる．などの状況を想定する． ここで紹介する使い方では，共通の 上流 (upstream) リポジトリを作成し，全リポジトリの commit 集約・管理する．各作業場所では，これまで同様ローカルに git のリポジトリを持つとともに，その 内容を上流リポジトリと同期する．手元の変更を上流に送る操作を push, 上流に存在する変更を手元 に取り込む操作を pull と呼ぶ． .git/... /desktoprepository /desktopworking directory source.py commit ☁ /buildingupstream repositorypush pull .git/... /home repository /home working directory source.py pull A.3.1 上流リポジトリの作成 ファイルシステム上に作成する場合と，外部サービスを利用する場合に分けて説明する．前者は， git コマンドやファイル操作を使える環境なら場所を問わない．つまり，手元のコンピュータでも ECCS でも良い． ファイルシステム上の場所を決め，リポジト リを設定する．右記は， /tildelow /git に projectname 用のリポジトリを作成する例である．オプショ ン --bare に注意． 

**Terminal**

```bash
$ mkdir ˜/git
$ cd ˜/git
$ git init --bare projectname.git
```

外部サービスを使う場合は，リポジトリはウェブ等のユーザインターフェースで作成することが 多い． 利用可能な外部サービスとしては github ( https://github.com/) が現在最も有名である．学生特 典もある．他に，bitbucket (https://bitbucket.org/) や gitlab ( https://about.gitlab.com/) も 選択肢で，教員としては，特定のサービスを勧めるわけではない．一般にどのサービスでもアカウン トを作成する必要がある．その際には何らかの契約が行われるので， terms and conditions (terms of service, terms of use) などの文書を熟読すること。通常は，サービス提供側の免責が書いてあること が多いが，利用者の義務が課せられていないかどうかを注意して読むこと．一般に自分が同意した

### A.3.2 上流リポジトリの活用 (p.188)

<!-- source: pdf_page=188; md_page_heading=p.189 -->

A.3 リモートリポジトリの利用と共同開発 ファイルは，保存しておくことを推奨． A.3.2 上流リポジトリの活用 これまで開発してきた手元のリポジトリと上流リポジトリをつなげる方法，つづいて，上流リポジ トリを共有する新しい作業場所を作る方法を説明する． まず，上流リポジトリ (がどこか) を特定するためには (一般の意味の) URL を用いる．よく使うも のは次の 2 通り．
- 同じ計算機のファイルシステムの場合，ファイルパスを使う． 例 /tildelow /git/projectname.git
- リモートの計算機を ssh login で使う場合や github のように ssh での認証をする場合は，リモー トのユーザ名，@，リモートのサーバドメイン名，:，リモートでのファイルパス，をつなげる． 例 git@github.com:tkaneko/submarine-py.git, git+ssh://9876543210@ssh01.ecc.u-tokyo.ac.jp:/home/9876543210/git/projectname.git 正式には，git+ssh: のようなプロトコルの指定を URL の先頭に書くが，多くの場合省略可能． ローカルのリポジトリに上流を指定するには， 右図の 2 つのコマンドを使う． git remote add までが動作の指示で， origin は上流を表す名称 (当面このまま使う)． 

**Terminal**

```bash
$ git remote add origin URL
$ git push -u origin main
```

main は，ブランチ と呼ばれる歴史の名前に相 当し，最初の git init の際に標準のブランチ として自動で設定された名前である． git に馴 染んだら，開発バージョンと安定バージョンな どブランチを分けることが有用である．2） /lightbulb main v.s. master default の branch 名 称 は ，新 し め の 環 境 で は main が 標 準 的 で あ る ．古 く は master が使われていた． 2） https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell

### A.3.3 複数人での開発 (p.189-190)

<!-- source: pdf_page=189; md_page_heading=p.190 -->

A.3 リモートリポジトリの利用と共同開発 上流の場所は，git remote -v で確認できる． 出力の fetch と push はそれぞれアップロード とダウンロードに対応する．今回は同じ URL が 表示されるはずである． 

**Terminal**

```bash
$ git remote -v
```

origin URL (fetch) 新しい環境に作業場所を設定するには，git clone を用いる． 

**Terminal**

```bash
$ git clone URL
```

/lightbulb これまでの成果 ここまでで，複数の開発環境を，共通の上流リポジトリを通じて，同期させる準備ができた． 今後，典型的な開発は以下のようになる
- ワーキングディレクトリで通常の開発を行い，commit する．この時点では，そのコミットは手元 でのみ使える．
- push により，上流リポジトリに新しいコミットを送る．
- 別のワーキングディレクトリでは，新たに編集する前に pull により，上流リポジトリの新しい コミットをローカルに反映させる Notice 

> **Notice:** 注意 pull する前に手元のファイルを編集したり，手元の編集履歴を push する前に別の場所で push が行われて上流の履歴が書き換わると，編集履歴が二股に別れる．そのようなコミット自体は 保存されているので，後から対応可能である．とはいえ，分かれた履歴の統合手順を学ぶまで は，上記の手順に従うことがお勧め． A.3.3 複数人での開発 リポジトリは，通常は個人用に初期設定される．共同作業を行う場合は，読み書きの権限を適切な 人で共有する必要がある． 共通の外部サービスを使っている場合は，ユーザごとに read, write などの権限を設定できる．研究 室などでファイルシステムを使う場合は，OS の「グループ」を使ったアクセス制限が可能である．た だ eccs の student グループは学生全員となってしまうため，目的に適さないことが多いと思われる． 参考書籍 Pro Git ( 初めの 1-2 章に目を通せば十分使える) がお勧め

<!-- source: pdf_page=190; md_page_heading=p.191 -->

A.3 リモートリポジトリの利用と共同開発
- 和訳の PDF, epub など http://progit-ja.github.io/，
- 和訳の HTMLhttp://git-scm.com/book/ja
