package model;

import java.util.ArrayList;
import java.util.List;

// วัตถุดิบรับผิดชอบยอดสต็อกของตัวเอง และเป็นเจ้าของประวัติ StockMovement
public class Ingredient {
    // stockQty คือยอดปัจจุบัน ส่วน movements เก็บเหตุการณ์ทุกครั้งที่ยอดเปลี่ยน
    private String ingredientId;
    private String name;
    private String unit;
    private double stockQty;
    private double minQty;
    // has-a (Composition): Ingredient เป็นเจ้าของ StockMovement ของตนเอง
    // เมื่อลบวัตถุดิบ ประวัติที่เป็นส่วนของมันถูกทำลายตาม
    private List<StockMovement> movements;
    private boolean destroyed;

    // สร้างวัตถุดิบโดยยอดสต็อกเริ่มที่ศูนย์และกำหนดยอดขั้นต่ำ
    public Ingredient(String ingredientId, String name, String unit, double minQty) {
        if (!Double.isFinite(minQty) || minQty < 0)
            throw new IllegalArgumentException("ขั้นต่ำติดลบไม่ได้");
        this.ingredientId = ingredientId;
        this.name = name;
        this.unit = unit;
        this.minQty = minQty;
        this.movements = new ArrayList<StockMovement>();
    }

    // ตรวจว่าสต็อกมีพอต่อจำนวนที่ต้องใช้หรือไม่
    public boolean hasEnough(double qty) {
        return stockQty + 0.000001 >= qty;
    }

    // รับของ ตัดขาย และคืนของ ใช้เมธอดเดียวกันบันทึกยอดกับประวัติ
    private void changeStock(double change, String type, String reference,
            String reason, Employee employee) {
        if (destroyed)
            throw new IllegalStateException("วัตถุดิบนี้ถูกลบแล้ว");
        stockQty = Math.round((stockQty + change) * 1000.0) / 1000.0;
        String id = ingredientId + "-MOV-" + (movements.size() + 1);
        StockMovement movement = new StockMovement(id, type, change, stockQty,
                reference, reason, employee);
        movements.add(movement);
    }

    // เพิ่มยอดรับเข้าคลังและสร้างประวัติการเคลื่อนไหว
    public void receive(double quantity, String reference, Employee employee) {
        if (!Double.isFinite(quantity) || quantity < 0)
            throw new IllegalArgumentException("จำนวนรับติดลบไม่ได้");
        changeStock(quantity, "รับเข้า", reference, "รับวัตถุดิบ", employee);
    }

    // ชื่อ operation ตาม P7; งานรับ PO ที่ระบุพนักงานใช้ receive(..., employee)
    public void increaseStock(double qty, String ref) {
        receive(qty, ref, null);
    }

    // ตรวจยอดก่อนตัดตามออเดอร์ แล้วสร้างประวัติการขาย
    public void deduct(double qty, String ref) {
        if (!Double.isFinite(qty) || qty < 0 || !hasEnough(qty)) {
            throw new IllegalArgumentException("วัตถุดิบไม่พอ: " + name);
        }
        changeStock(-qty, "ขาย", ref, "ตัดตามสูตร", null);
    }

    // คืนสต็อกเมื่อยกเลิกหรือแก้จำนวนอาหาร
    public void restore(double qty, String ref) {
        if (!Double.isFinite(qty) || qty < 0)
            throw new IllegalArgumentException("จำนวนคืนติดลบไม่ได้");
        changeStock(qty, "คืน", ref, "ยกเลิกหรือแก้จำนวนอาหาร", null);
    }

    // ปรับยอดให้ตรงกับการตรวจนับ โดยต้องบอกเหตุผล
    public void adjustStock(double newQty, String reason, Employee by) {
        if (!Double.isFinite(newQty) || newQty < 0 || reason.trim().isEmpty()) {
            throw new IllegalArgumentException("ยอดต้องไม่ติดลบและต้องมีเหตุผล");
        }
        changeStock(newQty - stockQty, "ปรับยอด", "ตรวจนับ", reason, by);
    }

    // แก้ชื่อ หน่วย และยอดขั้นต่ำของวัตถุดิบ
    public void update(String name, String unit, double minQty) {
        if (!Double.isFinite(minQty) || minQty < 0)
            throw new IllegalArgumentException("ขั้นต่ำติดลบไม่ได้");
        this.name = name;
        this.unit = unit;
        this.minQty = minQty;
    }

    // Composition: เมื่อลบวัตถุดิบ ประวัติที่เป็นส่วนของวัตถุดิบนี้ถูกทำลายตาม
    public void destroy() {
        for (int i = 0; i < movements.size(); i++)
            movements.get(i).destroy();
        movements.clear();
        destroyed = true;
    }

    // เมธอดอ่านข้อมูลสต็อกและประวัติ โดยไม่แก้ยอดจากภายนอกโดยตรง
    public String ingredientId() {
        return ingredientId;
    }

    public String name() {
        return name;
    }

    public String unit() {
        return unit;
    }

    public double stockQty() {
        return stockQty;
    }

    public double minQty() {
        return minQty;
    }

    public List<StockMovement> movements() {
        return movements;
    }

    public boolean isDestroyed() {
        return destroyed;
    }
}
