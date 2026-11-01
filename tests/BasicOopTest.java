import java.util.ArrayList;
import model.*;

// ทดสอบกฎที่มีโอกาสผิดจากการเขียนใหม่ รันด้วย tests/run_tests.py
public class BasicOopTest {
    static int checks = 0;

    static void check(boolean condition, String message) {
        checks++;
        if (!condition) throw new AssertionError(message);
    }

    static void near(double actual, double expected, String message) {
        check(Math.abs(actual - expected) < 0.00001, message + ": " + actual);
    }

    public static void main(String[] args) {
        Employee manager = new Employee("E1", "Manager", "ผู้จัดการ");
        Employee cook = new Employee("E2", "Cook", "คนครัว");
        Employee cashier = new Employee("E3", "Cashier", "แคชเชียร์");
        Ingredient fish = new Ingredient("I1", "Fish", "kg", 1);
        Ingredient egg = new Ingredient("I2", "Egg", "piece", 2);
        fish.receive(10, "OPEN", manager);
        egg.receive(10, "OPEN", manager);
        Menu menu = new Menu("M1", "Food", 100, "Food", "ครัวร้อน");
        Recipe recipe = new Recipe("R1", 1);
        recipe.addIngredient(fish, 1);
        recipe.complete();
        menu.addRecipe(recipe);
        menu.addOption("Egg", 10);
        menu.addOptionIngredient(0, egg, 1);
        menu.openSale();
        SOP sop = new SOP("S1", "Cook food", menu);
        sop.addStep("Prepare", 2);
        sop.addStep("Cook", 3);
        sop.publish();
        near(sop.getTotalMinutes(), 5, "SOP duration");

        Table table = new Table("T1", "QR1", 4);
        Customer customer = new Customer("C1");
        Member member = new Member("MB1", "Member", "0812345678");
        member.earnPoints(1000, null);
        customer.setMember(member);
        Order order = new Order("O1", table, customer);
        OrderItem item = order.addItem(menu, 2, "mild", "note");
        item.addOption(0);
        order.confirm();
        near(fish.getStockQty(), 8, "Stock deducted");
        near(egg.getStockQty(), 8, "Option stock deducted");
        order.changeQuantity(0, 3);
        near(fish.getStockQty(), 7, "Increase quantity deducts difference");
        order.changeQuantity(0, 2);
        near(egg.getStockQty(), 8, "Decrease quantity restores difference");
        // การแก้ราคาเมนูและสูตรใหม่ต้องไม่เปลี่ยนราคา/สูตรของบิลเดิม
        menu.update("Food", 200, "Food", "ครัวร้อน");
        Recipe next = recipe.createNewVersion("R2");
        next.changeQuantity(0, 2);
        next.complete();
        menu.addRecipe(next);
        near(order.calculateTotal(), 220, "Order price snapshot");
        check(item.getRecipe() == recipe, "Old order keeps recipe version");
        check(menu.getCurrentRecipe() == next, "New order uses latest recipe");
        item.startCooking(cook, sop.getTotalMinutes());
        item.markReady();
        item.serve(cashier);
        order.refreshStatus();
        check(order.isServed(), "Served order");
        Payment payment = new Payment("P1", order, cashier);
        payment.pay("เงินสด", 300, 10);
        near(payment.getNetAmount(), 210, "Net payment");
        near(payment.getChange(), 90, "Change");
        payment.confirm();
        check(member.getPoints() == 14, "Redeem 10 then earn 4");
        boolean rejected = false;
        try { payment.confirm(); } catch (IllegalStateException e) { rejected = true; }
        check(rejected && member.getPoints() == 14, "Repeated confirmation blocked");
        Payment duplicate = new Payment("P2", order, cashier);
        rejected = false;
        try { duplicate.pay("QR", 0, 0); } catch (IllegalStateException e) { rejected = true; }
        check(rejected, "Duplicate payment blocked");

        // สต็อกต้องตรวจรวมทุกจานก่อนตัด เมื่อไม่พอต้องไม่เปลี่ยนยอดใด ๆ
        Order tooLarge = new Order("O2", table, new Customer("C2"));
        tooLarge.addItem(menu, 3, "", "");
        tooLarge.addItem(menu, 3, "", "");
        double before = fish.getStockQty();
        rejected = false;
        try { tooLarge.confirm(); } catch (IllegalArgumentException e) { rejected = true; }
        check(rejected, "Insufficient aggregate stock rejected");
        near(fish.getStockQty(), before, "Failed order leaves stock intact");
        Order cart = new Order("O3", table, new Customer("C3"));
        cart.addItem(menu, 1, "", "");
        cart.cancelItem(0);
        near(fish.getStockQty(), before, "Unconfirmed cancellation does not restore stock");
        cart.destroy();

        Order cancelOrder = new Order("O4", table, new Customer("C4"));
        OrderItem cancelItem = cancelOrder.addItem(menu, 1, "", "");
        OrderItem remaining = cancelOrder.addItem(menu, 1, "", "");
        cancelOrder.confirm();
        cancelItem.startCooking(cook, 5);
        cancelItem.requestChange("ยกเลิก", "Waiting too long", "");
        rejected = false;
        try { cancelItem.markReady(); } catch (IllegalStateException e) { rejected = true; }
        check(rejected, "Pending cancellation must be decided before ready");
        cancelItem.decideRequest(true, "Approved", manager);
        cancelOrder.refreshStatus();
        near(fish.getStockQty(), before - 2, "Approved cancellation restores one dish");
        remaining.startCooking(cook, 5);
        remaining.markReady();
        remaining.serve(cashier);
        cancelOrder.refreshStatus();
        check(cancelOrder.isServed(), "Cancelled items do not prevent checkout");
        Payment qr = new Payment("P3", cancelOrder, cashier);
        qr.pay("QR", 0, 0);
        qr.confirm();
        near(qr.getReceived(), 200, "QR receives exact net amount");

        Supplier supplier = new Supplier("SUP1", "Supplier");
        supplier.addIngredient(fish);
        PurchaseOrder po = new PurchaseOrder("PO1", supplier, manager);
        po.addItem(fish, 5);
        po.markOrdered();
        ArrayList<Double> actual = new ArrayList<Double>();
        actual.add(-1.0);
        before = fish.getStockQty();
        rejected = false;
        try { po.receive(actual); } catch (IllegalArgumentException e) { rejected = true; }
        check(rejected, "Negative receipt rejected");
        near(fish.getStockQty(), before, "Failed receipt leaves stock intact");
        actual.set(0, 4.0);
        po.receive(actual);
        near(fish.getStockQty(), before + 4, "Actual PO receipt");
        rejected = false;
        try { po.receive(actual); } catch (IllegalStateException e) { rejected = true; }
        check(rejected, "Repeated receipt blocked");

        // ตรวจ Composition ทั้งห้าคู่: เก็บลูกไว้ แล้วลบแม่เพื่อตรวจว่าลูกถูกทำลายตาม
        OrderItem child = order.getItems().get(0);
        order.destroy();
        check(child.isDestroyed() && order.getItems().isEmpty(), "Order -> OrderItem");
        SOPStep step = sop.getSteps().get(0);
        sop.destroy();
        check(step.isDestroyed() && sop.getSteps().isEmpty(), "SOP -> SOPStep");
        PointTransaction transaction = member.getTransactions().get(0);
        member.destroy();
        check(transaction.isDestroyed() && member.getTransactions().isEmpty(), "Member -> PointTransaction");
        StockMovement movement = fish.getMovements().get(0);
        fish.destroy();
        check(movement.isDestroyed() && fish.getMovements().isEmpty(), "Ingredient -> StockMovement");
        menu.destroy();
        check(recipe.isDestroyed() && next.isDestroyed() && menu.getRecipes().isEmpty(), "Menu -> Recipe");
        System.out.println("PASS: " + checks + " domain checks");
    }
}
