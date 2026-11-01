# P9: ทฤษฎีการเขียน Java OOP และ Composition

เอกสารนี้เรียบเรียงตามหัวข้อของสไลด์ทฤษฎีหน้า 339 ใน PDF ตัวอย่าง `ระบบจัดการpizza9.pdf` แล้วใช้ **โค้ดร้านข้าวต้มในโฟลเดอร์นี้** เป็นตัวอย่างจริง ไม่คัดชื่อคลาสหรือผลลัพธ์ของร้านพิซซ่ามาใช้

## 1. Class, Object, Constructor, Field และ Method

**Class** คือแบบพิมพ์ที่ระบุว่าข้อมูลและพฤติกรรมของสิ่งหนึ่งมีอะไรบ้าง เช่น `Customer` ระบุรหัสลูกค้าและสมาชิกที่ผูกอยู่ **Object** คือสิ่งที่สร้างจากแบบพิมพ์นั้น เช่น `new Customer("C001")` ได้ลูกค้าหนึ่งคน

**Field** เก็บข้อมูลของ object; **constructor** ทำงานเมื่อสร้าง object เพื่อกำหนดค่าเริ่มต้น; **method** ทำงานตามคำสั่งเมื่อถูกเรียก ตัวอย่างจาก `src/model/Customer.java`:

```java
private String customerId;  // field: ข้อมูลประจำลูกค้า
private Member member;      // field: อ้างถึงบัญชีสมาชิก ถ้ายังไม่สมัครจะเป็น null

public Customer(String customerId) {  // constructor: รับรหัสตอนสร้าง
    this.customerId = customerId;
}

public boolean checkCustomerStatus() {  // method ใน P7
    return member != null;
}
```

Constructor **ไม่ใช้แทนการอ่านหรือแก้ข้อมูลภายหลังโดยอัตโนมัติ** เพราะ constructor ทำงานตอนสร้างเท่านั้น แต่ `Main` ต้องผูกสมาชิกภายหลังและอ่านสมาชิกตอนคิดแต้ม โค้ดจึงมี `linkMember()` กับ `linkedMember()` เป็นเมธอดช่วยใช้งานที่กล่อง P7 ไม่แสดง โดยไม่มี getter/setter ใน `Customer`

## 2. Has-a, Association และ Composition

**Has-a** หมายถึง object หนึ่งมีหรือรู้จักอีก object หนึ่ง ตัวอย่าง `Order` มี `Table` และมีรายการ `OrderItem` แต่ความสัมพันธ์สองแบบนี้ไม่เหมือนกัน:

| ความสัมพันธ์ | ตัวอย่าง | เมื่อเจ้าของหายไป |
|---|---|---|
| Association | `Order` อ้างถึง `Table` | โต๊ะยังอยู่และรับลูกค้ากลุ่มใหม่ได้ |
| Composition | `Order` เป็นเจ้าของ `OrderItem` | รายการอาหารเฉพาะออเดอร์นั้นหมดความหมายและถูกทำลายตาม |

ใน UML ใช้ **ข้าวหลามตัดทึบ ◆ ที่ฝั่งเจ้าของ** เพื่อบอก Composition; ส่วนเส้น Association ไม่มีข้าวหลามตัดทึบ ตาม [OMG UML 2.5.1](https://www.omg.org/spec/UML/2.5.1/PDF) ส่วนย่อยของ Composition มีเจ้าของพร้อมกันได้ไม่เกินหนึ่ง composite

> ภาพเปรียบเทียบใน PDF ตัวอย่างใช้ `Document ◆ Page` และ `Order ◆ OrderItem` หลักคิดเดียวกัน แต่รายละเอียดคลาสและโค้ดของงานนี้ต้องยึด P7 และ Java ของร้านข้าวต้ม

## 3. วิธีตัดสินว่าเป็น Composition

1. อ่าน Use Case หรือ Class Diagram แล้วหาประโยค “A มี B”
2. ถามว่า **B ถูกสร้างและจัดการโดย A หรือไม่** และ B เป็นส่วนเฉพาะของ A หรือไม่
3. ถ้า A ถูกลบ B ยังมีความหมายในระบบนี้หรือไม่
4. ดูโค้ดจริงว่า A เก็บ B ใน field, สร้าง/เพิ่ม B และจัดการ B เมื่อ A ถูกทำลายหรือไม่

ตัวอย่าง: `Order` สร้าง `OrderItem` ใน `addItem()` และเรียก `item.destroy()` ทุกตัวใน `destroy()` จึงเป็น Composition ในแบบจำลองนี้ แต่ `Order` เพียงเก็บตัวอ้างอิง `Table`; ลบ Order แล้วโต๊ะไม่ถูกทำลาย จึงเป็น Association

## 4. เขียน Composition เป็น Java อย่างไร

```java
// ตัดจากแนวคิดใน src/model/Order.java
private ArrayList<OrderItem> items;  // Order เก็บส่วนย่อยไว้

public OrderItem addItem(Menu menu, int quantity, String spice, String note) {
    OrderItem item = new OrderItem(orderId + "-ITEM-" + itemNumber,
                                   menu, quantity, spice, note);
    items.add(item);                 // เจ้าของเพิ่มส่วนย่อยของตน
    return item;
}

public void destroy() {
    for (OrderItem item : items) item.destroy();
    items.clear();                   // เลิกเก็บส่วนย่อย
    // ...เคลียร์การอ้างถึง object อื่น
}
```

`destroy()` เป็นเมธอดที่โปรเจ็กต์เขียนเพื่อจำลองการสิ้นสุดวงจรชีวิตของส่วนย่อย ไม่ใช่คำสั่งทำลายหน่วยความจำทันทีของ Java; [garbage collector ของ Java](https://docs.oracle.com/en/java/javase/21/gctuning/) จัดการหน่วยความจำภายหลังเมื่อ object เข้าถึงไม่ได้แล้ว

## 5. คู่ Composition ที่แสดงในโค้ดปัจจุบัน

| เจ้าของ | ส่วนย่อย | หลักฐานในโค้ด |
|---|---|---|
| `Order` | `OrderItem` | `Order.addItem()` สร้างรายการ; `Order.destroy()` ทำลายรายการ |
| `Menu` | `Recipe` | `Menu` เก็บสูตรหลายเวอร์ชัน; `Menu.destroy()` ทำลายสูตร |
| `SOP` | `SOPStep` | `SOP.addStep()` สร้างขั้นตอน; `SOP.destroy()` ทำลายขั้นตอน |
| `Ingredient` | `StockMovement` | วัตถุดิบเก็บประวัติการเคลื่อนไหว; `Ingredient.destroy()` ทำลายประวัติ |
| `Member` | `PointTransaction` | สมาชิกสร้างประวัติแต้ม; `Member.destroy()` ทำลายประวัติ |

**ข้อควรพูดให้ตรงกับโค้ด:** `Order` อ้างถึง `Payment` แต่ `Order.destroy()` เพียงตั้ง `payment = null` และ `Payment` ไม่มี `destroy()` จึงยังไม่ควรยกเป็นตัวอย่างที่พิสูจน์ Composition ด้วยโค้ดชุดนี้ แม้ PDF ร้านพิซซ่าจะใช้ `Order ◆ Payment` เป็นตัวอย่าง

## 6. เชื่อมทฤษฎีกับ P9 และ FR1–FR8

`Main.java` รับคำสั่งและแสดง Text Mode; คลาสใน `model` เก็บข้อมูลและกฎธุรกิจ เช่น FR1 สร้าง `OrderItem` ใน `Order`, FR4 ใช้ `Payment` คิดยอดและแต้ม, FR5 ให้ `Ingredient` เก็บ `StockMovement` การตามรอยแบบ **FR → หน้าจอ → method → field/object → ผลรัน** ทำให้ผู้ฟังเห็นว่ากล่อง Class Diagram ถูกใช้จริงตรงไหน

## แหล่งอ้างอิง

1. PDF ตัวอย่าง `ระบบจัดการpizza9.pdf`, หน้า 2 (เลขสไลด์ 339): ลำดับหัวข้อทฤษฎีและตัวอย่าง Composition
2. [Object Management Group, UML 2.5.1](https://www.omg.org/spec/UML/2.5.1/PDF), §11.2.3: ความหมายของ composite aggregation
3. [Oracle, Classes and Objects](https://docs.oracle.com/javase/tutorial/java/javaOO/summaryclasses.html): class, field, constructor, method
4. [Oracle, Java SE 21 Garbage Collection Tuning Guide](https://docs.oracle.com/en/java/javase/21/gctuning/): การจัดการหน่วยความจำของ object ใน Java
