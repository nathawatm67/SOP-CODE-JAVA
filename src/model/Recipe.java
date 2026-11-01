package model;

import java.util.ArrayList;
import java.util.List;

// สูตรหนึ่งเวอร์ชัน: วัตถุดิบหนึ่งชนิดจับคู่กับปริมาณต่อหนึ่งจาน
public class Recipe {
    public enum RecipeStatus { DRAFT, COMPLETE }

    // ingredients และ quantities จับคู่กันด้วย index เดียวกัน
    private String recipeId;
    private int version;
    private RecipeStatus status;
    // has-a (Association): Recipe อ้างถึง Ingredient ในคลัง แต่ไม่ได้เป็นเจ้าของวัตถุดิบ
    private List<Ingredient> ingredients;
    private List<Double> quantities;
    private boolean destroyed;

    // สร้างสูตรฉบับร่างหนึ่งเวอร์ชัน
    public Recipe(String recipeId, int version) {
        this.recipeId = recipeId;
        this.version = version;
        this.status = RecipeStatus.DRAFT;
        this.ingredients = new ArrayList<Ingredient>();
        this.quantities = new ArrayList<Double>();
    }

    // เพิ่มวัตถุดิบกับปริมาณที่ตำแหน่งเดียวกัน ถ้ามีอยู่แล้วให้บวกปริมาณ
    public void addItem(Ingredient ingredient, double qty) {
        if (status != RecipeStatus.DRAFT || destroyed)
            throw new IllegalStateException("แก้ได้เฉพาะสูตรร่างที่ยังไม่ลบ");
        if (ingredient == null || !Double.isFinite(qty) || qty <= 0)
            throw new IllegalArgumentException("วัตถุดิบและปริมาณไม่ถูกต้อง");
        int index = ingredients.indexOf(ingredient);
        if (index >= 0)
            quantities.set(index, quantities.get(index) + qty);
        else {
            ingredients.add(ingredient);
            quantities.add(qty);
        }
    }

    // ชื่อเดิมยังใช้ใน Main และแบบทดสอบ
    public void addIngredient(Ingredient ingredient, double quantity) {
        addItem(ingredient, quantity);
    }

    // เปลี่ยนปริมาณได้เฉพาะสูตรร่าง
    public void changeQty(Ingredient ingredient, double qty) {
        if (status != RecipeStatus.DRAFT)
            throw new IllegalStateException("สร้างเวอร์ชันใหม่ก่อนแก้สูตรสมบูรณ์");
        int index = ingredients.indexOf(ingredient);
        if (index < 0 || !Double.isFinite(qty) || qty <= 0)
            throw new IllegalArgumentException("วัตถุดิบหรือปริมาณไม่ถูกต้อง");
        quantities.set(index, qty);
    }

    // แปลงตำแหน่งในหน้าจอเป็นวัตถุดิบแล้วเปลี่ยนปริมาณ
    public void changeQuantity(int index, double quantity) {
        changeQty(ingredients().get(index), quantity);
    }

    // ทำสูตรให้สมบูรณ์เมื่อมีวัตถุดิบอย่างน้อยหนึ่งชนิด
    public void complete() {
        if (ingredients.isEmpty())
            throw new IllegalStateException("สูตรต้องมีวัตถุดิบ");
        status = RecipeStatus.COMPLETE;
    }

    // สูตรใหม่มีรายการของตัวเอง แต่ยังอ้างวัตถุดิบในคลังตัวเดียวกัน
    public Recipe createNewVersion(String id) {
        Recipe next = new Recipe(id, version + 1);
        for (int i = 0; i < ingredients.size(); i++)
            next.addItem(ingredients.get(i), quantities.get(i));
        return next;
    }

    // คัดลอกส่วนผสมไปเป็นสูตรร่างเวอร์ชันถัดไป
    public Recipe createNewVersion() {
        return createNewVersion(recipeId + "-v" + (version + 1));
    }

    public void destroy() {
        ingredients.clear();
        quantities.clear();
        destroyed = true;
    }

    // เมธอดอ่านสูตร; รายการที่คืนออกไปเป็นสำเนาเพื่อกันการแก้จากภายนอก

    public int version() { return version; }
    public String statusText() { return status == RecipeStatus.DRAFT ? "ร่าง" : "สมบูรณ์"; }
    public ArrayList<Ingredient> ingredients() { return new ArrayList<Ingredient>(ingredients); }
    public double quantity(int index) { return quantities.get(index); }
    public boolean isDestroyed() { return destroyed; }
}
