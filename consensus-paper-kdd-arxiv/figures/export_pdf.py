#!/usr/bin/env python3
"""
用法：python3 export_pdf.py [html文件名]
默认导出 figure-cases.html，输出同名 .pdf

说明：
  HTML 渲染尺寸 1440×680px（96dpi），对应物理尺寸：
    width  = 1440 / 96 * 25.4 = 381 mm
    height =  680 / 96 * 25.4 = 179.9 mm ≈ 180 mm
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright


def export_pdf(html_file="figure-cases.html"):
    base = Path(__file__).parent
    html_path = (base / html_file).resolve()
    pdf_path = html_path.with_suffix(".pdf")

    # 1440px / 96dpi * 25.4mm/in = 381mm
    # 680px  / 96dpi * 25.4mm/in ≈ 180mm
    page_width_mm  = round(1440 / 96 * 25.4, 2)   # 381.0 mm
    page_height_mm = round(680  / 96 * 25.4, 2)   # 179.92 mm

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 680})
        page.goto(f"file://{html_path}")
        page.wait_for_timeout(300)   # 等待字体渲染

        page.pdf(
            path=str(pdf_path),
            width=f"{page_width_mm}mm",
            height=f"{page_height_mm}mm",
            print_background=True,   # 保留背景色和图案
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
        )
        browser.close()

    print(f"✓ {pdf_path}")
    print(f"  page size: {page_width_mm}mm × {page_height_mm}mm")
    print(f"  (1440×680 px @ 96 dpi)")


if __name__ == "__main__":
    html_file = sys.argv[1] if len(sys.argv) > 1 else "figure-cases.html"
    export_pdf(html_file)
