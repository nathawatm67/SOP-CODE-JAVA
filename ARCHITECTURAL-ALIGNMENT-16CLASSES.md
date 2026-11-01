# โครงสร้างฉบับ Java OOP พื้นฐาน

ซอร์สใน `src` มี `Main.java` 1 ไฟล์ และคลาสสาธารณะใน `src/model` 16 คลาส ไม่มีคลาสซ้อน ไม่มี enum และไม่มีคลาสสนับสนุนในโฟลเดอร์ ui/data/util

ตัวเลือกเมนูเป็นข้อมูลใน Menu และ OrderItem คำขอแก้ไขเป็นข้อมูลใน OrderItem กฎแต้มเป็น static field ใน Member และใบเสร็จใช้ข้อมูลจาก Payment

Composition 5 คู่แสดงผ่านรายการลูกและเมธอด destroy():

- Order → OrderItem
- Menu → Recipe
- SOP → SOPStep
- Ingredient → StockMovement
- Member → PointTransaction

ทุกคลาสมีรหัสของตัวเอง Main สร้างรหัสคลาสหลัก ส่วนคลาสแม่สร้างรหัสลูกภายในตัวเอง

ฉบับนี้ลดความซับซ้อนเพื่อเรียนและอธิบาย OOP ชื่อฟิลด์/เมธอดและหน้าจอเปลี่ยนจากฉบับเดิม ไม่ได้ยืนยันว่าตรงแผนภาพ P8 ภายนอกทุกฟิลด์ สคริปต์เทียบเอกสารเดิมเก็บในไฟล์สำรอง และใช้ tests/run_tests.py ทดสอบฉบับนี้แทน

ซอร์สและไฟล์รันก่อนปรับอยู่ใน backups/before-basic-oop.zip
