package model;

import java.util.ArrayList;
import java.util.List;

// ผู้จำหน่ายอ้างถึงวัตถุดิบในร้าน ไม่ได้เป็นเจ้าของอายุของวัตถุดิบ
public class Supplier {
    // เก็บรายการ Ingredient ที่รายนี้ส่งได้ โดยอ้างถึง object ในคลังเดียวกัน
    private String supplierId;
    private String name;
    // has-a (Association): Supplier อ้างถึง Ingredient ที่ส่งได้ ไม่ได้เป็นเจ้าของสต็อก
    private List<Ingredient> suppliedIngredients;

    // สร้างผู้จำหน่ายและเตรียมรายการวัตถุดิบที่ส่งได้
    public Supplier(String supplierId, String name) {
        this.supplierId = supplierId;
        this.name = name;
        this.suppliedIngredients = new ArrayList<Ingredient>();
    }

    // เพิ่มวัตถุดิบที่รายนี้ส่งได้โดยไม่เพิ่มซ้ำ
    public void addIngredient(Ingredient ingredient) {
        if (!suppliedIngredients.contains(ingredient))
            suppliedIngredients.add(ingredient);
    }

    // ตรวจว่าผู้จำหน่ายรายนี้ส่งวัตถุดิบชนิดนี้หรือไม่
    public boolean supplies(Ingredient ingredient) {
        return suppliedIngredients.contains(ingredient);
    }

    // หน้าจออ่านชื่อผู้จำหน่ายผ่านเมธอด เพราะ field เป็น private
    public String name() {
        return name;
    }

}
