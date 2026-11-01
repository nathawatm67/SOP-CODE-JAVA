package model;

import java.util.ArrayList;

// สูตรเก็บวัตถุดิบและปริมาณต่อหนึ่งเสิร์ฟ โดยตำแหน่ง i ของสองรายการเป็นคู่กัน
public class Recipe {
    private String recipeId;
    private int version;
    private String status;
    private ArrayList<Ingredient> ingredients;
    private ArrayList<Double> quantities;
    private boolean destroyed;

    public Recipe(String recipeId, int version) {
        this.recipeId = recipeId;
        this.version = version;
        this.status = "ร่าง";
        this.ingredients = new ArrayList<Ingredient>();
        this.quantities = new ArrayList<Double>();
    }

    public void addIngredient(Ingredient ingredient, double quantity) {
        if (!status.equals("ร่าง") || destroyed) {
            throw new IllegalStateException("แก้ได้เฉพาะสูตรร่างที่ยังไม่ลบ");
        }
        if (!Double.isFinite(quantity) || !Double.isFinite(quantity) || quantity <= 0)
            throw new IllegalArgumentException("ปริมาณต้องมากกว่า 0");
        int index = ingredients.indexOf(ingredient);
        if (index == -1) {
            ingredients.add(ingredient);
            quantities.add(quantity);
        } else {
            quantities.set(index, quantities.get(index) + quantity);
        }
    }

    public void changeQuantity(int index, double quantity) {
        if (!status.equals("ร่าง"))
            throw new IllegalStateException("สร้างเวอร์ชันใหม่ก่อนแก้สูตรสมบูรณ์");
        if (!Double.isFinite(quantity) || !Double.isFinite(quantity) || quantity <= 0)
            throw new IllegalArgumentException("ปริมาณต้องมากกว่า 0");
        quantities.set(index, quantity);
    }

    public void complete() {
        if (ingredients.isEmpty())
            throw new IllegalStateException("สูตรต้องมีวัตถุดิบ");
        status = "สมบูรณ์";
    }

    // สูตรใหม่มีรายการของตัวเอง แต่ยังใช้วัตถุดิบในคลังตัวเดียวกัน
    public Recipe createNewVersion(String id) {
        Recipe next = new Recipe(id, version + 1);
        for (int i = 0; i < ingredients.size(); i++) {
            next.addIngredient(ingredients.get(i), quantities.get(i));
        }
        return next;
    }

    public void destroy() {
        ingredients.clear();
        quantities.clear();
        destroyed = true;
    }

    public String getRecipeId() {
        return recipeId;
    }

    public int getVersion() {
        return version;
    }

    public String getStatus() {
        return status;
    }

    public ArrayList<Ingredient> getIngredients() {
        return ingredients;
    }

    public double getQuantity(int index) {
        return quantities.get(index);
    }

    public boolean isDestroyed() {
        return destroyed;
    }
}
