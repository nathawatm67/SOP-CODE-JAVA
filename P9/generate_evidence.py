#!/usr/bin/env python3
"""คอมไพล์ Java และบันทึกผล Text Mode จริงสำหรับสไลด์ P9."""
from pathlib import Path
import os
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'P9' / 'evidence'
OUT.mkdir(parents=True, exist_ok=True)

javac = shutil.which('javac')
java = shutil.which('java')
if not javac:
    fallback = Path('/home/liella/.gemini/antigravity-ide/scratch/jdk/bin')
    javac, java = str(fallback / 'javac'), str(fallback / 'java')

CASES = {
    'FR1-P4-ตัวอย่าง': [
        1, 1, 4, '0999999999',
        1, 5, 2, 2, 2, '1', 'ไข่ดาวไม่สุก', 1,
        1, 2, 1, 1, 3, '', 1,
        4, 0,
    ],
    'FR1-FR3-FR4-FR6-เส้นทางครบ': [
        1, 1, 1, '0812345678', 1, 1, 1, 1, '', 1, 4,
        3, 2, 1, 1, 1, 3, 3, 1, 1, 1, 3, 5, 1, 1,
        4, 1, 1, '', 10, 1, 100, 1, 6, 1, 8, 5, 0, 0,
    ],
    'FR2-FR7-คู่มือและสูตร': [
        7, 2, 'ชาใหม่', 25, 'เครื่องดื่ม', 3, 0,
        7, 3, 6, 0, 1, 6, .02, 0, 1, 7, 4, 6,
        2, 2, 6, 'SOP ชาใหม่', 'ต้มชา', 2, 0, 1,
        2, 4, 6, 2, 6, 6, 2, 6, 6,
        2, 5, 6, 0,
        7, 2, 'เมนูร่าง', 20, 'เครื่องดื่ม', 3, 0,
        2, 2, 7, 'SOP ร่าง', 'เตรียม', 1, 0, 1,
        2, 7, 7, 1, 0,
    ],
    'FR5-สต็อกและใบสั่งซื้อ': [
        5, 2, 1, 1, 2, 0, 1, 5, 3, 1, 2, 1,
        5, 4, 1, 6, 'ตรวจนับ', 1, 5, 7, 1, 0,
    ],
    'FR8-สมาชิกและแต้ม': [
        8, 1, '0899999999', 'สมาชิกใหม่', 1,
        8, 4, '0899999999', 'แก้ชื่อ', '0899999999', 1,
        8, 5, 1, 100, 2, 5, 8, 5, 0, 0,
    ],
}

with tempfile.TemporaryDirectory(prefix='p9-evidence-') as build:
    sources = sorted((ROOT / 'src' / 'model').glob('*.java')) + [ROOT / 'src' / 'Main.java']
    subprocess.run([javac, '-encoding', 'UTF-8', '-d', build, *map(str, sources)], check=True)
    for name, answers in CASES.items():
        input_text = '\n'.join(map(str, answers)) + '\n'
        run = subprocess.run([java, '-Dfile.encoding=UTF-8', '-cp', build, 'Main'],
                             input=input_text, text=True, capture_output=True, encoding='utf-8', timeout=30)
        if run.returncode or 'Exception' in run.stderr or 'ทำรายการไม่ได้' in run.stdout:
            raise RuntimeError(f'{name}: run failed\n{run.stderr}\n{run.stdout[-2000:]}')
        (OUT / f'{name}-input.txt').write_text(input_text)
        (OUT / f'{name}-output.txt').write_text(run.stdout)
        print(name, len(run.stdout.splitlines()), 'output lines')
