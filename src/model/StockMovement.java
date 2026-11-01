package model;

import java.time.LocalDateTime;

// ประวัติหนึ่งครั้ง: เปลี่ยนเท่าไร เหลือเท่าไร เพราะอะไร และใครทำ
public class StockMovement {
    public enum MovementType { RECEIVE, SALE, RESTORE, ADJUST }

    // ประวัติหนึ่งแถวระบุชนิด จำนวนเปลี่ยน ยอดคงเหลือ และผู้ทำรายการ
    private String stockMovementId;
    private LocalDateTime time;
    private MovementType type;
    private double qty;
    private double balance;
    private String reference;
    private String reason;
    // has-a (Association): ประวัติอ้างถึง Employee ผู้ทำรายการ
    private Employee doneBy;
    private boolean destroyed;

    // สร้างประวัติการเปลี่ยนสต็อกหนึ่งครั้ง
    public StockMovement(String stockMovementId, MovementType type, double qty, double balance,
            String ref, String reason, Employee by) {
        this.stockMovementId = stockMovementId;
        recordStockMovement(type, qty, balance, ref, reason, by);
    }

    // สร้างประวัติการเปลี่ยนสต็อกหนึ่งครั้ง
    public StockMovement(String stockMovementId, String type, double qty, double balance,
            String ref, String reason, Employee by) {
        this(stockMovementId, parseType(type), qty, balance, ref, reason, by);
    }

    // แปลงข้อความภาษาไทยเป็นชนิด MovementType
    private static MovementType parseType(String text) {
        if (text.equals("รับเข้า")) return MovementType.RECEIVE;
        if (text.equals("ขาย")) return MovementType.SALE;
        if (text.equals("คืน")) return MovementType.RESTORE;
        if (text.equals("ปรับยอด")) return MovementType.ADJUST;
        throw new IllegalArgumentException("ชนิดประวัติสต็อกไม่ถูกต้อง");
    }

    // บันทึกได้ครั้งเดียว ประวัติที่สร้างแล้วไม่ควรถูกแก้ย้อนหลัง
    public void recordStockMovement(MovementType type, double qty, double balance,
            String ref, String reason, Employee by) {
        if (time != null) throw new IllegalStateException("บันทึกประวัติซ้ำไม่ได้");
        if (type == null || !Double.isFinite(qty) || !Double.isFinite(balance))
            throw new IllegalArgumentException("ข้อมูลประวัติสต็อกไม่ถูกต้อง");
        this.time = LocalDateTime.now();
        this.type = type;
        this.qty = qty;
        this.balance = balance;
        this.reference = ref;
        this.reason = reason;
        this.doneBy = by;
    }

    public void destroy() {
        destroyed = true;
        doneBy = null;
    }

    // เมธอดอ่านประวัติสต็อกที่บันทึกไว้แล้ว

    public LocalDateTime time() { return time; }
    public String typeText() {
        if (type == MovementType.RECEIVE) return "รับเข้า";
        if (type == MovementType.SALE) return "ขาย";
        if (type == MovementType.RESTORE) return "คืน";
        return "ปรับยอด";
    }
    public double quantity() { return qty; }
    public double balance() { return balance; }
    public String reference() { return reference; }
    public String reason() { return reason; }
    public Employee employee() { return doneBy; }
    public boolean isDestroyed() { return destroyed; }
}
