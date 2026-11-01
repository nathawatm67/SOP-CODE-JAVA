# P9 · Java OOP และผลรัน Text Mode

ไฟล์นี้เป็นข้อความวางสไลด์ฉบับใหม่สำหรับโค้ดในโฟลเดอร์นี้ ใช้ **16 คลาส model + Main.java** ผลบนจอเป็นบรรทัดที่คัดจากการรันจริงด้วย `P9/generate_evidence.py` ไม่ใช้ผลรันของ P9 เก่าในชุด SOP ซึ่งอ้างถึง 17 คลาสและโฟลเดอร์ `ui/data/util` ที่ไม่มีในโค้ดปัจจุบัน

## สไลด์ 1 — ชื่อและขอบเขต

**P9: Java OOP ระบบร้านข้าวต้มอารมณ์ดี**

ฉบับผลรันของโค้ดปัจจุบัน — ตรวจชื่อ operation กับ Class Diagram P7 จาก Canva ฉบับที่ยืนยันแล้ว

- `Main.java` รับคำตอบและแสดงหน้าจอ Text Mode
- `model` มี 16 คลาส แทนสิ่งในร้านและกฎการทำงาน
- FR1–FR8 เชื่อมกับเมนู 1–8 ตามลำดับ
- ข้อมูลอยู่ในหน่วยความจำ; QR/การชำระ QR เป็นการจำลอง

คำอธิบายพูด: “สไลด์ต่อไปแสดงผลที่โปรแกรม Java พิมพ์จริง และชี้ว่ากฎนั้นอยู่ในคลาสใด”

## สไลด์ 2 — ทฤษฎี: FR และการตามรอย

**Functional Requirement (FR)** คือข้อกำหนดว่าระบบต้องให้ผลหรือพฤติกรรมใดแก่ผู้ใช้ ตามคำจำกัดความของ [IREB CPRE Glossary](https://cpre.ireb.org/en/downloads-and-resources/glossary?exam-relevant=true&first-letter=F)

| เอกสาร | คำถามที่ตอบ |
|---|---|
| P2 | ระบบต้องทำอะไร (FR1–FR8) |
| P3/P4 | ผู้ใช้เห็นขั้นตอนและ Text Mode อย่างไร |
| P7 | ข้อมูลและ operation อยู่ในคลาสใด |
| P9 | Java เรียกเมธอดจริงและแสดงผลอย่างไร |

การจับคู่ FR → เมนู → ผลรัน → เมธอด ทำให้ผู้ฟังตามรอยจากข้อกำหนดไปถึงหลักฐานการทำงานได้

## สไลด์ 3 — FR1 สั่งอาหารผ่าน QR

**หน้าที่:** ลูกค้าเลือกโต๊ะ ผูกสมาชิก เลือกอาหาร และยืนยันส่งครัว

**เมธอดหลัก:** `Main.uc01()` → `Table.scanTableQRCode()` → `Order.addItem()` → `Order.confirm()` → `Ingredient.deduct()`

```text
โต๊ะ: TBL-004 - ตะกร้า: CRT-20261101-0001
1. ผัดกะเพราปลา x2 - 168.00 บาท
2. ยำหมูยอ/แหนม x1 - 65.00 บาท
ราคารวม: 233.00 บาท (ไม่นับรายการยกเลิก)
วัตถุดิบเพียงพอ - ส่งครัวแล้ว ORD-20261101-0001
เนื้อปลา = 5.000 กก.
ไข่ไก่ = 1.000 ฟอง
```

อธิบาย: สองจานแรก 2 × (69 + 15) = 168 บาท; ยำ 65 บาท; รวม 233 บาท ตรวจสต็อกทุกชนิดก่อนตัดจริง

หลักฐาน: [`FR1-P4-ตัวอย่าง-output.txt`](evidence/FR1-P4-ตัวอย่าง-output.txt) และคำตอบที่ป้อน [`input.txt`](evidence/FR1-P4-ตัวอย่าง-input.txt)

## สไลด์ 4 — FR2 จัดการ SOP

**หน้าที่:** ผู้จัดการสร้างขั้นตอน เผยแพร่ ปิดใช้ และเปิดใช้อีกครั้ง

**เมธอดหลัก:** `Main.uc02()` → `SOP.addStep()` → `SOP.publish()` / `disable()` / `enable()` → `SOP.getTotalMinutes()`

```text
SOP ชาใหม่ - เผยแพร่
1. ต้มชา - 2.0 นาที
รวม 2.0 นาที
...
SOP ชาใหม่ - ปิดใช้
1. ต้มชา - 2.0 นาที
รวม 2.0 นาที
```

หลักฐาน: [`FR2-FR7-คู่มือและสูตร-output.txt`](evidence/FR2-FR7-คู่มือและสูตร-output.txt)

## สไลด์ 5 — FR3 ปรุงและเสิร์ฟตาม SOP

**หน้าที่:** คนครัวดูคิว เริ่มปรุง เทียบเวลา ทำเสร็จ; แคชเชียร์เสิร์ฟ

**เมธอดหลัก:** `Main.uc03()` → `OrderItem.startCooking()` → `markReady()` → `serve()`; เวลา SOP จาก `SOP.getTotalMinutes()`

```text
==== จอครัว KDS - ครัวร้อน ====
[1] ORD-20261101-0001 - ข้าวต้มปลา x1 - รับออเดอร์
SOP ข้าวต้มปลา - เผยแพร่
1. เตรียมปลาและข้าว - 2.0 นาที
2. ต้มและจัดชาม - 5.0 นาที
รวม 7.0 นาที
...
สถานะออเดอร์: ORD-20261101-0001 - โต๊ะ TBL-001 - พร้อมเสิร์ฟ
...
สถานะออเดอร์: ORD-20261101-0001 - โต๊ะ TBL-001 - เสิร์ฟแล้ว
```

หลักฐาน: [`FR1-FR3-FR4-FR6-เส้นทางครบ-output.txt`](evidence/FR1-FR3-FR4-FR6-เส้นทางครบ-output.txt)

## สไลด์ 6 — FR4 ชำระเงิน

**หน้าที่:** เลือกบิลที่เสิร์ฟครบ ใช้แต้ม เลือกเงินสดหรือ QR และออกใบเสร็จ

**เมธอดหลัก:** `Main.uc04()` → `Payment.pay()` → `Payment.confirm()` → `Member.redeemPoints()` / `earnPoints()`

```text
==== เลือกช่องทางการชำระเงิน ====
1 เงินสด / 2 QR (จำลอง) / 0 ยกเลิก
> สุทธิ 70.00 / ส่วนลด 10.00 / เงินทอน 30.00
ส่วนลด 10.00 / สุทธิ 70.00 บาท
ช่องทาง เงินสด / รับ 100.00 / ทอน 30.00
ใช้ 10 แต้ม / ได้ 1 แต้ม
```

อธิบาย: ข้าวต้มปลา 80 บาท − ส่วนลด 10 บาท = สุทธิ 70 บาท; รับ 100 บาท ทอน 30 บาท

หลักฐาน: [`FR1-FR3-FR4-FR6-เส้นทางครบ-output.txt`](evidence/FR1-FR3-FR4-FR6-เส้นทางครบ-output.txt)

## สไลด์ 7 — FR5 สต็อกและใบสั่งซื้อ

**หน้าที่:** ผู้จัดการดูวัตถุดิบต่ำ ออก PO รับของจริง และปรับยอดเมื่อผลนับต่าง

**เมธอดหลัก:** `Main.uc05()` → `PurchaseOrder.addItem()` → `markOrdered()` → `receive()` → `Ingredient.receive()` / `adjustStock()`

```text
==== ตรวจรับสินค้าจากใบสั่งซื้อ ====
[1] PO-21 - ร้านวัตถุดิบชุมชน
> เนื้อปลา สั่ง 2.0 กก.
> รับแล้ว PO-21
[1] ING-1 - เนื้อปลา - 7.300 - 2.000 - กก. - ปกติ
...
[1] ING-1 - เนื้อปลา - 6.000 - 2.000 - กก. - ปกติ
```

อธิบาย: ปลาเริ่ม 5.3 กก. รับเพิ่ม 2 กก. เป็น 7.3 กก. แล้วผู้จัดการตรวจนับและปรับเป็น 6 กก.; `StockMovement` เก็บประวัติทั้งสองเหตุการณ์

หลักฐาน: [`FR5-สต็อกและใบสั่งซื้อ-output.txt`](evidence/FR5-สต็อกและใบสั่งซื้อ-output.txt)

## สไลด์ 8 — FR6 ภาพรวมและรายงาน

**หน้าที่:** ผู้จัดการเลือกวันและดูยอดจากบิลที่ชำระจริง แยกช่องทางและอันดับอาหาร

**เมธอดหลัก:** `Main.uc06()` → `printSales()` วนอ่าน `Order` และ `Payment`

```text
==== ผู้จัดการ: แผงควบคุมภาพรวมร้าน ====
ออเดอร์ที่สร้าง 1 / กำลังปรุง 0 / ชำระในช่วงนี้ 1
ยอดสุทธิ 70.00 - เงินสด 70.00 - QR 0.00 บาท
อันดับขายดี (จำนวนจาน)
1 ข้าวต้มปลา = 1
```

หลักฐาน: [`FR1-FR3-FR4-FR6-เส้นทางครบ-output.txt`](evidence/FR1-FR3-FR4-FR6-เส้นทางครบ-output.txt)

## สไลด์ 9 — FR7 เมนูและสูตร

**หน้าที่:** ผู้จัดการเพิ่มเมนู กำหนดสูตรหลายเวอร์ชัน และเปิดขายเมื่อสูตรสมบูรณ์

**เมธอดหลัก:** `Main.uc07()` → `Menu.update()` / `openSale()` → `Recipe.addItem()` / `complete()` / `createNewVersion()`

```text
[6] ชาใหม่ - เครื่องดื่ม - 25.00 บาท - ปิดขาย
...
[6] ชาใหม่ - เครื่องดื่ม - 25.00 บาท - เปิดขาย
```

อธิบาย: สร้างเมนูแล้วเริ่มปิดขาย ทำสูตรให้สมบูรณ์ก่อนจึงเปิดขายได้

หลักฐาน: [`FR2-FR7-คู่มือและสูตร-output.txt`](evidence/FR2-FR7-คู่มือและสูตร-output.txt)

## สไลด์ 10 — FR8 สมาชิกและแต้ม

**หน้าที่:** สมัคร/ค้น/แก้สมาชิก ดูประวัติแต้ม และตั้งกฎแต้มกลางร้าน

**เมธอดหลัก:** `Main.uc08()` → `Member.changePhone()` / `rename()` / `setRule()`; การจ่ายจริงใช้ `earnPoints()` และ `redeemPoints()` ใน FR4

```text
> สมัครสมาชิกสำเร็จ
MBR-21 - สมาชิกใหม่ - 0899999999 - 0 แต้ม
> แก้ข้อมูลแล้ว
MBR-21 - แก้ชื่อ - 0899999999 - 0 แต้ม
> เปลี่ยนกฎสำหรับการชำระครั้งต่อไปแล้ว
กฎ: ทุก 100 บาท = 1 แต้ม - 1 แต้ม = 2.0 บาท - ขั้นต่ำ 5
```

หลักฐาน: [`FR8-สมาชิกและแต้ม-output.txt`](evidence/FR8-สมาชิกและแต้ม-output.txt)

## สไลด์ 11 — ทฤษฎี OOP และ Composition

ตามโครงทฤษฎีใน PDF ตัวอย่าง หน้า 2 (สไลด์ 339): **Class** เป็นแบบพิมพ์, **Object** คือสิ่งที่สร้างจาก class, **field** เก็บข้อมูล, **constructor** ตั้งค่าแรก และ **method** ทำงานเมื่อถูกเรียก ดู [Oracle Java: Classes and Objects](https://docs.oracle.com/javase/tutorial/java/javaOO/summaryclasses.html)

**Composition** คือความสัมพันธ์ has-a แบบเจ้าของกับส่วนย่อย: `Order ◆ OrderItem` และเพชรทึบอยู่ฝั่ง `Order` ส่วนย่อยหนึ่งอยู่ใน composite ได้ไม่เกินหนึ่งตัว ณ เวลาหนึ่ง ตาม [OMG UML 2.5.1 §11.2.3](https://www.omg.org/spec/UML/2.5.1/PDF) วิธีหา: อ่าน Use Case → หา “A มี B” → ถามว่า B ยังมีความหมายไหมเมื่อไม่มี A → ดู field และการสร้าง/ทำลายในโค้ด

| ตัวหลัก | ส่วนย่อย | จุดที่เห็นในโค้ด |
|---|---|---|
| `Order` | `OrderItem` | `Order.destroy()` วนเรียก `item.destroy()` |
| `Menu` | `Recipe` | `Menu.destroy()` วนเรียก `recipe.destroy()` |
| `SOP` | `SOPStep` | `SOP.destroy()` วนเรียก `step.destroy()` |
| `Ingredient` | `StockMovement` | `Ingredient.destroy()` วนเรียก `movement.destroy()` |
| `Member` | `PointTransaction` | `Member.destroy()` วนเรียก `transaction.destroy()` |

โค้ดนี้จำลองการสิ้นสุดส่วนย่อยด้วย `destroy()`; Java จัดการหน่วยความจำภายหลัง อ่านคำอธิบายทีละขั้นและตัวอย่าง Association ที่ต่างกันได้ใน [`P9-THEORY.md`](P9-THEORY.md)

## สไลด์ 12 — โค้ด Composition: Order และ Menu

โค้ดจริงจาก `src/model/Order.java` และ `src/model/Menu.java`:

```java
// Order เป็นเจ้าของ OrderItem
public void destroy() {
    for (int i = 0; i < items.size(); i++)
        items.get(i).destroy();
    items.clear();
    table = null;
    customer = null;
    payment = null;
    destroyed = true;
}

// Menu เป็นเจ้าของ Recipe
public void destroy() {
    for (int i = 0; i < recipes.size(); i++)
        recipes.get(i).destroy();
    recipes.clear();
    optionNames.clear();
    optionPrices.clear();
    extraOptionIndexes.clear();
    extraIngredients.clear();
    extraQuantities.clear();
    destroyed = true;
}
```

`table = null` เป็นเพียงการเลิกอ้างถึงโต๊ะ ไม่ใช่ Composition; โต๊ะยังอยู่ในรายการของร้าน

## สไลด์ 13 — โค้ด Composition: อีกสามคู่

โค้ดจริงจาก `SOP`, `Ingredient` และ `Member` ย่อเฉพาะส่วนที่แสดงการเป็นเจ้าของ:

```java
// SOP → SOPStep
for (int i = 0; i < steps.size(); i++)
    steps.get(i).destroy();
steps.clear();

// Ingredient → StockMovement
for (int i = 0; i < movements.size(); i++)
    movements.get(i).destroy();
movements.clear();

// Member → PointTransaction
for (int i = 0; i < transactions.size(); i++)
    transactions.get(i).destroy();
transactions.clear();
```

## สไลด์ 14 — หลักฐานและขอบเขตที่ต้องบอกตรง ๆ

- ผล Text Mode ในสไลด์เป็น **บรรทัดคัดจาก stdout ที่รันจริง**; ไฟล์เต็มและคำตอบที่ป้อนอยู่ใน `P9/evidence/`
- รันซ้ำได้ด้วย `python3 P9/generate_evidence.py` และตรวจ 8 งานด้วย `python3 tests/run_tests.py`
- วันที่ เวลา และเลขลำดับบางส่วนขึ้นกับเวลาที่รัน จึงไม่ควรอ้างว่าตรง P3/P4 ทุกบรรทัด
- QR โต๊ะและ QR Payment เป็นการจำลอง; ข้อมูลไม่เก็บถาวร
- `Customer.checkCustomerStatus()` มีใน P7 และ Java แล้ว; ชื่อ operation 73 รายการของ P7 มีใน Java ครบ ลายเซ็นตรง 72 รายการ; `PurchaseOrder.receive()` ใช้ List ตามข้อกำหนดก่อนหน้าแทน Map ใน P7 และจำนวน field/method ยังไม่เท่าทุกตัว ดู [`P7-STRICT-AUDIT.md`](P7-STRICT-AUDIT.md)

## สไลด์ 15 — แหล่งอ้างอิง

1. IREB CPRE, [Online Glossary: Functional requirement](https://cpre.ireb.org/en/downloads-and-resources/glossary?exam-relevant=true&first-letter=F) — นิยาม FR
2. Object Management Group, [Unified Modeling Language 2.5.1](https://www.omg.org/spec/UML/2.5.1/PDF), §11.2.3 — ความหมายของ Composition
3. Oracle, [Classes and Objects](https://docs.oracle.com/javase/tutorial/java/javaOO/summaryclasses.html) — field, constructor และ method
4. Oracle, [Java SE 21 List Interface](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/List.html) — ลำดับและ index ของ List
5. [Canva P7 ฉบับที่ยืนยัน](https://www.canva.com/design/DAHXaK2zQ38/3Sd-YVMVB1DkWuToNWdsRQ/edit), หน้า 270–289; โค้ดและผลรันในโฟลเดอร์นี้
6. PDF ตัวอย่าง `ระบบจัดการpizza9.pdf`, หน้า 2 (เลขสไลด์ 339): โครงหัวข้อทฤษฎี Composition; ปรับตัวอย่างให้ตรงกับโค้ดร้านข้าวต้มใน [`P9-THEORY.md`](P9-THEORY.md)
