package model;

import java.util.ArrayList;
import java.util.List;

// เมนูเป็นเจ้าของสูตรหลายเวอร์ชัน ตัวเลือกเสริมเก็บเป็นข้อมูลภายใน ไม่สร้างคลาสที่ 17
public class Menu {
    public enum SaleStatus { ON_SALE, OFF_SALE }

    // เมนูหนึ่งรายการมีสูตรได้หลายเวอร์ชัน และตัวเลือกมีราคาเพิ่มของตัวเอง
    private String menuId;
    private String name;
    private double price;
    private String category;
    private String station;
    private SaleStatus status;
    private boolean spiceSelectable;
    private boolean everOrdered;
    private boolean destroyed;
    // has-a (Composition): Menu เป็นเจ้าของ Recipe; เมื่อลบ Menu จะลบสูตรด้วย
    private List<Recipe> recipes;
    // List สองชุดนี้จับคู่ด้วย index เดียวกัน เช่น ชื่อที่ 0 มีราคาที่ 0
    private List<String> options;
    private List<Double> optionPrices;
    // สามรายการนี้จับคู่กัน: ตัวเลือกเลขใด ใช้วัตถุดิบอะไร ปริมาณเท่าไร
    private ArrayList<Integer> extraOptionIndexes;
    private ArrayList<Ingredient> extraIngredients;
    private ArrayList<Double> extraQuantities;

    // สร้างเมนูใหม่ โดยเริ่มปิดขายจนกว่าจะมีสูตรสมบูรณ์
    public Menu(String menuId, String name, double price) {
        this(menuId, name, price, "ยังไม่ระบุ", "ครัวร้อน");
    }

    // สร้างเมนูใหม่ โดยเริ่มปิดขายจนกว่าจะมีสูตรสมบูรณ์
    public Menu(String id, String name, double price, String category, String station) {
        this.menuId = id;
        update(name, price, category, station);
        this.status = SaleStatus.OFF_SALE;
        this.recipes = new ArrayList<Recipe>();
        this.options = new ArrayList<String>();
        this.optionPrices = new ArrayList<Double>();
        this.extraOptionIndexes = new ArrayList<Integer>();
        this.extraIngredients = new ArrayList<Ingredient>();
        this.extraQuantities = new ArrayList<Double>();
    }

    // แก้ชื่อ ราคา หมวด และสถานีครัว โดยราคาต้องมากกว่าศูนย์
    public void update(String name, double price, String category, String station) {
        if (!Double.isFinite(price) || price <= 0)
            throw new IllegalArgumentException("ราคาต้องมากกว่า 0");
        this.name = name;
        this.price = price;
        this.category = category;
        this.station = station;
    }

    // เก็บสูตรอีกหนึ่งเวอร์ชันไว้กับเมนู
    public void addRecipe(Recipe recipe) {
        recipes.add(recipe);
    }

    // เลือกสูตรสมบูรณ์ที่มีเลขเวอร์ชันสูงสุด
    public Recipe currentRecipe() {
        Recipe latest = null;
        for (int i = 0; i < recipes.size(); i++) {
            Recipe recipe = recipes.get(i);
            if (recipe.statusText().equals("สมบูรณ์")) {
                if (latest == null || recipe.version() > latest.version())
                    latest = recipe;
            }
        }
        return latest;
    }

    // เปิดขายได้เมื่อมีสูตรสมบูรณ์และเมนูยังไม่ถูกลบ
    public void openSale() {
        if (destroyed || currentRecipe() == null) {
            throw new IllegalStateException("ต้องมีสูตรสมบูรณ์และเมนูยังไม่ถูกลบ");
        }
        status = SaleStatus.ON_SALE;
    }

    // ปิดขายเมนูชั่วคราว
    public void closeSale() {
        status = SaleStatus.OFF_SALE;
    }

    // จำว่าเคยยืนยันสั่งเมนูนี้แล้ว เพื่อป้องกันการลบข้อมูลเก่า
    public void noteOrdered() {
        everOrdered = true;
    }

    // ลบเมนูได้เฉพาะเมื่อยังไม่เคยถูกสั่งจริง
    public boolean isDeletable() {
        return !everOrdered;
    }

    // เพิ่มชื่อตัวเลือกและราคาเพิ่ม
    public void addOption(String name, double price) {
        if (!Double.isFinite(price) || price < 0)
            throw new IllegalArgumentException("ราคาตัวเลือกติดลบไม่ได้");
        int index = options.indexOf(name);
        if (index >= 0)
            optionPrices.set(index, price);
        else {
            options.add(name);
            optionPrices.add(price);
        }
    }

    // ผูกตัวเลือกกับวัตถุดิบและปริมาณที่ใช้เพิ่ม
    public void addOptionIngredient(int optionIndex, Ingredient ingredient, double quantity) {
        if (optionIndex < 0 || optionIndex >= options.size() || !Double.isFinite(quantity) || quantity <= 0) {
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
        options.clear();
        optionPrices.clear();
        extraOptionIndexes.clear();
        extraIngredients.clear();
        extraQuantities.clear();
        destroyed = true;
    }

    // เมธอดอ่านข้อมูลเมนูและตัวเลือก; สถานะ enum ถูกแปลงเป็นคำไทย
    public String menuId() {
        return menuId;
    }

    public String name() {
        return name;
    }

    public double price() {
        return price;
    }

    public String category() {
        return category;
    }

    public String station() {
        return station;
    }

    public String statusText() {
        return status == SaleStatus.ON_SALE ? "เปิดขาย" : "ปิดขาย";
    }

    public boolean isSpiceSelectable() {
        return spiceSelectable;
    }

    public void allowSpiceSelection(boolean value) {
        spiceSelectable = value;
    }

    public ArrayList<Recipe> recipes() {
        return new ArrayList<Recipe>(recipes);
    }

    public ArrayList<String> optionNames() {
        return new ArrayList<String>(options);
    }

    public double optionPrice(int index) {
        return optionPrices.get(index);
    }

    public int extraCount() {
        return extraIngredients.size();
    }

    public int extraOptionIndex(int index) {
        return extraOptionIndexes.get(index);
    }

    public Ingredient extraIngredient(int index) {
        return extraIngredients.get(index);
    }

    public double extraQuantity(int index) {
        return extraQuantities.get(index);
    }

    public boolean isDestroyed() {
        return destroyed;
    }
}
