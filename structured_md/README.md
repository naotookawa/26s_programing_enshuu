# structured_md

このフォルダは、`2026p_full_memo.md` を `outline.csv` の目次情報に基づいて再構成した初期版です。

## 方針

- 見出し末尾に原典PDFのページ番号を付与。
- 各章ファイル冒頭に `source_pages` / `source_md_pages` / `keywords` をコメントとして付与。
- 元mdのページ見出し `### p.N` は、本文PDFページより1大きいズレがあるため、CSVページ `p.X` に対して md見出し `p.(X+1)` を対応させています。
- 本文は意味を改変せず、軽微なOCR記号のみ置換しています。

## 主要ファイル

- `index.md`: 人間向け章一覧
- `agent_index.md`: AI agent向けの短い検索索引
- `chapters/`: 章別md
- `page_map.csv`: 目次行と出力ファイル・ページ範囲の対応表

## 注意

これは自動変換の初期版です。コードブロック・表・図キャプションの完全復元は、次段階で章ごとに追加整形する想定です。


## 整形方針メモ

この版では、初期版の章分割とページ対応を維持したまま、章本文に対して以下の整形を加えた。

- `Python3` / `C++` / `C++11` / `Terminal` / 実行例を、OCR上の行番号を手掛かりに fenced code block へ可能な範囲で復元
- `例題`・`問題`・`回答例`・`ヒント`・`提出条件`などのラベルを Markdown 上で探しやすい形に整形
- 箇条書き記号を Markdown bullet に変換
- Notice / Note 系の注意枠を blockquote に変換
- 元PDFページとmd上のページ見出し対応は `<!-- source: pdf_page=...; md_page_heading=p... -->` として維持

OCR由来の図表崩れ・文字化けは、原情報を失わないことを優先して残している。
