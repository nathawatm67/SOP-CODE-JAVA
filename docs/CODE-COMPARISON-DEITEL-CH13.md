# 📚 การเปรียบเทียบโค้ดระบบข้าวต้มอารมณ์ดี กับ ตำรา ATM Case Study Part 2
**เอกสารอ้างอิงหลัก:** Deitel & Deitel, *Java How to Program, 8/e*, Chapter 13: "ATM Case Study Part 2: Implementing an Object-Oriented Design"  
**เป้าหมาย:** พิสูจน์ความถูกต้องตามหลักการวิเคราะห์และออกแบบเชิงวัตถุ (OOAD) และใช้เป็นแนวทางตอบคำถามอาจารย์ในการสอบป้องกันโค้ด (Code Defense)

---

## 1. ภาพรวมการเทียบเคียงสถาปัตยกรรม (Architecture Mapping)

ในบทที่ 13 ของตำรา Deitel & Deitel ได้แสดงกระบวนการแปลงจาก UML Class Diagram สู่ภาษา Java ผ่านระบบ ATM จำลอง ซึ่งมีโครงสร้างเทียบเคียงกับระบบร้านข้าวต้มอารมณ์ดีของเรา ดังนี้:

| องค์ประกอบใน ATM Case Study (Deitel Ch.13) | เทียบเคียงในระบบข้าวต้มอารมณ์ดี (Our Project) | บทบาทและหน้าที่ตามหลัก OOAD |
|---|---|---|
| **`ATM`** (คลาสหลักของระบบ) | **`Order`** / **`Main`** | คลาสที่เป็น Aggregate Root คอยควบคุมการทำงานหลัก |
| **`Screen` / `Keypad`** | **`Table` / `Customer`** | องค์ประกอบส่วนหน้า (Front Boundary / Entity) |
| **`CashDispenser` / `DepositSlot`** | **`Ingredient` / `StockMovement`** | กลไกจัดการทรัพยากร (ตัดสต็อก / เบิกจ่าย / บันทึกประวัติ) |
| **`BankDatabase`** (คลังข้อมูลบัญชี) | **`Menu` / `Recipe` / `Ingredient`** | ที่เก็บข้อมูลหลักของระบบ (Catalog & Stores) |
| **`Account`** (บัญชีลูกค้า) | **`Member`** | บัญชีระบุตัวตนบุคคล พร้อมยอดเงินคงเหลือ / ยอดแต้มสะสม |
| **`Transaction` / `Withdrawal` / `Deposit`** | **`OrderItem` / `Payment`** | รายการธุรกรรมที่เกิดขึ้นในระบบ (Business Transactions) |
| **`ATMCaseStudy.java`** (Driver) | **`Main.java`** | คลาสที่มีเมธอด `main()` สำหรับจำลองการทำงาน (Text Mode Simulator) |

---

## 2. มิติที่ 1: การแปลงกล่อง UML 3 ช่องสู่โค้ด Java (Section 13.2 Four Guidelines)

ในสไลด์หน้า 7 ของบทที่ 13 (Section 13.2) ได้กำหนด **กฎ 4 ข้อ (Four Guidelines)** ในการแปลงกล่อง Class Diagram แต่ละคลาสสู่ภาษา Java ซึ่งโค้ดระบบของเราปฏิบัติตามอย่างเคร่งครัด 100%:

### 📋 กฎข้อที่ 1: Compartment ที่ 1 ──▶ Class Declaration & Constructor (Fig 13.3)
- **ตำรา Deitel:** นำชื่อคลาสในช่องบนสุดมาประกาศเป็น `public class` และสร้าง Constructor
- **โค้ดของเรา:**
  ```java
  // src/model/Order.java
  public class Order {
      public Order(String orderId, Table table) { ... }
      public Order(String orderId, Table table, Customer customer) { ... }
  }
  ```

### 📋 กฎข้อที่ 2: Compartment ที่ 2 ──▶ Private Instance Variables (Fig 13.4)
- **ตำรา Deitel:** นำ Attribute ทุกตัวในช่องที่ 2 มาประกาศเป็นตัวแปรแบบ `private` เพื่อรักษาหลักการ Encapsulation
- **โค้ดของเรา:**
  ```java
  // src/model/Order.java (Attributes)
  private String orderId;
  private OrderStatus status;
  private double totalAmount;
  private LocalDateTime createdAt;
  ```

### 📋 กฎข้อที่ 3: เส้นความสัมพันธ์และ Navigability ──▶ Object Reference Fields (Fig 13.5)
- **ตำรา Deitel:** นำ Association และ Navigability Arrow มาประกาศเป็นตัวแปรอ้างอิง (Object References) ไปยังคลาสปลายทาง
- **โค้ดของเรา:**
  ```java
  // src/model/Order.java (References from Associations)
  private Table table;         // Order ──▶ Table (1:1)
  private Customer customer;   // Order ──▶ Customer (1:1)
  private Payment payment;     // Order ──▶ Payment (1:0..1)
  private List<OrderItem> items; // Order ◆──▶ OrderItem (Composition 1..*)
  ```

### 📋 กฎข้อที่ 4: Compartment ที่ 3 ──▶ Public Method Signatures (Fig 13.6)
- **ตำรา Deitel:** นำ Operations ในช่องล่างสุดมาประกาศเป็นเมธอดแบบ `public` พร้อมกำหนด Parameter และ Return Type
- **โค้ดของเรา:**
  ```java
  // src/model/Order.java (Operations)
  public OrderItem addItem(Menu menu, int qty, String spice, String note) { ... }
  public void removeItem(OrderItem item) { ... }
  public void attachMember(Member member) { ... }
  public double calculateTotal() { ... }
  public void confirm() { ... }
  public void cancel() { ... }
  ```

---

## 3. มิติที่ 2: Navigability (ทิศทางของลูกศร) สู่การถือ Reference

ในสไลด์หน้า 4–5 (Section 13.2 Navigability) ระบุไว้ว่า:
> *"Programmers use navigability arrows to determine which objects need references to other objects."*  
> (โปรแกรมเมอร์ใช้ลูกศร Navigability ในการตัดสินว่า Object ใดต้องถือ Reference ไปยัง Object อื่น)

### การเปรียบเทียบในโค้ด:

| กรณีในตำรา Deitel (ATM) | โค้ดในตำรา (Java) | กรณีในระบบข้าวต้มอารมณ์ดี | โค้ดในโปรเจกต์ (Java) | เหตุผลทาง OOAD |
|---|---|---|---|---|
| **ATM ──▶ Screen** | ใน `ATM.java`<br>`private Screen screen;` | **Order ──▶ Table** | ใน `Order.java`<br>`private Table table;` | ออเดอร์ต้องรู้ว่าส่งที่โต๊ะใด แต่โต๊ะไม่ต้องเก็บประวัติออเดอร์ทั้งหมดในตัวมันเอง |
| **Withdrawal ──▶ Keypad** | ใน `Withdrawal.java`<br>`private Keypad keypad;` | **OrderItem ──▶ Menu** | ใน `OrderItem.java`<br>`private Menu menu;` | รายการอาหารต้องรู้ว่าสร้างจากเมนูใด เพื่อดึงราคาและชื่อเมนู |
| **ATM ──▶ BankDatabase** | ใน `ATM.java`<br>`private BankDatabase bankDatabase;` | **Order ──▶ Payment** | ใน `Order.java`<br>`private Payment payment;` | ออเดอร์ต้องเชื่อมกับใบชำระเงินเมื่อลูกค้าเช็กบิล |
| **Withdrawal ──▶ CashDispenser** | ใน `Withdrawal.java`<br>`private CashDispenser cashDispenser;` | **OrderItem ──▶ Employee** | ใน `OrderItem.java`<br>`private Employee handledBy;` | รายการอาหารอ้างถึงกุ๊กผู้ปรุง (`handledBy`) เพื่อบันทึกเวลาเทียบ SOP |

---

## 4. มิติที่ 3: กลไก Composition (เพชรทึบ ◆) ในโค้ด Java

ในสไลด์หน้า 5 (Fig 13.2) และโค้ด `ATM.java` (สไลด์หน้า 22–23) กับ `BankDatabase.java` (สไลด์หน้า 39):
- **ในตำรา Deitel:**
  `ATM` มีความสัมพันธ์แบบ Composition กับ `Screen`, `Keypad`, `CashDispenser`, `DepositSlot`
  โค้ดใน `ATM.java` แสดงให้เห็นว่า **Constructor ของ ATM เป็นผู้สร้าง Object เหล่านี้เองโดยตรง**:
  ```java
  // ATM.java (Deitel Fig 13.13)
  public ATM() {
      userAuthenticated = false;
      currentAccountNumber = 0;
      screen = new Screen();           // <-- ATM สร้าง Screen เอง
      keypad = new Keypad();           // <-- ATM สร้าง Keypad เอง
      cashDispenser = new CashDispenser(); // <-- ATM สร้าง CashDispenser เอง
      depositSlot = new DepositSlot();     // <-- ATM สร้าง DepositSlot เอง
      bankDatabase = new BankDatabase();
  }
  ```

- **ในระบบข้าวต้มอารมณ์ดีของเรา:**
  เราปฏิบัติตามกลไกนี้อย่างเคร่งครัดใน **Composition ทั้ง 5 คู่**:
  
  **1. Order ◆── OrderItem:**
  ```java
  // src/model/Order.java
  public OrderItem addItem(Menu menu, int qty, String spice, String note) {
      itemNumber++;
      // Order เป็นผู้สร้าง OrderItem เองโดยตรง ห้ามสร้างข้างนอกแล้วยัดเข้ามา
      OrderItem item = new OrderItem(orderId + "-ITEM-" + itemNumber, menu, qty, spice, note);
      items.add(item);
      return item;
  }
  ```

  **2. Member ◆── PointTransaction:**
  ```java
  // src/model/Member.java
  private void addTransaction(String type, int amount, Payment payment) {
      String id = memberId + "-PTX-" + (transactions.size() + 1);
      // Member ควบคุมการสร้าง PointTransaction ในสมุดบัญชีแต้มของตนเอง
      transactions.add(new PointTransaction(id, type, amount, points, payment));
  }
  ```

  **3. การทำลายส่วนประกอบ (Cascade Destruction / Lifecycle Binding):**
  ตามนิยามของ Composition เมื่อ Whole ถูกทำลาย Part ต้องตายตาม:
  ```java
  // src/model/Order.java
  public void destroy() {
      // ทำลาย OrderItem ทุกตัวที่อยู่ในการดูแล
      for (int i = 0; i < items.size(); i++)
          items.get(i).destroy();
      items.clear();
      
      // ปลด Reference ที่เป็น Association (โต๊ะและลูกค้ายังคงอยู่ ไม่ได้ถูกทำลายตาม)
      table = null;
      customer = null;
      payment = null;
      destroyed = true;
  }
  ```

---

## 5. มิติที่ 4: การเติมเต็ม Logic ระหว่างเขียนโค้ดจริง (Section 13.5)

ในสไลด์หน้า 21 ของบทที่ 13 (Section 13.5) ระบุข้อความสำคัญระดับทองคำว่า:
> *"Our ATM design does not specify all the program logic and may not specify all the attributes and operations required to complete the ATM implementation. This is a normal part of the object-oriented design process. As we implement the system, we complete the program logic and add attributes and behaviors as necessary to construct the ATM system specified by the requirements document in Section 12.2."*

### 💡 ความหมายสำหรับตอบอาจารย์:
หากอาจารย์ถามว่า: *"ทำไมในโค้ดถึงมีเมธอดอย่าง `allIngredients()`, `requiredQuantity()`, หรือการเช็ก validation ต่างๆ ที่ไม่ได้เขียนอยู่ในกล่อง Class Diagram ตั้งแต่แรก?"*
- **แนวทางตอบ:** *"นี่คือธรรมชาติของกระบวนการ OOAD ตามที่ตำรา Deitel & Deitel ระบุไว้ใน Section 13.5 เลยครับอาจารย์ ในขั้น Class Diagram เราออกแบบเฉพาะ Interface และ Contract หลักของคลาส แต่ในระหว่างการ Implementation ในภาษา Java เราจำเป็นต้องเติมเต็ม Internal Program Logic, Helper Methods และ Data Validation ตาม Use Case Requirements ของระบบเพื่อให้โปรแกรมทำงานได้จริงสมบูรณ์แบบครับ"*

---

## 6. สรุปตารางเทียบเคียง Code Snippet ต่อ Code Snippet

| หัวข้อทางเทคนิค | ตัวอย่างในตำรา Deitel (ATM Case Study) | ตัวอย่างในโค้ดระบบข้าวต้มอารมณ์ดี |
|---|---|---|
| **Class Declaration** | `public class Withdrawal` (Fig 13.3) | `public class Order` (`Order.java:7`) |
| **Attributes** | `private int accountNumber;` (Fig 13.4) | `private String orderId;` (`Order.java:9`) |
| **Static Attributes** | `private final static int INITIAL_COUNT = 500;` (Fig 13.16) | `private static int bahtPerPoint = 50;` (`Member.java:18`) |
| **Object Reference** | `private Screen screen;` (Fig 13.5) | `private Table table;` (`Order.java:13`) |
| **Collection Reference** | `private Account[] accounts;` (Fig 13.19) | `private List<OrderItem> items;` (`Order.java:22`) |
| **Operation Implementation** | `public void execute() { ... }` (Fig 13.6) | `public double calculateTotal() { ... }` (`Order.java:75`) |
| **Driver Main Program** | `public class ATMCaseStudy` มี `ATM theATM = new ATM(); theATM.run();` (Fig 13.24) | `public class Main` มี Text Simulator รัน Use Case FR1–FR8 (`Main.java`) |

---

## 7. บทสรุปสำหรับการป้องกันงาน (Defense Summary)

1. โค้ดของระบบข้าวต้มอารมณ์ดี **ยึดตามหลักการของ Deitel & Deitel บทที่ 13 อย่างถูกต้อง 100%** ทั้ง 4 Guidelines ใน Section 13.2
2. การเลือกใช้ประเภทความสัมพันธ์ (Composition vs Association vs Aggregation) สอดคล้องกับทิศทางของ Navigability และการถือ Reference Field ในภาษา Java
3. เมธอดเสริมและ Data Validation ในโค้ดสอดคล้องกับหลักการ Section 13.5 ว่าด้วยการเติมเต็ม Program Logic ในขั้น Implementation เพื่อให้ตอบสนอง Functional Requirements (FR1–FR8) ได้ครบถ้วน
