import java.util.ArrayList;
import java.util.Scanner;
import java.time.LocalDate;
import model.*;

/*
 * เริ่มอ่านจาก main() → createSampleData() → เมนู uc01() ถึง uc08()
 * Main รับคำตอบและแสดงผล ส่วน model เก็บข้อมูลและกฎการทำงานของแต่ละ object
 * ใช้ข้อมูลร้านชุดเดียวกันตลอดการเปิดโปรแกรม ปิดแล้วข้อมูลหาย (ไม่มีฐานข้อมูล)
 */
public class Main {
    // static ทำให้เมธอดใน Main ใช้รายการเหล่านี้ร่วมกันได้
    static Scanner keyboard = new Scanner(System.in, "UTF-8");
    static ArrayList<Table> tables = new ArrayList<Table>();
    static ArrayList<Menu> menus = new ArrayList<Menu>();
    static ArrayList<Ingredient> ingredients = new ArrayList<Ingredient>();
    static ArrayList<Member> members = new ArrayList<Member>();
    static ArrayList<Supplier> suppliers = new ArrayList<Supplier>();
    static ArrayList<SOP> sops = new ArrayList<SOP>();
    static ArrayList<Order> orders = new ArrayList<Order>();
    static ArrayList<PurchaseOrder> purchaseOrders = new ArrayList<PurchaseOrder>();
    static Employee manager = new Employee("EMP-1", "ผู้จัดการ", "ผู้จัดการ");
    static Employee cashier = new Employee("EMP-2", "แคชเชียร์", "แคชเชียร์");
    static Employee cook = new Employee("EMP-3", "คนครัว", "คนครัว");
    static int nextNumber = 0;
    static int nextOrderNumber = 0;
    static int nextPaymentNumber = 0;
    static boolean running = true;

    // หน้าจอแบบ Text Mode P4: ใช้เส้น = และ - เท่านั้น ไม่มีกรอบข้าง
    static void screen(String title, String role) {
        System.out.println("\n========================================================================");
        System.out.println("==== " + title + " ====");
        System.out.println("------------------------------------------------------------------------");
        System.out.println("บทบาท: " + role);
        System.out.println("------------------------------------------------------------------------");
    }

    static void line() {
        System.out.println("------------------------------------------------------------------------");
    }

    public static void main(String[] args) {
        createSampleData();
        while (running) {
            screen("ร้านข้าวต้มอารมณ์ดี - เมนูหลัก", "ลูกค้า / พนักงาน / ผู้จัดการ");
            System.out.println("1 สั่งอาหารผ่าน QR โต๊ะ (จำลอง) / ติดตามออเดอร์");
            System.out.println("2 จัดการคู่มือ SOP");
            System.out.println("3 ปรุงอาหารและเสิร์ฟ");
            System.out.println("4 ชำระเงิน");
            System.out.println("5 สต็อกและใบสั่งซื้อ");
            System.out.println("6 ภาพรวมและรายงานยอดขาย");
            System.out.println("7 จัดการเมนูและสูตรอาหาร");
            System.out.println("8 สมาชิกและแต้ม");
            System.out.println("0 ออกจากโปรแกรม");
            System.out.println("========================================================================");
            // จับข้อผิดพลาดจาก model แล้วแจ้งผู้ใช้ โดยไม่ปิดโปรแกรมทั้งตัว
            try {
                int choice = readInt("เลือกเมนู", 0, 8);
                if (choice == 0)
                    running = false;
                else if (choice == 1)
                    uc01();
                else if (choice == 2)
                    uc02();
                else if (choice == 3)
                    uc03();
                else if (choice == 4)
                    uc04();
                else if (choice == 5)
                    uc05();
                else if (choice == 6)
                    uc06();
                else if (choice == 7)
                    uc07();
                else if (choice == 8)
                    uc08();
            } catch (IllegalArgumentException e) {
                System.out.println("ทำรายการไม่ได้: " + e.getMessage());
            } catch (IllegalStateException e) {
                System.out.println("ทำรายการไม่ได้: " + e.getMessage());
            }
        }
        System.out.println("จบการทำงาน");
    }

    // ---------- เครื่องมือรับคำตอบ: อ่านเป็นข้อความก่อน แล้วค่อยแปลงเป็นตัวเลข
    // ----------
    static String readText(String question) {
        System.out.print(question + "\n> ");
        // ถ้าปิดช่องรับข้อมูล (เช่น Ctrl+D) ให้กลับไปจบโปรแกรมอย่างปกติ
        if (!keyboard.hasNextLine()) {
            running = false;
            throw new IllegalStateException("สิ้นสุดข้อมูลที่รับเข้า");
        }
        return keyboard.nextLine().trim();
    }

    static String readRequired(String question) {
        String text = readText(question);
        while (text.isEmpty()) {
            System.out.println("กรุณากรอกข้อมูล");
            text = readText(question);
        }
        return text;
    }

    static int readInt(String question, int minimum, int maximum) {
        while (true) {
            String text = readText(question);
            try {
                int number = Integer.parseInt(text);
                if (number >= minimum && number <= maximum)
                    return number;
            } catch (NumberFormatException e) {
                // กรอกไม่ใช่จำนวนเต็ม ให้แสดงคำแนะนำแล้ววนถามใหม่
            }
            System.out.println("กรอกจำนวนเต็ม " + minimum + " ถึง " + maximum);
        }
    }

    static double readNumber(String question, double minimum, double maximum) {
        while (true) {
            String text = readText(question);
            try {
                double number = Double.parseDouble(text);
                if (Double.isFinite(number) && number >= minimum && number <= maximum)
                    return number;
            } catch (NumberFormatException e) {
                // แปลงไม่ได้ ให้ถามใหม่
            }
            System.out.println("กรอกตัวเลข " + minimum + " ถึง " + maximum);
        }
    }

    static boolean confirm(String question) {
        return readInt(question + " (1 ยืนยัน / 0 ยกเลิก)", 0, 1) == 1;
    }

    static String newId(String prefix) {
        nextNumber++;
        return prefix + "-" + nextNumber;
    }

    // รหัสแบบเดียวกับตัวอย่าง P4 แต่ใช้วันที่จริงขณะรัน
    static String newOrderId() {
        nextOrderNumber++;
        return "ORD-" + LocalDate.now().format(java.time.format.DateTimeFormatter.BASIC_ISO_DATE)
                + "-" + String.format("%04d", nextOrderNumber);
    }

    static String newPaymentId() {
        nextPaymentNumber++;
        return "PAY-" + LocalDate.now().format(java.time.format.DateTimeFormatter.BASIC_ISO_DATE)
                + "-" + String.format("%04d", nextPaymentNumber);
    }

    static String cartId(Order order) {
        return order.getOrderId().replace("ORD-", "CRT-");
    }

    // ข้อความบนจอ P4 ใช้คำว่า "รับออเดอร์" สำหรับรายการที่รอครัว
    static String displayStatus(String status) {
        if (status.equals("รอปรุง") || status.equals("ยืนยันแล้ว"))
            return "รับออเดอร์";
        if (status.equals("เปิดขาย"))
            return "พร้อมขาย";
        return status;
    }

    static LocalDate readDate(String question) {
        while (true) {
            try {
                return LocalDate.parse(readText(question + " (ปี-เดือน-วัน เช่น 2026-11-01)"));
            } catch (java.time.format.DateTimeParseException e) {
                System.out.println("วันที่ไม่ถูกต้อง");
            }
        }
    }

    // ---------- ข้อมูลเริ่มต้น: new สร้าง object แล้ว add เก็บลงรายการ ----------
    static void createSampleData() {
        for (int i = 1; i <= 8; i++) {
            String tableId = String.format("TBL-%03d", i);
            tables.add(new Table(tableId, "QR-" + tableId, 4));
        }
        // ข้อมูลสาธิต P4: เมื่อสั่งกะเพราปลา 2 จานกับยำ 1 จาน ยอดเป็น 233 บาท
        Ingredient fish = addIngredient("เนื้อปลา", "กก.", 5.3, 2);
        Ingredient rice = addIngredient("ข้าวสาร", "กก.", 50.24, 20);
        Ingredient basil = addIngredient("ใบกะเพรา", "กำ", 6.4, 10);
        Ingredient egg = addIngredient("ไข่ไก่", "ฟอง", 3, 30);
        Ingredient oil = addIngredient("น้ำมัน", "ลิตร", 8.06, 3);
        Ingredient herb = addIngredient("มะตูมแห้ง", "กก.", 2, 1);
        Ingredient ham = addIngredient("หมูยอ", "กก.", 1, 0.5);
        Ingredient pork = addIngredient("หมูเนื้อแดง", "กก.", 5, 2);

        Menu porridge = new Menu("MNU-001", "ข้าวต้มปลา", 80, "ต้ม/นึ่ง", "ครัวร้อน");
        Recipe porridgeRecipe = new Recipe(newId("RCP"), 1);
        porridgeRecipe.addIngredient(fish, 0.15);
        porridgeRecipe.addIngredient(rice, 0.1);
        porridgeRecipe.complete();
        porridge.addRecipe(porridgeRecipe);
        porridge.openSale();
        menus.add(porridge);

        Menu garlic = new Menu("MNU-018", "หมูกระเทียม", 120, "ผัด", "ครัวร้อน");
        Recipe garlicRecipe = new Recipe(newId("RCP"), 1);
        garlicRecipe.addIngredient(pork, 0.2);
        garlicRecipe.addIngredient(oil, 0.02);
        garlicRecipe.complete();
        garlic.addRecipe(garlicRecipe);
        garlic.openSale();
        menus.add(garlic);

        Menu stir = new Menu("MNU-029", "ผัดกะเพราปลา", 69, "ผัด", "ครัวร้อน");
        stir.setSpiceSelectable(true);
        Recipe stirRecipe = new Recipe(newId("RCP"), 1);
        stirRecipe.addIngredient(fish, 0.15);
        stirRecipe.addIngredient(rice, 0.12);
        stirRecipe.addIngredient(basil, 0.2);
        stirRecipe.addIngredient(oil, 0.02);
        stirRecipe.complete();
        stir.addRecipe(stirRecipe);
        stir.addOption("เพิ่มไข่ดาว", 15);
        stir.addOptionIngredient(0, egg, 1);
        stir.addOptionIngredient(0, oil, 0.01);
        stir.addOption("เพิ่มข้าว", 10);
        stir.addOptionIngredient(1, rice, 0.12);
        stir.openSale();
        menus.add(stir);

        Menu yum = new Menu("MNU-007", "ยำหมูยอ/แหนม", 65, "ยำ", "ครัวเย็น");
        yum.setSpiceSelectable(true);
        Recipe yumRecipe = new Recipe(newId("RCP"), 1);
        yumRecipe.addIngredient(ham, 0.1);
        yumRecipe.complete();
        yum.addRecipe(yumRecipe);
        yum.openSale();
        menus.add(yum);

        Menu drink = new Menu("MNU-033", "น้ำมะตูม", 45, "เครื่องดื่ม", "บาร์น้ำ");
        Recipe drinkRecipe = new Recipe(newId("RCP"), 1);
        drinkRecipe.addIngredient(herb, 0.05);
        drinkRecipe.complete();
        drink.addRecipe(drinkRecipe);
        drink.openSale();
        menus.add(drink);

        createSop(porridge, "เตรียมปลาและข้าว", 2, "ต้มและจัดชาม", 5);
        createSop(garlic, "เตรียมหมูและกระเทียม", 2, "ผัดและจัดจาน", 5);
        createSop(stir, "เตรียมวัตถุดิบ", 2, "ผัดและจัดจาน", 5);
        createSop(yum, "เตรียมหมูยอและน้ำยำ", 2, "คลุกและจัดจาน", 3);
        createSop(drink, "ต้มมะตูมและกรอง", 3, "เติมน้ำแข็งและเสิร์ฟ", 1);

        Supplier supplier = new Supplier(newId("SUP"), "ร้านวัตถุดิบชุมชน");
        for (int i = 0; i < ingredients.size(); i++)
            supplier.addIngredient(ingredients.get(i));
        suppliers.add(supplier);
        Member p4Member = new Member("MBR-0001", "Human", "0999999999");
        p4Member.earnPoints(2300, null);
        members.add(p4Member);
        Member member = new Member(newId("MBR"), "สมชาย", "0812345678");
        member.earnPoints(2300, null); // ข้อมูลประวัติเริ่มต้น: 2300 / 50 = 46 แต้ม
        members.add(member);
    }

    static Ingredient addIngredient(String name, String unit, double quantity, double minimum) {
        Ingredient ingredient = new Ingredient(newId("ING"), name, unit, minimum);
        ingredient.receive(quantity, "ยอดเริ่มต้น", manager);
        ingredients.add(ingredient);
        return ingredient;
    }

    static void createSop(Menu menu, String first, double firstMinutes, String second, double secondMinutes) {
        SOP sop = new SOP(newId("SOP"), "SOP " + menu.getName(), menu);
        sop.addStep(first, firstMinutes);
        sop.addStep(second, secondMinutes);
        sop.publish();
        sops.add(sop);
    }

    // ---------- เลือก object: ผู้ใช้เห็นเลขเริ่ม 1 แต่ ArrayList ใช้ตำแหน่งเริ่ม 0
    // ----------
    static Menu chooseMenu() {
        screen("รายการเมนูอาหารทั้งหมด", "ผู้จัดการ / ลูกค้า");
        for (int i = 0; i < menus.size(); i++) {
            Menu menu = menus.get(i);
            System.out.printf("[%d] %s - %s - %.2f บาท - %s%n", i + 1, menu.getName(), menu.getCategory(),
                    menu.getPrice(), menu.getStatus());
        }
        int choice = readInt("เลือกเมนู (0 กลับ)", 0, menus.size());
        if (choice == 0)
            return null;
        return menus.get(choice - 1);
    }

    // P4 เลือกหมวดก่อน แล้วจึงเลือกอาหารในหมวดนั้น
    static Menu chooseMenuForOrder(Order order) {
        String[] categories = { "ต้ม/นึ่ง", "ยำ", "ปลา", "ทอด", "ผัด", "ทานเล่น",
                "น้ำสมุนไพร", "อิตาเลียนโซดา", "น้ำผลไม้", "น้ำปั่น", "เครื่องดื่ม" };
        while (true) {
            screen("เลือกหมวดหมู่อาหาร", "ลูกค้า");
            for (int i = 0; i < categories.length; i++) {
                System.out.println("[" + (i + 1) + "] " + categories[i]);
            }
            line();
            System.out.println("[C] ดูตะกร้าอาหาร - [0] ย้อนกลับ");
            String answer = readText("เลือกหมวด (1-11) หรือ C");
            if (answer.equalsIgnoreCase("C")) {
                showOrder(order);
                continue;
            }
            int categoryNumber;
            try {
                categoryNumber = Integer.parseInt(answer);
            } catch (NumberFormatException e) {
                System.out.println("กรอกเลขหมวด 1 ถึง 11 หรือ C");
                continue;
            }
            if (categoryNumber == 0)
                return null;
            if (categoryNumber < 1 || categoryNumber > categories.length) {
                System.out.println("กรอกเลขหมวด 1 ถึง 11 หรือ C");
                continue;
            }
            String category = categories[categoryNumber - 1];
            ArrayList<Menu> choices = new ArrayList<Menu>();
            screen("หมวด " + category, "ลูกค้า");
            for (int i = 0; i < menus.size(); i++) {
                Menu menu = menus.get(i);
                if (menu.getCategory().equals(category)) {
                    choices.add(menu);
                    System.out.printf("[%d] %s %s - %.2f บาท - [%s]%n", choices.size(),
                            menu.getMenuId(), menu.getName(), menu.getPrice(), displayStatus(menu.getStatus()));
                }
            }
            if (choices.isEmpty())
                System.out.println("หมวดนี้ยังไม่มีเมนูสาธิต");
            int menuNumber = readInt("เลือกเมนู (0 กลับไปเลือกหมวด)", 0, choices.size());
            if (menuNumber != 0)
                return choices.get(menuNumber - 1);
        }
    }

    static Ingredient chooseIngredient() {
        showStock();
        int choice = readInt("เลือกวัตถุดิบ (0 กลับ)", 0, ingredients.size());
        if (choice == 0)
            return null;
        return ingredients.get(choice - 1);
    }

    static Order chooseOrder() {
        for (int i = 0; i < orders.size(); i++) {
            Order order = orders.get(i);
            System.out.printf("[%d] %s - โต๊ะ %s - %s - %.2f บาท%n", i + 1, order.getOrderId(),
                    order.getTable().getTableId(), order.getStatus(), order.calculateTotal());
        }
        int choice = readInt("เลือกออเดอร์ (0 กลับ)", 0, orders.size());
        if (choice == 0)
            return null;
        return orders.get(choice - 1);
    }

    static int chooseItem(Order order) {
        showOrder(order);
        return readInt("เลือกรายการอาหาร (0 กลับ)", 0, order.getItems().size()) - 1;
    }

    static Member findMember(String phone) {
        for (int i = 0; i < members.size(); i++) {
            if (members.get(i).getPhone().equals(phone))
                return members.get(i);
        }
        return null;
    }

    static SOP findSop(Menu menu) {
        for (int i = 0; i < sops.size(); i++) {
            if (sops.get(i).getMenu() == menu)
                return sops.get(i);
        }
        return null;
    }

    static void showOrder(Order order) {
        if (order.getStatus().equals("ตะกร้า")) {
            screen("ตรวจสอบตะกร้าอาหาร (Cart)", "ลูกค้า");
            System.out.println("โต๊ะ: " + order.getTable().getTableId() + " - ตะกร้า: " + cartId(order));
        } else {
            screen("ติดตามสถานะการปรุงในครัว", "ลูกค้า");
            System.out.println("สถานะออเดอร์: " + order.getOrderId() + " - โต๊ะ " + order.getTable().getTableId()
                    + " - " + displayStatus(order.getStatus()));
        }
        line();
        for (int i = 0; i < order.getItems().size(); i++) {
            OrderItem item = order.getItems().get(i);
            if (order.getStatus().equals("ตะกร้า")) {
                System.out.printf("%d. %s x%d - %.2f บาท%n", i + 1, item.getMenu().getName(),
                        item.getQuantity(), item.getPrice());
            } else {
                System.out.printf("%d. %s x%d - %.2f บาท - [%s]%n", i + 1,
                        item.getMenu().getName(), item.getQuantity(), item.getPrice(), displayStatus(item.getStatus()));
            }
            System.out.println("  เผ็ด: " + item.getSpice() + " ตัวเลือก: " + item.getOptionNames() + " หมายเหตุ: "
                    + item.getNote());
            if (!item.getRequestStatus().equals("ไม่มี")) {
                System.out.println("  คำขอ: " + item.getRequestType() + " - " + item.getRequestStatus() + " - "
                        + item.getRequestReason());
                System.out.println("  ผลพิจารณา: " + item.getDecisionReason());
            }
        }
        line();
        System.out.printf("ราคารวม: %.2f บาท (ไม่นับรายการยกเลิก)%n", order.calculateTotal());
        System.out.println("========================================================================");
    }

    // ---------- UC-01 สั่งอาหารและติดตาม ----------
    static void uc01() {
        screen("ข้าวต้มอารมณ์ดี - สั่งอาหารผ่าน QR Code", "ลูกค้า - แคชเชียร์ - ผู้จัดการ");
        System.out.println("จำลองการสั่งอาหาร ปรับแต่งเมนู ส่งเข้าครัว และติดตามสถานะ");
        line();
        System.out.println("[1] สแกน QR Code และสั่งอาหารใหม่");
        System.out.println("[2] ติดตามสถานะและจัดการออเดอร์");
        System.out.println("[0] ย้อนกลับหน้าหลัก");
        int choice = readInt("เลือกงานสั่งอาหาร", 0, 2);
        if (choice == 0)
            return;
        if (choice == 2) {
            manageOrder();
            return;
        }
        for (int i = 0; i < tables.size(); i++) {
            System.out.println("[" + (i + 1) + "] " + tables.get(i).getTableId() + " - " + tables.get(i).getStatus());
        }
        int tableChoice = readInt("เลือก QR ของโต๊ะ (0 กลับ)", 0, tables.size());
        if (tableChoice == 0)
            return;
        Table table = tables.get(tableChoice - 1);
        screen("สแกน QR Code ประจำโต๊ะ", "ลูกค้า");
        System.out.println("ระบบระบุโต๊ะ " + table.getTableId() + " จาก " + table.getQrCode());
        screen("สิทธิพิเศษสมาชิกและสะสมแต้ม", "ลูกค้า");
        System.out.println(
                "ทุก " + Member.getBahtPerPoint() + " บาท = 1 แต้ม - 1 แต้ม = " + Member.getPointValue() + " บาท");
        Customer customer = new Customer(newId("CUS"));
        String phone = readText("เบอร์สมาชิก (Enter ข้าม)");
        if (!phone.isEmpty()) {
            Member member = findMember(phone);
            if (member == null)
                System.out.println("ไม่พบสมาชิก บิลนี้ยังไม่ผูกสมาชิก");
            else {
                customer.setMember(member);
                System.out.println("ระบบผูกเบอร์ " + phone + " (" + member.getName() + " - "
                        + member.getMemberId() + ") กับออเดอร์เพื่อสะสมแต้มตอนชำระเงิน");
            }
        }
        Order order = new Order(newOrderId(), table, customer);
        System.out.println("สร้างตะกร้า " + cartId(order) + " ให้อัตโนมัติ");
        boolean editing = true;
        while (editing) {
            showOrder(order);
            System.out.println("[1] เลือกหมวดและเพิ่มอาหาร");
            System.out.println("[2] แก้จำนวนจาน");
            System.out.println("[3] ลบรายการ");
            System.out.println("[4] ยืนยันส่งออเดอร์เข้าครัว");
            System.out.println("[0] ทิ้งตะกร้าและกลับหน้าหลัก");
            int action = readInt("เลือกตัวเลือกในตะกร้า", 0, 4);
            if (action == 0) {
                order.destroy();
                return;
            }
            if (action == 1)
                addFood(order);
            else if (action == 2) {
                int index = chooseItem(order);
                if (index >= 0)
                    order.changeQuantity(index, readInt("จำนวนใหม่", 1, 100));
            } else if (action == 3) {
                int index = chooseItem(order);
                if (index >= 0)
                    order.removeItem(index);
            } else if (action == 4) {
                // ถ้าสต็อกไม่พอ ให้กลับมาแก้ตะกร้าเดิมได้
                try {
                    screen("ยืนยันการสั่งอาหารเข้าครัว", "ลูกค้า");
                    System.out.printf("สรุปรายการ %d รายการ รวม %.2f บาท%n", order.getItems().size(),
                            order.calculateTotal());
                    order.confirm();
                    orders.add(order);
                    System.out.println("วัตถุดิบเพียงพอ - ส่งครัวแล้ว " + order.getOrderId());
                    System.out.println("ตัดสต็อกตามสูตรทันที - สต็อกคงเหลือ:");
                    for (int i = 0; i < ingredients.size(); i++) {
                        Ingredient ingredient = ingredients.get(i);
                        System.out.printf("%s = %.3f %s%n", ingredient.getName(),
                                ingredient.getStockQty(), ingredient.getUnit());
                    }
                    int hot = 0;
                    int cold = 0;
                    int bar = 0;
                    for (int i = 0; i < order.getItems().size(); i++) {
                        String station = order.getItems().get(i).getMenu().getStation();
                        if (station.equals("ครัวร้อน"))
                            hot++;
                        else if (station.equals("ครัวเย็น"))
                            cold++;
                        else if (station.equals("บาร์น้ำ"))
                            bar++;
                    }
                    System.out.println("ส่งรายการเข้าจอ KDS: ครัวร้อน " + hot + " - ครัวเย็น "
                            + cold + " - บาร์น้ำ " + bar + " รายการ");
                    showOrder(order);
                    editing = false;
                } catch (IllegalArgumentException e) {
                    System.out.println(e.getMessage());
                } catch (IllegalStateException e) {
                    System.out.println(e.getMessage());
                }
            }
        }
    }

    static void addFood(Order order) {
        Menu menu = chooseMenuForOrder(order);
        if (menu == null)
            return;
        if (!menu.getStatus().equals("เปิดขาย")) {
            System.out.println("เมนูนี้ปิดขาย");
            return;
        }
        screen("ปรับแต่งเมนูอาหาร", "ลูกค้า");
        System.out.printf("%s %s - %s - ราคา %.2f บาท%n", menu.getMenuId(), menu.getName(), menu.getStation(),
                menu.getPrice());
        int quantity = readInt("จำนวนจาน", 1, 100);
        String spice = "ไม่ระบุ";
        if (menu.isSpiceSelectable()) {
            System.out.println("ระดับความเผ็ด: [1] ไม่เผ็ด [2] เผ็ดน้อย [3] เผ็ดปกติ [4] เผ็ดมาก");
            String[] levels = { "ไม่เผ็ด", "เผ็ดน้อย", "เผ็ดปกติ", "เผ็ดมาก" };
            spice = levels[readInt("ระดับความเผ็ด [1-4]", 1, 4) - 1];
        }
        for (int i = 0; i < menu.getOptionNames().size(); i++) {
            System.out.printf("[%d] %s +%.2f บาท%n", i + 1, menu.getOptionNames().get(i), menu.getOptionPrice(i));
        }
        String options = "0";
        if (!menu.getOptionNames().isEmpty())
            options = readText("ตัวเลือกเพิ่มเติม (เลขหลายอันคั่นด้วย , หรือ 0)");
        String note = readText("หมายเหตุ (Enter ไม่มี)");
        OrderItem item = order.addItem(menu, quantity, spice, note);
        String[] chosen = options.split(",");
        for (int i = 0; i < chosen.length; i++) {
            try {
                int optionNumber = Integer.parseInt(chosen[i].trim());
                if (optionNumber >= 1 && optionNumber <= menu.getOptionNames().size())
                    item.addOption(optionNumber - 1);
            } catch (NumberFormatException e) {
                System.out.println("ข้ามตัวเลือกที่ไม่ใช่ตัวเลข: " + chosen[i]);
            }
        }
        System.out.printf("ราคารายการ: %.2f บาท%n", item.getPrice());
        if (!confirm("ใส่ตะกร้าหรือไม่")) {
            order.removeItem(order.getItems().size() - 1);
            return;
        }
        System.out.println("เพิ่มลงตะกร้าแล้ว (" + order.getItems().size() + " รายการ)");
    }

    static void manageOrder() {
        screen("ติดตามสถานะและจัดการออเดอร์", "ลูกค้า");
        Order order = chooseOrder();
        if (order == null)
            return;
        int index = chooseItem(order);
        if (index < 0)
            return;
        if (order.getPayment() != null) {
            System.out.println("ชำระแล้ว แก้ไขไม่ได้");
            return;
        }
        OrderItem item = order.getItems().get(index);
        int action = readInt("1 แก้จำนวน / 2 ยกเลิก / 3 ขอแก้หมายเหตุ / 0 กลับ", 0, 3);
        if (action == 0)
            return;
        if (action == 1)
            order.changeQuantity(index, readInt("จำนวนใหม่", 1, 100));
        else if (action == 2 && item.getStatus().equals("รอปรุง"))
            order.cancelItem(index);
        else if (action == 2)
            item.requestChange("ยกเลิก", readRequired("เหตุผล"), "");
        else {
            String note = readRequired("หมายเหตุใหม่");
            if (item.getStatus().equals("รอปรุง"))
                item.setNote(note);
            else
                item.requestChange("แก้หมายเหตุ", readRequired("เหตุผล"), note);
        }
        releaseTable(order.getTable());
        showOrder(order);
    }

    // ---------- UC-02 จัดการคู่มือ SOP ----------
    static void uc02() {
        screen("ข้าวต้มอารมณ์ดี - จัดการ SOP (Standard Operating Procedure)", "ผู้จัดการ");
        System.out.println("[1] ดูรายการ SOP ทั้งหมด");
        System.out.println("[2] สร้าง SOP ใหม่และกำหนดขั้นตอน");
        System.out.println("[3] แก้ไข SOP ฉบับร่าง");
        System.out.println("[4] เผยแพร่ SOP ให้ครัวใช้");
        System.out.println("[5] แก้ไข SOP ที่เผยแพร่แล้ว");
        System.out.println("[6] ปิดใช้งานหรือเปิดใช้งาน SOP อีกครั้ง");
        System.out.println("[7] ลบ SOP ฉบับร่าง");
        System.out.println("[0] ย้อนกลับหน้าหลัก");
        int action = readInt("เลือกงาน SOP", 0, 7);
        if (action == 0)
            return;
        if (action == 1) {
            screen("รายการคู่มือขั้นตอนการปรุงอาหาร (SOP ทั้งหมด)", "ผู้จัดการ");
            for (int i = 0; i < sops.size(); i++) {
                SOP sop = sops.get(i);
                System.out.println(sop.getName() + " - " + sop.getMenu().getName() + " - " + sop.getStatus());
            }
            return;
        }
        if (action == 2) {
            Menu menu = chooseMenu();
            if (menu == null)
                return;
            if (findSop(menu) != null) {
                System.out.println("เมนูนี้มี SOP แล้ว");
                return;
            }
            SOP sop = new SOP(newId("SOP"), readRequired("ชื่อ SOP"), menu);
            do {
                sop.addStep(readRequired("รายละเอียดขั้นตอน"), readNumber("เวลามาตรฐาน (นาที)", 0.01, 1440));
            } while (confirm("เพิ่มอีกขั้นตอนหรือไม่"));
            if (confirm("บันทึกร่างหรือไม่"))
                sops.add(sop);
            else
                sop.destroy();
            return;
        }
        SOP sop = chooseSop();
        if (sop == null)
            return;
        if (action == 3 || action == 5) {
            if (action == 3 && !sop.getStatus().equals("ร่าง")) {
                System.out.println("เมนูนี้ไม่ใช่ SOP ฉบับร่าง");
                return;
            }
            if (action == 5 && !sop.getStatus().equals("เผยแพร่")) {
                System.out.println("เมนูนี้ยังไม่เผยแพร่");
                return;
            }
            showSop(sop);
            if (confirm("แก้ไขหรือไม่")) {
                if (isCooking(sop.getMenu())) {
                    System.out.println("ยังมีอาหารของเมนูนี้กำลังปรุง");
                    return;
                }
                String name = readRequired("ชื่อ SOP ใหม่");
                int step = readInt("ขั้นที่จะแก้ (0 เพิ่มขั้นตอน)", 0, sop.getSteps().size());
                String description = readRequired("คำอธิบาย");
                double minutes = readNumber("เวลามาตรฐาน (นาที)", 0.01, 1440);
                if (confirm("บันทึกหรือไม่")) {
                    sop.setName(name);
                    if (step == 0)
                        sop.addStep(description, minutes);
                    else
                        sop.getSteps().get(step - 1).update(description, minutes);
                }
            }
        } else if (action == 4)
            sop.publish();
        else if (action == 6) {
            if (sop.getStatus().equals("เผยแพร่")) {
                if (isCooking(sop.getMenu())) {
                    System.out.println("กำลังมีอาหารปรุงตามคู่มือนี้");
                    return;
                }
                sop.disable();
            } else if (sop.getStatus().equals("ปิดใช้"))
                sop.enable();
            else
                System.out.println("ฉบับร่างยังปิดใช้งานไม่ได้");
        } else if (action == 7) {
            if (!sop.isDeletable()) {
                System.out.println("ลบได้เฉพาะร่าง ให้ปิดใช้แทน");
                return;
            }
            if (confirm("ลบคู่มือและขั้นตอนทั้งหมดหรือไม่")) {
                sop.destroy();
                sops.remove(sop);
                return;
            }
        }
        showSop(sop);
    }

    static SOP chooseSop() {
        for (int i = 0; i < sops.size(); i++) {
            SOP sop = sops.get(i);
            System.out.println("[" + (i + 1) + "] " + sop.getName() + " - " + sop.getStatus() + " - "
                    + sop.getMenu().getStation());
        }
        int choice = readInt("เลือก SOP (0 กลับ)", 0, sops.size());
        if (choice == 0)
            return null;
        return sops.get(choice - 1);
    }

    static void showSop(SOP sop) {
        screen("รายละเอียดคู่มือขั้นตอนการปรุงอาหาร", "ผู้จัดการ / คนครัว");
        System.out.println(sop.getName() + " - " + sop.getStatus());
        for (int i = 0; i < sop.getSteps().size(); i++) {
            SOPStep step = sop.getSteps().get(i);
            System.out.println(
                    step.getNumber() + ". " + step.getDescription() + " - " + step.getStandardMinutes() + " นาที");
        }
        System.out.println("รวม " + sop.getTotalMinutes() + " นาที");
    }

    static boolean isCooking(Menu menu) {
        for (int i = 0; i < orders.size(); i++) {
            for (int j = 0; j < orders.get(i).getItems().size(); j++) {
                OrderItem item = orders.get(i).getItems().get(j);
                if (item.getMenu() == menu && item.getStatus().equals("กำลังปรุง"))
                    return true;
            }
        }
        return false;
    }

    // ---------- UC-03 ครัวและการเสิร์ฟ ----------
    static void uc03() {
        screen("ข้าวต้มอารมณ์ดี - ปรุงอาหารตาม SOP และงานเสิร์ฟ", "คนครัว - แคชเชียร์");
        System.out.println("คนครัวเลือกสถานี ดูคิว ปรุงตาม SOP และส่งอาหารไปเสิร์ฟ");
        line();
        System.out.println("[1] เลือกสถานีและดูคิวออเดอร์");
        System.out.println("[2] เริ่มปรุงอาหารตาม SOP");
        System.out.println("[3] บันทึกปรุงเสร็จและเทียบเวลา");
        System.out.println("[4] ดูรายการอาหารพร้อมเสิร์ฟ");
        System.out.println("[5] ยืนยันเสิร์ฟอาหารถึงโต๊ะ");
        System.out.println("[0] ย้อนกลับหน้าหลัก");
        int action = readInt("เลือกงานครัวและเสิร์ฟ", 0, 5);
        if (action == 0)
            return;
        String station = "";
        if (action <= 3) {
            station = chooseStation();
            cook.setStation(station);
            screen("จอครัว KDS - " + station, "คนครัว");
        } else
            screen("รายการอาหารพร้อมเสิร์ฟ", "แคชเชียร์");
        ArrayList<Order> queueOrders = new ArrayList<Order>();
        ArrayList<OrderItem> queueItems = new ArrayList<OrderItem>();
        for (int i = 0; i < orders.size(); i++) {
            Order order = orders.get(i);
            for (int j = 0; j < order.getItems().size(); j++) {
                OrderItem item = order.getItems().get(j);
                boolean matches = false;
                if (action == 1 && item.getMenu().getStation().equals(station)
                        && !item.getStatus().equals("ยกเลิก") && !item.getStatus().equals("เสิร์ฟแล้ว"))
                    matches = true;
                else if (action == 2 && item.getMenu().getStation().equals(station)
                        && item.getStatus().equals("รอปรุง"))
                    matches = true;
                else if (action == 3 && item.getMenu().getStation().equals(station)
                        && item.getStatus().equals("กำลังปรุง"))
                    matches = true;
                else if (action >= 4 && item.getStatus().equals("พร้อมเสิร์ฟ"))
                    matches = true;
                if (matches) {
                    queueOrders.add(order);
                    queueItems.add(item);
                    System.out.println(
                            "[" + queueItems.size() + "] " + order.getOrderId() + " - " + item.getMenu().getName()
                                    + " x" + item.getQuantity() + " - " + displayStatus(item.getStatus()));
                }
            }
        }
        if (queueItems.isEmpty())
            System.out.println("ไม่มีรายการในขั้นตอนนี้");
        if (action == 1 || action == 4)
            return;
        int choice = readInt("เลือกรายการครัว (0 กลับ)", 0, queueItems.size());
        if (choice == 0)
            return;
        Order order = queueOrders.get(choice - 1);
        OrderItem item = queueItems.get(choice - 1);
        System.out.println(
                "เผ็ด: " + item.getSpice() + " ตัวเลือก: " + item.getOptionNames() + " หมายเหตุ: " + item.getNote());
        if (action == 2) {
            SOP sop = findSop(item.getMenu());
            if (sop == null || !sop.getStatus().equals("เผยแพร่")) {
                System.out.println("ยังไม่มี SOP เผยแพร่ เริ่มปรุงไม่ได้");
                return;
            }
            showSop(sop);
            if (confirm("เริ่มปรุงหรือไม่"))
                item.startCooking(cook, sop.getTotalMinutes());
        } else if (action == 3) {
            if (confirm("ปรุงเสร็จแล้วหรือไม่")) {
                item.markReady();
                System.out.printf("ใช้จริง %.2f นาที / มาตรฐาน %.2f นาที%n", item.getCookingMinutes(),
                        item.getStandardMinutes());
                if (item.getCookingMinutes() > item.getStandardMinutes())
                    System.out.println("เกินเวลามาตรฐาน");
            }
        } else if (action == 5) {
            if (confirm("แคชเชียร์นำไปเสิร์ฟแล้วหรือไม่"))
                item.serve(cashier);
        }
        order.refreshStatus();
        showOrder(order);
    }

    static String chooseStation() {
        int choice = readInt("สถานี: 1 ครัวร้อน / 2 ครัวเย็น / 3 บาร์น้ำ", 1, 3);
        if (choice == 1)
            return "ครัวร้อน";
        if (choice == 2)
            return "ครัวเย็น";
        return "บาร์น้ำ";
    }

    // ---------- UC-04 ชำระเงิน ----------
    static void uc04() {
        screen("ข้าวต้มอารมณ์ดี - จุดชำระเงิน POS (Point of Sale)", "แคชเชียร์");
        System.out.println("เลือกโต๊ะรอชำระ ตรวจรายการ แลกแต้ม รับเงิน และออกใบเสร็จ");
        line();
        System.out.println("[1] เลือกออเดอร์ที่ต้องการชำระเงิน");
        System.out.println("[2] ตรวจสอบยอดรวมและสมาชิก");
        System.out.println("[3] ระบุแต้มที่ใช้แลกส่วนลด");
        System.out.println("[4] เลือกช่องทางชำระเงิน");
        System.out.println("[5] บันทึกการชำระและแต้ม");
        System.out.println("[6] แสดงใบเสร็จรับเงิน");
        System.out.println("[0] ย้อนกลับหน้าหลัก");
        if (readInt("เลือก 1 เพื่อเริ่มชำระเงิน", 0, 1) == 0)
            return;
        screen("เคาน์เตอร์แคชเชียร์: เรียกดูโต๊ะรอชำระเงิน", "แคชเชียร์");
        ArrayList<Order> unpaid = new ArrayList<Order>();
        for (int i = 0; i < orders.size(); i++) {
            Order order = orders.get(i);
            if (order.isServed() && order.getPayment() == null) {
                unpaid.add(order);
                System.out.printf("[%d] %s - โต๊ะ %s - %.2f บาท%n", unpaid.size(), order.getOrderId(),
                        order.getTable().getTableId(), order.calculateTotal());
            }
        }
        int choice = readInt("เลือกบิลรอชำระ (0 กลับ)", 0, unpaid.size());
        if (choice == 0)
            return;
        Order order = unpaid.get(choice - 1);
        screen("รายละเอียดบิลค่าอาหาร", "แคชเชียร์");
        showOrder(order);
        screen("ตรวจสอบสมาชิกเพื่อสะสมหรือแลกแต้ม", "แคชเชียร์");
        String phone = readText("เบอร์สมาชิก (Enter ใช้สมาชิกเดิมถ้ามี / 0 ไม่ผูกสมาชิก)");
        if (phone.equals("0"))
            order.getCustomer().setMember(null);
        else if (!phone.isEmpty()) {
            Member member = findMember(phone);
            if (member == null) {
                System.out.println("ไม่พบสมาชิก");
                return;
            }
            order.getCustomer().setMember(member);
        }
        int points = 0;
        if (order.getMember() != null) {
            showMember(order.getMember());
            points = readInt("ใช้กี่แต้ม (0 ไม่ใช้)", 0, order.getMember().getPoints());
        }
        Payment payment = new Payment(newPaymentId(), order, cashier);
        screen("เลือกช่องทางการชำระเงิน", "แคชเชียร์");
        int channel = readInt("1 เงินสด / 2 QR (จำลอง) / 0 ยกเลิก", 0, 2);
        if (channel == 0)
            return;
        if (channel == 1)
            payment.pay("เงินสด", readNumber("เงินที่รับ", 0, 10000000), points);
        else
            payment.pay("QR", 0, points);
        System.out.printf("สุทธิ %.2f / ส่วนลด %.2f / เงินทอน %.2f%n", payment.getNetAmount(), payment.getDiscount(),
                payment.getChange());
        if (confirm("ยืนยันการชำระหรือไม่")) {
            payment.confirm();
            releaseTable(order.getTable());
            printReceipt(payment);
        }
    }

    // โต๊ะจะว่างเมื่อไม่มีออเดอร์ค้างของโต๊ะนั้นแล้ว
    static void releaseTable(Table table) {
        for (int i = 0; i < orders.size(); i++) {
            Order order = orders.get(i);
            if (order.getTable() == table && order.getPayment() == null && !order.getStatus().equals("ยกเลิก"))
                return;
        }
        table.setStatus("ว่าง");
    }

    static void printReceipt(Payment payment) {
        screen("ใบเสร็จรับเงิน (Official Receipt) " + payment.getReceiptNo(), "แคชเชียร์");
        System.out.println(payment.getTime() + " - ผู้รับเงิน " + payment.getEmployee().getName());
        showOrder(payment.getOrder());
        System.out.printf("ส่วนลด %.2f / สุทธิ %.2f บาท%n", payment.getDiscount(), payment.getNetAmount());
        System.out.printf("ช่องทาง %s / รับ %.2f / ทอน %.2f%n", payment.getMethod(), payment.getReceived(),
                payment.getChange());
        System.out.println("ใช้ " + payment.getPointsToRedeem() + " แต้ม / ได้ " + payment.getEarnedPoints() + " แต้ม");
        System.out.println("แสดงใบเสร็จบนหน้าจอ (ไม่ได้เชื่อมเครื่องพิมพ์)");
    }

    // ---------- UC-05 สต็อกและสั่งซื้อ ----------
    static void uc05() {
        screen("ข้าวต้มอารมณ์ดี - คลังวัตถุดิบและจัดซื้อ (Inventory & Procurement)", "ผู้จัดการ");
        System.out.println("[1] ตรวจสอบคลังวัตถุดิบและแจ้งเตือนของใกล้หมด");
        System.out.println("[2] สร้างใบสั่งซื้อ PO");
        System.out.println("[3] ตรวจรับวัตถุดิบตาม PO");
        System.out.println("[4] ปรับยอดสต็อกจากการนับจริง");
        System.out.println("[5] เพิ่มวัตถุดิบใหม่");
        System.out.println("[6] แก้ข้อมูลวัตถุดิบและเกณฑ์ขั้นต่ำ");
        System.out.println("[7] ดูประวัติความเคลื่อนไหวสต็อก");
        System.out.println("[0] ย้อนกลับหน้าหลัก");
        int action = readInt("เลือกงานคลังวัตถุดิบ", 0, 7);
        if (action == 0)
            return;
        if (action == 1) {
            showStock();
            int low = 0;
            for (int i = 0; i < ingredients.size(); i++) {
                if (ingredients.get(i).getStockQty() < ingredients.get(i).getMinQty())
                    low++;
            }
            System.out.println("พบวัตถุดิบ " + low + " รายการต่ำกว่าจุดสั่งซื้อขั้นต่ำ");
        } else if (action == 2)
            createPurchaseOrder();
        else if (action == 3)
            receivePurchaseOrder();
        else if (action == 5) {
            String name = readRequired("ชื่อวัตถุดิบ");
            String unit = readRequired("หน่วย");
            double minimum = readNumber("ขั้นต่ำ", 0, 100000);
            Ingredient ingredient = new Ingredient(newId("ING"), name, unit, minimum);
            ingredients.add(ingredient);
            for (int i = 0; i < suppliers.size(); i++) {
                if (confirm("ให้ " + suppliers.get(i).getName() + " ส่งวัตถุดิบนี้หรือไม่"))
                    suppliers.get(i).addIngredient(ingredient);
            }
            System.out.println("เพิ่มแล้ว ยอดเริ่มต้น 0 รับเพิ่มผ่าน PO");
        } else {
            Ingredient ingredient = chooseIngredient();
            if (ingredient == null)
                return;
            if (action == 4) {
                double actual = readNumber("ยอดที่นับจริง", 0, 100000);
                String reason = readRequired("เหตุผล");
                if (confirm("ปรับยอดหรือไม่"))
                    ingredient.adjustStock(actual, reason, manager);
            } else if (action == 6) {
                String name = readRequired("ชื่อใหม่");
                String unit = readRequired("หน่วย");
                double minimum = readNumber("ขั้นต่ำ", 0, 100000);
                String reason = readRequired("เหตุผลการแก้ไข");
                if (confirm("บันทึกหรือไม่")) {
                    ingredient.update(name, unit, minimum);
                    System.out.println("บันทึกแล้ว: " + reason);
                }
            } else if (action == 7) {
                for (int i = 0; i < ingredient.getMovements().size(); i++) {
                    StockMovement movement = ingredient.getMovements().get(i);
                    String employee = "ระบบ";
                    if (movement.getEmployee() != null)
                        employee = movement.getEmployee().getName();
                    System.out.println(movement.getTime() + " - " + movement.getType() + " - " + movement.getQuantity()
                            + " - เหลือ " + movement.getBalance() + " - " + movement.getReference() + " - "
                            + movement.getReason() + " - " + employee);
                }
            }
        }
    }

    static void showStock() {
        screen("ตารางสต็อกวัตถุดิบคงคลัง", "ผู้จัดการ");
        System.out.println("รหัส - ชื่อวัตถุดิบ - คงเหลือ - ขั้นต่ำ - หน่วย - สถานะ");
        for (int i = 0; i < ingredients.size(); i++) {
            Ingredient ingredient = ingredients.get(i);
            String warning = "ปกติ";
            if (ingredient.getStockQty() < ingredient.getMinQty())
                warning = "ต่ำกว่าขั้นต่ำ";
            System.out.printf("[%d] %s - %s - %.3f - %.3f - %s - %s%n", i + 1, ingredient.getIngredientId(),
                    ingredient.getName(), ingredient.getStockQty(), ingredient.getMinQty(), ingredient.getUnit(),
                    warning);
        }
    }

    static void createPurchaseOrder() {
        screen("สร้างใบสั่งซื้อ (Purchase Order)", "ผู้จัดการ");
        for (int i = 0; i < suppliers.size(); i++)
            System.out.println((i + 1) + " " + suppliers.get(i).getName());
        int supplierChoice = readInt("เลือกผู้จำหน่าย (0 กลับ)", 0, suppliers.size());
        if (supplierChoice == 0)
            return;
        Supplier supplier = suppliers.get(supplierChoice - 1);
        PurchaseOrder po = new PurchaseOrder(newId("PO"), supplier, manager);
        boolean adding = true;
        while (adding) {
            Ingredient ingredient = chooseIngredient();
            if (ingredient == null)
                break;
            if (!supplier.supplies(ingredient))
                System.out.println("ผู้จำหน่ายรายนี้ไม่ส่งวัตถุดิบนี้");
            else
                po.addItem(ingredient, readNumber("จำนวนสั่ง", 0.001, 100000));
            adding = confirm("เพิ่มรายการอีกหรือไม่");
        }
        if (confirm("ยืนยันออก PO หรือไม่")) {
            po.markOrdered();
            purchaseOrders.add(po);
            System.out.println("ออกใบสั่งซื้อ " + po.getPoId());
        }
    }

    static void receivePurchaseOrder() {
        screen("ตรวจรับสินค้าจากใบสั่งซื้อ", "ผู้จัดการ");
        ArrayList<PurchaseOrder> waiting = new ArrayList<PurchaseOrder>();
        for (int i = 0; i < purchaseOrders.size(); i++) {
            PurchaseOrder po = purchaseOrders.get(i);
            if (po.getStatus().equals("สั่งแล้ว")) {
                waiting.add(po);
                System.out.println("[" + waiting.size() + "] " + po.getPoId() + " - " + po.getSupplier().getName());
            }
        }
        int choice = readInt("เลือก PO รับของ (0 กลับ)", 0, waiting.size());
        if (choice == 0)
            return;
        PurchaseOrder po = waiting.get(choice - 1);
        ArrayList<Double> actual = new ArrayList<Double>();
        for (int i = 0; i < po.getIngredients().size(); i++) {
            Ingredient ingredient = po.getIngredients().get(i);
            System.out.println(ingredient.getName() + " สั่ง " + po.getOrderedQty(i) + " " + ingredient.getUnit());
            actual.add(readNumber("จำนวนรับจริง", 0, 100000));
        }
        if (confirm("รับเข้าคลังหรือไม่")) {
            po.receive(actual);
            System.out.println("รับแล้ว " + po.getPoId());
        }
    }

    // ---------- UC-06 รายงาน: รวมจากออเดอร์ที่สร้างจริงระหว่างเปิดโปรแกรม
    // ----------
    static void uc06() {
        screen("ข้าวต้มอารมณ์ดี - แดชบอร์ดและรายงานวิเคราะห์ยอดขาย", "ผู้จัดการ");
        System.out.println("[1] ดูภาพรวมยอดขายวันนี้");
        System.out.println("[2] ดูรายงานยอดขายตามช่วงวันที่");
        System.out.println("[3] ดูประวัติออเดอร์และรายละเอียดบิล");
        System.out.println("[0] ย้อนกลับหน้าหลัก");
        int action = readInt("เลือกงานรายงาน", 0, 3);
        if (action == 0)
            return;
        LocalDate today = LocalDate.now();
        if (action == 1) {
            screen("ผู้จัดการ: แผงควบคุมภาพรวมร้าน", "ผู้จัดการ");
            System.out.println("วันที่ " + today);
            printSales(today, today);
            showStock();
        } else if (action == 2) {
            screen("รายงานยอดขายและอันดับเมนูอาหาร", "ผู้จัดการ");
            LocalDate start = readDate("วันเริ่มต้น");
            LocalDate end = readDate("วันสิ้นสุด");
            if (start.isAfter(end)) {
                System.out.println("วันเริ่มต้องไม่เกินวันสิ้นสุด");
                return;
            }
            printSales(start, end);
        } else {
            screen("ประวัติออเดอร์และสถานะบิล", "ผู้จัดการ");
            Order order = chooseOrder();
            if (order != null) {
                showOrder(order);
                if (order.getPayment() != null)
                    printReceipt(order.getPayment());
            }
        }
    }

    static void printSales(LocalDate start, LocalDate end) {
        double total = 0;
        double cash = 0;
        double qr = 0;
        int paid = 0;
        int created = 0;
        int cookingCount = 0;
        // แต่ละตำแหน่งตรงกับเมนูใน menus เก็บจำนวนจานที่ขายในช่วงวันที่
        int[] sold = new int[menus.size()];
        for (int i = 0; i < orders.size(); i++) {
            Order order = orders.get(i);
            LocalDate createdDate = order.getCreatedAt().toLocalDate();
            if (inRange(createdDate, start, end)) {
                created++;
                if (order.getStatus().equals("กำลังปรุง"))
                    cookingCount++;
            }
            Payment payment = order.getPayment();
            if (payment != null && inRange(payment.getTime().toLocalDate(), start, end)) {
                paid++;
                total += payment.getNetAmount();
                if (payment.getMethod().equals("เงินสด"))
                    cash += payment.getNetAmount();
                else
                    qr += payment.getNetAmount();
                System.out.printf("%s - %s - %.2f บาท%n", payment.getTime(), order.getOrderId(),
                        payment.getNetAmount());
                for (int j = 0; j < order.getItems().size(); j++) {
                    OrderItem item = order.getItems().get(j);
                    if (!item.getStatus().equals("ยกเลิก")) {
                        int index = menus.indexOf(item.getMenu());
                        if (index >= 0)
                            sold[index] += item.getQuantity();
                    }
                }
            }
        }
        System.out.println("ช่วง " + start + " ถึง " + end);
        System.out.println("ออเดอร์ที่สร้าง " + created + " / กำลังปรุง " + cookingCount + " / ชำระในช่วงนี้ " + paid);
        System.out.printf("ยอดสุทธิ %.2f - เงินสด %.2f - QR %.2f บาท%n", total, cash, qr);
        // เรียงดัชนีด้วยลูปพื้นฐาน เพื่อเก็บลำดับ menus จริงไว้ตามเดิม
        int[] indexes = new int[menus.size()];
        for (int i = 0; i < indexes.length; i++)
            indexes[i] = i;
        for (int i = 0; i < indexes.length; i++) {
            for (int j = i + 1; j < indexes.length; j++) {
                if (sold[indexes[j]] > sold[indexes[i]]) {
                    int temporary = indexes[i];
                    indexes[i] = indexes[j];
                    indexes[j] = temporary;
                }
            }
        }
        System.out.println("อันดับขายดี (จำนวนจาน)");
        for (int i = 0; i < indexes.length && i < 3; i++) {
            System.out.println((i + 1) + " " + menus.get(indexes[i]).getName() + " = " + sold[indexes[i]]);
        }
        System.out.println("อันดับขายต่ำ (จำนวนจาน)");
        for (int i = indexes.length - 1; i >= 0 && i >= indexes.length - 3; i--) {
            System.out.println(menus.get(indexes[i]).getName() + " = " + sold[indexes[i]]);
        }
    }

    static boolean inRange(LocalDate date, LocalDate start, LocalDate end) {
        return !date.isBefore(start) && !date.isAfter(end);
    }

    // ---------- UC-07 เมนูและสูตร ----------
    static void uc07() {
        screen("ข้าวต้มอารมณ์ดี - จัดการเมนูและสูตรอาหาร (Menu & Recipe Management)", "ผู้จัดการ");
        System.out.println("เพิ่มเมนู ผูกสูตร ตรวจสอบ SOP และควบคุมสถานะการขาย");
        line();
        System.out.println("[1] ดูรายการเมนูทั้งหมด");
        System.out.println("[2] เพิ่มเมนูอาหารใหม่");
        System.out.println("[3] กำหนดสูตรอาหารหรือสร้างเวอร์ชันใหม่");
        System.out.println("[4] เปิดขายเมนู");
        System.out.println("[5] แก้ไขข้อมูลเมนูหรือปิดขายชั่วคราว");
        System.out.println("[6] ปรับปรุงสูตรอาหารเดิมเป็นเวอร์ชันใหม่");
        System.out.println("[7] ลบเมนูที่ไม่มีประวัติสั่งซื้อ");
        System.out.println("[8] กำหนดตัวเลือกเพิ่มเติม");
        System.out.println("[0] ย้อนกลับหน้าหลัก");
        int action = readInt("เลือกงานเมนูและสูตร", 0, 8);
        if (action == 0)
            return;
        if (action == 1) {
            chooseMenu();
            return;
        }
        if (action == 2) {
            String name = readRequired("ชื่อเมนู");
            double price = readNumber("ราคา", 0.01, 100000);
            String category = readRequired("หมวด");
            Menu menu = new Menu(newId("MNU"), name, price, category, chooseStation());
            menu.setSpiceSelectable(confirm("ให้เลือกความเผ็ดหรือไม่"));
            menus.add(menu);
            System.out.println("สร้างแล้ว ยังปิดขายจนกว่าจะมีสูตรสมบูรณ์");
            return;
        }
        Menu menu = chooseMenu();
        if (menu == null)
            return;
        if (action == 3 || action == 6)
            manageRecipe(menu);
        else if (action == 4)
            menu.openSale();
        else if (action == 5) {
            int edit = readInt("1 แก้ข้อมูล / 2 ปิดขายชั่วคราว", 1, 2);
            if (edit == 1) {
                String name = readRequired("ชื่อเมนูใหม่");
                double price = readNumber("ราคา", 0.01, 100000);
                String category = readRequired("หมวด");
                String station = chooseStation();
                if (confirm("บันทึกหรือไม่"))
                    menu.update(name, price, category, station);
            } else
                menu.closeSale();
        } else if (action == 7) {
            if (!menu.isDeletable()) {
                System.out.println("เคยยืนยันสั่งเมนูนี้แล้ว ให้ปิดขายแทน");
                return;
            }
            if (confirm("ลบเมนูและสูตรทั้งหมดหรือไม่")) {
                SOP sop = findSop(menu);
                if (sop != null) {
                    sop.destroy();
                    sops.remove(sop);
                }
                menu.destroy();
                menus.remove(menu);
            }
        } else if (action == 8) {
            String name = readRequired("ชื่อตัวเลือก เช่น เพิ่มไข่ดาว");
            double price = readNumber("ราคาเพิ่มต่อจาน", 0, 100000);
            menu.addOption(name, price);
            int index = menu.getOptionNames().size() - 1;
            while (confirm("ตัวเลือกนี้ใช้วัตถุดิบเพิ่มหรือไม่")) {
                Ingredient ingredient = chooseIngredient();
                if (ingredient == null)
                    break;
                menu.addOptionIngredient(index, ingredient, readNumber("ปริมาณเพิ่มต่อจาน", 0.001, 1000));
            }
        }
    }

    static void manageRecipe(Menu menu) {
        screen("กำหนดสูตรอาหาร (Recipe Definition) - " + menu.getName(), "ผู้จัดการ");
        for (int i = 0; i < menu.getRecipes().size(); i++) {
            Recipe recipe = menu.getRecipes().get(i);
            System.out.println("[" + (i + 1) + "] สูตร v" + recipe.getVersion() + " - " + recipe.getStatus());
        }
        int choice = readInt("เลือกสูตร (0 สร้างใหม่ / คัดลอกฉบับสมบูรณ์ล่าสุด)", 0, menu.getRecipes().size());
        Recipe recipe;
        if (choice == 0) {
            Recipe current = menu.getCurrentRecipe();
            int version = 1;
            for (int i = 0; i < menu.getRecipes().size(); i++) {
                if (menu.getRecipes().get(i).getVersion() >= version)
                    version = menu.getRecipes().get(i).getVersion() + 1;
            }
            recipe = new Recipe(newId("RCP"), version);
            if (current != null) {
                for (int i = 0; i < current.getIngredients().size(); i++) {
                    recipe.addIngredient(current.getIngredients().get(i), current.getQuantity(i));
                }
            }
            menu.addRecipe(recipe);
        } else
            recipe = menu.getRecipes().get(choice - 1);
        for (int i = 0; i < recipe.getIngredients().size(); i++) {
            System.out
                    .println((i + 1) + " " + recipe.getIngredients().get(i).getName() + " = " + recipe.getQuantity(i));
        }
        if (!recipe.getStatus().equals("ร่าง")) {
            System.out.println("ฉบับสมบูรณ์แก้ตรง ๆ ไม่ได้ ให้เลือก 0 สร้างเวอร์ชันใหม่");
            return;
        }
        int action = readInt("1 เพิ่มวัตถุดิบ / 2 แก้ปริมาณ / 3 ยืนยันสมบูรณ์ / 0 เก็บร่าง", 0, 3);
        if (action == 1) {
            do {
                Ingredient ingredient = chooseIngredient();
                if (ingredient == null)
                    break;
                recipe.addIngredient(ingredient, readNumber("ปริมาณต่อจาน", 0.001, 1000));
            } while (confirm("เพิ่มอีกหรือไม่"));
            if (confirm("ยืนยันสูตรสมบูรณ์หรือไม่"))
                recipe.complete();
        } else if (action == 2) {
            int index = readInt("วัตถุดิบลำดับที่ (0 กลับ)", 0, recipe.getIngredients().size());
            if (index == 0)
                return;
            recipe.changeQuantity(index - 1, readNumber("ปริมาณใหม่ต่อจาน", 0.001, 1000));
            if (confirm("ยืนยันสูตรสมบูรณ์หรือไม่"))
                recipe.complete();
        } else if (action == 3)
            recipe.complete();
    }

    // ---------- UC-08 สมาชิก แต้ม และคำขอที่ผู้จัดการพิจารณา ----------
    static void uc08() {
        screen("ข้าวต้มอารมณ์ดี - สมาชิกและระบบสะสมแต้ม (Loyalty Program)", "แคชเชียร์ - ผู้จัดการ");
        System.out.println("กฎ: ทุก " + Member.getBahtPerPoint() + " บาท = 1 แต้ม - 1 แต้ม = " + Member.getPointValue()
                + " บาท - ขั้นต่ำ " + Member.getMinRedeem());
        System.out.println("[1] ค้นหาหรือสมัครสมาชิกใหม่");
        System.out.println("[2] จำลองการสะสมและแลกแต้มที่หน้าชำระเงิน");
        System.out.println("[3] ดูประวัติความเคลื่อนไหวแต้ม");
        System.out.println("[4] แก้ไขข้อมูลสมาชิก");
        System.out.println("[5] ผู้จัดการดูรายชื่อและกำหนดกฎแต้ม");
        System.out.println("[6] ผู้จัดการพิจารณาคำขออาหาร");
        System.out.println("[0] ย้อนกลับหน้าหลัก");
        int action = readInt("เลือกงานสมาชิก", 0, 6);
        if (action == 0)
            return;
        if (action == 1) {
            screen("เคาน์เตอร์แคชเชียร์: ค้นหาหรือสมัครสมาชิกใหม่", "แคชเชียร์");
            String phone = readRequired("เบอร์โทร 10 หลัก");
            Member existing = findMember(phone);
            if (existing != null) {
                showMember(existing);
                return;
            }
            Member member = new Member(newId("MBR"), readRequired("ชื่อสมาชิก"), phone);
            if (confirm("ยืนยันสมัครสมาชิกหรือไม่")) {
                members.add(member);
                System.out.println("สมัครสมาชิกสำเร็จ");
                showMember(member);
            }
        } else if (action == 2) {
            screen("จำลองการสะสมและแลกแต้มที่หน้าชำระเงิน", "แคชเชียร์");
            Member member = findMember(readRequired("เบอร์โทร"));
            if (member == null) {
                System.out.println("ไม่พบสมาชิก");
                return;
            }
            showMember(member);
            double amount = readNumber("ยอดสุทธิของบิล (บาท)", 0, 10000000);
            int earned = (int) (amount / Member.getBahtPerPoint());
            System.out.println(
                    "คำนวณแต้มสะสม: " + amount + " / " + Member.getBahtPerPoint() + " (ปัดลง) = +" + earned + " แต้ม");
            int points = readInt("จำนวนแต้มที่ใช้แลก (0 = ไม่ใช้)", 0, member.getPoints());
            if (points > 0) {
                if (points < Member.getMinRedeem())
                    System.out.println("ต้องแลกอย่างน้อย " + Member.getMinRedeem() + " แต้ม");
                else if (points * Member.getPointValue() > amount)
                    System.out.println("ส่วนลดเกินยอดบิล");
                else
                    System.out.printf("ส่วนลด: %.2f บาท - หักแต้มเมื่อชำระเงินจริง%n", points * Member.getPointValue());
            }
            System.out.println("นี่เป็นตัวอย่างคำนวณ - จ่ายเงินจริงที่เมนู 4 ชำระเงิน");
        } else if (action == 3) {
            screen("ตรวจสอบประวัติและสถิติแต้มสมาชิก", "แคชเชียร์");
            Member member = findMember(readRequired("เบอร์โทร"));
            if (member == null) {
                System.out.println("ไม่พบสมาชิก");
                return;
            }
            showMember(member);
            for (int i = 0; i < member.getTransactions().size(); i++) {
                PointTransaction transaction = member.getTransactions().get(i);
                String reference = "ยอดเริ่มต้น";
                if (transaction.getPayment() != null)
                    reference = transaction.getPayment().getReceiptNo();
                System.out.println(transaction.getTime() + " - " + transaction.getType() + " " + transaction.getPoints()
                        + " - เหลือ " + transaction.getBalance() + " - " + reference);
            }
        } else if (action == 4) {
            screen("แก้ไขข้อมูลสมาชิก", "แคชเชียร์");
            Member member = findMember(readRequired("เบอร์โทร"));
            if (member == null) {
                System.out.println("ไม่พบสมาชิก");
                return;
            }
            showMember(member);
            String name = readRequired("ชื่อใหม่");
            String phone = readRequired("เบอร์ใหม่");
            Member duplicate = findMember(phone);
            if (duplicate != null && duplicate != member) {
                System.out.println("เบอร์ซ้ำ");
                return;
            }
            if (confirm("บันทึกข้อมูลสมาชิกหรือไม่")) {
                member.setPhone(phone);
                member.setName(name);
                System.out.println("แก้ข้อมูลแล้ว");
            }
        } else if (action == 5) {
            screen("รายชื่อสมาชิกทั้งหมดในระบบ", "ผู้จัดการ");
            for (int i = 0; i < members.size(); i++)
                showMember(members.get(i));
            if (confirm("กำหนดนโยบายแต้มใหม่หรือไม่")) {
                screen("ผู้จัดการ: กำหนดเงื่อนไขและนโยบายแต้มสะสมทั้งร้าน", "ผู้จัดการ");
                int baht = readInt("บาทต่อ 1 แต้ม", 1, 100000);
                double value = readNumber("มูลค่า 1 แต้ม", 0.01, 10000);
                int minimum = readInt("แต้มขั้นต่ำ", 1, 100000);
                Member.setRule(baht, value, minimum);
                System.out.println("เปลี่ยนกฎสำหรับการชำระครั้งต่อไปแล้ว");
            }
        } else if (action == 6)
            approveRequests();
    }

    static void showMember(Member member) {
        System.out.println(member.getMemberId() + " - " + member.getName() + " - " + member.getPhone() + " - "
                + member.getPoints() + " แต้ม");
    }

    static void approveRequests() {
        screen("การพิจารณาคำขอแก้ไขหรือยกเลิกรายการ", "ผู้จัดการ");
        for (int i = 0; i < orders.size(); i++) {
            Order order = orders.get(i);
            for (int j = 0; j < order.getItems().size(); j++) {
                OrderItem item = order.getItems().get(j);
                if (item.getRequestStatus().equals("รออนุมัติ")) {
                    System.out.println(order.getOrderId() + " - " + item.getMenu().getName() + " - ขอ"
                            + item.getRequestType() + " - " + item.getRequestReason());
                    int decision = readInt("1 อนุมัติ / 2 ปฏิเสธ / 0 ข้าม", 0, 2);
                    if (decision != 0) {
                        item.decideRequest(decision == 1, readRequired("เหตุผลการตัดสินใจ"), manager);
                        order.refreshStatus();
                        releaseTable(order.getTable());
                    }
                }
            }
        }
    }
}
