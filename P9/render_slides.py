#!/usr/bin/env python3
"""แปลงข้อความ P9 เป็นสไลด์ HTML เปิดในเบราว์เซอร์และพิมพ์ PDF ได้."""
from pathlib import Path
import html
import re

HERE = Path(__file__).resolve().parent
source = (HERE / 'P9-สไลด์-FR1-FR8.md').read_text()
parts = re.split(r'(?=^## สไลด์ \d+)', source, flags=re.M)[1:]


def inline(text):
    value = html.escape(text)
    value = re.sub(r'\[([^\]]+)\]\(([^)]+)\)',
                   lambda m: '<a href="' + html.escape(m.group(2), quote=True) + '">' + m.group(1) + '</a>', value)
    value = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', value)
    value = re.sub(r'`([^`]+)`', r'<code>\1</code>', value)
    return value


def blocks(lines):
    output = []
    i = 0
    while i < len(lines):
        row = lines[i].rstrip()
        if not row:
            i += 1
            continue
        if row.startswith('```'):
            language = row[3:].strip()
            code = []
            i += 1
            while i < len(lines) and not lines[i].startswith('```'):
                code.append(lines[i])
                i += 1
            output.append('<pre class="' + html.escape(language) + '"><code>' + html.escape('\n'.join(code)) + '</code></pre>')
            i += 1
            continue
        if row.startswith('|'):
            cells = []
            while i < len(lines) and lines[i].startswith('|'):
                cells.append([c.strip() for c in lines[i].strip().strip('|').split('|')])
                i += 1
            if len(cells) > 1 and all(re.fullmatch(r':?-+:?', c) for c in cells[1]):
                header, data = cells[0], cells[2:]
            else:
                header, data = cells[0], cells[1:]
            output.append('<table><thead><tr>' + ''.join('<th>' + inline(c) + '</th>' for c in header) + '</tr></thead><tbody>' +
                          ''.join('<tr>' + ''.join('<td>' + inline(c) + '</td>' for c in row) + '</tr>' for row in data) + '</tbody></table>')
            continue
        if row.startswith('- ') or re.match(r'^\d+\. ', row):
            ordered = not row.startswith('- ')
            tag = 'ol' if ordered else 'ul'
            items = []
            while i < len(lines) and (lines[i].startswith('- ') or re.match(r'^\d+\. ', lines[i])):
                item = re.sub(r'^(?:- |\d+\. )', '', lines[i].rstrip())
                items.append('<li>' + inline(item) + '</li>')
                i += 1
            output.append(f'<{tag}>' + ''.join(items) + f'</{tag}>')
            continue
        paragraph = [row]
        i += 1
        while i < len(lines) and lines[i].strip() and not lines[i].startswith(('```', '|', '- ')) and not re.match(r'^\d+\. ', lines[i]):
            paragraph.append(lines[i].rstrip())
            i += 1
        output.append('<p>' + inline(' '.join(paragraph)) + '</p>')
    return '\n'.join(output)


slides = []
for n, part in enumerate(parts, 1):
    lines = part.splitlines()
    title = lines[0].removeprefix('## ').strip()
    body = blocks(lines[1:])
    slides.append(f'<section class="slide" id="slide-{n}" aria-label="{html.escape(title, quote=True)}">'
                  f'<div class="kicker">P9 · JAVA OOP <span>{n:02d} / {len(parts):02d}</span></div>'
                  f'<h1>{html.escape(title)}</h1><div class="rule"></div><div class="content">{body}</div>'
                  f'<div class="footer">ร้านข้าวต้มอารมณ์ดี · ผลจากการรัน Java จริง</div></section>')

css = '''
:root{font-family:Arial,"Noto Sans Thai",sans-serif;color:#101827;background:#d8dce3}
*{box-sizing:border-box}body{margin:0}nav{position:fixed;z-index:10;top:12px;right:16px;background:#101827;color:white;padding:9px 14px;border-radius:8px;font-size:14px}nav button{background:#eab308;border:0;border-radius:5px;padding:4px 10px;margin-left:5px;cursor:pointer;font-weight:bold}
.slide{width:min(94vw,1280px);aspect-ratio:16/9;min-height:720px;margin:28px auto;padding:48px 58px 38px;background:#fbfaf7;box-shadow:0 8px 32px #11182722;position:relative;overflow:hidden;display:none}
.slide.active{display:block}.kicker{font-size:15px;letter-spacing:.18em;color:#697386;font-weight:700}.kicker span{float:right}h1{font-size:34px;margin:18px 0 9px;color:#111827}.rule{width:210px;height:5px;background:#eab308;border-radius:8px;margin-bottom:25px}.content{font-size:20px;line-height:1.55}.content p{margin:0 0 14px}.content ul,.content ol{margin:0 0 15px;padding-left:28px}.content li{margin:4px 0}.content code:not(pre code){font-size:.9em;background:#eef0f3;padding:1px 4px;border-radius:4px}.content pre{background:#101827;color:#eef2ff;padding:18px 22px;border-radius:10px;font-size:18px;line-height:1.42;white-space:pre-wrap;max-height:340px;overflow:auto;margin:14px 0}.content table{border-collapse:collapse;width:100%;font-size:17px;margin:13px 0}.content th,.content td{border-bottom:1px solid #d7dce3;text-align:left;padding:6px 10px;vertical-align:top}.content th{background:#ece8db}.content a{color:#1d4ed8;text-decoration:none}.content a:hover{text-decoration:underline}.footer{position:absolute;left:58px;right:58px;bottom:22px;border-top:1px solid #d9dde3;padding-top:7px;font-size:12px;color:#7c8594}
#slide-12 .content,#slide-13 .content{font-size:18px}#slide-12 pre,#slide-13 pre{font-size:15px;max-height:500px}#slide-11 .content,#slide-15 .content{font-size:18px}#slide-11 table{font-size:15px}#slide-15 li{margin-bottom:9px}
@media(max-width:800px){.slide{width:100vw;min-height:100vh;aspect-ratio:auto;padding:70px 22px 45px;overflow:auto}.content{font-size:17px}.content pre{font-size:14px}.footer{left:22px;right:22px;position:static;margin-top:20px}h1{font-size:26px}}
@media print{body{background:white}nav{display:none}.slide,.slide.active{display:block;width:100%;height:100vh;min-height:0;margin:0;box-shadow:none;break-after:page;page-break-after:always}.content pre{overflow:hidden} @page{size:16in 9in;margin:0}}
'''

script = '''
let current=0;const slides=[...document.querySelectorAll('.slide')];
function show(n){current=Math.max(0,Math.min(slides.length-1,n));slides.forEach((s,i)=>s.classList.toggle('active',i===current));document.getElementById('count').textContent=(current+1)+' / '+slides.length);location.hash='slide-'+(current+1)}
document.getElementById('prev').onclick=()=>show(current-1);document.getElementById('next').onclick=()=>show(current+1);
document.addEventListener('keydown',e=>{if(e.key==='ArrowRight'||e.key==='PageDown')show(current+1);if(e.key==='ArrowLeft'||e.key==='PageUp')show(current-1)});
const first=Number((location.hash.match(/slide-(\\d+)/)||[])[1]||1);show(first-1);
'''

page = '<!doctype html><html lang="th"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>P9 · FR1–FR8 Java Text Mode</title><style>' + css + '</style></head><body>'
page += '<nav><span id="count"></span><button id="prev">◀</button><button id="next">▶</button></nav>' + '\n'.join(slides)
page += '<script>' + script + '</script></body></html>'
(HERE / 'P9-FR1-FR8-วางสไลด์.html').write_text(page)
print('Rendered', len(slides), 'slides')
