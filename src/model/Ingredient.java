package model;

import java.util.ArrayList;

// วัตถุดิบรับผิดชอบยอดสต็อกของตัวเอง และเป็นเจ้าของประวัติ StockMovement
public class Ingredient {
    private String ingredientId;
    private String name;
    private String unit;
    private double stockQty;
    private double minQty;
    private ArrayList<StockMovement> movements;
    private boolean destroyed;

    public Ingredient(String id, String name, String unit, double minQty) {
        if (!Double.isFinite(minQty) || minQty < 0)
            throw new IllegalArgumentException("ขั้นต่ำติดลบไม่ได้");
        this.ingredientId = id;
        this.name = name;
        this.unit = unit;
        this.minQty = minQty;
        this.movements = new ArrayList<StockMovement>();
    }

    public boolean hasEnough(double quantity) {
        return stockQty + 0.000001 >= quantity;
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

    public void receive(double quantity, String reference, Employee employee) {
        if (!Double.isFinite(quantity) || quantity < 0)
            throw new IllegalArgumentException("จำนวนรับติดลบไม่ได้");
        changeStock(quantity, "รับเข้า", reference, "รับวัตถุดิบ", employee);
    }

    public void deduct(double quantity, String reference) {
        if (!Double.isFinite(quantity) || quantity < 0 || !hasEnough(quantity)) {
            throw new IllegalArgumentException("วัตถุดิบไม่พอ: " + name);
        }
        changeStock(-quantity, "ขาย", reference, "ตัดตามสูตร", null);
    }

    public void restore(double quantity, String reference) {
        if (!Double.isFinite(quantity) || quantity < 0)
            throw new IllegalArgumentException("จำนวนคืนติดลบไม่ได้");
        changeStock(quantity, "คืน", reference, "ยกเลิกหรือแก้จำนวนอาหาร", null);
    }

    public void adjustStock(double actual, String reason, Employee employee) {
        if (!Double.isFinite(actual) || actual < 0 || reason.trim().isEmpty()) {
            throw new IllegalArgumentException("ยอดต้องไม่ติดลบและต้องมีเหตุผล");
        }
        changeStock(actual - stockQty, "ปรับยอด", "ตรวจนับ", reason, employee);
    }

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

    public String getIngredientId() {
        return ingredientId;
    }

    public String getName() {
        return name;
    }

    public String getUnit() {
        return unit;
    }

    public double getStockQty() {
        return stockQty;
    }

    public double getMinQty() {
        return minQty;
    }

    public ArrayList<StockMovement> getMovements() {
        return movements;
    }

    public boolean isDestroyed() {
        return destroyed;
    }
}
