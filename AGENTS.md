# AGENTS.md

このリポジトリは、学校課題を解くための資料・課題文・回答草案・提出用ファイルを管理する作業用リポジトリである。
AI agent は、`structured_md/` 以下の講義資料を参照しながら、ch01〜ch09 の提出課題に対して、正確で検証可能な実装・回答を作成すること。

## 基本方針

* 対象とする課題は、原則として **ch01〜ch09** の各章末にある提出課題である。
* 課題文を最優先の仕様として扱う。
* 回答・実装は、講義資料に基づいて作成する。
* 各章の最後にある「この章の提出課題」またはそれに相当する節を必ず確認する。
* 講義資料に根拠がある場合は、該当章・該当ページを明示する。
* 不明な点を推測で補わない。
* 生成した回答・コード・notebook は、人間が読んで理解しやすく、後から修正しやすい形にする。
* Python 課題では、提出用 notebook を直接作り始めず、まず `.py` ファイルで実装・検証する。
* Codex は notebook 作成だけで完了せず、notebook の実行確認まで行う。

## 対象範囲

取り組む対象は次の章である。

```text
ch01
ch02
ch03
ch04
ch05
ch06
ch07
ch08
ch09
```

各章について、章末の提出課題を確認し、提出に必要な実装・説明・実行確認を行う。「どれか一つでいい」と言われている場合も、全ての問題に対して回答を行う。
•問題(? なし) を全てPython で解く(通常コース)
•? つきの問題を解く(通常コースに苦労がない場合)
のような指示がある場合、?の判定が厳しいと思うので全ての問題について回答を行う。



## ch と week の対応

原則として、章番号と提出 notebook の week 番号は次のように対応させる。

```text
ch01 -> week1
ch02 -> week2
ch03 -> week3
ch04 -> week4
ch05 -> week5
ch06 -> week6
ch07 -> week7
ch08 -> week8
ch09 -> week9
```


## 参照すべき資料

講義資料は `structured_md/` に整理されている。

主要ファイル:

* `structured_md/index.md`

  * 人間向けの章一覧。
  * 全体像を把握するときに読む。

* `structured_md/agent_index.md`

  * AI agent 向けの短い検索索引。
  * 課題に関係する章・節を探すときに最初に読む。

* `structured_md/page_map.csv`

  * 目次行と、出力ファイル・ページ範囲の対応表。
  * 回答にページ番号を付けるときに参照する。

* `structured_md/chapters/`

  * 章別に分割された本文。
  * 実際の根拠確認にはこの中の章ファイルを読む。

## 提出課題の探し方

各章の提出課題は、章の最後にある。

優先して探す見出し:

* `この章の提出課題`
* `提出課題`
* `この章の課題`
* `総合問題`
* `提出条件`
* `回答例`
* `ヒント`

課題に取り組むときは、まず該当章ファイルの末尾付近を確認する。
必要に応じて、前半の説明・例題・問題・ヒントも参照する。

例:

* ch01: 第1章の提出課題を確認する。
* ch02: 第2章の提出課題を確認する。
* ch03: 第3章の提出課題を確認する。
* ch04: 第4章の提出課題を確認する。
* ch05: 第5章の提出課題を確認する。
* ch06: 第6章の提出課題を確認する。
* ch07: 第7章の提出課題を確認する。
* ch08: 第8章の提出課題を確認する。
* ch09: 第9章の提出課題を確認する。

## ページ番号の扱い

`structured_md/` は、元 PDF のページ番号と、OCR 元 Markdown のページ見出しのズレを補正している。

* 原典 PDF ページ: `pdf_page`
* 元 Markdown ページ見出し: `md_page_heading`
* CSV 目次のページ `p.X` に対して、元 Markdown 見出しは `p.(X+1)` に対応する。

章ファイル内には、次のようなコメントが含まれている場合がある。

```html
<!-- source: pdf_page=64; md_page_heading=p65 -->
```

回答・作業メモで参照ページを書く場合は、原則として **PDF ページ番号** を使う。

例:

```markdown
配列の要素の書き換えについては、4.1節で説明されている（p.64）。
```

## 実行環境

実行環境は Python3 を使用する。
パッケージ管理には `uv` を使用する。

原則として、Python 実行は次の形式を優先する。

```bash
uv run python script.py
```

notebook を扱う場合も、プロジェクトの Python 環境は `uv` で管理する。

必要に応じて、次のようなファイルを確認・作成する。

```text
pyproject.toml
uv.lock
.venv/
```

`.venv/` は Git 管理対象にしない。

## 提出フォーマット

提出形式は、原則として Jupyter Notebook から作成した次の形式である。

```text
weekN-(学生証番号).ipynb
```

ここで `N` は週・章に対応する番号である。

例:

```text
week1-1234567890.ipynb
week2-1234567890.ipynb
week3-1234567890.ipynb
```

提出直前に、`STUDENT_ID` を実際の学生証番号へ置換すること。
今回使用する学生証番号は'08252018'である。

## 実装・検証・notebook 作成の基本方針

提出用 notebook を直接書き始めるのではなく、まず `.py` ファイルで実装と検証を行う。

基本フローは次の通り。

1. 章末の提出課題を確認する。
2. `outputs/chNN/answer.py` に Python 実装を書く。
3. `uv run python outputs/chNN/answer.py` で実行確認する。
4. エラーがあれば `.py` 側で修正する。
5. 実行結果が課題条件を満たすことを確認する。
6. 検証済みコードを `notebooks/weekN-STUDENT_ID.ipynb` に反映する。
7. notebook を実行して、セルが上から順に正常終了することを確認する。
8. 実行済み notebook を保存する。
9. 最後に提出条件を満たしているか確認する。

`.py` は検証用の実装ファイル、`.ipynb` は提出用ファイルとして扱う。

## Python 実装ファイルの配置

Python 課題では、まず次の場所に実装ファイルを作る。

```text
outputs/chNN/answer.py
```

例:

```text
outputs/ch01/answer.py
outputs/ch02/answer.py
outputs/ch03/answer.py
```

実行確認は次のコマンドで行う。

```bash
uv run python outputs/chNN/answer.py
```

例:

```bash
uv run python outputs/ch03/answer.py
```

`answer.py` には、課題の条件を確認できる最低限の実行例を含める。
関数だけを書いて終了せず、必要に応じて `if __name__ == "__main__":` 以下に確認用コードを書く。

例:

```python
def solve(...):
    ...


if __name__ == "__main__":
    # 最小限の動作確認を書く
    print(solve(...))
```

## notebook への反映

`.py` で検証済みのコードを、提出用 notebook に反映する。

提出用 notebook は原則として次の形式にする。

```text
notebooks/weekN-STUDENT_ID.ipynb
```

notebook には、少なくとも次のセルを含める。

```markdown
# weekN 提出課題

## 課題の要約

課題で求められていることを簡潔に整理する。
```

```markdown
## 実装方針

どのような考え方で実装したかを簡潔に説明する。
```

```python
# 実装コード
```

```python
# 実行例・動作確認
```

```markdown
## 確認

課題条件を満たしていることを確認する。
```

notebook 内のコードは、`.py` で検証済みの内容と矛盾しないようにする。

## notebook の実行確認

Codex は、notebook を作成しただけで完了としてはならない。
提出用 notebook を実際に実行し、すべてのセルが上から順に正常終了することを確認する。

notebook の実行確認には、原則として次を使う。

```bash
uv run jupyter nbconvert \
  --to notebook \
  --execute notebooks/weekN-STUDENT_ID.ipynb \
  --output weekN-STUDENT_ID.executed.ipynb \
  --output-dir outputs/chNN/executed
```

例:

```bash
uv run jupyter nbconvert \
  --to notebook \
  --execute notebooks/week3-STUDENT_ID.ipynb \
  --output week3-STUDENT_ID.executed.ipynb \
  --output-dir outputs/ch03/executed
```

`jupyter` や `nbconvert` が未導入の場合は、必要性を確認した上で追加する。

```bash
uv add jupyter nbconvert ipykernel
```

ただし、不要な外部パッケージを安易に追加しない。
notebook 実行確認に必要な最小限のパッケージのみ追加する。

注意:

* `nbconvert --execute` は、notebook の配置場所や起動時のカレントディレクトリによって、`outputs/chNN/answer.py` の相対 import が失敗することがある。
* notebook から検証用 `.py` を参照する場合は、`Path` を使って notebook 基準で相対パスを明示するか、実行時の作業ディレクトリ差を吸収する書き方にする。
* `from outputs...` のような通常 import を使う場合は、`outputs/` と各 `outputs/chNN/` に `__init__.py` を置くか、`sys.path` を明示的に調整してから実行確認する。

## 実行済み notebook の扱い

実行済み notebook は、検証用として次に保存する。

```text
outputs/chNN/executed/weekN-STUDENT_ID.executed.ipynb
```

提出用 notebook 本体は、次に保存する。

```text
notebooks/weekN-STUDENT_ID.ipynb
```

提出時に実行結果が notebook 内に残っている必要がある場合は、実行済み notebook の内容を確認し、必要に応じて提出用 notebook に反映する。

## Codex に求める完了条件

Codex は、次の状態まで作業すること。

* `outputs/chNN/answer.py` が作成されている。
* `uv run python outputs/chNN/answer.py` が正常終了している。
* `notebooks/weekN-STUDENT_ID.ipynb` が作成または更新されている。
* notebook 内に、課題要約・実装方針・コード・実行例・確認が含まれている。
* notebook が上から順に実行できる。
* `nbconvert --execute` による実行確認が完了している。
* 実行済み notebook が `outputs/chNN/executed/` に保存されている。
* 実行ログまたは作業ログに、確認したコマンドと結果が記録されている。

## C++ 課題への対応

章によっては C++ の実装が求められる場合がある。

C++ 課題では、次を守る。

* 課題文で C++ が指定されている場合は、Python に置き換えない。
* C++ のソースコードは、notebook 内に貼るだけでなく、必要に応じて `.cpp` ファイルとして保存する。
* コンパイル方法と実行方法を明記する。
* C++11 が指定されている場合は、`-std=c++11` を使う。

例:

```bash
g++ -std=c++11 main.cpp -o main
./main
```

提出 notebook に C++ コードを含める必要がある場合は、notebook 内に次を含める。

* 課題文の要約
* C++ ソースコード
* コンパイル方法
* 実行例
* 実行結果
* 必要なら簡単な説明

C++ 課題の場合も、可能であれば `outputs/chNN/` 以下に検証用ファイルを保存する。

例:

```text
outputs/ch08/answer.cpp
```

コンパイル例:

```bash
g++ -std=c++11 outputs/ch08/answer.cpp -o outputs/ch08/answer
outputs/ch08/answer
```

## notebook 作成方針

提出用 notebook には、原則として次の要素を含める。

```markdown
# weekN 提出課題

## 課題の要約

課題で求められていることを簡潔に整理する。

## 実装方針

どのような考え方で実装したかを書く。

## コード

実装コードを書く。

## 実行結果

実行結果を貼る。

## 確認

課題文の条件を満たしていることを確認する。
```

notebook 内では、説明 Markdown セルとコードセルを適切に分ける。

過度に長い説明は避けるが、人間が採点・確認しやすい程度の説明は入れる。

## 推奨ディレクトリ構成

```text
project/
├── AGENTS.md
├── README.md
├── pyproject.toml
├── uv.lock
├── structured_md/
│   ├── index.md
│   ├── agent_index.md
│   ├── page_map.csv
│   └── chapters/
├── assignments/
│   ├── ch01.md
│   ├── ch02.md
│   ├── ch03.md
│   ├── ch04.md
│   ├── ch05.md
│   ├── ch06.md
│   ├── ch07.md
│   ├── ch08.md
│   └── ch09.md
├── notebooks/
│   ├── week1-STUDENT_ID.ipynb
│   ├── week2-STUDENT_ID.ipynb
│   └── ...
├── outputs/
│   ├── ch01/
│   │   ├── answer.py
│   │   └── executed/
│   ├── ch02/
│   │   ├── answer.py
│   │   └── executed/
│   ├── ch03/
│   │   ├── answer.py
│   │   └── executed/
│   ├── ch04/
│   ├── ch05/
│   ├── ch06/
│   ├── ch07/
│   ├── ch08/
│   └── ch09/
└── src/
```

`assignments/` は、章末課題だけを抜き出して管理したい場合に使う。
`notebooks/` は提出用 `.ipynb` を保存する。
`outputs/` は中間生成物・実行結果・補助コードを保存する。
`src/` は複数課題で再利用する補助コードがある場合に使う。

## 課題に取り組む手順

課題を解くときは、次の順序で進める。

1. 対象章を確認する。

2. `structured_md/agent_index.md` で対象章・関連キーワードを確認する。

3. `structured_md/chapters/` の該当章ファイルを読む。

4. 章末の「この章の提出課題」を特定する。

5. 課題文を箇条書きで分解する。

6. 必要な実装言語を確認する。

   * Python3 か
   * C++ か
   * notebook のみでよいか
   * 外部ファイルが必要か

7. 実装方針を短くまとめる。

8. Python 課題の場合は、まず `outputs/chNN/answer.py` に実装する。

9. `uv run python outputs/chNN/answer.py` で実行確認する。

10. 実行結果が課題条件を満たすか確認する。

11. 検証済みコードを提出用 notebook `notebooks/weekN-STUDENT_ID.ipynb` に反映する。

12. notebook を `nbconvert --execute` で実行確認する。

13. 実行済み notebook を `outputs/chNN/executed/` に保存する。

14. 参照した章・節・ページを notebook または作業メモに記録する。

15. 最終チェックリストを確認する。

## Python コード課題の方針

Python コードを書く課題では、以下を守る。

* Python3 で実装する。
* 講義資料内で扱われた書き方を優先する。
* 不必要に高度なライブラリや未習事項を使わない。
* 課題で標準ライブラリのみが想定される場合は、外部パッケージを追加しない。
* 実行可能なコードを書く。
* 可能であれば最小限のテストを作る。
* 実行方法を回答内または notebook 内に書く。
* notebook に移す前に、必ず `.py` ファイルで実行確認する。

Python ファイルを作る場合:

```text
outputs/chNN/answer.py
```

実行例:

```bash
uv run python outputs/chNN/answer.py
```

## uv の扱い

新しいパッケージが必要な場合は、安易に追加しない。
まず標準ライブラリまたは講義資料で扱われた範囲で実装できるか検討する。

パッケージ追加が必要な場合のみ、次を使う。

```bash
uv add package_name
```

実行確認は次の形式を使う。

```bash
uv run python path/to/script.py
```

notebook の実行環境が必要な場合は、プロジェクトの `.venv` を Jupyter kernel として使える状態にする。

notebook 実行確認に必要なパッケージがない場合のみ、次を追加してよい。

```bash
uv add jupyter nbconvert ipykernel
```

## レポート・説明課題の方針

レポートや説明を書く課題では、以下を守る。

* 講義資料の用語を優先して使う。
* 主張と根拠を分けて書く。
* 章・節・ページ番号を明示する。
* 断定しすぎず、資料から言える範囲で書く。
* 文字数指定がある場合は、概算ではなく実際に文字数を確認する。
* notebook に記述する場合は、Markdown セルとして読みやすく整理する。

## 参照表記

回答内では、できるだけ次の形式で参照を書く。

```markdown
（第4章 4.1「配列の要素の書き換え」, p.64）
```

複数箇所を参照する場合:

```markdown
（第3章 3.4「配列とループ」, p.52; 第4章 4.1「配列の要素の書き換え」, p.64）
```

提出 notebook にすべての参照を書く必要がない場合でも、作業メモには参照箇所を残す。

## OCR 崩れへの対応

`structured_md/` は OCR 由来の崩れを含む可能性がある。

* コードブロック、表、図キャプションは完全復元されていない可能性がある。
* 文字化けや不自然な記号がある場合は、文脈から慎重に読む。
* 意味が確定できない場合は、回答に使わないか、「OCR が不明瞭」と明記する。
* コードらしき部分は、前後の説明と合わせて解釈する。
* 提出課題の条件が不明瞭な場合は、同じ章の例題・問題・ヒントを確認する。

## agent_index.md の使い方

課題に取り組むときは、まず `structured_md/agent_index.md` を検索索引として使う。

例:

* 再帰に関する課題なら、`再帰`, `二分探索`, `Merge Sort` などで探す。
* クラスに関する課題なら、`クラス`, `オブジェクト`, `継承`, `インターフェース` などで探す。
* ファイル処理に関する課題なら、`CSV`, `JSON`, `path`, `テキストファイル` などで探す。
* Git や SSH に関する課題なら、`付録A`, `git`, `SSH`, `リモートリポジトリ` などで探す。

関連章が見つかったら、必ず `chapters/` の本文で確認する。

## 作業ログ

複雑な課題では、回答ファイルまたは notebook の末尾に簡単な作業ログを残す。

```markdown
## 作業ログ

- 章末の提出課題を確認した。
- `outputs/chNN/answer.py` を作成した。
- `uv run python outputs/chNN/answer.py` で実行確認した。
- `notebooks/weekN-STUDENT_ID.ipynb` を作成した。
- `uv run jupyter nbconvert --execute ...` で notebook の実行確認をした。
- 実行済み notebook を `outputs/chNN/executed/` に保存した。
```

## 禁止事項

* 課題文を読まずに回答を書き始めない。
* 章末の提出課題を確認せずに実装しない。
* 講義資料にない内容を、講義資料に書かれているかのように扱わない。
* ページ番号を推測で付けない。
* OCR が崩れている箇所を、確信なく修正しない。
* コード課題で、実行確認なしに「動作する」と断言しない。
* Python 指定の課題で、不要に別言語へ置き換えない。
* C++ 指定の課題で、Python だけで代替しない。
* notebook だけを作成して、`.py` での検証を省略しない。
* notebook の実行確認を省略しない。
* 不要に高度なライブラリや未習事項を使わない。
* 不要に大きな書き換えやファイル移動をしない。
* `.venv/` や実行キャッシュを Git 管理対象にしない。

## 最終チェックリスト

回答・notebook を完成させる前に、次を確認する。

* [ ] 対象章が ch01〜ch09 の範囲にある。
* [ ] 章末の提出課題を確認した。
* [ ] 課題文の要求にすべて答えている。
* [ ] 提出形式が `weekN-STUDENT_ID.ipynb` または指定形式になっている。
* [ ] 学生証番号が必要な箇所は、提出前に実番号へ置換する前提になっている。
* [ ] 実装言語が課題指定に合っている。
* [ ] Python 課題は Python3 で実装している。
* [ ] Python 実行は `uv run python ...` で確認している。
* [ ] C++ 課題の場合、コンパイル方法と実行方法を確認している。
* [ ] 参照した章・節・ページが記録されている。
* [ ] 講義資料外の知識を使った場合、その旨を書いている。
* [ ] OCR 不明瞭箇所を推測で補っていない。
* [ ] notebook 内に課題要約・実装方針・コード・実行結果・確認が含まれている。
* [ ] `outputs/chNN/answer.py` を作成した。
* [ ] `uv run python outputs/chNN/answer.py` が正常終了した。
* [ ] 検証済みコードを notebook に反映した。
* [ ] `notebooks/weekN-STUDENT_ID.ipynb` を作成または更新した。
* [ ] notebook を上から順に実行確認した。
* [ ] `nbconvert --execute` が正常終了した。
* [ ] 実行済み notebook を `outputs/chNN/executed/` に保存した。
