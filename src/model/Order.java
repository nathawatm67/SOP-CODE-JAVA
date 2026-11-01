package model;

import java.time.LocalDateTime;
import java.util.ArrayList;

// ออเดอร์เป็นเจ้าของ OrderItem และอ้างถึงโต๊ะ ลูกค้า และการชำระเงิน
public class Order {
    private String orderId;
    private Table table;
    private Customer customer;
    private Payment payment;
    private String status;
    private LocalDateTime createdAt;
    private ArrayList<OrderItem> items;
    private int itemNumber;
    private boolean destroyed;

    public Order(String id, Table table, Customer customer) {
        this.orderId = id;
        this.table = table;
        this.customer = customer;
        this.status = "ตะกร้า";
        this.createdAt = LocalDateTime.now();
        this.items = new ArrayList<OrderItem>();
    }

    public OrderItem addItem(Menu menu, int quantity, String spice, String note) {
        if (!status.equals("ตะกร้า"))
            throw new IllegalStateException("เพิ่มอาหารได้เฉพาะในตะกร้า");
        if (!menu.getStatus().equals("เปิดขาย"))
            throw new IllegalArgumentException("เมนูปิดขาย");
        itemNumber++;
        OrderItem item = new OrderItem(orderId + "-ITEM-" + itemNumber, menu, quantity, spice, note);
        items.add(item);
        return item;
    }

    public void removeItem(int index) {
        if (!status.equals("ตะกร้า"))
            throw new IllegalStateException("ลบได้เฉพาะตะกร้า");
        items.get(index).destroy();
        items.remove(index);
    }

    public double calculateTotal() {
        double total = 0;
        for (int i = 0; i < items.size(); i++) {
            if (!items.get(i).getStatus().equals("ยกเลิก"))
                total += items.get(i).getPrice();
        }
        return total;
    }

    // รวบรวมชื่อวัตถุดิบโดยไม่ซ้ำ เพื่อให้ตรวจยอดรวมของหลายจานได้
    private ArrayList<Ingredient> allIngredients() {
        ArrayList<Ingredient> result = new ArrayList<Ingredient>();
        for (int i = 0; i < items.size(); i++) {
            OrderItem item = items.get(i);
            if (!item.getStatus().equals("ยกเลิก")) {
                for (int j = 0; j < item.getIngredients().size(); j++) {
                    Ingredient ingredient = item.getIngredients().get(j);
                    if (!result.contains(ingredient))
                        result.add(ingredient);
                }
            }
        }
        return result;
    }

    private double requiredQuantity(Ingredient ingredient) {
        double total = 0;
        for (int i = 0; i < items.size(); i++) {
            OrderItem item = items.get(i);
            if (!item.getStatus().equals("ยกเลิก")) {
                total += item.amountPerDish(ingredient) * item.getQuantity();
            }
        }
        return total;
    }

    public void confirm() {
        if (!status.equals("ตะกร้า") || items.isEmpty())
            throw new IllegalStateException("ตะกร้าต้องมีอาหารและยังไม่ยืนยัน");
        ArrayList<Ingredient> ingredients = allIngredients();
        // ตรวจให้ครบทุกชนิดก่อน แล้วค่อยตัด
        // เพื่อไม่ให้ตัดไปครึ่งหนึ่งแล้วพบว่าอีกชนิดไม่พอ
        for (int i = 0; i < ingredients.size(); i++) {
            Ingredient ingredient = ingredients.get(i);
            if (!ingredient.hasEnough(requiredQuantity(ingredient))) {
                throw new IllegalArgumentException("วัตถุดิบไม่พอ: " + ingredient.getName());
            }
        }
        for (int i = 0; i < ingredients.size(); i++) {
            Ingredient ingredient = ingredients.get(i);
            ingredient.deduct(requiredQuantity(ingredient), orderId);
        }
        for (int i = 0; i < items.size(); i++)
            items.get(i).markConfirmed();
        status = "ยืนยันแล้ว";
        table.setStatus("ใช้งาน");
    }

    public void changeQuantity(int index, int newQuantity) {
        OrderItem item = items.get(index);
        if (newQuantity <= 0 || !item.getStatus().equals("รอปรุง") || payment != null) {
            throw new IllegalArgumentException("แก้ได้เฉพาะรายการรอปรุงที่ยังไม่ชำระ และจำนวนต้องมากกว่า 0");
        }
        if (status.equals("ตะกร้า")) {
            item.changeQuantity(newQuantity);
            return;
        }
        int difference = newQuantity - item.getQuantity();
        ArrayList<Ingredient> ingredients = allIngredients();
        if (difference > 0) {
            for (int i = 0; i < ingredients.size(); i++) {
                Ingredient ingredient = ingredients.get(i);
                if (!ingredient.hasEnough(item.amountPerDish(ingredient) * difference)) {
                    throw new IllegalArgumentException("วัตถุดิบไม่พอ: " + ingredient.getName());
                }
            }
        }
        for (int i = 0; i < ingredients.size(); i++) {
            Ingredient ingredient = ingredients.get(i);
            double change = item.amountPerDish(ingredient) * difference;
            if (change > 0)
                ingredient.deduct(change, orderId);
            else if (change < 0)
                ingredient.restore(-change, orderId);
        }
        item.changeQuantity(newQuantity);
    }

    public void cancelItem(int index) {
        if (payment != null)
            throw new IllegalStateException("ชำระแล้ว แก้รายการไม่ได้");
        items.get(index).cancel();
        refreshStatus();
    }

    public boolean isServed() {
        boolean hasFood = false;
        for (int i = 0; i < items.size(); i++) {
            String itemStatus = items.get(i).getStatus();
            if (!itemStatus.equals("ยกเลิก")) {
                hasFood = true;
                if (!itemStatus.equals("เสิร์ฟแล้ว"))
                    return false;
            }
        }
        return hasFood;
    }

    // สถานะออเดอร์สรุปจากอาหารที่ยังไม่ยกเลิกทั้งหมด
    public void refreshStatus() {
        if (status.equals("ตะกร้า") || status.equals("ชำระแล้ว"))
            return;
        int active = 0;
        int ready = 0;
        int served = 0;
        boolean cooking = false;
        for (int i = 0; i < items.size(); i++) {
            String value = items.get(i).getStatus();
            if (!value.equals("ยกเลิก"))
                active++;
            if (value.equals("กำลังปรุง"))
                cooking = true;
            if (value.equals("พร้อมเสิร์ฟ"))
                ready++;
            if (value.equals("เสิร์ฟแล้ว"))
                served++;
        }
        if (active == 0)
            status = "ยกเลิก";
        else if (served == active)
            status = "เสิร์ฟแล้ว";
        else if (ready + served == active)
            status = "พร้อมเสิร์ฟ";
        else if (cooking)
            status = "กำลังปรุง";
        else
            status = "ยืนยันแล้ว";
    }

    void markPaid(Payment payment) {
        this.payment = payment;
        status = "ชำระแล้ว";
    }

    public void destroy() {
        for (int i = 0; i < items.size(); i++)
            items.get(i).destroy();
        items.clear();
        table = null;
        customer = null;
        payment = null;
        destroyed = true;
    }

    public String getOrderId() {
        return orderId;
    }

    public Table getTable() {
        return table;
    }

    public Customer getCustomer() {
        return customer;
    }

    public Member getMember() {
        return customer.getMember();
    }

    public Payment getPayment() {
        return payment;
    }

    public String getStatus() {
        return status;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public ArrayList<OrderItem> getItems() {
        return items;
    }

    public boolean isDestroyed() {
        return destroyed;
    }
}
