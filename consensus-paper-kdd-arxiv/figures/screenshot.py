#!/usr/bin/env python3
"""
用法：python3 screenshot.py [html文件名]
默认截 figure-cases.html，输出同名 .png
"""
import sys
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

def screenshot(html_file="figure-cases.html"):
    base = Path(__file__).parent
    html_path = (base / html_file).resolve()
    png_path = html_path.with_suffix(".png")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 680})
        page.goto(f"file://{html_path}")
        page.wait_for_timeout(300)  # 等待字体渲染
        page.screenshot(path=str(png_path), full_page=False)
        browser.close()

    print(f"✓ {png_path}")

if __name__ == "__main__":
    html_file = sys.argv[1] if len(sys.argv) > 1 else "figure-cases.html"
    screenshot(html_file)
