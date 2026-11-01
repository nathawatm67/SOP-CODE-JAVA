# P9 ฉบับ Java ปัจจุบัน

- [สไลด์ HTML 15 หน้า](P9-FR1-FR8-วางสไลด์.html) เปิดในเบราว์เซอร์ กดปุ่มหรือปุ่มลูกศรเพื่อเปลี่ยนหน้า และพิมพ์เป็น PDF ได้
- [ข้อความสไลด์](P9-สไลด์-FR1-FR8.md) สำหรับอ่านและคัดไป Canva
- [ตารางตรวจ P7 แบบนับทุกช่อง](P7-STRICT-AUDIT.md) แสดงจุดที่โค้ดยังต่างจาก P7
- [ข้อความ Class Diagram P7 ล่าสุด](P7-CANVA-LATEST.json) และ [สคริปต์ตรวจชื่อ/ชนิด](check_p7_contract.py) สำหรับตรวจซ้ำหลังแก้ Java
- [ทฤษฎี P9 แบบ HTML พร้อมสารบัญคลิกได้](P9-THEORY.html) เรียบเรียงตาม PDF ตัวอย่างและใช้โค้ดร้านข้าวต้มจริง · [ต้นฉบับ Markdown](P9-THEORY.md)
- [หลักฐานผล Text Mode](evidence/) มีทั้งคำตอบที่ป้อนและ stdout จาก Java จริง

สร้างหลักฐานและ HTML ใหม่หลังแก้โค้ด:

```bash
python3 P9/generate_evidence.py
python3 P9/render_slides.py
python3 P9/render_theory.py
python3 tests/run_tests.py
```

สไลด์ใช้ข้อมูลของโค้ดในโฟลเดอร์นี้ ไม่ใช้ข้อความ P9 เก่าจากชุด SOP ที่ระบุ 17 คลาสและ `ui/data/util` เพราะไม่ตรงกับโครงสร้างปัจจุบัน วันเวลาใน stdout เปลี่ยนตามการรัน ตรวจกล่อง Class Diagram P7 จากลิงก์ Canva ที่ผู้ใช้ยืนยันแล้ว โดยส่งลิงก์เต็มพร้อม collaboration token
