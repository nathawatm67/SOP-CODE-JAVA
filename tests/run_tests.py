#!/usr/bin/env python3
"""คอมไพล์ในโฟลเดอร์ชั่วคราว แล้วทดสอบ model และเมนูจริงทั้ง 8 งาน"""
from pathlib import Path
import os
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent.parent
JAVA_HOME = os.environ.get('JAVA_HOME', '')
fallback = Path('/home/liella/.gemini/antigravity-ide/scratch/jdk/bin')
javac = shutil.which('javac')
java = shutil.which('java')
if not javac and JAVA_HOME:
    javac = str(Path(JAVA_HOME) / 'bin/javac')
    java = str(Path(JAVA_HOME) / 'bin/java')
if not javac and (fallback / 'javac').exists():
    javac = str(fallback / 'javac')
    java = str(fallback / 'java')
if not javac or not java:
    raise SystemExit('Install JDK 17+ or set JAVA_HOME')

model_files = sorted((ROOT / 'src/model').glob('*.java'))
assert len(model_files) == 16, 'Expected exactly 16 model classes'
assert len(list((ROOT / 'src').rglob('*.java'))) == 17, 'Expected Main + 16 model files'

with tempfile.TemporaryDirectory(prefix='p9-test-') as build:
    subprocess.run([javac, '-encoding', 'UTF-8', '-d', build,
                    *map(str, model_files), str(ROOT / 'src/Main.java'),
                    str(ROOT / 'tests/BasicOopTest.java')], check=True)
    subprocess.run([java, '-cp', build, 'BasicOopTest'], check=True)

    def run_case(name, answers, expected):
        result = subprocess.run([java, '-Dfile.encoding=UTF-8', '-cp', build, 'Main'],
                                input='\n'.join(map(str, answers)) + '\n',
                                capture_output=True, text=True, encoding='utf-8', timeout=10)
        assert result.returncode == 0, (name, result.stderr)
        assert 'Exception' not in result.stderr, (name, result.stderr)
        assert '|' not in result.stdout, (name, 'พบกรอบข้างใน Text Mode')
        for text in expected:
            assert text in result.stdout, (name, text, result.stdout[-3000:])
        assert 'ทำรายการไม่ได้' not in result.stdout, (name, result.stdout[-3000:])
        print('PASS:', name)
        return result.stdout

    # สั่งข้าวต้มปลา 1 จาน -> เริ่มปรุง -> เสร็จ -> เสิร์ฟ -> จ่ายและใช้แต้ม -> รายงาน
    run_case('UC01 + UC03 + UC04 + UC06 full workflow',
             [1, 1, 1, '0812345678', 1, 1, 1, 1, '', 1, 4,
              3, 2, 1, 1, 1, 3, 3, 1, 1, 1, 3, 5, 1, 1,
              4, 1, 1, '', 10, 1, 100, 1, 6, 1, 8, 5, 0, 0],
             ['ส่งครัวแล้ว', 'เสิร์ฟแล้ว', 'สุทธิ 70.00', 'ทอน 30.00', 'ยอดสุทธิ 70.00', '37 แต้ม'])
    run_case('UC01 cancellation request and manager approval',
             [1, 1, 1, '', 1, 5, 2, 1, 2, 0, '', 1, 4,
              3, 2, 1, 1, 1,
              1, 2, 1, 1, 2, 'รอนาน',
              8, 6, 1, 'อนุมัติคืนสต็อก', 6, 1, 0],
             ['รออนุมัติ', 'ขอยกเลิก', 'ยกเลิก', 'ยอดสุทธิ 0.00', 'เนื้อปลา - 5.300'])
    p4 = run_case('P4 UC01 sample basket: table 4, member Human, total 233',
             [1, 1, 4, '0999999999',
              1, 5, 2, 2, 2, '1', 'ไข่ดาวไม่สุก', 1,
              1, 2, 1, 1, 3, '', 1,
              4, 0],
             ['TBL-004', 'MBR-0001', 'MNU-029', 'MNU-007',
              'ราคารวม: 233.00 บาท', 'เนื้อปลา = 5.000 กก.',
              'ใบกะเพรา = 6.000 กำ', 'ไข่ไก่ = 1.000 ฟอง',
              'หมูยอ = 0.900 กก.', 'ครัวร้อน 1 - ครัวเย็น 1'])
    assert '|' not in p4, 'Text Mode output must not contain vertical borders'
    # สร้างเมนูใหม่ -> SOP ร่าง -> เผยแพร่ ปิด และเปิดใช้ -> ดู -> ลบร่างอีกฉบับ
    run_case('UC02 SOP lifecycle and UC07 menu/recipe',
             [7, 2, 'ชาใหม่', 25, 'เครื่องดื่ม', 3, 0,
              7, 3, 6, 0, 1, 6, .02, 0, 1, 7, 4, 6,
              2, 2, 6, 'SOP ชาใหม่', 'ต้มชา', 2, 0, 1,
              2, 4, 6, 2, 6, 6, 2, 6, 6,
              2, 5, 6, 0,
              7, 2, 'เมนูร่าง', 20, 'เครื่องดื่ม', 3, 0,
              2, 2, 7, 'SOP ร่าง', 'เตรียม', 1, 0, 1,
              2, 7, 7, 1, 0],
             ['สร้างแล้ว', 'SOP ชาใหม่ - เผยแพร่', 'SOP ชาใหม่ - ปิดใช้', 'สมบูรณ์'])
    run_case('UC05 PO receipt, adjustment, history',
             [5, 2, 1, 1, 2, 0, 1, 5, 3, 1, 2, 1,
              5, 4, 1, 6, 'ตรวจนับ', 1, 5, 7, 1, 0],
             ['ออกใบสั่งซื้อ', 'รับแล้ว', 'ปรับยอด', 'ตรวจนับ'])
    run_case('UC08 membership, edit and rules',
             [8, 1, '0899999999', 'สมาชิกใหม่', 1,
              8, 4, '0899999999', 'แก้ชื่อ', '0899999999', 1,
              8, 5, 1, 100, 2, 5, 8, 5, 0, 0],
             ['สมาชิกใหม่', 'แก้ข้อมูลแล้ว', 'เปลี่ยนกฎ', 'แก้ชื่อ', 'ทุก 100 บาท'])
    run_case('Empty lists and invalid numeric input',
             ['abc', 99, 3, 1, 1, 4, 0, 5, 3, 0, 0],
             ['กรอกจำนวนเต็ม', 'จบการทำงาน'])
    eof = subprocess.run([java, '-cp', build, 'Main'], input='', capture_output=True, text=True)
    assert eof.returncode == 0 and 'Exception' not in eof.stderr, eof.stderr
    print('PASS: EOF exits cleanly')
print('PASS: Main + exactly 16 model classes')
