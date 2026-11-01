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
        customer.linkMember(member);
        Order order = new Order("O1", table, customer);
        OrderItem item = order.addItem(menu, 2, "mild", "note");
        item.addOption(0);
        order.confirm();
        near(fish.stockQty(), 8, "Stock deducted");
        near(egg.stockQty(), 8, "Option stock deducted");
        order.changeQuantity(0, 3);
        near(fish.stockQty(), 7, "Increase quantity deducts difference");
        order.changeQuantity(0, 2);
        near(egg.stockQty(), 8, "Decrease quantity restores difference");
        // การแก้ราคาเมนูและสูตรใหม่ต้องไม่เปลี่ยนราคา/สูตรของบิลเดิม
        menu.update("Food", 200, "Food", "ครัวร้อน");
        Recipe next = recipe.createNewVersion("R2");
        next.changeQuantity(0, 2);
        next.complete();
        menu.addRecipe(next);
        near(order.calculateTotal(), 220, "Order price snapshot");
        check(item.recipe() == recipe, "Old order keeps recipe version");
        check(menu.currentRecipe() == next, "New order uses latest recipe");
        item.startCooking(cook, sop.getTotalMinutes());
        item.markReady();
        item.serve(cashier);
        order.refreshStatus();
        check(order.isServed(), "Served order");
        Payment payment = new Payment("P1", order, cashier);
        payment.pay("เงินสด", 300, 10);
        near(payment.netAmount(), 210, "Net payment");
        near(payment.change(), 90, "Change");
        payment.confirm();
        check(member.points() == 14, "Redeem 10 then earn 4");
        check(payment.printReceipt().contains(payment.receiptNo()), "P7 receipt uses saved receipt number");
        near(payment.calculateChange(), 90, "P7 change calculation");
        boolean rejected = false;
        try { payment.confirm(); } catch (IllegalStateException e) { rejected = true; }
        check(rejected && member.points() == 14, "Repeated confirmation blocked");
        Payment duplicate = new Payment("P2", order, cashier);
        rejected = false;
        try { duplicate.pay("QR", 0, 0); } catch (IllegalStateException e) { rejected = true; }
        check(rejected, "Duplicate payment blocked");

        // สต็อกต้องตรวจรวมทุกจานก่อนตัด เมื่อไม่พอต้องไม่เปลี่ยนยอดใด ๆ
        Order tooLarge = new Order("O2", table, new Customer("C2"));
        tooLarge.addItem(menu, 3, "", "");
        tooLarge.addItem(menu, 3, "", "");
        double before = fish.stockQty();
        rejected = false;
        try { tooLarge.confirm(); } catch (IllegalArgumentException e) { rejected = true; }
        check(rejected, "Insufficient aggregate stock rejected");
        near(fish.stockQty(), before, "Failed order leaves stock intact");
        Order cart = new Order("O3", table, new Customer("C3"));
        cart.addItem(menu, 1, "", "");
        cart.cancelItem(0);
        near(fish.stockQty(), before, "Unconfirmed cancellation does not restore stock");
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
        near(fish.stockQty(), before - 2, "Approved cancellation restores one dish");
        remaining.startCooking(cook, 5);
        remaining.markReady();
        remaining.serve(cashier);
        cancelOrder.refreshStatus();
        check(cancelOrder.isServed(), "Cancelled items do not prevent checkout");
        Payment qr = new Payment("P3", cancelOrder, cashier);
        qr.pay("QR", 0, 0);
        qr.confirm();
        near(qr.received(), 200, "QR receives exact net amount");

        Supplier supplier = new Supplier("SUP1", "Supplier");
        supplier.addIngredient(fish);
        PurchaseOrder po = new PurchaseOrder("PO1", supplier, manager);
        po.addItem(fish, 5);
        po.markOrdered();
        ArrayList<Double> actual = new ArrayList<Double>();
        actual.add(-1.0);
        before = fish.stockQty();
        rejected = false;
        try { po.receive(actual); } catch (IllegalArgumentException e) { rejected = true; }
        check(rejected, "Negative receipt rejected");
        near(fish.stockQty(), before, "Failed receipt leaves stock intact");
        actual.set(0, 4.0);
        po.receive(actual);
        near(fish.stockQty(), before + 4, "Actual PO receipt");
        check(po.ingredients().get(0) == fish, "PO keeps ingredient order");
        near(po.orderedQty(0), 5, "PO pairs ingredient with ordered quantity");
        check(supplier.supplies(fish), "P7 supplier checks supplied ingredient");
        check(recipe.ingredients().get(0) == fish, "Recipe keeps ingredient order");
        near(recipe.quantity(0), 1, "Recipe pairs ingredient with quantity");
        Recipe listRecipe = new Recipe("R-LIST", 1);
        listRecipe.addItem(fish, 0.5);
        listRecipe.addItem(egg, 1);
        listRecipe.addItem(fish, 0.25);
        check(listRecipe.ingredients().size() == 2, "Repeated ingredient keeps one list position");
        near(listRecipe.quantity(0), 0.75, "Repeated ingredient updates matching quantity");
        menu.addOption("Egg", 12);
        check(menu.optionNames().size() == 1, "Repeated option keeps one list position");
        near(menu.optionPrice(0), 12, "Repeated option updates matching price");
        supplier.addIngredient(egg);
        PurchaseOrder listPo = new PurchaseOrder("PO-LIST", supplier, manager);
        listPo.addItem(fish, 1);
        listPo.addItem(egg, 2);
        listPo.addItem(fish, 0.5);
        near(listPo.orderedQty(0), 1.5, "Repeated PO ingredient updates matching quantity");
        listPo.markOrdered();
        ArrayList<Double> invalidReceipt = new ArrayList<Double>();
        invalidReceipt.add(1.0);
        invalidReceipt.add(-1.0);
        double fishBeforeInvalid = fish.stockQty();
        rejected = false;
        try { listPo.receive(invalidReceipt); } catch (IllegalArgumentException e) { rejected = true; }
        check(rejected, "Invalid second receipt line rejected");
        near(fish.stockQty(), fishBeforeInvalid, "Invalid receipt leaves first ingredient unchanged");
        invalidReceipt.set(1, 2.0);
        listPo.receive(invalidReceipt);
        near(fish.stockQty(), fishBeforeInvalid + 1, "List PO receives first ingredient");
        near(listPo.receivedQty(1), 2, "List PO keeps second received quantity");
        check(Member.validateRedeem(10, 20), "P7 point rule validation");
        check(!Member.validateRedeem(9, 20), "P7 point minimum validation");
        PointTransaction pointEntry = new PointTransaction("PT1", PointTransaction.PointType.EARN, 2, 2);
        check(pointEntry.typeText().equals("สะสม"), "P7 point transaction enum");
        Order newCart = new Order("O5", table);
        newCart.attachMember(new Member("MB2", "Another", "0899999999"));
        check(newCart.linkedMember() != null, "P7 order attaches member");
        OrderItem newCartItem = newCart.addItem(menu, 1, "", "");
        newCart.removeItem(newCartItem);
        check(newCart.items().isEmpty(), "P7 order removes item object");
        rejected = false;
        try { po.receive(actual); } catch (IllegalStateException e) { rejected = true; }
        check(rejected, "Repeated receipt blocked");

        // ตรวจ Composition ทั้งห้าคู่: เก็บลูกไว้ แล้วลบแม่เพื่อตรวจว่าลูกถูกทำลายตาม
        OrderItem child = order.items().get(0);
        order.destroy();
        check(child.isDestroyed() && order.items().isEmpty(), "Order -> OrderItem");
        SOPStep step = sop.steps().get(0);
        sop.destroy();
        check(step.isDestroyed() && sop.steps().isEmpty(), "SOP -> SOPStep");
        PointTransaction transaction = member.transactions().get(0);
        member.destroy();
        check(transaction.isDestroyed() && member.transactions().isEmpty(), "Member -> PointTransaction");
        StockMovement movement = fish.movements().get(0);
        fish.destroy();
        check(movement.isDestroyed() && fish.movements().isEmpty(), "Ingredient -> StockMovement");
        menu.destroy();
        check(recipe.isDestroyed() && next.isDestroyed() && menu.recipes().isEmpty(), "Menu -> Recipe");
        System.out.println("PASS: " + checks + " domain checks");
    }
}
