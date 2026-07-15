from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable

try:
    from pypdf import PdfReader
except ImportError as exc:  # pragma: no cover - runtime dependency message
    raise SystemExit(
        "Missing dependency: pypdf. Install it with `uv add pypdf` and rerun."
    ) from exc


ROOT = Path(__file__).resolve().parent
OUTLINE = ROOT / "outline.csv"
PDF = ROOT / "2026p.pdf"
MEMO = ROOT / "2026p_interface_memo.md"
FULL_MEMO = ROOT / "2026p_full_memo.md"


def find_interface_pages(rows: Iterable[dict[str, str]]) -> list[int]:
    pages: list[int] = []
    for row in rows:
        title = row["章タイトル"].strip()
        if title == "インターフェース" or title.endswith("インターフェース"):
            pages.append(int(row["ページ"]))
    return pages


def extract_pages(pdf_path: Path, start_page: int, end_page: int) -> dict[int, str]:
    reader = PdfReader(str(pdf_path))
    result: dict[int, str] = {}
    for page_num in range(start_page, end_page + 1):
        text = reader.pages[page_num - 1].extract_text() or ""
        result[page_num] = " ".join(text.split())
    return result


def extract_all_pages(pdf_path: Path) -> dict[int, str]:
    reader = PdfReader(str(pdf_path))
    result: dict[int, str] = {}
    for page_num, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        result[page_num] = " ".join(text.split())
    return result


def summarize_page(text: str, limit: int = 260) -> str:
    clean = " ".join(text.split())
    if len(clean) <= limit:
        return clean
    return clean[: limit - 1].rstrip() + "…"


def main() -> None:
    if not OUTLINE.exists():
        raise SystemExit(f"Missing file: {OUTLINE}")
    if not PDF.exists():
        raise SystemExit(f"Missing file: {PDF}")

    with OUTLINE.open(newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))

    pages = find_interface_pages(rows)
    if not pages:
        raise SystemExit("Could not find a chapter row for インターフェース.")

    start_page = pages[0]
    next_chapter_pages = [
        int(row["ページ"])
        for row in rows
        if row["章番号"].startswith("第") and int(row["ページ"]) > start_page
    ]
    end_page = min(next_chapter_pages) - 1 if next_chapter_pages else start_page

    extracted = extract_pages(PDF, start_page, end_page)
    full_extracted = extract_all_pages(PDF)
    page_summaries = {page_num: summarize_page(text) for page_num, text in extracted.items()}

    memo_lines = [
        "# 2026p.pdf メモ",
        "",
        "## 第7章 インターフェース",
        f"- 対応ページ: {start_page}-{end_page}",
        f"- 索引上の開始ページ: {start_page}",
        "",
    ]
    for page_num, summary in page_summaries.items():
        memo_lines.extend(
            [
                f"### p.{page_num}",
                summary,
                "",
            ]
        )
    MEMO.write_text("\n".join(memo_lines), encoding="utf-8")

    full_lines = [
        "# 2026p.pdf 全文メモ",
        "",
        "## 1-208ページ",
        "- 形式: 各ページを見出しで分け、抽出できた本文をそのまま記録",
        "",
    ]
    for page_num, text in full_extracted.items():
        full_lines.extend(
            [
                f"### p.{page_num}",
                text if text else "(本文抽出なし)",
                "",
            ]
        )
    FULL_MEMO.write_text("\n".join(full_lines), encoding="utf-8")

    print(f"outline.csv -> インターフェース starts at page {start_page}")
    print(f"PDF range: pages {start_page}-{end_page}")
    print(f"memo saved to: {MEMO.name}")
    print(f"full memo saved to: {FULL_MEMO.name}")
    print(f"pages captured: {len(full_extracted)}")


if __name__ == "__main__":
    main()
