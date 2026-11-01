package model;

import java.util.ArrayList;

// ผู้จำหน่ายอ้างถึงวัตถุดิบในร้าน ไม่ได้เป็นเจ้าของอายุของวัตถุดิบ
public class Supplier {
    private String supplierId;
    private String name;
    private ArrayList<Ingredient> ingredients;

    public Supplier(String supplierId, String name) {
        this.supplierId = supplierId;
        this.name = name;
        this.ingredients = new ArrayList<Ingredient>();
    }

    public void addIngredient(Ingredient ingredient) {
        if (!ingredients.contains(ingredient))
            ingredients.add(ingredient);
    }

    public boolean supplies(Ingredient ingredient) {
        return ingredients.contains(ingredient);
    }

    public String getSupplierId() {
        return supplierId;
    }

    public String getName() {
        return name;
    }

    public ArrayList<Ingredient> getIngredients() {
        return ingredients;
    }
}
