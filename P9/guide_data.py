# -*- coding: utf-8 -*-
"""
Detailed educational data, analysis, and metadata for the 16 Model Classes
and Main.java in Khao Tom Arom Dee project.
"""

CLASSES_INFO = [
    {
        "name": "Customer",
        "file": "Customer.java",
        "domain": "โดเมนบุคคลและสถานที่ (People & Table)",
        "uml": "Customer --(0..1)--> Member",
        "purpose": "ทำหน้าที่เป็นตัวแทนของลูกค้าที่เข้ามาใช้บริการและเปิดคำสั่งซื้อในร้าน โดยลูกค้าทั่วไปสามารถเข้ามาสั่งอาหารได้ทันทีโดยไม่จำเป็นต้องเป็นสมาชิก (member สามารถเป็น null ได้) และสามารถผูกบัญชีสมาชิกในภายหลังได้เมื่อลูกค้าแจ้งเบอร์โทรศัพท์",
        "fields": [
            ("customerId", "String", "private", "รหัสประจำตัวลูกค้า เช่น 'CUS-1'"),
            ("member", "Member", "private", "ตัวอ้างอิงไปยังอ็อบเจกต์ Member ที่ผูกไว้ (has-a Association) หากไม่ได้เป็นสมาชิกจะมีค่าเป็น null")
        ],
        "relationships": [
            ("Association (has-a)", "Member", "0..1", "Customer รู้จัก Member แต่ไม่ได้เป็นเจ้าของ Member เมื่อ Customer สิ้นสุดหรือถูกลบ บัญชี Member ยังคงอยู่ในระบบตามเดิม")
        ],
        "methods_desc": [
            ("Customer(String customerId)", "Constructor", "กำหนดรหัสลูกค้า โดยตั้งต้นค่า member เป็น null ตามธรรมชาติของลูกค้าทั่วไป"),
            ("linkedMember() : Member", "Query / Accessor", "คืนค่าอ็อบเจกต์ Member ที่ผูกอยู่ เพื่อให้ Order และ Payment ดึงไปใช้คำนวณแต้มและส่วนลด"),
            ("linkMember(Member member)", "Mutator", "ผูกบัญชีสมาชิกเข้ากับลูกค้าหลังจากค้นหาพบเบอร์โทรศัพท์ในระบบ"),
            ("checkCustomerStatus() : boolean", "Business Logic (P7)", "ตรวจสอบว่าลูกค้ารายนี้เป็นสมาชิกหรือไม่ โดยคืนค่า true หาก member != null และ false หากยังไม่ได้ผูกสมาชิก")
        ],
        "design_notes": "ใน Class Diagram P7 เมธอด checkCustomerStatus() คืนค่า boolean เพื่อตอบคำถามว่ามีสถานะสมาชิกหรือไม่ แต่ในขั้นตอนชำระเงินจริง ระบบจำเป็นต้องเข้าถึงแต้มของสมาชิกด้วย ดังนั้นจึงมีการเพิ่มเมธอด linkedMember() และ linkMember() ขึ้นมาเพื่อสนับสนุนการทำงานจริงโดยที่ยังคงรักษา Encapsulation ไว้อย่างสมบูรณ์",
        "qa": "ทำไม Customer ถึงไม่สืบทอด (Inheritance) มาจาก Member? -> เพราะลูกค้าไม่ได้ 'เป็น' สมาชิกเสมอไป ลูกค้า 1 คนอาจเลือกไม่เป็นสมาชิกก็ได้ และหากเป็นสมาชิก ก็เป็นการ 'ถือครองสิทธิ' (Role/Association) ไม่ใช่การสืบทอดพันธุกรรมทางคลาส"
    },
    {
        "name": "Employee",
        "file": "Employee.java",
        "domain": "โดเมนบุคคลและสถานที่ (People & Table)",
        "uml": "Employee",
        "purpose": "ทำหน้าที่เก็บข้อมูลของพนักงานร้านอาหาร รวมถึงการควบคุมสิทธิ์การเข้าถึงการทำงานต่าง ๆ ตามบทบาทหน้าที่ (Role-Based Access Control) เช่น ผู้จัดการ, แคชเชียร์, หรือคนครัว และบันทึกสถานีครัวที่รับผิดชอบ",
        "fields": [
            ("Role", "enum { MANAGER, CASHIER, COOK }", "public", "ชุดค่าคงที่กำหนดบทบาทหน้าที่ของพนักงาน"),
            ("employeeId", "String", "private", "รหัสประจำตัวพนักงาน เช่น 'EMP-1'"),
            ("name", "String", "private", "ชื่อ-นามสกุลของพนักงาน เช่น 'ผู้จัดการ', 'คนครัว'"),
            ("role", "Role", "private", "บทบาทหน้าที่ของพนักงานตัวนี้"),
            ("station", "String", "private", "สถานีครัวที่พนักงานได้รับมอบหมาย เช่น 'ครัวร้อน', 'ครัวยำ'")
        ],
        "relationships": [
            ("Association Target", "StockMovement, Payment, OrderItem, PurchaseOrder", "1", "ถูกอ้างอิงโดยคลาสอื่นในฐานะผู้ทำรายการ (doneBy / handledBy / receivedBy)")
        ],
        "methods_desc": [
            ("Employee(String id, String name, Role role)", "Constructor", "กำหนดรหัส ชื่อ และบทบาท enum ตั้งต้น โดยกำหนด station เริ่มต้นเป็น 'ยังไม่กำหนด'"),
            ("Employee(String id, String name, String role)", "Overloaded Constructor", "Constructor เสริมที่รับสตริงภาษาไทย ('ผู้จัดการ', 'แคชเชียร์', 'คนครัว') แล้วแปลงเป็น enum อัตโนมัติ"),
            ("parseRole(String text) : Role", "Helper (private static)", "แปลงข้อความภาษาไทยจากหน้าจอเป็นค่า Enum ป้องกันการใส่ข้อมูลผิดพลาด"),
            ("authenticateRole(Role requiredRole) : boolean", "Security / Auth", "ตรวจสอบว่าพนักงานมีบทบาทตรงกับงานที่จำเป็นต้องใช้สิทธิ์หรือไม่"),
            ("assignStationDuty(String station)", "Mutator", "มอบหมายหน้าที่ประจำสถานีครัวให้แก่คนครัว"),
            ("name(), roleName(), station()", "Accessors", "เมธอดอ่านค่าสำหรับนำไปแสดงผลบนหน้าจอ Text Mode")
        ],
        "design_notes": "การใช้ enum ซ้อนอยู่ภายในคลาส Employee (Employee.Role) ช่วยจำกัดขอบเขตบทบาทไม่ให้สะกดผิดพลาด และยังคงทำให้โครงสร้างไฟล์ยังคงเป็น 16 คลาสหลักอย่างเคร่งครัดตามข้อกำหนด ไม่มีการแตกไฟล์ enum ย่อยภายนอก",
        "qa": "ทำไมต้องมี authenticateRole()? -> เพื่อป้องกันไม่ให้คนครัวหรือแคชเชียร์มากดอนุมัติคำขอยกเลิกอาหาร หรือแก้กฎแต้มกลางของร้านซึ่งเป็นอำนาจเฉพาะของผู้จัดการเท่านั้น"
    },
    {
        "name": "Table",
        "file": "Table.java",
        "domain": "โดเมนบุคคลและสถานที่ (People & Table)",
        "uml": "Table <--(1)-- Order",
        "purpose": "ทำหน้าที่เป็นตัวแทนของโต๊ะรับประทานอาหารภายในร้าน จัดการรหัสโต๊ะ รหัส QR สำหรับการสั่งอาหาร จำนวนที่นั่ง และสถานะของโต๊ะ (ว่าง หรือ ใช้งาน)",
        "fields": [
            ("tableId", "String", "private", "รหัสโต๊ะ เช่น 'T01', 'T02'"),
            ("qrCode", "String", "private", "รหัส QR จำลองประจำโต๊ะ เช่น 'QR-T01'"),
            ("seatCapacity", "int", "private", "จำนวนที่นั่งรองรับ เช่น 4 ที่นั่ง"),
            ("status", "String", "private", "สถานะของโต๊ะ ('ว่าง' หรือ 'ใช้งาน')"),
            ("qrScanned", "boolean", "private", "แฟล็กจำลองว่าโต๊ะนี้ถูกลูกค้าสแกน QR แล้วหรือไม่")
        ],
        "relationships": [
            ("Association Target", "Order", "1", "โต๊ะถูกอ้างถึงโดย Order เมื่อมีการเปิดบิล แต่โต๊ะไม่ได้ถูกทำลายเมื่อ Order จบลง")
        ],
        "methods_desc": [
            ("Table(String tableId, String qrCode, int seatCapacity)", "Constructor", "กำหนดค่าเริ่มต้นของโต๊ะ โดยตั้งค่าสถานะเริ่มต้นเป็น 'ว่าง'"),
            ("scanTableQRCode()", "Simulation", "จำลองการที่ลูกค้านำมือถือมาสแกน QR Code เพื่อเริ่มกระบวนการสั่งอาหาร"),
            ("identifyTableNumber() : String", "Business Logic (P7)", "คืนรหัสโต๊ะ แต่มีเงื่อนไขตรวจสอบว่าต้องผ่านการสแกน QR มาก่อน (qrScanned == true) มิเช่นนั้นจะโยน IllegalStateException"),
            ("changeTableStatus(String status)", "State Mutator", "เปลี่ยนสถานะโต๊ะ เช่น เมื่อยืนยันออเดอร์จะเปลี่ยนเป็น 'ใช้งาน' และเมื่อชำระเงินเรียบร้อยจะเปลี่ยนเป็น 'ว่าง'"),
            ("tableId(), qrCode(), statusText()", "Accessors", "อ่านค่าสำหรับแสดงผลบนหน้าจอ")
        ],
        "design_notes": "ในระบบ Terminal ไม่มีกล้องจริง การจำลองสแกน QR ผ่าน scanTableQRCode() และตรวจสอบใน identifyTableNumber() ช่วยสะท้อน Use Case Diagram และ Sequence Diagram P6 ได้อย่างตรงไปตรงมา",
        "qa": "ทำไม Table ไม่เก็บ Order ไว้ในตัวเอง? -> เพื่อลด Coupling (Loose Coupling) โต๊ะเป็นเพียงสถานที่กายภาพ ไม่ควรผูกมัดกับโครงสร้างบิลเงินหรือรายการอาหาร ให้ Order เป็นฝ่ายชี้มาที่ Table จะยืดหยุ่นกว่า"
    },
    {
        "name": "Supplier",
        "file": "Supplier.java",
        "domain": "โดเมนคลังวัตถุดิบและการจัดซื้อ (Inventory & Purchasing)",
        "uml": "Supplier --(*)--> Ingredient",
        "purpose": "ทำหน้าที่เก็บข้อมูลของผู้จัดจำหน่ายวัตถุดิบ (ซัพพลายเออร์) และรายการวัตถุดิบที่ซัพพลายเออร์รายนั้นสามารถจัดส่งให้ร้านได้ เพื่อใช้ตรวจสอบตอนออกใบสั่งซื้อ (Purchase Order)",
        "fields": [
            ("supplierId", "String", "private", "รหัสประจำตัวผู้จัดจำหน่าย เช่น 'SUP-1'"),
            ("name", "String", "private", "ชื่อบริษัทหรือร้านค้าผู้จัดจำหน่าย เช่น 'เจริญฟาร์มปลาและไข่'"),
            ("suppliedIngredients", "List<Ingredient>", "private", "รายการอ็อบเจกต์วัตถุดิบที่ผู้จัดจำหน่ายรายนี้สามารถส่งได้ (Association)")
        ],
        "relationships": [
            ("Association (has-a)", "Ingredient", "*", "Supplier อ้างอิงวัตถุดิบที่มีอยู่ในคลังกลาง ไม่ได้เป็นเจ้าของสต็อกวัตถุดิบนั้น"),
            ("Association Target", "PurchaseOrder", "1", "PurchaseOrder ชี้มาที่ Supplier เพื่อระบุว่าสั่งซื้อจากใคร")
        ],
        "methods_desc": [
            ("Supplier(String supplierId, String name)", "Constructor", "กำหนดรหัส ชื่อผู้จัดจำหน่าย และเตรียม List วัตถุดิบ"),
            ("addIngredient(Ingredient ingredient)", "Mutator", "เพิ่มวัตถุดิบที่จัดส่งได้เข้าสู่รายการ โดยตรวจสอบป้องกันการเพิ่มซ้ำด้วย contains()"),
            ("supplies(Ingredient ingredient) : boolean", "Validation (P7)", "ตรวจสอบว่าผู้จัดจำหน่ายรายนี้สามารถจัดส่งวัตถุดิบที่ต้องการได้หรือไม่"),
            ("name() : String", "Accessor", "อ่านชื่อผู้จัดจำหน่าย")
        ],
        "design_notes": "Supplier ใช้ List<Ingredient> ร่วมกับ Ingredient กลางของร้าน ทำให้เมื่อออกใบสั่งซื้อ ระบบสามารถตรวจ supplies(ingredient) ได้ทันทีโดยไม่ต้องเปรียบเทียบแค่ข้อความชื่อ",
        "qa": "ทำไม Supplier ไม่ลบ Ingredient เมื่อ Supplier เลิกกิจการ? -> เพราะเป็น Association ไม่ใช่ Composition วัตถุดิบเป็นทรัพย์สินของร้านอาหาร แม้เปลี่ยนผู้จัดจำหน่าย วัตถุดิบในคลังก็ยังต้องอยู่"
    },
    {
        "name": "SOPStep",
        "file": "SOPStep.java",
        "domain": "โดเมนเมนู คู่มือ และสูตรอาหาร (Menu, Recipe & SOP)",
        "uml": "SOPStep <--(Composition)-- SOP",
        "purpose": "ทำหน้าที่เป็นตัวแทนของขั้นตอนย่อย 1 ขั้นตอนในคู่มือการปฏิบัติงานมาตรฐาน (SOP) เช่น 'เตรียมเนื้อปลาและล้างให้สะอาด' กำหนดเวลามาตรฐาน (นาที) และรองรับการทำลายตามวงจรชีวิตของ SOP",
        "fields": [
            ("sopStepId", "String", "private", "รหัสขั้นตอน เช่น 'SOP-1-STP-1'"),
            ("no", "int", "private", "ลำดับของขั้นตอน เริ่มต้นที่ 1"),
            ("description", "String", "private", "คำอธิบายรายละเอียดการปฏิบัติงาน"),
            ("standardMinutes", "double", "private", "เวลามาตรฐานในการทำงานสำหรับขั้นตอนนี้ (นาที)"),
            ("destroyed", "boolean", "private", "แฟล็กระบุว่าขั้นตอนนี้ถูกทำลายตาม SOP แล้วหรือไม่")
        ],
        "relationships": [
            ("Composition (Part-of)", "SOP", "1", "SOPStep เป็นส่วนย่อยของ SOP โดยสมบูรณ์ ถูกสร้างขึ้นโดย SOP และถูกทำลายเมื่อ SOP ถูกทำลาย")
        ],
        "methods_desc": [
            ("SOPStep(String id, int no, String desc, double minutes)", "Constructor", "กำหนดรหัส ลำดับ และเรียก update() เพื่อตรวจสอบความถูกต้อง"),
            ("update(String description, double minutes)", "Mutator / Validation", "แก้ไขคำอธิบายและเวลามาตรฐาน โดยตรวจเงื่อนไข minutes > 0 และเป็นตัวเลขจำกัด"),
            ("destroy()", "Lifecycle (Composition)", "ทำเครื่องหมาย destroyed = true ปลดการใช้งานเมื่อคู่มือแม่ถูกลบ"),
            ("number(), description(), standardMinutes(), isDestroyed()", "Accessors", "อ่านข้อมูลของขั้นตอนย่อย")
        ],
        "design_notes": "การมีเมธอด destroy() ใน SOPStep เป็นหลักฐานเชิงประจักษ์ของการออกแบบตามหลัก Composition ในภาษา Java เมื่ออ็อบเจกต์ SOP ถูกเรียก destroy() จะทำการวนลูปเรียก destroy() ของทุกขั้นตอนย่อยด้วย",
        "qa": "ทำไม SOPStep จึงไม่ควรอยู่เดี่ยว ๆ โดยไม่มี SOP? -> เพราะขั้นตอนหนึ่งขั้นตอนจะไร้ความหมายหากไม่รู้ว่ากำลังทำเมนูอะไรและเป็นส่วนหนึ่งของคู่มือฉบับใด"
    },
    {
        "name": "StockMovement",
        "file": "StockMovement.java",
        "domain": "โดเมนคลังวัตถุดิบและการจัดซื้อ (Inventory & Purchasing)",
        "uml": "StockMovement <--(Composition)-- Ingredient",
        "purpose": "ทำหน้าที่เป็นบันทึกประวัติการเปลี่ยนแปลงสต็อก (Audit Trail) แต่ละครั้ง ว่ามีการรับเข้า, ตัดขาย, คืนสต็อก หรือปรับยอด จำนวนเท่าใด ยอดคงเหลือหลังรายการเท่าใด อ้างอิงเอกสารใด เหตุผลอะไร และใครเป็นผู้ทำรายการ",
        "fields": [
            ("MovementType", "enum { RECEIVE, SALE, RESTORE, ADJUST }", "public", "ชนิดของการเคลื่อนไหวสต็อก"),
            ("stockMovementId", "String", "private", "รหัสรายการเคลื่อนไหว เช่น 'ING-1-MOV-1'"),
            ("time", "LocalDateTime", "private", "วันและเวลาที่เกิดรายการขึ้นจริง"),
            ("type", "MovementType", "private", "ชนิดรายการ"),
            ("qty", "double", "private", "จำนวนที่เปลี่ยนแปลง (บวกคือเพิ่ม ลบคือลด)"),
            ("balance", "double", "private", "ยอดคงเหลือหลังการทำรายการ"),
            ("reference", "String", "private", "เอกสารอ้างอิง เช่น 'ORD-1', 'PO-1', 'ตรวจนับ'"),
            ("reason", "String", "private", "เหตุผล เช่น 'ตัดตามสูตร', 'รับวัตถุดิบ', 'สินค้าเน่าเสีย'"),
            ("doneBy", "Employee", "private", "พนักงานผู้รับผิดชอบทำรายการ (Association)"),
            ("destroyed", "boolean", "private", "แฟล็กสถานะการทำลายตาม Ingredient")
        ],
        "relationships": [
            ("Composition (Part-of)", "Ingredient", "1", "StockMovement เป็นประวัติเฉพาะตัวของ Ingredient หนึ่ง ๆ ถูกสร้างขึ้นภายใน Ingredient และถูกทำลายเมื่อ Ingredient ถูกทำลาย"),
            ("Association", "Employee", "0..1", "อ้างอิงพนักงานผู้ทำรายการ")
        ],
        "methods_desc": [
            ("StockMovement(...)", "Constructors", "สร้างประวัติการเคลื่อนไหวและเรียก recordStockMovement"),
            ("recordStockMovement(...)", "Immutable State Recording", "บันทึกข้อมูลและตรวจสอบความถูกต้อง โดยมีเงื่อนไขห้ามบันทึกซ้ำ (time != null จะโยน Exception) เพื่อรักษาความถูกต้องของประวัติบัญชี"),
            ("destroy()", "Lifecycle", "ทำลายประวัติและตัดการเชื่อมโยงไปยัง Employee"),
            ("time(), typeText(), quantity(), balance(), reference(), reason(), employee()", "Accessors", "เมธอดอ่านค่าสำหรับหน้าจอแสดงประวัติสต็อก")
        ],
        "design_notes": "ประวัติสต็อกเป็นข้อมูลแบบ Write-Once-Read-Many (WORM) เมื่อถูกสร้างแล้วจะไม่มีเมธอดแก้ไขย้อนหลัง เพื่อป้องกันการทุจริตและการบิดเบือนข้อมูลสต็อกสินค้า",
        "qa": "ทำไม StockMovement ถึงเป็น Composition กับ Ingredient? -> เพราะประวัติการเคลื่อนไหวของเนื้อปลาจะไม่มีความหมายใด ๆ ในระบบ หากตัววัตถุดิบเนื้อปลาถูกลบทิ้งไปจากสารบบของร้าน"
    },
    {
        "name": "PointTransaction",
        "file": "PointTransaction.java",
        "domain": "โดเมนออเดอร์และการเงิน (Order Lifecycle & Financial)",
        "uml": "PointTransaction <--(Composition)-- Member",
        "purpose": "ทำหน้าที่เป็นบันทึกประวัติการสะสมและการแลกใช้แต้มสะสมของสมาชิกแต่ละราย เพื่อความโปร่งใสและสามารถตรวจสอบย้อนหลังได้ โดยเชื่อมโยงกับใบชำระเงิน (Payment) ที่เกี่ยวข้อง",
        "fields": [
            ("PointType", "enum { EARN, REDEEM }", "public", "ประเภทรายการ: EARN (สะสมแต้ม) หรือ REDEEM (แลกแต้ม)"),
            ("pointTransactionId", "String", "private", "รหัสรายการประวัติแต้ม เช่น 'MEM-1-PTX-1'"),
            ("date", "LocalDateTime", "private", "วันเวลาที่เกิดรายการ"),
            ("type", "PointType", "private", "ชนิดรายการแต้ม"),
            ("points", "int", "private", "จำนวนแต้มที่สะสมเพิ่ม หรือจำนวนแต้มที่ใช้แลกไป"),
            ("balance", "int", "private", "ยอดแต้มคงเหลือสุทธิหลังทำรายการ"),
            ("payment", "Payment", "private", "อ้างอิงใบชำระเงินที่ทำให้เกิดการสะสมหรือแลกแต้ม (Association)"),
            ("destroyed", "boolean", "private", "แฟล็กสถานะการทำลายตาม Member")
        ],
        "relationships": [
            ("Composition (Part-of)", "Member", "1", "เป็นประวัติส่วนตัวของสมาชิกรายนั้น เมื่อสมาชิกถูกลบ ประวัติแต้มจะถูกทำลายตาม"),
            ("Association", "Payment", "0..1", "อ้างอิงใบเสร็จที่เกี่ยวข้อง (nullable)")
        ],
        "methods_desc": [
            ("PointTransaction(...)", "Constructors", "สร้างประวัติแต้มพร้อมบันทึกเวลาปัจจุบัน"),
            ("recordPointTransaction(...)", "State Recording", "บันทึกข้อมูลแต้มพร้อมเงื่อนไขป้องกันการบันทึกซ้ำ"),
            ("destroy()", "Lifecycle", "ทำลายประวัติและเคลียร์การอ้างอิง payment = null"),
            ("time(), typeText(), points(), balance(), payment()", "Accessors", "อ่านข้อมูลประวัติแต้มเพื่อแสดงผล")
        ],
        "design_notes": "PointTransaction ช่วยให้สมาชิกสามารถดู Statement แต้มย้อนหลังได้ว่า ได้รับแต้มจากบิลใบเสร็จใบไหน และเคยแลกส่วนลดไปเมื่อใด",
        "qa": "ทำไม PointTransaction ไม่ถูกเก็บรวมเป็นก้อนเดียวในระดับร้าน? -> เพราะตามหลัก OOAD แต้มเป็นสมบัติส่วนตัวของ Member แต่ละคน การเก็บไว้ใน Member ทำให้เกิด Encapsulation และ Low Coupling"
    },
    {
        "name": "Ingredient",
        "file": "Ingredient.java",
        "domain": "โดเมนคลังวัตถุดิบและการจัดซื้อ (Inventory & Purchasing)",
        "uml": "Ingredient ◆--(*)--> StockMovement",
        "purpose": "ทำหน้าที่เป็นตัวแทนของวัตถุดิบแต่ละชนิดในคลังสินค้า ควบคุมยอดคงเหลือ (stockQty), ยอดจุดสั่งซื้อขั้นต่ำ (minQty), การตัดสต็อกเมื่อขาย, การคืนสต็อกเมื่อยกเลิก, การรับเข้าจากใบสั่งซื้อ, และการปรับยอด พร้อมทั้งเป็นเจ้าของประวัติ StockMovement",
        "fields": [
            ("ingredientId", "String", "private", "รหัสวัตถุดิบ เช่น 'ING-1'"),
            ("name", "String", "private", "ชื่อวัตถุดิบ เช่น 'เนื้อปลา', 'ไข่ไก่', 'หมูยอ'"),
            ("unit", "String", "private", "หน่วยนับ เช่น 'กก.', 'ฟอง', 'แท่ง'"),
            ("stockQty", "double", "private", "ยอดสต็อกคงเหลือปัจจุบัน"),
            ("minQty", "double", "private", "ยอดขั้นต่ำเตือนสั่งซื้อ (Safety Stock / Reorder Point)"),
            ("movements", "List<StockMovement>", "private", "รายการประวัติการเคลื่อนไหวสต็อก (Composition)"),
            ("destroyed", "boolean", "private", "แฟล็กสถานะการทำลาย")
        ],
        "relationships": [
            ("Composition (Composite Owner)", "StockMovement", "*", "เป็นเจ้าของประวัติการเคลื่อนไหวทั้งหมดของตนเอง"),
            ("Association Target", "Recipe, OrderItem, PurchaseOrder, Supplier", "*", "ถูกอ้างถึงในสูตรอาหาร, บิลสั่งอาหาร, ใบสั่งซื้อ และรายการสินค้าของผู้จัดจำหน่าย")
        ],
        "methods_desc": [
            ("Ingredient(String id, String name, String unit, double minQty)", "Constructor", "สร้างวัตถุดิบ ยอดเริ่มต้นเป็น 0 และเตรียม List สำหรับ movements"),
            ("hasEnough(double qty) : boolean", "Check / Invariant", "ตรวจสอบว่าสต็อกมีเพียงพอต่อจำนวนที่ต้องการตัดหรือไม่ (มี delta 0.000001 ป้องกันปัญหา floating point)"),
            ("changeStock(double change, String type, ...)", "Core Helper (private)", "ปรับปรุงยอด stockQty และสร้างอ็อบเจกต์ StockMovement เพิ่มลงใน List ทันที"),
            ("receive(double qty, String ref, Employee emp)", "Business Logic", "รับวัตถุดิบเข้าคลัง เพิ่มยอดและบันทึกประวัติ 'รับเข้า'"),
            ("deduct(double qty, String ref)", "Business Logic", "ตัดสต็อกวัตถุดิบ ตรวจสอบ hasEnough() ก่อนตัดจริง หากไม่พอจะโยน IllegalArgumentException"),
            ("restore(double qty, String ref)", "Business Logic", "คืนสต็อกวัตถุดิบเมื่อมีการยกเลิกอาหารหรือลดจำนวนจาน"),
            ("adjustStock(double newQty, String reason, Employee by)", "Business Logic", "ปรับยอดสต็อกให้ตรงกับการตรวจนับจริง บันทึกเหตุผลและผู้รับผิดชอบ"),
            ("destroy()", "Lifecycle (Composition)", "วนลูปสั่ง movement.destroy() ทุกตัว ล้าง movements.clear() และตั้ง destroyed = true")
        ],
        "design_notes": "การที่ Ingredient จัดการตัดสต็อกและบันทึก Movement ภายในตัวเอง ทำให้ Main หรือ Order ไม่จำเป็นต้องรู้สูตรคณิตศาสตร์หรือวิธีสร้าง Movement เลย เป็นไปตามหลัก Information Expert ใน GRASP Pattern",
        "qa": "ทำไมยอดเริ่มต้นของ Ingredient ถึงเป็น 0? -> เพราะในทางบัญชีสต็อก วัตถุดิบต้องมียอดเริ่มต้นจากการ 'รับเข้า' อย่างเป็นทางการ (ผ่านใบสั่งซื้อหรือยอดยกมา) เพื่อให้มีหลักฐาน Movement บันทึกไว้ตั้งแต่กิโลกรัมแรก"
    },
    {
        "name": "Recipe",
        "file": "Recipe.java",
        "domain": "โดเมนเมนู คู่มือ และสูตรอาหาร (Menu, Recipe & SOP)",
        "uml": "Recipe ◆<--(Composition)-- Menu, Recipe --(*)--> Ingredient",
        "purpose": "ทำหน้าที่เก็บสูตรอาหารหนึ่งเวอร์ชัน โดยระบุว่าเมนูนี้ใช้วัตถุดิบอะไรบ้างและปริมาณเท่าใดต่อ 1 จาน มีสถานะเป็นฉบับร่าง (DRAFT) หรือฉบับสมบูรณ์ (COMPLETE) และรองรับการแตกเวอร์ชันใหม่ (Versioning)",
        "fields": [
            ("RecipeStatus", "enum { DRAFT, COMPLETE }", "public", "สถานะของสูตร: DRAFT (กำลังแก้ไข) หรือ COMPLETE (เสร็จสมบูรณ์พร้อมใช้)"),
            ("recipeId", "String", "private", "รหัสสูตร เช่น 'RCP-1-v1'"),
            ("version", "int", "private", "หมายเลขเวอร์ชันของสูตร เช่น 1, 2"),
            ("status", "RecipeStatus", "private", "สถานะสูตรปัจจุบัน"),
            ("ingredients", "List<Ingredient>", "private", "รายการวัตถุดิบที่ใช้ (Association ชี้ไปที่ Ingredient ในคลัง)"),
            ("quantities", "List<Double>", "private", "รายการปริมาณที่ใช้ต่อ 1 จาน (จับคู่ตาม index เดียวกับ ingredients)"),
            ("destroyed", "boolean", "private", "แฟล็กสถานะการทำลาย")
        ],
        "relationships": [
            ("Composition (Part-of)", "Menu", "1", "Recipe เป็นส่วนประกอบย่อยของ Menu ถูกสร้างและทำลายโดย Menu"),
            ("Association", "Ingredient", "*", "อ้างอิง Ingredient ในคลังกลางของร้าน")
        ],
        "methods_desc": [
            ("Recipe(String recipeId, int version)", "Constructor", "สร้างสูตรฉบับร่าง (DRAFT) เวอร์ชันที่กำหนด และเตรียม List ทั้งสองชุด"),
            ("addItem(Ingredient ing, double qty)", "Mutator / Validation", "เพิ่มวัตถุดิบและปริมาณ ทำได้เฉพาะสถานะ DRAFT หากมีวัตถุดิบเดิมอยู่แล้วจะบวกปริมาณเพิ่ม"),
            ("changeQty(Ingredient ing, double qty)", "Mutator", "เปลี่ยนปริมาณวัตถุดิบ ทำได้เฉพาะสูตรฉบับร่าง DRAFT เท่านั้น"),
            ("complete()", "Lifecycle State Transition", "ยืนยันความสมบูรณ์ของสูตร เปลี่ยนสถานะเป็น COMPLETE โดยตรวจว่าต้องมีวัตถุดิบอย่างน้อย 1 ชนิด"),
            ("createNewVersion() : Recipe", "Versioning", "สร้างสูตรฉบับร่างเวอร์ชันถัดไป (v+1) โดยคัดลอกส่วนผสมเดิมทั้งหมดมาให้ เพื่อให้เชฟปรับปรุงสูตรใหม่โดยไม่กระทบสูตรเก่า"),
            ("destroy()", "Lifecycle", "เคลียร์รายการวัตถุดิบและปริมาณทิ้งทั้งหมด")
        ],
        "design_notes": "สูตรที่ COMPLETE แล้วจะถูกล็อกไม่ให้แก้ไขตรง ๆ (Immutability Pattern) หากต้องการปรับสูตร ต้องเรียก createNewVersion() เพื่อสร้างเวอร์ชันใหม่เท่านั้น เพื่อป้องกันการกระทบยอดอาหารที่อยู่ในครัว",
        "qa": "ทำไมใช้ List สองชุด (ingredients และ quantities) แทนที่จะใช้ Map? -> เพื่อให้การเรียนรู้ OOP ในระดับพื้นฐานเข้าใจง่าย ลำดับของ List ทั้งสองตรงกัน และสามารถอธิบายผ่าน index เดียวกันได้ชัดเจน"
    },
    {
        "name": "SOP",
        "file": "SOP.java",
        "domain": "โดเมนเมนู คู่มือ และสูตรอาหาร (Menu, Recipe & SOP)",
        "uml": "SOP ◆--(*)--> SOPStep, SOP --(1)--> Menu",
        "purpose": "ทำหน้าที่เป็นคู่มือการปฏิบัติงานมาตรฐาน (Standard Operating Procedure) ของเมนูอาหารฉบับหนึ่ง ควบคุมขั้นตอนการปรุงตามลำดับ คำนวณเวลารวมมาตรฐาน และบริหารวงจรชีวิตของคู่มือ (DRAFT, PUBLISHED, DISABLED)",
        "fields": [
            ("SopStatus", "enum { DRAFT, PUBLISHED, DISABLED }", "public", "สถานะคู่มือ: DRAFT (ร่าง), PUBLISHED (เผยแพร่ใช้งาน), DISABLED (ปิดใช้งานชั่วคราว)"),
            ("sopId", "String", "private", "รหัสคู่มือ เช่น 'SOP-1'"),
            ("name", "String", "private", "ชื่อคู่มือ เช่น 'SOP ผัดกะเพราปลา'"),
            ("status", "SopStatus", "private", "สถานะของคู่มือ"),
            ("menu", "Menu", "private", "เมนูอาหารที่คู่มือฉบับนี้ใช้ควบคุม (Association)"),
            ("steps", "List<SOPStep>", "private", "รายการขั้นตอนการปฏิบัติงาน (Composition)"),
            ("destroyed", "boolean", "private", "แฟล็กสถานะการทำลาย")
        ],
        "relationships": [
            ("Composition (Composite Owner)", "SOPStep", "*", "เป็นเจ้าของขั้นตอนย่อย SOPStep ทั้งหมด เมื่อลบ SOP ขั้นตอนย่อยจะถูกทำลายตาม"),
            ("Association", "Menu", "1", "คู่มือผูกกับเมนูอาหารของร้าน")
        ],
        "methods_desc": [
            ("SOP(String sopId, String name, Menu menu)", "Constructor", "สร้างคู่มือฉบับร่าง (DRAFT) ผูกกับ Menu"),
            ("addStep(String description, double minutes)", "Composition Creator", "สร้างอ็อบเจกต์ SOPStep ใหม่ กำหนดเลขลำดับอัตโนมัติ และเก็บเข้า List steps"),
            ("getTotalMinutes() : double", "Aggregation / Calculation", "วนลูปคำนวณผลรวมเวลามาตรฐานของทุกขั้นตอน เพื่อใช้เป็นเป้าหมายเวลาในครัว"),
            ("publish()", "State Transition", "เผยแพร่คู่มือเพื่อให้คนครัวนำไปใช้ได้ ต้องเป็นฉบับร่างและมีขั้นตอนอย่างน้อย 1 ขั้น"),
            ("disable() / enable()", "State Mutators", "ปิดใช้ หรือเปิดใช้คู่มือที่เคยเผยแพร่แล้ว"),
            ("isDeletable() : boolean", "Business Rule", "ลบคู่มือได้เฉพาะเมื่อยังคงเป็นฉบับร่าง (DRAFT) เท่านั้น"),
            ("destroy()", "Lifecycle (Composition)", "สั่ง destroy() ขั้นตอนย่อยทุกตัว ล้าง List และตัดการเชื่อมโยง menu = null")
        ],
        "design_notes": "SOP ทำให้ครัวมีมาตรฐาน เวลาปรุงจริงใน OrderItem จะถูกนำมาเปรียบเทียบกับ getTotalMinutes() ของ SOP เพื่อประเมินประสิทธิภาพของคนครัว",
        "qa": "ทำไมลบ SOP แล้วไม่ลบ Menu ตามไปด้วย? -> เพราะ SOP เป็นเพียงคู่มือที่กำกับเมนู (Association) เมนูอาหารยังคงมีอยู่และเปิดขายได้ตามปกติแม้คู่มือฉบับนั้นจะถูกลบ"
    },
    {
        "name": "Menu",
        "file": "Menu.java",
        "domain": "โดเมนเมนู คู่มือ และสูตรอาหาร (Menu, Recipe & SOP)",
        "uml": "Menu ◆--(*)--> Recipe",
        "purpose": "ทำหน้าที่เป็นตัวแทนของเมนูอาหารในร้าน จัดการราคาขาย หมวดหมู่อาหาร สถานีครัวที่ปรุง สถานะการเปิด/ปิดขาย (ON_SALE/OFF_SALE) ตัวเลือกเสริม (Options เช่น เพิ่มไข่ดาว) และเป็นเจ้าของสูตร Recipe ทุกเวอร์ชัน",
        "fields": [
            ("SaleStatus", "enum { ON_SALE, OFF_SALE }", "public", "สถานะการขาย: ON_SALE (เปิดขาย) หรือ OFF_SALE (ปิดขาย)"),
            ("menuId", "String", "private", "รหัสเมนู เช่น 'M01', 'M02'"),
            ("name", "String", "private", "ชื่อเมนูอาหาร เช่น 'ผัดกะเพราปลา', 'ยำหมูยอ/แหนม'"),
            ("price", "double", "private", "ราคาขายพื้นฐานต่อจาน (บาท)"),
            ("category", "String", "private", "หมวดหมู่อาหาร เช่น 'จานเดียว', 'กับข้าว', 'เครื่องดื่ม'"),
            ("station", "String", "private", "สถานีครัวที่รับผิดชอบ เช่น 'ครัวร้อน', 'ครัวยำ'"),
            ("status", "SaleStatus", "private", "สถานะการขายปัจจุบัน"),
            ("spiceSelectable", "boolean", "private", "สามารถเลือกระดับความเผ็ดได้หรือไม่"),
            ("everOrdered", "boolean", "private", "เคยมีลูกค้าสั่งเมนูนี้ไปแล้วหรือไม่ (ใช้ล็อกห้ามลบ)"),
            ("recipes", "List<Recipe>", "private", "รายการสูตรอาหารทุกเวอร์ชันของเมนูนี้ (Composition)"),
            ("options, optionPrices", "List<String>, List<Double>", "private", "ชื่อตัวเลือกเสริมและราคาเพิ่มตามลำดับ index"),
            ("extraOptionIndexes, extraIngredients, extraQuantities", "Lists", "private", "การผูกตัวเลือกเสริมเข้ากับวัตถุดิบและปริมาณที่ต้องใช้เพิ่ม")
        ],
        "relationships": [
            ("Composition (Composite Owner)", "Recipe", "*", "Menu เป็นเจ้าของสูตรทุกเวอร์ชัน เมื่อลบ Menu สูตรทั้งหมดจะถูกทำลายตาม"),
            ("Association Target", "Order, OrderItem, SOP", "*", "ถูกอ้างอิงในรายการสั่งอาหารและคู่มือ SOP")
        ],
        "methods_desc": [
            ("Menu(...)", "Constructors", "สร้างเมนูอาหาร โดยตั้งสถานะเริ่มต้นเป็นปิดขาย (OFF_SALE) จนกว่าจะมีสูตรสมบูรณ์"),
            ("addRecipe(Recipe recipe)", "Composition Linker", "ผูกสูตรอาหารเข้ากับเมนู"),
            ("currentRecipe() : Recipe", "Business Logic", "เลือกสูตรที่มีสถานะ 'สมบูรณ์' (COMPLETE) และมีหมายเลขเวอร์ชันสูงสุดเพื่อนำไปใช้ปรุง"),
            ("openSale()", "State Transition", "เปิดขายเมนู มีเงื่อนไขเข้มงวด: ต้องมีสูตรที่สมบูรณ์แล้วอย่างน้อย 1 สูตร และเมนูยังไม่ถูกลบ"),
            ("closeSale()", "State Mutator", "ปิดขายเมนูชั่วคราว เช่น เมื่อวัตถุดิบหมด"),
            ("addOption(String name, double price)", "Option Management", "เพิ่มตัวเลือกเสริม เช่น 'เพิ่มไข่ดาว' ราคา 15 บาท"),
            ("addOptionIngredient(int optIdx, Ingredient ing, double qty)", "Option Inventory", "ผูกว่าตัวเลือกเสริมนั้นต้องตัดวัตถุดิบใดเพิ่ม (เช่น ไข่ไก่ 1 ฟอง)"),
            ("isDeletable() : boolean", "Business Rule", "ตรวจสอบว่าสามารถลบเมนูได้หรือไม่ (ถ้า everOrdered == true จะห้ามลบ)"),
            ("destroy()", "Lifecycle (Composition)", "สั่ง destroy() สูตรทุกเวอร์ชัน เคลียร์ตัวเลือกเสริม และตั้ง destroyed = true")
        ],
        "design_notes": "การไม่ยอมให้เปิดขาย (openSale) จนกว่าจะมีสูตรสมบูรณ์ เป็น Business Invariant ที่ยอดเยี่ยม ป้องกันไม่ให้ออเดอร์หลุดเข้าไปในระบบโดยที่ครัวไม่รู้วิธีทำและไม่รู้ว่าจะตัดสต็อกวัตถุดิบใด",
        "qa": "ทำไมเก็บตัวเลือกเสริม (Options) ไว้ใน Menu เลย ไม่สร้างคลาส Option แยก? -> เพื่อควบคุมจำนวนคลาสให้คงไว้ที่ 16 คลาสโมเดลหลักตามข้อกำหนดสถาปัตยกรรม โดยเก็บเป็นข้อมูลโครงสร้างภายใน"
    },
    {
        "name": "PurchaseOrder",
        "file": "PurchaseOrder.java",
        "domain": "โดเมนคลังวัตถุดิบและการจัดซื้อ (Inventory & Purchasing)",
        "uml": "PurchaseOrder --(1)--> Supplier, PurchaseOrder --(*)--> Ingredient",
        "purpose": "ทำหน้าที่เป็นใบสั่งซื้อวัตถุดิบจากผู้จัดจำหน่าย (PO) ติดตามสถานะตั้งแต่ฉบับร่าง (DRAFT) สั่งซื้อแล้ว (ORDERED) จนถึงตรวจรับสินค้าเข้าคลังจริง (RECEIVED) พร้อมปรับเพิ่มยอดสต็อกอัตโนมัติ",
        "fields": [
            ("PoStatus", "enum { DRAFT, ORDERED, RECEIVED }", "public", "สถานะใบสั่งซื้อ: DRAFT (ร่าง), ORDERED (ส่งคำสั่งซื้อแล้ว), RECEIVED (ตรวจรับเข้าคลังแล้ว)"),
            ("poId", "String", "private", "รหัสใบสั่งซื้อ เช่น 'PO-1'"),
            ("status", "PoStatus", "private", "สถานะใบสั่งซื้อปัจจุบัน"),
            ("createdAt", "LocalDateTime", "private", "วันและเวลาที่ออกใบสั่งซื้อ"),
            ("supplier", "Supplier", "private", "ผู้จัดจำหน่ายที่ออกใบสั่งซื้อให้ (Association)"),
            ("createdBy", "Employee", "private", "พนักงานผู้เปิดใบสั่งซื้อ (Association)"),
            ("ingredients", "List<Ingredient>", "private", "รายการวัตถุดิบที่สั่งซื้อ"),
            ("orderedQty", "List<Double>", "private", "จำนวนที่สั่งซื้อตามลำดับ index"),
            ("receivedQty", "List<Double>", "private", "จำนวนที่ได้รับจริงตามลำดับ index")
        ],
        "relationships": [
            ("Association", "Supplier", "1", "อ้างอิงผู้จัดจำหน่าย"),
            ("Association", "Ingredient", "*", "อ้างอิงวัตถุดิบในคลัง"),
            ("Association", "Employee", "1", "อ้างอิงผู้จัดทำเอกสาร")
        ],
        "methods_desc": [
            ("PurchaseOrder(String poId, Supplier supplier, Employee by)", "Constructor", "สร้างใบสั่งซื้อสถานะ DRAFT พร้อมจดเวลาปัจจุบันและเตรียม List"),
            ("addItem(Ingredient ing, double qty)", "Validation / Mutator", "เพิ่มรายการวัตถุดิบที่ต้องการสั่ง โดยตรวจสอบก่อนว่า supplier.supplies(ing) หรือไม่"),
            ("markOrdered()", "State Transition", "เปลี่ยนสถานะจาก DRAFT เป็น ORDERED เมื่อมีรายการสั่งอย่างน้อย 1 รายการ"),
            ("receive(List<Double> qtys)", "Atomic Receiving & Stocking", "ตรวจรับสินค้าจริง: ตรวจสอบความถูกต้องของตัวเลขทุกรายการให้ครบก่อน แล้วจึงวนลูปเรียก ing.receive(qty, poId, createdBy) เพื่อเพิ่มสต็อกเข้าคลังและเปลี่ยนสถานะเป็น RECEIVED"),
            ("poId(), supplier(), statusText(), ingredients(), orderedQty(), receivedQty()", "Accessors", "อ่านข้อมูลใบสั่งซื้อเพื่อแสดงผล")
        ],
        "design_notes": "ในเมธอด receive() มีการใช้รูปแบบ Two-Pass Validation (ตรวจผ่านทุกตัวก่อน ค่อยเริ่มอัปเดตสต็อก) ป้องกันปัญหาข้อมูลสต็อกไม่สอดคล้องกัน (Inconsistent State) หากเกิดข้อผิดพลาดกลางคัน",
        "qa": "ทำไมต้องมีสถานะ ORDERED คั่นกลางระหว่าง DRAFT กับ RECEIVED? -> เพราะในโลกความเป็นจริง เมื่อส่งใบสั่งซื้อไปแล้ว ร้านต้องรอให้ซัพพลายเออร์นำของมาส่ง ซึ่งจำนวนที่ส่งจริงอาจไม่เท่ากับที่สั่ง (Short shipment) จึงต้องมีการกรอก receivedQty ตอนรับจริง"
    },
    {
        "name": "OrderItem",
        "file": "OrderItem.java",
        "domain": "โดเมนออเดอร์และการเงิน (Order Lifecycle & Financial)",
        "uml": "OrderItem ◆<--(Composition)-- Order, OrderItem --(1)--> Menu",
        "purpose": "ทำหน้าที่เป็นตัวแทนของอาหาร 1 บรรทัดในออเดอร์ (เช่น ผัดกะเพราปลา 2 จาน เพิ่มไข่ดาว) ทำการ Snapshot ราคาและสูตร ณ เวลาสั่ง ควบคุมวงจรชีวิตการปรุงในครัว และจัดการระบบคำขอแก้ไข/ยกเลิกอาหารส่งให้ผู้จัดการพิจารณา",
        "fields": [
            ("ItemStatus", "enum { WAITING, COOKING, READY, SERVED, CANCELLED }", "public", "สถานะการปรุงอาหาร"),
            ("RequestType", "enum { CANCEL, CHANGE_NOTE }", "public", "ชนิดคำขอแก้ไข: ขอยกเลิก หรือ ขอแก้หมายเหตุ"),
            ("RequestStatus", "enum { NONE, PENDING, APPROVED, REJECTED }", "public", "สถานะคำขอ: ไม่มี, รออนุมัติ, อนุมัติแล้ว, ปฏิเสธ"),
            ("orderItemId", "String", "private", "รหัสรายการอาหาร เช่น 'ORD-1-ITEM-1'"),
            ("menu, recipe", "Menu, Recipe", "private", "เมนูและสูตรอาหารที่ใช้อ้างอิง (Association)"),
            ("qty", "int", "private", "จำนวนจานที่สั่ง"),
            ("price", "double", "private", "ราคาต่อหน่วยที่บันทึก Snapshot ไว้ (รวมค่าตัวเลือกเสริม)"),
            ("spiceLevel, note, option", "String", "private", "ระดับความเผ็ด หมายเหตุพิเศษ และข้อความตัวเลือกเสริม"),
            ("status", "ItemStatus", "private", "สถานะการปรุงปัจจุบัน (เริ่มต้น WAITING)"),
            ("startTime, endTime", "LocalDateTime", "private", "เวลาเริ่มปรุง และเวลาปรุงเสร็จจริง"),
            ("standardMinutes", "double", "private", "เวลามาตรฐานตาม SOP (นาที)"),
            ("handledBy", "Employee", "private", "คนครัวผู้ปรุง หรือบริกรผู้เสิร์ฟ"),
            ("requestType, requestStatus, requestReason, decisionReason", "Enums/Strings", "private", "ข้อมูลการยื่นและพิจารณาคำขอแก้ไขอาหาร"),
            ("stockDeducted", "boolean", "private", "แฟล็กจำว่ารายการนี้ถูกตัดสต็อกจริงไปแล้วหรือไม่ เพื่อความถูกต้องตอนคืนสต็อก"),
            ("optionNames, ingredients, quantities", "Lists", "private", "รายการ Snapshot ส่วนผสมและปริมาณต่อจาน")
        ],
        "relationships": [
            ("Composition (Part-of)", "Order", "1", "OrderItem เป็นส่วนประกอบย่อยของ Order ถูกสร้างและทำลายโดย Order"),
            ("Association", "Menu, Recipe, Employee", "1", "อ้างอิงเมนู สูตร และพนักงาน")
        ],
        "methods_desc": [
            ("OrderItem(...)", "Constructor", "Snapshot ราคาจาก menu.price() และคัดลอก ingredients กับ quantities จาก currentRecipe() มาเก็บไว้เองทันที"),
            ("addOption(int index)", "Option Calculator", "เพิ่มตัวเลือกเสริม บวกราคาเพิ่ม และดึงวัตถุดิบเสริมของตัวเลือกนั้นมาใส่ใน Snapshot"),
            ("amountPerDish(Ingredient ing) : double", "Calculation", "รวมปริมาณวัตถุดิบทั้งหมดต่อ 1 จาน (รวมทั้งจากสูตรหลักและตัวเลือกเสริม)"),
            ("startCooking(Employee cook, double stdMin)", "Kitchen Workflow", "เปลี่ยนสถานะเป็น COOKING บันทึกเวลาเริ่ม startTime และเวลามาตรฐาน SOP"),
            ("markReady()", "Kitchen Workflow", "เปลี่ยนสถานะเป็น READY บันทึก endTime และตรวจห้ามข้ามคำขอที่รออนุมัติ"),
            ("serve(Employee by)", "Kitchen Workflow", "เปลี่ยนสถานะเป็น SERVED (เสิร์ฟแล้ว) บันทึกพนักงาน"),
            ("cookingMinutes() / compareTime()", "KPI Analysis", "คำนวณเวลาที่ใช้ปรุงจริง และเปรียบเทียบกับเวลามาตรฐาน SOP (ถ้าเป็นบวกคือปรุงช้ากว่าเกณฑ์)"),
            ("cancel() / forceCancel()", "Cancellation & Stock Restore", "ยกเลิกรายการอาหาร หากเคยตัดสต็อกไปแล้ว (stockDeducted == true) จะคืนสต็อก ing.restore() ทันที"),
            ("requestChange(...)", "Manager Approval Workflow", "ยื่นคำขอยกเลิกหรือเปลี่ยนหมายเหตุขณะอาหารกำลังปรุง สถานะเปลี่ยนเป็น PENDING"),
            ("decideRequest(boolean approve, ...)", "Manager Approval Workflow", "ผู้จัดการพิจารณาอนุมัติ (ทำการยกเลิกจริง) หรือปฏิเสธคำขอ"),
            ("destroy()", "Lifecycle", "เคลียร์รายการ Snapshot ทั้งหมดและตัดการเชื่อมโยง")
        ],
        "design_notes": "การ Snapshot ราคาและสูตรไว้ใน OrderItem เป็นหลักการสำคัญของระบบค้าปลีกและร้านอาหาร เพราะหากในอนาคตผู้จัดการเปลี่ยนราคาเมนูจาก 69 เป็น 80 บาท หรือเปลี่ยนสูตรอาหาร บิลเก่าของลูกค้าที่สั่งไปแล้วจะต้องคงยอดเดิมไว้เสมอ",
        "qa": "ทำไมลูกค้าถึงกดยกเลิกอาหารเองไม่ได้เมื่ออาหารอยู่ในสถานะ COOKING? -> เพราะครัวได้ลงมือปรุงและใช้วัตถุดิบไปแล้ว หากลูกค้ายกเลิกโดยพลการร้านจะสูญเสียต้นทุน จึงต้องส่งคำขอให้ผู้จัดการพิจารณา (requestChange) เป็นกรณีพิเศษ"
    },
    {
        "name": "Order",
        "file": "Order.java",
        "domain": "โดเมนออเดอร์และการเงิน (Order Lifecycle & Financial)",
        "uml": "Order ◆--(*)--> OrderItem, Order --(1)--> Table, Order --(1)--> Customer",
        "purpose": "ทำหน้าที่เป็นตัวแทนของคำสั่งซื้อทั้งใบ (บิลอาหาร) ควบคุมสถานะภาพรวมของออเดอร์ จัดการตะกร้าสินค้า (CART) คำนวณยอดเงินรวม รวมรายการวัตถุดิบที่ต้องใช้และตัดสต็อกแบบอะตอมมิกเมื่อยืนยัน (CONFIRMED) ตลอดจนประสานงานระหว่างครัวและการชำระเงิน",
        "fields": [
            ("OrderStatus", "enum { CART, CONFIRMED, COOKING, READY, SERVED, PAID, CANCELLED }", "public", "สถานะภาพรวมของออเดอร์"),
            ("orderId", "String", "private", "รหัสออเดอร์ เช่น 'ORD-1'"),
            ("table", "Table", "private", "โต๊ะอาหารที่เปิดออเดอร์นี้ (Association)"),
            ("customer", "Customer", "private", "ลูกค้าผู้สั่งอาหาร (Association)"),
            ("payment", "Payment", "private", "ใบชำระเงินเมื่อเช็คบิลแล้ว (Association)"),
            ("status", "OrderStatus", "private", "สถานะออเดอร์ปัจจุบัน"),
            ("totalAmount", "double", "private", "ยอดเงินรวมล่าสุด"),
            ("createdAt", "LocalDateTime", "private", "วันเวลาที่เปิดบิล"),
            ("items", "List<OrderItem>", "private", "รายการอาหารทั้งหมดในบิลนี้ (Composition)"),
            ("itemNumber", "int", "private", "ตัวนับลำดับไอเทมในบิล"),
            ("destroyed", "boolean", "private", "แฟล็กสถานะการทำลาย")
        ],
        "relationships": [
            ("Composition (Composite Owner)", "OrderItem", "*", "Order เป็นเจ้าของ OrderItem ทั้งหมด เมื่อลบ Order รายการอาหารทั้งหมดจะถูกทำลายตาม"),
            ("Association", "Table", "1", "อ้างอิงโต๊ะอาหาร"),
            ("Association", "Customer", "1", "อ้างอิงลูกค้า"),
            ("Association", "Payment", "0..1", "อ้างอิงใบชำระเงินเมื่อจ่ายเงินแล้ว")
        ],
        "methods_desc": [
            ("Order(String orderId, Table table, Customer customer)", "Constructor", "สร้างออเดอร์ใหม่ในสถานะตะกร้า (CART) พร้อมจดเวลาเปิดบิล"),
            ("addItem(Menu menu, int qty, String spice, String note) : OrderItem", "Composition Creator", "สร้าง OrderItem ใหม่เก็บไว้ในรายการ ทำได้เฉพาะสถานะ CART และเมนูต้องเปิดขายอยู่"),
            ("removeItem(int index)", "Cart Management", "ลบอาหารออกจากตะกร้าก่อนยืนยัน สั่ง item.destroy() และนำออกจาก List"),
            ("calculateTotal() : double", "Financial Calculation", "คำนวณผลรวมราคาของรายการอาหารทั้งหมดที่ไม่ถูกยกเลิก (statusText != 'ยกเลิก')"),
            ("allIngredients() / requiredQuantity()", "Inventory Aggregation (private)", "รวมรายชื่อวัตถุดิบและคำนวณปริมาณที่ต้องใช้ทั้งหมดของทั้งบิล เพื่อนำไปตรวจสต็อก"),
            ("confirm()", "Atomic Stock Check & Deduct", "หัวใจสำคัญ: ตรวจสอบวัตถุดิบทุกชนิดให้ครบว่าพอหรือไม่ (Loop 1) หากพอครบทุกตัว จึงวนลูปตัดสต็อกจริง (Loop 2) แล้วเปลี่ยนสถานะเป็น CONFIRMED และเปลี่ยนโต๊ะเป็น 'ใช้งาน'"),
            ("changeQuantity(int index, int newQty)", "Differential Stock Update", "ปรับจำนวนจานอาหารที่รอปรุง หากเพิ่มจานจะตรวจและตัดสต็อกส่วนต่าง หากลดจานจะคืนสต็อกส่วนต่าง"),
            ("refreshStatus()", "Status Rollup", "สรุปสถานะของออเดอร์ทั้งใบโดยดูจากสถานะของ OrderItem แต่ละตัว (เช่น ถ้าปรุงเสร็จครบทุกจานจะเป็น READY ถ้าเสิร์ฟครบจะเป็น SERVED)"),
            ("isServed() : boolean", "Payment Prerequisite", "ตรวจสอบว่าอาหารที่สั่งทั้งหมดได้รับการเสิร์ฟครบถ้วนแล้วหรือยัง เพื่อเป็นเงื่อนไขก่อนคิดเงิน"),
            ("markPaid(Payment payment)", "Settlement", "บันทึกการชำระเงินและเปลี่ยนสถานะเป็น PAID"),
            ("cancel()", "Cancellation", "ยกเลิกออเดอร์ทั้งใบ (ทำได้เฉพาะเมื่อยังไม่มีรายการใดเริ่มปรุง)"),
            ("destroy()", "Lifecycle (Composition)", "สั่ง item.destroy() ทุกรายการ ล้าง items.clear() และตัดการเชื่อมโยงทั้งหมด")
        ],
        "design_notes": "ใน confirm() การแบ่งเป็น 2 Loop (Loop ตรวจเช็กก่อน แล้วค่อย Loop ตัดสต็อก) เป็นรูปแบบ Two-Phase Commit แบบย่อ เพื่อการันตีความเป็น Atomic Transaction ป้องกันกรณีตัดปลาไปแล้ว แต่พบว่าไข่ไก่ไม่พอ ซึ่งจะทำให้สต็อกปลาหายไปฟรี ๆ",
        "qa": "ทำไม Order ถึงไม่เก็บสถานะโต๊ะไว้เอง ทำไมต้องไปสั่ง table.changeTableStatus('ใช้งาน')? -> เพื่อให้โต๊ะตัวจริงถูกเปลี่ยนสถานะในระบบกลาง และหน้าจอเปิดโต๊ะใหม่จะไม่เปิดซ้ำโต๊ะที่มีคนนั่งอยู่"
    },
    {
        "name": "Member",
        "file": "Member.java",
        "domain": "โดเมนบุคคลและสถานที่ (People & Table)",
        "uml": "Member ◆--(*)--> PointTransaction",
        "purpose": "ทำหน้าที่เก็บข้อมูลสมาชิกของร้านอาหาร (ชื่อ, เบอร์โทรศัพท์ 10 หลัก, ยอดแต้มสะสม), จัดการการคำนวณแต้มสะสมจากการรับประทานอาหาร, การแลกแต้มเป็นส่วนลดเงินสด, เป็นเจ้าของประวัติ PointTransaction และควบคุมกฎการคิดแต้มระดับร้าน (Static Rules)",
        "fields": [
            ("memberId", "String", "private", "รหัสสมาชิก เช่น 'MEM-1'"),
            ("name", "String", "private", "ชื่อ-นามสกุลของสมาชิก"),
            ("phone", "String", "private", "เบอร์โทรศัพท์ 10 หลักขึ้นต้นด้วย 0 (มี Regex ตรวจสอบ)"),
            ("points", "int", "private", "ยอดแต้มสะสมปัจจุบันของสมาชิกรายนี้"),
            ("transactions", "List<PointTransaction>", "private", "รายการประวัติการได้/ใช้แต้มของสมาชิก (Composition)"),
            ("destroyed", "boolean", "private", "แฟล็กสถานะการทำลาย"),
            ("bahtPerPoint", "int", "private static", "กฎกลาง: ยอดซื้อกี่บาทได้ 1 แต้ม (ค่าเริ่มต้น 50 บาท/แต้ม)"),
            ("pointValue", "double", "private static", "กฎกลาง: 1 แต้มมีมูลค่าส่วนลดกี่บาท (ค่าเริ่มต้น 1 บาท/แต้ม)"),
            ("minRedeem", "int", "private static", "กฎกลาง: ขั้นต่ำในการแลกแต้มกี่แต้ม (ค่าเริ่มต้น 10 แต้ม)")
        ],
        "relationships": [
            ("Composition (Composite Owner)", "PointTransaction", "*", "Member เป็นเจ้าของประวัติแต้มทั้งหมดของตนเอง เมื่อลบสมาชิก ประวัติจะถูกทำลายตาม"),
            ("Association Target", "Customer", "0..1", "Customer อ้างอิง Member เมื่อลูกค้าแจ้งเบอร์โทร")
        ],
        "methods_desc": [
            ("Member(String memberId, String name, String phone)", "Constructor", "สร้างสมาชิกใหม่ ตรวจสอบเบอร์โทร และเตรียม List ประวัติแต้ม"),
            ("changePhone(String phone)", "Validation / Mutator", "เปลี่ยนเบอร์โทรศัพท์ ตรวจด้วย Regular Expression: '0[0-9]{9}' หากไม่ถูกต้องจะโยน IllegalArgumentException"),
            ("earnPoints(double netAmount, Payment payment) : int", "Loyalty Business Logic", "คำนวณแต้มใหม่: netAmount / bahtPerPoint (ปัดเศษทิ้ง) บวกแต้มเพิ่ม และสร้าง PointTransaction ประเภท 'สะสม'"),
            ("redeemPoints(int use, Payment payment)", "Loyalty Business Logic", "แลกแต้ม: ตรวจสอบ use >= minRedeem และ use <= points หักแต้ม และสร้าง PointTransaction ประเภท 'แลก'"),
            ("setRule(int b, double v, int m)", "Class-Level Configuration (public static)", "ผู้จัดการแก้ไขกฎแต้มกลางของร้าน มีผลต่อสมาชิกทุกคนทันที"),
            ("validateRedeem(int points, double amount) : boolean", "Validation Helper (public static)", "ตรวจเงื่อนไขแต้มขั้นต่ำและมูลค่าส่วนลดไม่เกินยอดบิล"),
            ("destroy()", "Lifecycle (Composition)", "สั่ง destroy() ประวัติแต้มทุกตัว ล้าง List และตั้ง destroyed = true")
        ],
        "design_notes": "การใช้คีย์เวิร์ด static สำหรับ bahtPerPoint, pointValue, minRedeem เป็นตัวอย่างที่สมบูรณ์แบบของการแบ่งแยกระหว่าง Instance Variable (แต้มของใครของมัน) กับ Class Variable (กฎเกณฑ์ที่ร้านใช้ร่วมกันทุกคน)",
        "qa": "ทำไมยอดแต้มที่ได้ถึงแปลงเป็น int (ปัดเศษทิ้ง)? -> เพราะแต้มสะสมไม่มีหน่วยเป็นทศนิยม เศษของเงินที่ไม่ครบ 50 บาท (ตามอัตรา 50 บาท/แต้ม) จะไม่ถูกนำมาคิดเป็นแต้ม"
    },
    {
        "name": "Payment",
        "file": "Payment.java",
        "domain": "โดเมนออเดอร์และการเงิน (Order Lifecycle & Financial)",
        "uml": "Payment --(1)--> Order, Payment --(1)--> Employee",
        "purpose": "ทำหน้าที่บริหารการชำระเงิน ออกใบเสร็จรับเงิน คำนวณส่วนลดจากการแลกแต้มสมาชิก คำนวณยอดเงินสุทธิ คำนวณเงินทอน และยืนยันการปิดบิลพร้อมบันทึกแต้มสะสมใหม่เข้าสู่บัญชีสมาชิกแบบเบ็ดเสร็จ",
        "fields": [
            ("PayMethod", "enum { CASH, QR }", "public", "วิธีการชำระเงิน: CASH (เงินสด) หรือ QR (สแกนจ่าย)"),
            ("paymentId", "String", "private", "รหัสการชำระเงิน เช่น 'PAY-1'"),
            ("order", "Order", "private", "ออเดอร์ที่ทำการชำระเงิน (Association)"),
            ("receivedBy", "Employee", "private", "แคชเชียร์ผู้รับเงิน (Association)"),
            ("method", "PayMethod", "private", "ช่องทางการชำระเงิน"),
            ("received", "double", "private", "จำนวนเงินที่รับจากลูกค้า"),
            ("change", "double", "private", "จำนวนเงินทอน"),
            ("discount", "double", "private", "มูลค่าส่วนลดที่ได้จากการแลกแต้ม"),
            ("netAmount", "double", "private", "ยอดเงินสุทธิที่ต้องชำระหลังหักส่วนลด"),
            ("pointsToRedeem", "int", "private", "จำนวนแต้มที่ลูกค้าขอใช้แลกส่วนลด"),
            ("earnedPoints", "int", "private", "จำนวนแต้มใหม่ที่ลูกค้าได้รับจากบิลนี้"),
            ("time", "LocalDateTime", "private", "เวลาที่ยืนยันการชำระเงินสำเร็จ"),
            ("receiptNo", "String", "private", "เลขที่ใบเสร็จ เช่น 'RCT-PAY-1'"),
            ("confirmed", "boolean", "private", "แฟล็กยืนยันว่าการชำระเงินเสร็จสมบูรณ์แล้ว")
        ],
        "relationships": [
            ("Association", "Order", "1", "อ้างอิงออเดอร์ที่ทำการชำระเงิน"),
            ("Association", "Employee", "1", "อ้างอิงแคชเชียร์ผู้รับเงิน")
        ],
        "methods_desc": [
            ("Payment(String paymentId, Order order, Employee by)", "Constructor", "สร้างใบชำระเงิน ผูกกับออเดอร์และแคชเชียร์ พร้อมสร้าง receiptNo"),
            ("calculateDiscount(int points) : double", "Discount Calculator", "คำนวณส่วนลดจากแต้ม ตรวจสอบสิทธิ์และจำนวนแต้มคงเหลือของสมาชิก"),
            ("calculateChange() : double", "Change Calculator", "คำนวณเงินทอน: received - netAmount (ปัดทศนิยม 2 ตำแหน่ง)"),
            ("pay(String method, double received, int points)", "Preparation & Validation", "คำนวณยอดเงิน เตรียมบิล ตรวจสอบเงินรับว่าพอหรือไม่ แต่ยังไม่หักแต้มและยังไม่ปิดออเดอร์"),
            ("confirm()", "Atomic Settlement", "ยืนยันการชำระเงินจริง: หักแต้มที่แลก (redeemPoints), แจกแต้มใหม่ (earnPoints), บันทึกเวลาชำระเงิน, ตั้ง confirmed = true และสั่ง order.markPaid(this) ปิดออเดอร์ทันที ป้องกันการยืนยันซ้ำ"),
            ("receiptNo(), method(), received(), change(), discount(), netAmount(), earnedPoints()", "Accessors", "อ่านข้อมูลสำหรับพิมพ์ใบเสร็จและทำรายงานยอดขาย")
        ],
        "design_notes": "การแยกเป็น 2 ขั้นตอนระหว่าง pay() (เตรียมคำนวณและแสดงตัวอย่างบิล) กับ confirm() (ยืนยันตัดเงินและแต้มจริง) ช่วยให้ผู้ใช้สามารถตรวจสอบความถูกต้องบนหน้าจอก่อนยืนยันขั้นสุดท้ายได้อย่างปลอดภัย",
        "qa": "ทำไม Payment ไม่เป็น Composition กับ Order? -> ในสถาปัตยกรรมนี้ Payment ถูกออกแบบให้เป็นเอกสารทางการเงินอิสระ (Association) แม้ Order จะถูกเคลียร์หรือยกเลิก ข้อมูลการเงินใน Payment ยังสามารถใช้สอบทานบัญชีในรายงาน UC06 ได้"
    }
]

print(f"Loaded {len(CLASSES_INFO)} classes specifications.")
