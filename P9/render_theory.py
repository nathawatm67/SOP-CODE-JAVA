#!/usr/bin/env python3
"""สร้าง HTML ทฤษฎีพร้อมสารบัญจาก P9-THEORY.md โดยใช้ตัวแปลงของสไลด์."""
from pathlib import Path
import ast
import html
import re

HERE = Path(__file__).resolve().parent
# ใช้ฟังก์ชันแปลง Markdown เดียวกับสไลด์ โดยไม่รันส่วนสร้างไฟล์สไลด์
module = ast.parse((HERE / 'render_slides.py').read_text())
helpers = ast.Module(body=[n for n in module.body
                          if isinstance(n, ast.FunctionDef) and n.name in ('inline', 'blocks')],
                     type_ignores=[])
namespace = {'html': html, 're': re}
exec(compile(helpers, 'render_slides.py', 'exec'), namespace)
source = (HERE / 'P9-THEORY.md').read_text()
lines = source.splitlines()
title = lines[0].removeprefix('# ')
sections = re.split(r'(?=^## )', '\n'.join(lines[1:]), flags=re.M)
intro = namespace['blocks'](sections[0].splitlines())
toc, body = [], []
for number, section in enumerate(sections[1:], 1):
    heading, *content = section.splitlines()
    heading = heading.removeprefix('## ')
    anchor = f'section-{number}'
    toc.append(f'<li><a href="#{anchor}">{html.escape(heading)}</a></li>')
    body.append(f'<section id="{anchor}"><h2>{html.escape(heading)}</h2>'
                + namespace['blocks'](content)
                + '<p class="back"><a href="#toc">กลับสารบัญ ↑</a></p></section>')
css = '''
:root{font-family:"Noto Sans Thai",Tahoma,Arial,sans-serif;color:#172334;background:#f2f4f7;line-height:1.8;scroll-behavior:smooth}
*{box-sizing:border-box}body{margin:0}header{background:#172334;color:white;padding:42px max(24px,calc((100vw - 1160px)/2))}header a{color:#ffe09a}h1{line-height:1.4;font-size:clamp(26px,4vw,38px);margin:12px 0}.layout{max-width:1200px;margin:28px auto;display:grid;grid-template-columns:290px minmax(0,1fr);gap:28px;padding:0 20px}nav{position:sticky;top:20px;align-self:start;background:white;padding:22px;border-radius:12px;border-top:5px solid #d69b27}nav h2{margin:0;font-size:21px}nav ul{list-style:none;padding:0;margin:12px 0}nav li{margin:9px 0}a{color:#185ca2;text-underline-offset:3px}nav a{text-decoration:none}nav a:hover{text-decoration:underline}main{min-width:0;background:white;padding:30px 36px;border-radius:12px}section{scroll-margin-top:24px;border-top:1px solid #dde2e8;margin-top:28px;padding-top:18px}h2{line-height:1.5;font-size:24px}pre{overflow:auto;background:#172334;color:#f2f6fc;padding:20px;border-radius:9px;line-height:1.6;font-size:14px}code{font-family:Consolas,monospace}p code,td code,li code{background:#edf1f5;padding:2px 4px;border-radius:3px}table{border-collapse:collapse;width:100%;font-size:15px}th,td{padding:10px;text-align:left;border-bottom:1px solid #dce2e8;vertical-align:top}th{background:#f5eedf}.back{font-size:14px}footer{text-align:center;padding:20px;color:#637086}
@media(max-width:850px){.layout{display:block}nav{position:static;margin-bottom:20px}main{padding:20px}table{display:block;overflow:auto}h2{font-size:21px}}
@media print{body{background:white}header{background:white;color:black;padding:0}header a,nav,.back,footer{display:none}.layout{display:block;margin:0;padding:0}main{padding:0}pre{white-space:pre-wrap;background:#f4f4f4;color:black}section{break-inside:auto}h2{break-after:avoid}@page{size:A4;margin:18mm}}
'''
page = ('<!doctype html><html lang="th"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        f'<title>{html.escape(title)}</title><style>{css}</style></head><body>'
        '<header><a href="P9-FR1-FR8-วางสไลด์.html">← สไลด์ P9</a>'
        f'<h1>{html.escape(title)}</h1><p>ร้านข้าวต้มอารมณ์ดี · เอกสารประกอบ P9</p></header>'
        '<div class="layout"><nav id="toc" aria-label="สารบัญ"><h2>สารบัญ</h2><ul>'
        + ''.join(toc) + '</ul><a href="P9-THEORY.md">อ่านต้นฉบับ Markdown</a></nav>'
        '<main>' + intro + ''.join(body) + '</main></div>'
        '<footer>P9 · ทฤษฎี Java OOP และ Composition</footer></body></html>')
output = HERE / 'P9-THEORY.html'
output.write_text(page)
print(f'Created {output.name}: {len(toc)} linked sections')
