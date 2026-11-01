package model;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

// ออเดอร์เป็นเจ้าของ OrderItem และอ้างถึงโต๊ะ ลูกค้า และการชำระเงิน
public class Order {
    public enum OrderStatus { CART, CONFIRMED, COOKING, READY, SERVED, PAID, CANCELLED }
    // Order เป็นเจ้าของรายการอาหาร แต่เพียงอ้างถึง Table, Customer และ Payment
    private String orderId;
    // has-a (Association): ออเดอร์อ้างถึงโต๊ะ ลูกค้า และใบชำระเงิน
    // object เหล่านี้ยังมีชีวิตได้ แม้ออเดอร์นี้ถูกลบ
    private Table table;
    private Customer customer;
    private Payment payment;
    private OrderStatus status;
    private double totalAmount;
    private LocalDateTime createdAt;
    // has-a (Composition): Order เป็นเจ้าของ OrderItem หลายรายการ
    // destroy() ของ Order จะเรียก destroy() ของแต่ละ OrderItem
    private List<OrderItem> items;
    private int itemNumber;
    private boolean destroyed;

    // สร้างออเดอร์ในสถานะตะกร้า และจดเวลาที่สร้าง
    public Order(String orderId, Table table) {
        this(orderId, table, new Customer("CUSTOMER-" + orderId));
    }

    // สร้างออเดอร์ในสถานะตะกร้า และจดเวลาที่สร้าง
    public Order(String orderId, Table table, Customer customer) {
        this.orderId = orderId;
        this.table = table;
        this.customer = customer;
        this.status = OrderStatus.CART;
        this.createdAt = LocalDateTime.now();
        this.items = new ArrayList<OrderItem>();
    }

    // เพิ่ม OrderItem เมื่อเมนูเปิดขายและออเดอร์ยังเป็นตะกร้า
    public OrderItem addItem(Menu menu, int qty, String spice, String note) {
        if (status != OrderStatus.CART)
            throw new IllegalStateException("เพิ่มอาหารได้เฉพาะในตะกร้า");
        if (!menu.statusText().equals("เปิดขาย"))
            throw new IllegalArgumentException("เมนูปิดขาย");
        itemNumber++;
        OrderItem item = new OrderItem(orderId + "-ITEM-" + itemNumber, menu, qty, spice, note);
        items.add(item);
        return item;
    }

    // ลบรายการจากตะกร้าก่อนยืนยัน
    public void removeItem(int index) {
        if (status != OrderStatus.CART)
            throw new IllegalStateException("ลบได้เฉพาะตะกร้า");
        items.get(index).destroy();
        items.remove(index);
    }

    // ลบรายการจากตะกร้าก่อนยืนยัน
    public void removeItem(OrderItem item) {
        int index = items.indexOf(item);
        if (index < 0) throw new IllegalArgumentException("ไม่พบรายการในออเดอร์");
        removeItem(index);
    }

    // ผูกสมาชิกกับลูกค้าในออเดอร์ก่อนยืนยัน
    public void attachMember(Member member) {
        if (status != OrderStatus.CART) throw new IllegalStateException("แนบสมาชิกได้ก่อนยืนยันเท่านั้น");
        customer.linkMember(member);
    }

    // รวมราคาของรายการที่ยังไม่ยกเลิก
    public double calculateTotal() {
        double total = 0;
        // รายการที่ยกเลิกไม่อยู่ในยอดบิล แม้ยังเก็บไว้เพื่อดูประวัติ
        for (int i = 0; i < items.size(); i++) {
            if (!items.get(i).statusText().equals("ยกเลิก"))
                total += items.get(i).price();
        }
        totalAmount = total;
        return totalAmount;
    }

    // รวบรวมชื่อวัตถุดิบโดยไม่ซ้ำ เพื่อให้ตรวจยอดรวมของหลายจานได้
    private ArrayList<Ingredient> allIngredients() {
        ArrayList<Ingredient> result = new ArrayList<Ingredient>();
        for (int i = 0; i < items.size(); i++) {
            OrderItem item = items.get(i);
            if (!item.statusText().equals("ยกเลิก")) {
                for (int j = 0; j < item.ingredients().size(); j++) {
                    Ingredient ingredient = item.ingredients().get(j);
                    if (!result.contains(ingredient))
                        result.add(ingredient);
                }
            }
        }
        return result;
    }

    // คำนวณจำนวนวัตถุดิบรวมของทุกรายการในออเดอร์
    private double requiredQuantity(Ingredient ingredient) {
        double total = 0;
        for (int i = 0; i < items.size(); i++) {
            OrderItem item = items.get(i);
            if (!item.statusText().equals("ยกเลิก")) {
                total += item.amountPerDish(ingredient) * item.quantity();
            }
        }
        return total;
    }

    // ตรวจวัตถุดิบทุกชนิดให้พอครบก่อนตัดสต็อกและส่งครัว
    public void confirm() {
        if (status != OrderStatus.CART || items.isEmpty())
            throw new IllegalStateException("ตะกร้าต้องมีอาหารและยังไม่ยืนยัน");
        ArrayList<Ingredient> ingredients = allIngredients();
        // ตรวจให้ครบทุกชนิดก่อน แล้วค่อยตัด
        // เพื่อไม่ให้ตัดไปครึ่งหนึ่งแล้วพบว่าอีกชนิดไม่พอ
        for (int i = 0; i < ingredients.size(); i++) {
            Ingredient ingredient = ingredients.get(i);
            if (!ingredient.hasEnough(requiredQuantity(ingredient))) {
                throw new IllegalArgumentException("วัตถุดิบไม่พอ: " + ingredient.name());
            }
        }
        for (int i = 0; i < ingredients.size(); i++) {
            Ingredient ingredient = ingredients.get(i);
            ingredient.deduct(requiredQuantity(ingredient), orderId);
        }
        // หลังตัดครบแล้วจึงเปลี่ยนรายการเป็นงานของครัว
        for (int i = 0; i < items.size(); i++)
            items.get(i).markConfirmed();
        status = OrderStatus.CONFIRMED;
        table.changeTableStatus("ใช้งาน");
    }

    // แก้จำนวนอาหารและตัดหรือคืนสต็อกเฉพาะส่วนต่าง
    public void changeQuantity(int index, int newQuantity) {
        OrderItem item = items.get(index);
        if (newQuantity <= 0 || !item.statusText().equals("รอปรุง") || payment != null) {
            throw new IllegalArgumentException("แก้ได้เฉพาะรายการรอปรุงที่ยังไม่ชำระ และจำนวนต้องมากกว่า 0");
        }
        if (status == OrderStatus.CART) {
            item.changeQuantity(newQuantity);
            return;
        }
        int difference = newQuantity - item.quantity();
        // เพิ่มจานต้องเช็กสต็อกส่วนต่าง; ลดจานจะคืนเฉพาะส่วนต่าง
        ArrayList<Ingredient> ingredients = allIngredients();
        if (difference > 0) {
            for (int i = 0; i < ingredients.size(); i++) {
                Ingredient ingredient = ingredients.get(i);
                if (!ingredient.hasEnough(item.amountPerDish(ingredient) * difference)) {
                    throw new IllegalArgumentException("วัตถุดิบไม่พอ: " + ingredient.name());
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

    // ยกเลิกรายการที่ยังไม่ชำระ แล้วอัปเดตสถานะออเดอร์
    public void cancelItem(int index) {
        if (payment != null)
            throw new IllegalStateException("ชำระแล้ว แก้รายการไม่ได้");
        items.get(index).cancel();
        refreshStatus();
    }

    // คืน true เมื่อรายการที่ไม่ถูกยกเลิกเสิร์ฟครบทุกจาน
    public boolean isServed() {
        boolean hasFood = false;
        for (int i = 0; i < items.size(); i++) {
            String itemStatus = items.get(i).statusText();
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
        if (status == OrderStatus.CART || status == OrderStatus.PAID)
            return;
        int active = 0;
        int ready = 0;
        int served = 0;
        boolean cooking = false;
        for (int i = 0; i < items.size(); i++) {
            String value = items.get(i).statusText();
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
            status = OrderStatus.CANCELLED;
        else if (served == active)
            status = OrderStatus.SERVED;
        else if (ready + served == active)
            status = OrderStatus.READY;
        else if (cooking)
            status = OrderStatus.COOKING;
        else
            status = OrderStatus.CONFIRMED;
    }

    // ผูก Payment ที่ยืนยันแล้วและเปลี่ยนสถานะเป็นชำระแล้ว
    void markPaid(Payment payment) {
        this.payment = payment;
        status = OrderStatus.PAID;
    }

    // ยกเลิกทั้งออเดอร์เมื่อยังไม่มีรายการเริ่มปรุง
    public void cancel() {
        if (payment != null) throw new IllegalStateException("ชำระแล้ว ยกเลิกไม่ได้");
        for (OrderItem item : items) {
            if (!item.statusText().equals("รอปรุง") && !item.statusText().equals("ยกเลิก"))
                throw new IllegalStateException("มีรายการเริ่มปรุงแล้ว ให้ส่งคำขอผู้จัดการ");
        }
        for (OrderItem item : items) if (!item.statusText().equals("ยกเลิก")) item.cancel();
        status = OrderStatus.CANCELLED;
    }

    // จำกัดการเปลี่ยนสถานะให้ผ่านขั้นตอนที่มีกฎรองรับ
    public void changeStatus(OrderStatus s) {
        if (s == OrderStatus.CANCELLED) { cancel(); return; }
        if (s == status) return;
        throw new IllegalStateException("สถานะเปลี่ยนผ่านขั้นตอนของรายการอาหารและการชำระเงิน");
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

    // เมธอดอ่านออเดอร์; statusText() แปลง enum เป็นข้อความที่ผู้ใช้เห็น
    public String orderId() {
        return orderId;
    }

    public Table table() {
        return table;
    }

    public Customer customer() {
        return customer;
    }

    public Member linkedMember() {
        return customer.linkedMember();
    }

    public Payment payment() {
        return payment;
    }

    public String statusText() {
        switch (status) {
            case CART: return "ตะกร้า";
            case CONFIRMED: return "ยืนยันแล้ว";
            case COOKING: return "กำลังปรุง";
            case READY: return "พร้อมเสิร์ฟ";
            case SERVED: return "เสิร์ฟแล้ว";
            case PAID: return "ชำระแล้ว";
            default: return "ยกเลิก";
        }
    }

    // อ่านยอดรวมล่าสุดโดยคำนวณใหม่ก่อนคืนค่า

    public LocalDateTime createdAt() {
        return createdAt;
    }

    public List<OrderItem> items() {
        return items;
    }

    public boolean isDestroyed() {
        return destroyed;
    }
}
