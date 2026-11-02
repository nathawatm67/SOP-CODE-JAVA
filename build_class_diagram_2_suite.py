#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class Diagram 2 Suite Generator (V3 Production Grade).
Aligned with Professor's Assignment Rubric (Item 1.4):
- 16 Official Model Classes (Zero MenuOption)
- 3 Compartments: Name + Thai Subtitle, Attributes (- priv), Operations (+ pub)
- Explicit Data Types and Signatures matching Java codebase
- 5 Composition Pairs highlighted with solid diamonds (◆)
- 1 Aggregation Pair with hollow diamond (◇)
- 15 Association lines with clean orthogonal collision-free routing
- Generates Vector SVG, 4K Ultra-Res PNG, 4 Focused Quadrant Slides, and HTML Viewer
"""

import os
import json
import html
import subprocess
import shutil

WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))
P9_DIR = os.path.join(WORKSPACE_DIR, "P9")
P8_DIR = os.path.abspath(os.path.join(WORKSPACE_DIR, "..", "P8"))

os.makedirs(P9_DIR, exist_ok=True)
if os.path.exists(P8_DIR):
    os.makedirs(P8_DIR, exist_ok=True)

CANVAS_W = 4300
CANVAS_H = 2650

CLASSES_SPEC = {
    "Table": {
        "x": 100, "y": 140, "w": 420,
        "title": "Table", "thai": "โต๊ะอาหาร",
        "badge": "Entity", "color": "#d97706", "bg_header": "#fef3c7",
        "attrs": [
            "- tableId : String",
            "- qrCode : String"
        ],
        "ops": [
            "+ Table(tableId, qrCode)",
            "+ scanTableQRCode() : void",
            "+ identifyTableNumber() : String"
        ]
    },
    "Customer": {
        "x": 100, "y": 420, "w": 420,
        "title": "Customer", "thai": "ลูกค้า / ผู้สั่งอาหาร",
        "badge": "Entity", "color": "#d97706", "bg_header": "#fef3c7",
        "attrs": [
            "- customerId : String",
            "- member : Member"
        ],
        "ops": [
            "+ Customer(customerId : String)",
            "+ checkCustomerStatus() : boolean",
            "+ setMember(member : Member) : void"
        ]
    },
    "Order": {
        "x": 680, "y": 140, "w": 480,
        "title": "Order", "thai": "คำสั่งซื้อ / บิลโต๊ะ (Whole ①)",
        "badge": "Whole ①", "color": "#ea580c", "bg_header": "#ffedd5",
        "is_whole": True, "comp_id": 1,
        "attrs": [
            "- orderId : String",
            "- status : OrderStatus",
            "- totalAmount : double",
            "- createdAt : LocalDateTime",
            "- items : List<OrderItem>  [◆ Comp 1]",
            "- table : Table",
            "- customer : Customer",
            "- payment : Payment"
        ],
        "ops": [
            "+ Order(orderId : String, table : Table)",
            "+ addItem(menu, qty, spice, note) : OrderItem",
            "+ removeItem(item : OrderItem) : void",
            "+ attachMember(member : Member) : void",
            "+ calculateTotal() : double",
            "+ confirm() : void",
            "+ cancel() : void",
            "+ changeStatus(s : OrderStatus) : void",
            "+ destroy() : void"
        ]
    },
    "OrderItem": {
        "x": 1300, "y": 140, "w": 540,
        "title": "OrderItem", "thai": "รายการอาหารในบิล (Part ①)",
        "badge": "Part ①", "color": "#ea580c", "bg_header": "#ffedd5",
        "is_part": True, "comp_id": 1,
        "attrs": [
            "- orderItemId : String",
            "- qty : int",
            "- price : double",
            "- spiceLevel : String",
            "- note : String",
            "- status : ItemStatus",
            "- startTime : LocalDateTime",
            "- endTime : LocalDateTime",
            "- requestType : RequestType",
            "- requestReason : String",
            "- requestStatus : RequestStatus",
            "- decisionReason : String",
            "- decidedBy : String",
            "- requestedAt : LocalDateTime",
            "- menu : Menu",
            "- option : String",
            "- recipe : Recipe",
            "- handledBy : Employee"
        ],
        "ops": [
            "+ OrderItem(id, menu, qty, recipe)",
            "+ startCooking(cook : Employee) : void",
            "+ markReady() : void",
            "+ serve(by : Employee) : void",
            "+ cancel() : void",
            "+ compareTime() : int",
            "+ changeStatus(s : ItemStatus) : void",
            "+ requestChange(type, reason) : void",
            "+ approve(by : Employee) : void",
            "+ reject(by : Employee, why) : void"
        ]
    },
    "Menu": {
        "x": 2000, "y": 140, "w": 490,
        "title": "Menu", "thai": "เมนูอาหาร (Whole ②)",
        "badge": "Whole ②", "color": "#059669", "bg_header": "#d1fae5",
        "is_whole": True, "comp_id": 2,
        "attrs": [
            "- menuId : String",
            "- name : String",
            "- price : double",
            "- category : String",
            "- station : String",
            "- spiceSelectable : boolean",
            "- status : SaleStatus",
            "- recipes : List<Recipe>  [◆ Comp 2]",
            "- options : Map<String, Double>"
        ],
        "ops": [
            "+ Menu(menuId : String, name, price)",
            "+ update(name, price, cat, station) : void",
            "+ openSale() : void",
            "+ closeSale() : void",
            "+ isDeletable() : boolean",
            "+ addRecipe(recipe : Recipe) : void",
            "+ addOption(name, extraPrice) : void"
        ]
    },
    "Recipe": {
        "x": 2640, "y": 140, "w": 450,
        "title": "Recipe", "thai": "สูตรอาหาร / BOM (Part ②)",
        "badge": "Part ②", "color": "#059669", "bg_header": "#d1fae5",
        "is_part": True, "comp_id": 2,
        "attrs": [
            "- recipeId : String",
            "- version : int",
            "- status : RecipeStatus",
            "- ingredients : Map<Ingredient, Double>"
        ],
        "ops": [
            "+ Recipe(recipeId : String, version : int)",
            "+ addItem(ing : Ingredient, qty : double) : void",
            "+ changeQty(ing : Ingredient, qty : double) : void",
            "+ complete() : void",
            "+ createNewVersion() : Recipe"
        ]
    },
    "SOP": {
        "x": 2000, "y": 790, "w": 490,
        "title": "SOP", "thai": "คู่มือขั้นตอนปฏิบัติงาน (Whole ③)",
        "badge": "Whole ③", "color": "#7c3aed", "bg_header": "#ede9fe",
        "is_whole": True, "comp_id": 3,
        "attrs": [
            "- sopId : String",
            "- name : String",
            "- status : SopStatus",
            "- menu : Menu",
            "- steps : List<SOPStep>  [◆ Comp 3]"
        ],
        "ops": [
            "+ SOP(sopId : String, name : String, menu : Menu)",
            "+ update(name : String) : void",
            "+ publish() : void",
            "+ disable() : void",
            "+ enable() : void",
            "+ isDeletable() : boolean",
            "+ getTotalMinutes() : double",
            "+ addStep(step : SOPStep) : void"
        ]
    },
    "SOPStep": {
        "x": 2640, "y": 790, "w": 450,
        "title": "SOPStep", "thai": "ขั้นตอนย่อย SOP (Part ③)",
        "badge": "Part ③", "color": "#7c3aed", "bg_header": "#ede9fe",
        "is_part": True, "comp_id": 3,
        "attrs": [
            "- sopStepId : String",
            "- no : int",
            "- description : String",
            "- standardMinutes : double"
        ],
        "ops": [
            "+ SOPStep(id, no, desc, minutes)",
            "+ getSopStepId() : String",
            "+ getNo() : int",
            "+ getStandardMinutes() : double"
        ]
    },
    "Ingredient": {
        "x": 2240, "y": 1420, "w": 490,
        "title": "Ingredient", "thai": "วัตถุดิบในคลัง (Whole ④)",
        "badge": "Whole ④", "color": "#e11d48", "bg_header": "#ffe4e6",
        "is_whole": True, "comp_id": 4,
        "attrs": [
            "- ingredientId : String",
            "- name : String",
            "- unit : String",
            "- stockQty : double",
            "- minQty : double",
            "- movements : List<StockMovement>  [◆ Comp 4]"
        ],
        "ops": [
            "+ Ingredient(id, name, unit, minQty)",
            "+ hasEnough(qty : double) : boolean",
            "+ deduct(qty : double, ref : String) : void",
            "+ restore(qty : double, ref : String) : void",
            "+ increaseStock(qty : double, ref : String) : void",
            "+ adjustStock(newQty, reason, by : Employee) : void",
            "+ update(name : String, unit, minQty) : void"
        ]
    },
    "StockMovement": {
        "x": 2890, "y": 1420, "w": 470,
        "title": "StockMovement", "thai": "ประวัติสต็อก / Audit Log (Part ④)",
        "badge": "Part ④", "color": "#e11d48", "bg_header": "#ffe4e6",
        "is_part": True, "comp_id": 4,
        "attrs": [
            "- stockMovementId : String",
            "- time : LocalDateTime",
            "- type : MovementType",
            "- qty : double",
            "- balance : double",
            "- reference : String",
            "- reason : String",
            "- doneBy : Employee"
        ],
        "ops": [
            "+ StockMovement(id, type, qty, bal, ref, reason, by)",
            "+ recordStockMovement(...) : void",
            "+ getStockMovementId() : String",
            "+ getType() : MovementType"
        ]
    },
    "PurchaseOrder": {
        "x": 1580, "y": 1420, "w": 490,
        "title": "PurchaseOrder", "thai": "ใบสั่งซื้อวัตถุดิบ (PO)",
        "badge": "Entity", "color": "#ea580c", "bg_header": "#ffedd5",
        "attrs": [
            "- poId : String",
            "- status : PoStatus",
            "- createdAt : LocalDateTime",
            "- orderedQty : Map<Ingredient, Double>",
            "- receivedQty : Map<Ingredient, Double>",
            "- supplier : Supplier",
            "- createdBy : Employee"
        ],
        "ops": [
            "+ PurchaseOrder(poId : String, supplier, by)",
            "+ addItem(ing : Ingredient, qty : double) : void",
            "+ markOrdered() : void",
            "+ receive(qtys : Map<Ingredient, Double>) : void"
        ]
    },
    "Supplier": {
        "x": 1580, "y": 2040, "w": 490,
        "title": "Supplier", "thai": "ผู้จัดจำหน่ายวัตถุดิบ",
        "badge": "Entity", "color": "#ea580c", "bg_header": "#ffedd5",
        "attrs": [
            "- supplierId : String",
            "- name : String",
            "- suppliedIngredients : List<Ingredient>"
        ],
        "ops": [
            "+ Supplier(supplierId : String, name : String)",
            "+ addIngredient(ingredient : Ingredient) : void",
            "+ supplies(ingredient : Ingredient) : boolean"
        ]
    },
    "Employee": {
        "x": 680, "y": 860, "w": 480,
        "title": "Employee", "thai": "พนักงานร้านอาหาร",
        "badge": "Staff Hub", "color": "#4f46e5", "bg_header": "#e0e7ff",
        "attrs": [
            "- employeeId : String",
            "- name : String",
            "- role : Role"
        ],
        "ops": [
            "+ Employee(employeeId, name, role)",
            "+ authenticateRole(requiredRole : Role) : boolean",
            "+ assignStationDuty(station : String) : void",
            "+ getEmployeeId() : String",
            "+ getRole() : Role"
        ]
    },
    "Payment": {
        "x": 100, "y": 860, "w": 420,
        "title": "Payment", "thai": "การชำระเงินและออกใบเสร็จ",
        "badge": "Entity", "color": "#0284c7", "bg_header": "#e0f2fe",
        "attrs": [
            "- paymentId : String",
            "- method : PayMethod",
            "- received : double",
            "- change : double",
            "- discount : double",
            "- receiptNo : String",
            "- time : LocalDateTime",
            "- receivedBy : Employee"
        ],
        "ops": [
            "+ Payment(id, order : Order, by : Employee)",
            "+ calculateDiscount(points : int) : double",
            "+ calculateChange() : double",
            "+ pay(method, received : double) : void",
            "+ confirm() : void",
            "+ printReceipt() : String"
        ]
    },
    "Member": {
        "x": 680, "y": 1420, "w": 480,
        "title": "Member", "thai": "สมาชิกและกฎแต้ม (Whole ⑤)",
        "badge": "Whole ⑤", "color": "#0891b2", "bg_header": "#cffafe",
        "is_whole": True, "comp_id": 5,
        "attrs": [
            "- memberId : String",
            "- name : String",
            "- phone : String",
            "- points : int",
            "- bahtPerPoint : int {static}",
            "- pointValue : double {static}",
            "- minRedeem : int {static}",
            "- transactions : List<PointTransaction>  [◆ Comp 5]"
        ],
        "ops": [
            "+ Member(memberId, name, phone)",
            "+ earnPoints(amount : double) : int",
            "+ redeemPoints(points : int) : void",
            "+ setRule(b, v, m) : void {static}",
            "+ validateRedeem(points, amount) : boolean {static}"
        ]
    },
    "PointTransaction": {
        "x": 100, "y": 1420, "w": 420,
        "title": "PointTransaction", "thai": "ประวัติแต้มสะสม (Part ⑤)",
        "badge": "Part ⑤", "color": "#0891b2", "bg_header": "#cffafe",
        "is_part": True, "comp_id": 5,
        "attrs": [
            "- pointTransactionId : String",
            "- date : LocalDateTime",
            "- type : PointType",
            "- points : int",
            "- balance : int",
            "- payment : Payment"
        ],
        "ops": [
            "+ PointTransaction(id, type, pts, bal)",
            "+ recordPointTransaction(type, pts, bal, pay) : void",
            "+ getPointTransactionId() : String",
            "+ getPoints() : int"
        ]
    }
}

for name, c in CLASSES_SPEC.items():
    header_h = 56
    attr_h = 16 + len(c["attrs"]) * 22
    op_h = 16 + len(c["ops"]) * 22
    c["header_h"] = header_h
    c["attr_h"] = attr_h
    c["op_h"] = op_h
    c["h"] = header_h + attr_h + op_h

RELATIONSHIPS = [
    # 5 Composition Pairs (◆)
    {
        "id": "R1", "type": "composition", "comp_num": 1,
        "from": "Order", "to": "OrderItem",
        "diamond_x": 1160, "diamond_y": 320, "diamond_dir": "right",
        "path": "M 1176 320 L 1298 320",
        "arrow_end": True,
        "color": "#ea580c",
        "role_from": "1", "role_to": "1..*",
        "pos_from": (1180, 342), "pos_to": (1275, 342),
        "field": "items [1..*]", "label_x": 1235, "label_y": 308
    },
    {
        "id": "R9", "type": "composition", "comp_num": 2,
        "from": "Menu", "to": "Recipe",
        "diamond_x": 2490, "diamond_y": 280, "diamond_dir": "right",
        "path": "M 2506 280 L 2638 280",
        "arrow_end": True,
        "color": "#059669",
        "role_from": "1", "role_to": "1..*",
        "pos_from": (2510, 302), "pos_to": (2615, 302),
        "field": "recipes [1..*]", "label_x": 2570, "label_y": 268
    },
    {
        "id": "R14", "type": "composition", "comp_num": 3,
        "from": "SOP", "to": "SOPStep",
        "diamond_x": 2490, "diamond_y": 920, "diamond_dir": "right",
        "path": "M 2506 920 L 2638 920",
        "arrow_end": True,
        "color": "#7c3aed",
        "role_from": "1", "role_to": "1..*",
        "pos_from": (2510, 942), "pos_to": (2615, 942),
        "field": "steps [1..*]", "label_x": 2570, "label_y": 908
    },
    {
        "id": "R15", "type": "composition", "comp_num": 4,
        "from": "Ingredient", "to": "StockMovement",
        "diamond_x": 2730, "diamond_y": 1620, "diamond_dir": "right",
        "path": "M 2746 1620 L 2888 1620",
        "arrow_end": True,
        "color": "#e11d48",
        "role_from": "1", "role_to": "0..*",
        "pos_from": (2750, 1642), "pos_to": (2865, 1642),
        "field": "movements [0..*]", "label_x": 2815, "label_y": 1608
    },
    {
        "id": "R22", "type": "composition", "comp_num": 5,
        "from": "Member", "to": "PointTransaction",
        "diamond_x": 680, "diamond_y": 1620, "diamond_dir": "left",
        "path": "M 664 1620 L 522 1620",
        "arrow_end": True,
        "color": "#0891b2",
        "role_from": "1", "role_to": "0..*",
        "pos_from": (658, 1642), "pos_to": (535, 1642),
        "field": "transactions [0..*]", "label_x": 598, "label_y": 1608
    },

    # 16 Associations & Aggregations
    {
        "id": "R2", "type": "association",
        "from": "Order", "to": "Table",
        "path": "M 680 240 L 522 240",
        "role_from": "0..*", "role_to": "1",
        "pos_from": (655, 260), "pos_to": (535, 260),
        "field": "table", "label_x": 600, "label_y": 230
    },
    {
        "id": "R3", "type": "association",
        "from": "Order", "to": "Customer",
        "path": "M 680 480 L 522 480",
        "role_from": "0..*", "role_to": "1",
        "pos_from": (655, 500), "pos_to": (535, 500),
        "field": "customer", "label_x": 600, "label_y": 470
    },
    {
        "id": "R4", "type": "association",
        "from": "Order", "to": "Payment",
        "path": "M 720 660 L 720 730 L 310 730 L 310 858",
        "role_from": "1", "role_to": "0..1",
        "pos_from": (740, 680), "pos_to": (330, 840),
        "field": "payment", "label_x": 515, "label_y": 720
    },
    {
        "id": "R5", "type": "association",
        "from": "OrderItem", "to": "Menu",
        "path": "M 1840 320 L 1998 320",
        "role_from": "*", "role_to": "1",
        "pos_from": (1860, 340), "pos_to": (1975, 340),
        "field": "menu", "label_x": 1920, "label_y": 308
    },
    {
        "id": "R7", "type": "association",
        "from": "OrderItem", "to": "Recipe",
        "path": "M 1840 460 L 1940 460 L 1940 70 L 2865 70 L 2865 138",
        "role_from": "*", "role_to": "1",
        "pos_from": (1860, 480), "pos_to": (2885, 120),
        "field": "recipe", "label_x": 2400, "label_y": 60
    },
    {
        "id": "R8", "type": "association",
        "from": "OrderItem", "to": "Employee",
        "path": "M 1300 820 L 1230 820 L 1230 920 L 1162 920",
        "role_from": "*", "role_to": "0..1",
        "pos_from": (1270, 840), "pos_to": (1175, 940),
        "field": "handledBy", "label_x": 1230, "label_y": 860
    },
    {
        "id": "R10", "type": "association",
        "from": "Recipe", "to": "Ingredient",
        "path": "M 2865 440 L 2865 730 L 2540 730 L 2540 1418",
        "role_from": "*", "role_to": "1..*",
        "pos_from": (2885, 460), "pos_to": (2560, 1400),
        "field": "ingredients", "label_x": 2700, "label_y": 720
    },
    {
        "id": "R13", "type": "association",
        "from": "SOP", "to": "Menu",
        "path": "M 2245 790 L 2245 642",
        "role_from": "0..*", "role_to": "1",
        "pos_from": (2265, 770), "pos_to": (2265, 660),
        "field": "menu", "label_x": 2245, "label_y": 715
    },
    {
        "id": "R16", "type": "association",
        "from": "StockMovement", "to": "Employee",
        "path": "M 3120 1860 L 3120 2420 L 920 2420 L 920 1242",
        "role_from": "*", "role_to": "1",
        "pos_from": (3140, 1890), "pos_to": (900, 1260),
        "field": "doneBy", "label_x": 2020, "label_y": 2410
    },
    {
        "id": "R17", "type": "association",
        "from": "PurchaseOrder", "to": "Ingredient",
        "path": "M 2070 1620 L 2238 1620",
        "role_from": "*", "role_to": "1..*",
        "pos_from": (2090, 1640), "pos_to": (2215, 1640),
        "field": "orderedQty", "label_x": 2155, "label_y": 1608
    },
    {
        "id": "R18", "type": "association",
        "from": "PurchaseOrder", "to": "Supplier",
        "path": "M 1825 1840 L 1825 2038",
        "role_from": "*", "role_to": "1",
        "pos_from": (1845, 1860), "pos_to": (1845, 2020),
        "field": "supplier", "label_x": 1825, "label_y": 1940
    },
    {
        "id": "R19", "type": "aggregation",
        "from": "Supplier", "to": "Ingredient",
        "diamond_x": 2070, "diamond_y": 2160, "diamond_dir": "right",
        "path": "M 2086 2160 L 2485 2160 L 2485 1962",
        "role_from": "1", "role_to": "1..*",
        "pos_from": (2100, 2180), "pos_to": (2505, 1980),
        "field": "suppliedIngredients [*]", "label_x": 2285, "label_y": 2150
    },
    {
        "id": "R20", "type": "association",
        "from": "PurchaseOrder", "to": "Employee",
        "path": "M 1580 1520 L 1230 1520 L 1230 1060 L 1162 1060",
        "role_from": "*", "role_to": "1",
        "pos_from": (1550, 1540), "pos_to": (1175, 1080),
        "field": "createdBy", "label_x": 1405, "label_y": 1510
    },
    {
        "id": "R21", "type": "association",
        "from": "Payment", "to": "Employee",
        "path": "M 520 1020 L 678 1020",
        "role_from": "*", "role_to": "1",
        "pos_from": (540, 1040), "pos_to": (655, 1040),
        "field": "receivedBy", "label_x": 600, "label_y": 1008
    },
    {
        "id": "R23", "type": "association",
        "from": "PointTransaction", "to": "Payment",
        "path": "M 310 1420 L 310 1262",
        "role_from": "*", "role_to": "0..1",
        "pos_from": (330, 1400), "pos_to": (330, 1280),
        "field": "payment", "label_x": 310, "label_y": 1340
    },
    {
        "id": "R24", "type": "association",
        "from": "Customer", "to": "Member",
        "path": "M 310 630 L 310 760 L 600 760 L 600 1490 L 678 1490",
        "role_from": "1", "role_to": "0..1",
        "pos_from": (330, 650), "pos_to": (655, 1510),
        "field": "member", "label_x": 455, "label_y": 750
    }
]

def make_diamond_polygon(cx, cy, direction, fill_color, stroke_color):
    if direction == "right":
        pts = f"{cx},{cy} {cx+8},{cy-6} {cx+16},{cy} {cx+8},{cy+6}"
    elif direction == "left":
        pts = f"{cx},{cy} {cx-8},{cy-6} {cx-16},{cy} {cx-8},{cy+6}"
    elif direction == "down":
        pts = f"{cx},{cy} {cx-6},{cy+8} {cx},{cy+16} {cx+6},{cy+8}"
    else:
        pts = f"{cx},{cy} {cx-6},{cy-8} {cx},{cy-16} {cx+6},{cy-8}"
    return f'<polygon points="{pts}" fill="{fill_color}" stroke="{stroke_color}" stroke-width="1.8"/>'

def generate_svg():
    svg_parts = []
    svg_parts.append(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CANVAS_W} {CANVAS_H}" width="{CANVAS_W}" height="{CANVAS_H}">
<defs>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@500;600;700&amp;family=Fira+Code:wght@400;500;600&amp;family=Sarabun:wght@400;500;600;700&amp;display=swap');
        text {{ font-family: 'Sarabun', 'Fira Code', sans-serif; }}
        .header-title {{ font-family: 'Chakra Petch', sans-serif; font-weight: 700; font-size: 21px; }}
        .header-thai {{ font-family: 'Sarabun', sans-serif; font-size: 13.5px; fill: #475569; }}
        .badge-text {{ font-family: 'Chakra Petch', sans-serif; font-weight: 600; font-size: 11.5px; }}
        .code-attr {{ font-family: 'Fira Code', monospace; font-size: 13.5px; fill: #1e293b; }}
        .code-op {{ font-family: 'Fira Code', monospace; font-size: 13px; fill: #0f172a; }}
        .vis-priv {{ font-weight: 700; fill: #ef4444; }}
        .vis-pub {{ font-weight: 700; fill: #10b981; }}
        .cardinality {{ font-family: 'Chakra Petch', monospace; font-weight: 700; font-size: 14.5px; fill: #0f172a; }}
        .role-text {{ font-family: 'Fira Code', monospace; font-size: 12.5px; fill: #1e293b; font-weight: 600; }}
        .banner-h1 {{ font-family: 'Chakra Petch', sans-serif; font-weight: 700; font-size: 34px; fill: #0f172a; }}
        .banner-p {{ font-family: 'Sarabun', sans-serif; font-size: 16px; fill: #475569; }}
    </style>
    <filter id="shadow" x="-3%" y="-2%" width="108%" height="106%" filterUnits="userSpaceOnUse">
        <feDropShadow dx="0" dy="6" stdDeviation="8" flood-color="#0f172a" flood-opacity="0.12"/>
    </filter>
    <filter id="comp-glow" x="-5%" y="-5%" width="110%" height="110%">
        <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#ea580c" flood-opacity="0.22"/>
    </filter>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
        <path d="M 0 1.5 L 9 5 L 0 8.5 z" fill="#475569"/>
    </marker>
    <marker id="arrow-comp-1" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
        <path d="M 0 1.5 L 9 5 L 0 8.5 z" fill="#ea580c"/>
    </marker>
    <marker id="arrow-comp-2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
        <path d="M 0 1.5 L 9 5 L 0 8.5 z" fill="#059669"/>
    </marker>
    <marker id="arrow-comp-3" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
        <path d="M 0 1.5 L 9 5 L 0 8.5 z" fill="#7c3aed"/>
    </marker>
    <marker id="arrow-comp-4" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
        <path d="M 0 1.5 L 9 5 L 0 8.5 z" fill="#e11d48"/>
    </marker>
    <marker id="arrow-comp-5" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
        <path d="M 0 1.5 L 9 5 L 0 8.5 z" fill="#0891b2"/>
    </marker>
</defs>

<!-- Subtle Grid Background -->
<rect width="{CANVAS_W}" height="{CANVAS_H}" fill="#f8fafc"/>
<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
    <rect width="40" height="40" fill="none"/>
    <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#e2e8f0" stroke-width="0.8"/>
</pattern>
<rect width="{CANVAS_W}" height="{CANVAS_H}" fill="url(#grid)" opacity="0.6"/>

<!-- Header Title Banner -->
<g transform="translate(100, 40)">
    <rect width="3320" height="70" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" filter="url(#shadow)"/>
    <text x="28" y="44" class="banner-h1">📐 Class Diagram 2 — ระบบบริหารจัดการร้านข้าวต้มอารมณ์ดี (16 คลาสทางการ · 21 ความสัมพันธ์ · 5 Composition)</text>
    <text x="1950" y="43" class="banner-p">ตามเกณฑ์ข้อ 1.4 ของอาจารย์: แสดง Attribute และ Operation ครบทุกคลาส · กำกับ Visibility (- private, + public) และ Data Types · เน้น Composition 5 คู่แท้ (◆)</text>
</g>

<!-- Top Legend / Key -->
<g transform="translate(3460, 40)">
    <rect width="740" height="70" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" filter="url(#shadow)"/>
    <polygon points="30,35 40,28 50,35 40,42" fill="#ea580c"/>
    <text x="58" y="40" font-family="'Chakra Petch', sans-serif" font-weight="700" font-size="14" fill="#0f172a">◆ Composition (5 คู่แท้)</text>
    
    <polygon points="250,35 260,28 270,35 260,42" fill="#ffffff" stroke="#475569" stroke-width="1.8"/>
    <text x="278" y="40" font-family="'Chakra Petch', sans-serif" font-weight="600" font-size="14" fill="#475569">◇ Aggregation (1 คู่)</text>

    <line x1="450" y1="35" x2="480" y2="35" stroke="#475569" stroke-width="2.2" marker-end="url(#arrow)"/>
    <text x="495" y="40" font-family="'Chakra Petch', sans-serif" font-weight="600" font-size="14" fill="#475569">─▶ Association</text>

    <text x="635" y="40" font-family="'Fira Code', monospace" font-size="13" fill="#64748b">- priv / + pub</text>
</g>
''')

    # Draw Relationship Lines
    svg_parts.append('<!-- ================= RELATIONSHIPS ================= -->\n<g id="relationships">')
    for rel in RELATIONSHIPS:
        rtype = rel["type"]
        path_d = rel["path"]
        rid = rel["id"]
        field = html.escape(rel.get("field", ""))
        lx = rel.get("label_x", 0)
        ly = rel.get("label_y", 0)
        r_from = rel.get("role_from", "")
        r_to = rel.get("role_to", "")
        p_from = rel.get("pos_from")
        p_to = rel.get("pos_to")

        if rtype == "composition":
            c_num = rel["comp_num"]
            color = rel["color"]
            marker_end = f"url(#arrow-comp-{c_num})"
            dx = rel["diamond_x"]
            dy = rel["diamond_y"]
            ddir = rel["diamond_dir"]

            svg_parts.append(f'''
    <!-- Composition {c_num}: {rel["from"]} -> {rel["to"]} ({rid}) -->
    <path d="{path_d}" stroke="{color}" stroke-width="3.5" fill="none" marker-end="{marker_end}"/>
    {make_diamond_polygon(dx, dy, ddir, color, color)}
    <g transform="translate({lx}, {ly})">
        <rect x="{-len(field)*4.8-10}" y="-14" width="{len(field)*9.6+20}" height="22" rx="5" fill="#ffffff" stroke="{color}" stroke-width="1.2" filter="url(#shadow)"/>
        <text x="0" y="2" text-anchor="middle" class="role-text" fill="{color}">{field}</text>
    </g>
''')
        elif rtype == "aggregation":
            dx = rel["diamond_x"]
            dy = rel["diamond_y"]
            ddir = rel["diamond_dir"]
            svg_parts.append(f'''
    <!-- Aggregation: {rel["from"]} -> {rel["to"]} ({rid}) -->
    <path d="{path_d}" stroke="#475569" stroke-width="2.4" stroke-dasharray="6,4" fill="none" marker-end="url(#arrow)"/>
    {make_diamond_polygon(dx, dy, ddir, "#ffffff", "#475569")}
    <g transform="translate({lx}, {ly})">
        <rect x="{-len(field)*4.5-8}" y="-14" width="{len(field)*9+16}" height="22" rx="5" fill="#ffffff" stroke="#cbd5e1" stroke-width="1" filter="url(#shadow)"/>
        <text x="0" y="2" text-anchor="middle" class="role-text" fill="#475569">{field}</text>
    </g>
''')
        else:
            svg_parts.append(f'''
    <!-- Association: {rel["from"]} -> {rel["to"]} ({rid}) -->
    <path d="{path_d}" stroke="#64748b" stroke-width="2.4" fill="none" marker-end="url(#arrow)"/>
    <g transform="translate({lx}, {ly})">
        <rect x="{-len(field)*4.5-8}" y="-14" width="{len(field)*9+16}" height="22" rx="5" fill="#ffffff" stroke="#cbd5e1" stroke-width="1" filter="url(#shadow)"/>
        <text x="0" y="2" text-anchor="middle" class="role-text" fill="#475569">{field}</text>
    </g>
''')

        if p_from and r_from:
            svg_parts.append(f'    <text x="{p_from[0]}" y="{p_from[1]}" class="cardinality">{r_from}</text>\n')
        if p_to and r_to:
            svg_parts.append(f'    <text x="{p_to[0]}" y="{p_to[1]}" class="cardinality">{r_to}</text>\n')

    svg_parts.append('</g>\n')

    # Draw Class Boxes
    svg_parts.append('<!-- ================= CLASS BOXES ================= -->\n<g id="classes">')
    for name, c in CLASSES_SPEC.items():
        x = c["x"]
        y = c["y"]
        w = c["w"]
        h = c["h"]
        hh = c["header_h"]
        ah = c["attr_h"]
        color = c["color"]
        bg_hdr = c["bg_header"]
        title = html.escape(c["title"])
        thai = html.escape(c["thai"])
        badge = html.escape(c.get("badge", "Entity"))

        glow_filter = 'filter="url(#comp-glow)"' if c.get("is_whole") or c.get("is_part") else 'filter="url(#shadow)"'
        border_stroke = color if c.get("is_whole") or c.get("is_part") else "#94a3b8"
        border_width = "2.8" if c.get("is_whole") or c.get("is_part") else "1.8"

        svg_parts.append(f'''
    <!-- Class {name} -->
    <g id="class-{name}" {glow_filter}>
        <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#ffffff" stroke="{border_stroke}" stroke-width="{border_width}"/>

        <!-- Header Compartment -->
        <path d="M {x} {y+10} Q {x} {y} {x+10} {y} L {x+w-10} {y} Q {x+w} {y} {x+w} {y+10} L {x+w} {y+hh} L {x} {y+hh} Z" fill="{bg_hdr}"/>
        <line x1="{x}" y1="{y+hh}" x2="{x+w}" y2="{y+hh}" stroke="{border_stroke}" stroke-width="1.5"/>

        <rect x="{x+w-95}" y="{y+8}" width="85" height="20" rx="4" fill="{color}" opacity="0.9"/>
        <text x="{x+w-52}" y="{y+22}" text-anchor="middle" fill="#ffffff" class="badge-text">{badge}</text>

        <text x="{x+18}" y="{y+28}" class="header-title" fill="{color}">{title}</text>
        <text x="{x+18}" y="{y+48}" class="header-thai">{thai}</text>

        <line x1="{x}" y1="{y+hh+ah}" x2="{x+w}" y2="{y+hh+ah}" stroke="#cbd5e1" stroke-width="1.2"/>
''')
        # Render Attributes
        cur_y = y + hh + 20
        for raw_attr in c["attrs"]:
            vis_sign = raw_attr[0]
            attr_text = html.escape(raw_attr[2:])
            svg_parts.append(f'''        <text x="{x+16}" y="{cur_y}">
            <tspan class="vis-priv">{vis_sign} </tspan>
            <tspan class="code-attr">{attr_text}</tspan>
        </text>''')
            cur_y += 22

        # Render Operations
        cur_y = y + hh + ah + 20
        for raw_op in c["ops"]:
            vis_sign = raw_op[0]
            op_text = html.escape(raw_op[2:])
            svg_parts.append(f'''        <text x="{x+16}" y="{cur_y}">
            <tspan class="vis-pub">{vis_sign} </tspan>
            <tspan class="code-op">{op_text}</tspan>
        </text>''')
            cur_y += 22

        svg_parts.append('    </g>\n')

    svg_parts.append('</g>\n</svg>')
    return "".join(svg_parts)

print("Generating V3 Production Vector SVG...")
svg_content = generate_svg()

svg_path_p9 = os.path.join(P9_DIR, "Class-Diagram-2.svg")
with open(svg_path_p9, "w", encoding="utf-8") as f:
    f.write(svg_content)
print(f"Saved: {svg_path_p9}")

if os.path.exists(P8_DIR):
    svg_path_p8 = os.path.join(P8_DIR, "Class-Diagram-2.svg")
    with open(svg_path_p8, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Saved: {svg_path_p8}")

# Build HTML Viewer
html_viewer = f'''<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Class Diagram 2 — ข้าวต้มอารมณ์ดี (16 คลาส · 5 Composition)</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@500;600;700&family=Fira+Code:wght@400;500;600&family=Sarabun:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root {{
    --primary: #ea580c;
    --bg: #0f172a;
    --panel-bg: #1e293b;
    --text: #f8fafc;
    --border: #334155;
}}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
    font-family: 'Sarabun', sans-serif;
    background: var(--bg);
    color: var(--text);
    overflow: hidden;
    height: 100vh;
    display: flex;
    flex-direction: column;
}}
.top-bar {{
    background: #1e293b;
    border-bottom: 1.5px solid #334155;
    padding: 12px 24px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 16px;
    z-index: 100;
}}
.title-group {{
    display: flex;
    align-items: center;
    gap: 12px;
}}
.badge {{
    background: linear-gradient(135deg, #ea580c, #f59e0b);
    color: white;
    font-family: 'Chakra Petch', sans-serif;
    font-weight: 700;
    font-size: 13px;
    padding: 4px 10px;
    border-radius: 6px;
}}
.h1-title {{
    font-family: 'Chakra Petch', sans-serif;
    font-size: 19px;
    font-weight: 700;
    color: #ffffff;
}}
.btn-group {{
    display: flex;
    gap: 8px;
    align-items: center;
}}
.btn {{
    background: #334155;
    color: #e2e8f0;
    border: 1px solid #475569;
    padding: 6px 14px;
    border-radius: 6px;
    font-family: 'Chakra Petch', sans-serif;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.15s ease;
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    gap: 6px;
}}
.btn:hover {{
    background: #475569;
    color: white;
}}
.btn-primary {{
    background: #ea580c;
    border-color: #c2410c;
    color: white;
}}
.btn-primary:hover {{
    background: #c2410c;
}}
.filter-btn.active {{
    background: #0284c7;
    border-color: #0369a1;
    color: white;
}}
.viewport {{
    flex: 1;
    position: relative;
    overflow: hidden;
    cursor: grab;
    background: #0b1120;
}}
.viewport:active {{
    cursor: grabbing;
}}
.diagram-container {{
    position: absolute;
    transform-origin: 0 0;
    transition: transform 0.05s ease-out;
}}
svg {{
    display: block;
    box-shadow: 0 20px 50px rgba(0,0,0,0.5);
}}
.zoom-hud {{
    position: absolute;
    bottom: 24px;
    right: 24px;
    background: rgba(30, 41, 59, 0.85);
    backdrop-filter: blur(8px);
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 8px 16px;
    font-family: 'Fira Code', monospace;
    font-size: 13px;
    color: #94a3b8;
    pointer-events: none;
}}
</style>
</head>
<body>

<div class="top-bar">
    <div class="title-group">
        <span class="badge">ข้อ 1.4</span>
        <h1 class="h1-title">Class Diagram 2 — แผนภาพรวมระบบละเอียด (16 คลาส · 21 ความสัมพันธ์ · 5 Composition)</h1>
    </div>
    <div class="btn-group">
        <button class="btn filter-btn active" onclick="filterDomain('all')">🌐 ทั้งหมด 16 คลาส</button>
        <button class="btn filter-btn" onclick="filterDomain('comp')">💎 5 Composition แท้</button>
        <button class="btn" onclick="resetZoom()">🔍 Reset View</button>
        <a href="Class-Diagram-2.svg" download="Class-Diagram-2.svg" class="btn">📥 ดาวน์โหลด SVG</a>
        <a href="Class-Diagram-2.png" download="Class-Diagram-2.png" class="btn btn-primary">📸 ดาวน์โหลด 4K PNG</a>
    </div>
</div>

<div class="viewport" id="viewport">
    <div class="diagram-container" id="container">
        {svg_content}
    </div>
    <div class="zoom-hud" id="zoomHud">Zoom: 100% | ลากเพื่อเลื่อน (Pan) | หมุนล้อเมาส์เพื่อซูม</div>
</div>

<script>
const viewport = document.getElementById('viewport');
const container = document.getElementById('container');
const hud = document.getElementById('zoomHud');

let scale = 0.38;
let pointX = 20;
let pointY = 20;
let startX = 0;
let startY = 0;
let isPanning = false;

function setTransform() {{
    container.style.transform = `translate(${{pointX}}px, ${{pointY}}px) scale(${{scale}})`;
    hud.innerText = `Zoom: ${{Math.round(scale * 100)}}% | ลากเมาส์เลื่อน (Pan) | หมุนล้อเมาส์เพื่อซูม`;
}}

setTransform();

viewport.onmousedown = function (e) {{
    e.preventDefault();
    startX = e.clientX - pointX;
    startY = e.clientY - pointY;
    isPanning = true;
}};

window.onmouseup = function (e) {{
    isPanning = false;
}};

window.onmousemove = function (e) {{
    if (!isPanning) return;
    pointX = e.clientX - startX;
    pointY = e.clientY - startY;
    setTransform();
}};

viewport.onwheel = function (e) {{
    e.preventDefault();
    const xs = (e.clientX - pointX) / scale;
    const ys = (e.clientY - pointY) / scale;
    const delta = -e.deltaY;
    (delta > 0) ? (scale *= 1.15) : (scale /= 1.15);
    scale = Math.min(Math.max(0.15, scale), 3.0);
    pointX = e.clientX - xs * scale;
    pointY = e.clientY - ys * scale;
    setTransform();
}};

function resetZoom() {{
    scale = 0.38;
    pointX = 20;
    pointY = 20;
    setTransform();
}}

function filterDomain(domain) {{
    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    event.target.classList.add('active');

    const classes = document.querySelectorAll('#classes > g');
    classes.forEach(g => {{
        if (domain === 'all') {{
            g.style.opacity = '1';
        }} else if (domain === 'comp') {{
            const isComp = g.id.includes('Order') || g.id.includes('Menu') || g.id.includes('Recipe') || 
                           g.id.includes('SOP') || g.id.includes('Ingredient') || g.id.includes('StockMovement') ||
                           g.id.includes('Member') || g.id.includes('PointTransaction');
            g.style.opacity = isComp ? '1' : '0.15';
        }}
    }});
}}
</script>
</body>
</html>
'''

html_path_p9 = os.path.join(P9_DIR, "Class-Diagram-2-Viewer.html")
with open(html_path_p9, "w", encoding="utf-8") as f:
    f.write(html_viewer)
print(f"Saved: {html_path_p9}")

if os.path.exists(P8_DIR):
    html_path_p8 = os.path.join(P8_DIR, "Class-Diagram-2-Viewer.html")
    with open(html_path_p8, "w", encoding="utf-8") as f:
        f.write(html_viewer)
    print(f"Saved: {html_path_p8}")

# Render to 4K PNG via Google Chrome Headless
render_wrapper_html = os.path.join(P9_DIR, "_render_wrapper.html")
with open(render_wrapper_html, "w", encoding="utf-8") as f:
    f.write(f'''<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
    body {{ margin: 0; padding: 0; background: #f8fafc; overflow: hidden; }}
    svg {{ display: block; }}
</style>
</head>
<body>
{svg_content}
</body>
</html>
''')

png_path_p9 = os.path.join(P9_DIR, "Class-Diagram-2.png")
print("Rendering 4K PNG via Google Chrome Headless...")
chrome_cmd = [
    "google-chrome-stable",
    "--headless",
    "--disable-gpu",
    "--window-size=4300,2650",
    f"--screenshot={png_path_p9}",
    render_wrapper_html
]
res = subprocess.run(chrome_cmd, capture_output=True, text=True)
if res.returncode == 0 and os.path.exists(png_path_p9):
    mb = os.path.getsize(png_path_p9) / (1024 * 1024)
    print(f"SUCCESS: Rendered 4K PNG: {png_path_p9} ({mb:.2f} MB)")
    if os.path.exists(P8_DIR):
        png_path_p8 = os.path.join(P8_DIR, "Class-Diagram-2.png")
        shutil.copyfile(png_path_p9, png_path_p8)
        print(f"Synced to P8: {png_path_p8}")
else:
    print("Error rendering PNG:", res.stderr)

if os.path.exists(render_wrapper_html):
    os.remove(render_wrapper_html)

# Generate 4 Quadrant Slide PNGs
quads = [
    ("Class-Diagram-2-Part1-Orders.png", "1780x950+80+110"),
    ("Class-Diagram-2-Part2-Kitchen.png", "1250x1100+1940+110"),
    ("Class-Diagram-2-Part3-Stock.png", "1900x1100+1500+1350"),
    ("Class-Diagram-2-Part4-Cashier.png", "1100x1450+80+800")
]

for name, crop in quads:
    out_p9 = os.path.join(P9_DIR, name)
    cmd = ["magick", png_path_p9, "-crop", crop, "+repage", out_p9]
    subprocess.run(cmd, check=True)
    if os.path.exists(P8_DIR):
        shutil.copyfile(out_p9, os.path.join(P8_DIR, name))
    print(f"Generated {name}")

print("Class Diagram 2 Suite generation complete!")
