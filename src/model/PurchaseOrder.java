package model;

import java.util.ArrayList;

// ใบสั่งซื้อเปลี่ยนสถานะจาก ร่าง → สั่งแล้ว → รับแล้ว
public class PurchaseOrder {
    private String poId;
    private Supplier supplier;
    private Employee employee;
    private String status;
    private ArrayList<Ingredient> ingredients;
    private ArrayList<Double> orderedQty;
    private ArrayList<Double> receivedQty;

    public PurchaseOrder(String poId, Supplier supplier, Employee employee) {
        this.poId = poId;
        this.supplier = supplier;
        this.employee = employee;
        this.status = "ร่าง";
        this.ingredients = new ArrayList<Ingredient>();
        this.orderedQty = new ArrayList<Double>();
        this.receivedQty = new ArrayList<Double>();
    }

    public void addItem(Ingredient ingredient, double quantity) {
        if (!status.equals("ร่าง"))
            throw new IllegalStateException("แก้ได้เฉพาะใบสั่งซื้อร่าง");
        if (!supplier.supplies(ingredient))
            throw new IllegalArgumentException("ผู้จำหน่ายไม่ส่งวัตถุดิบนี้");
        if (!Double.isFinite(quantity) || quantity <= 0)
            throw new IllegalArgumentException("จำนวนต้องมากกว่า 0");
        int index = ingredients.indexOf(ingredient);
        if (index == -1) {
            ingredients.add(ingredient);
            orderedQty.add(quantity);
            receivedQty.add(0.0);
        } else {
            orderedQty.set(index, orderedQty.get(index) + quantity);
        }
    }

    public void markOrdered() {
        if (!status.equals("ร่าง") || ingredients.isEmpty())
            throw new IllegalStateException("ใบสั่งซื้อต้องเป็นร่างและมีรายการ");
        status = "สั่งแล้ว";
    }

    public void receive(ArrayList<Double> quantities) {
        if (!status.equals("สั่งแล้ว"))
            throw new IllegalStateException("รับของซ้ำไม่ได้");
        if (quantities.size() != ingredients.size())
            throw new IllegalArgumentException("ต้องระบุครบทุกวัตถุดิบ");
        // ตรวจให้ครบก่อนเปลี่ยนยอด เพื่อไม่ให้เกิดการรับเพียงบางรายการเมื่อกรอกผิด
        for (int i = 0; i < quantities.size(); i++) {
            if (quantities.get(i) < 0 || !Double.isFinite(quantities.get(i))) {
                throw new IllegalArgumentException("จำนวนรับต้องเป็นตัวเลขไม่ติดลบ");
            }
        }
        for (int i = 0; i < ingredients.size(); i++) {
            receivedQty.set(i, quantities.get(i));
            ingredients.get(i).receive(quantities.get(i), poId, employee);
        }
        status = "รับแล้ว";
    }

    public String getPoId() {
        return poId;
    }

    public Supplier getSupplier() {
        return supplier;
    }

    public String getStatus() {
        return status;
    }

    public ArrayList<Ingredient> getIngredients() {
        return ingredients;
    }

    public double getOrderedQty(int index) {
        return orderedQty.get(index);
    }

    public double getReceivedQty(int index) {
        return receivedQty.get(index);
    }
}
