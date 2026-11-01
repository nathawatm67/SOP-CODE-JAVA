package model;

import java.util.ArrayList;

// เมนูเป็นเจ้าของสูตรหลายเวอร์ชัน ตัวเลือกเสริมเก็บเป็นข้อมูลภายใน ไม่สร้างคลาสที่ 17
public class Menu {
    private String menuId;
    private String name;
    private double price;
    private String category;
    private String station;
    private String status;
    private boolean spiceSelectable;
    private boolean everOrdered;
    private boolean destroyed;
    private ArrayList<Recipe> recipes;
    private ArrayList<String> optionNames;
    private ArrayList<Double> optionPrices;
    // สามรายการนี้จับคู่กัน: ตัวเลือกเลขใด ใช้วัตถุดิบอะไร ปริมาณเท่าไร
    private ArrayList<Integer> extraOptionIndexes;
    private ArrayList<Ingredient> extraIngredients;
    private ArrayList<Double> extraQuantities;

    public Menu(String id, String name, double price, String category, String station) {
        this.menuId = id;
        update(name, price, category, station);
        this.status = "ปิดขาย";
        this.recipes = new ArrayList<Recipe>();
        this.optionNames = new ArrayList<String>();
        this.optionPrices = new ArrayList<Double>();
        this.extraOptionIndexes = new ArrayList<Integer>();
        this.extraIngredients = new ArrayList<Ingredient>();
        this.extraQuantities = new ArrayList<Double>();
    }

    public void update(String name, double price, String category, String station) {
        if (!Double.isFinite(price) || price <= 0)
            throw new IllegalArgumentException("ราคาต้องมากกว่า 0");
        this.name = name;
        this.price = price;
        this.category = category;
        this.station = station;
    }

    public void addRecipe(Recipe recipe) {
        recipes.add(recipe);
    }

    public Recipe getCurrentRecipe() {
        Recipe latest = null;
        for (int i = 0; i < recipes.size(); i++) {
            Recipe recipe = recipes.get(i);
            if (recipe.getStatus().equals("สมบูรณ์")) {
                if (latest == null || recipe.getVersion() > latest.getVersion())
                    latest = recipe;
            }
        }
        return latest;
    }

    public void openSale() {
        if (destroyed || getCurrentRecipe() == null) {
            throw new IllegalStateException("ต้องมีสูตรสมบูรณ์และเมนูยังไม่ถูกลบ");
        }
        status = "เปิดขาย";
    }

    public void closeSale() {
        status = "ปิดขาย";
    }

    public void noteOrdered() {
        everOrdered = true;
    }

    public boolean isDeletable() {
        return !everOrdered;
    }

    public void addOption(String name, double price) {
        if (!Double.isFinite(price) || price < 0)
            throw new IllegalArgumentException("ราคาตัวเลือกติดลบไม่ได้");
        optionNames.add(name);
        optionPrices.add(price);
    }

    public void addOptionIngredient(int optionIndex, Ingredient ingredient, double quantity) {
        if (optionIndex < 0 || optionIndex >= optionNames.size() || !Double.isFinite(quantity) || quantity <= 0) {
            throw new IllegalArgumentException("ตัวเลือกหรือปริมาณไม่ถูกต้อง");
        }
        extraOptionIndexes.add(optionIndex);
        extraIngredients.add(ingredient);
        extraQuantities.add(quantity);
    }

    public void destroy() {
        for (int i = 0; i < recipes.size(); i++)
            recipes.get(i).destroy();
        recipes.clear();
        optionNames.clear();
        optionPrices.clear();
        extraOptionIndexes.clear();
        extraIngredients.clear();
        extraQuantities.clear();
        destroyed = true;
    }

    public String getMenuId() {
        return menuId;
    }

    public String getName() {
        return name;
    }

    public double getPrice() {
        return price;
    }

    public String getCategory() {
        return category;
    }

    public String getStation() {
        return station;
    }

    public String getStatus() {
        return status;
    }

    public boolean isSpiceSelectable() {
        return spiceSelectable;
    }

    public void setSpiceSelectable(boolean value) {
        spiceSelectable = value;
    }

    public ArrayList<Recipe> getRecipes() {
        return recipes;
    }

    public ArrayList<String> getOptionNames() {
        return optionNames;
    }

    public double getOptionPrice(int index) {
        return optionPrices.get(index);
    }

    public int getExtraCount() {
        return extraIngredients.size();
    }

    public int getExtraOptionIndex(int index) {
        return extraOptionIndexes.get(index);
    }

    public Ingredient getExtraIngredient(int index) {
        return extraIngredients.get(index);
    }

    public double getExtraQuantity(int index) {
        return extraQuantities.get(index);
    }

    public boolean isDestroyed() {
        return destroyed;
    }
}
