import pymupdf4llm
import pathlib


md_text = pymupdf4llm.to_markdown("./books/cap.pdf")
pathlib.Path("cap.md").write_bytes(md_text.encode())
