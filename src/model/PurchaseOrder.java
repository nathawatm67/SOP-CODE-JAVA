package model;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

// ใบสั่งซื้อเปลี่ยนสถานะจาก ร่าง → สั่งแล้ว → รับแล้ว
public class PurchaseOrder {
    public enum PoStatus { DRAFT, ORDERED, RECEIVED }

    // List ทั้งสามชุดใช้ index เดียวกัน: วัตถุดิบที่ 0 / สั่งที่ 0 / รับที่ 0
    private String poId;
    private PoStatus status;
    private LocalDateTime createdAt;
    // has-a (Association): PO อ้างถึง Ingredient, Supplier และ Employee ในระบบ
    private List<Ingredient> ingredients;
    private List<Double> orderedQty;
    private List<Double> receivedQty;
    private Supplier supplier;
    private Employee createdBy;

    // สร้างใบสั่งซื้อฉบับร่างพร้อมผู้จำหน่ายและผู้สร้าง
    public PurchaseOrder(String poId, Supplier supplier, Employee by) {
        this.poId = poId;
        this.supplier = supplier;
        this.createdBy = by;
        this.status = PoStatus.DRAFT;
        this.createdAt = LocalDateTime.now();
        this.ingredients = new ArrayList<Ingredient>();
        this.orderedQty = new ArrayList<Double>();
        this.receivedQty = new ArrayList<Double>();
    }

    // เพิ่มจำนวนสั่งของวัตถุดิบที่ผู้จำหน่ายรายนี้ส่งได้
    public void addItem(Ingredient ingredient, double qty) {
        if (status != PoStatus.DRAFT)
            throw new IllegalStateException("แก้ได้เฉพาะใบสั่งซื้อร่าง");
        if (!supplier.supplies(ingredient))
            throw new IllegalArgumentException("ผู้จำหน่ายไม่ส่งวัตถุดิบนี้");
        if (!Double.isFinite(qty) || qty <= 0)
            throw new IllegalArgumentException("จำนวนต้องมากกว่า 0");
        int index = ingredients.indexOf(ingredient);
        if (index >= 0)
            orderedQty.set(index, orderedQty.get(index) + qty);
        else {
            ingredients.add(ingredient);
            orderedQty.add(qty);
            receivedQty.add(0.0);
        }
    }

    // เปลี่ยนจากร่างเป็นสั่งแล้วเมื่อมีรายการ
    public void markOrdered() {
        if (status != PoStatus.DRAFT || orderedQty.isEmpty())
            throw new IllegalStateException("ใบสั่งซื้อต้องเป็นร่างและมีรายการ");
        status = PoStatus.ORDERED;
    }

    // ตรวจจำนวนรับให้ครบก่อนเพิ่มยอดวัตถุดิบจริง
    public void receive(List<Double> qtys) {
        if (status != PoStatus.ORDERED)
            throw new IllegalStateException("รับของซ้ำไม่ได้");
        if (qtys == null || qtys.size() != ingredients.size())
            throw new IllegalArgumentException("ต้องระบุครบทุกวัตถุดิบ");
        // ตรวจให้ครบก่อนเปลี่ยนยอด เพื่อไม่ให้รับเข้าบางรายการเมื่อข้อมูลผิด
        for (int i = 0; i < ingredients.size(); i++) {
            Double qty = qtys.get(i);
            if (qty == null || qty < 0 || !Double.isFinite(qty))
                throw new IllegalArgumentException("จำนวนรับต้องเป็นตัวเลขไม่ติดลบ");
        }
        // ข้อมูลทุกแถวผ่านแล้วจึงรับเข้าคลังทีละชนิด
        for (int i = 0; i < ingredients.size(); i++) {
            double qty = qtys.get(i);
            receivedQty.set(i, qty);
            ingredients.get(i).receive(qty, poId, createdBy);
        }
        status = PoStatus.RECEIVED;
    }

    // เมธอดอ่านใบสั่งซื้อ; รายการที่คืนออกไปเป็นสำเนาเพื่อกันการแก้ตรง ๆ
    public String poId() { return poId; }
    public Supplier supplier() { return supplier; }
    public String statusText() {
        if (status == PoStatus.DRAFT) return "ร่าง";
        if (status == PoStatus.ORDERED) return "สั่งแล้ว";
        return "รับแล้ว";
    }
    public LocalDateTime createdAt() { return createdAt; }
    public ArrayList<Ingredient> ingredients() { return new ArrayList<Ingredient>(ingredients); }
    public double orderedQty(int index) { return orderedQty.get(index); }
    public double receivedQty(int index) { return receivedQty.get(index); }
}
