package model;

import java.time.LocalDateTime;
import java.time.Duration;
import java.util.ArrayList;

// อาหารหนึ่งรายการ เก็บราคาและสูตร ณ ตอนสั่ง เพื่อไม่ให้เมนูที่แก้ภายหลังเปลี่ยนบิลเก่า
public class OrderItem {
    private String orderItemId;
    private Menu menu;
    private Recipe recipe;
    private int quantity;
    private double unitPrice;
    private String spice;
    private String note;
    private String status;
    private LocalDateTime startTime;
    private LocalDateTime endTime;
    private double standardMinutes;
    private Employee handledBy;
    private String requestReason;
    private String requestType;
    private String requestStatus;
    private String decisionReason;
    private String requestedNote;
    private boolean stockDeducted;
    private boolean destroyed;
    private ArrayList<String> optionNames;
    private ArrayList<Ingredient> ingredients;
    private ArrayList<Double> quantities;

    public OrderItem(String id, Menu menu, int quantity, String spice, String note) {
        if (quantity <= 0)
            throw new IllegalArgumentException("จำนวนต้องมากกว่า 0");
        this.orderItemId = id;
        this.menu = menu;
        this.recipe = menu.getCurrentRecipe();
        if (recipe == null)
            throw new IllegalArgumentException("เมนูยังไม่มีสูตรสมบูรณ์");
        this.quantity = quantity;
        this.unitPrice = menu.getPrice();
        this.spice = spice;
        this.note = note;
        this.status = "รอปรุง";
        this.requestStatus = "ไม่มี";
        this.optionNames = new ArrayList<String>();
        this.ingredients = new ArrayList<Ingredient>();
        this.quantities = new ArrayList<Double>();
        for (int i = 0; i < recipe.getIngredients().size(); i++) {
            ingredients.add(recipe.getIngredients().get(i));
            quantities.add(recipe.getQuantity(i));
        }
    }

    public void addOption(int index) {
        if (stockDeducted)
            throw new IllegalStateException("แก้ตัวเลือกหลังส่งครัวไม่ได้");
        String name = menu.getOptionNames().get(index);
        if (optionNames.contains(name))
            throw new IllegalArgumentException("เลือกตัวเลือกนี้แล้ว");
        optionNames.add(name);
        unitPrice += menu.getOptionPrice(index);
        for (int i = 0; i < menu.getExtraCount(); i++) {
            if (menu.getExtraOptionIndex(i) == index) {
                ingredients.add(menu.getExtraIngredient(i));
                quantities.add(menu.getExtraQuantity(i));
            }
        }
    }

    // รวมปริมาณของวัตถุดิบเดียวกันทั้งสูตรและตัวเลือก โดยคิดต่อหนึ่งจาน
    public double amountPerDish(Ingredient ingredient) {
        double total = 0;
        for (int i = 0; i < ingredients.size(); i++) {
            if (ingredients.get(i) == ingredient)
                total += quantities.get(i);
        }
        return total;
    }

    // เข้าถึงได้จาก Order ใน package model เพื่อให้ Order คุมการเปลี่ยนจำนวน
    void changeQuantity(int quantity) {
        this.quantity = quantity;
    }

    void markConfirmed() {
        stockDeducted = true;
        menu.noteOrdered();
    }

    public void startCooking(Employee cook, double standardMinutes) {
        if (!stockDeducted || !status.equals("รอปรุง"))
            throw new IllegalStateException("ต้องยืนยันและยังรอปรุงอยู่");
        this.status = "กำลังปรุง";
        this.startTime = LocalDateTime.now();
        this.standardMinutes = standardMinutes;
        this.handledBy = cook;
    }

    public void markReady() {
        if (requestStatus.equals("รออนุมัติ"))
            throw new IllegalStateException("ให้ผู้จัดการพิจารณาคำขอก่อนปรุงเสร็จ");
        if (!status.equals("กำลังปรุง"))
            throw new IllegalStateException("ต้องกำลังปรุง");
        status = "พร้อมเสิร์ฟ";
        endTime = LocalDateTime.now();
    }

    public void serve(Employee employee) {
        if (!status.equals("พร้อมเสิร์ฟ"))
            throw new IllegalStateException("ต้องพร้อมเสิร์ฟ");
        status = "เสิร์ฟแล้ว";
        handledBy = employee;
    }

    public double getCookingMinutes() {
        if (startTime == null || endTime == null)
            return 0;
        return Duration.between(startTime, endTime).getSeconds() / 60.0;
    }

    public void cancel() {
        if (!status.equals("รอปรุง"))
            throw new IllegalStateException("เริ่มปรุงแล้วต้องส่งคำขอผู้จัดการ");
        forceCancel();
    }

    private void forceCancel() {
        if (status.equals("ยกเลิก"))
            return;
        // คืนเฉพาะสต็อกที่เคยตัดจริง ตะกร้าที่ยังไม่ยืนยันจึงไม่ทำให้สต็อกเพิ่ม
        if (stockDeducted) {
            for (int i = 0; i < ingredients.size(); i++) {
                ingredients.get(i).restore(quantities.get(i) * quantity, orderItemId);
            }
            stockDeducted = false;
        }
        status = "ยกเลิก";
    }

    public void requestChange(String type, String reason, String newNote) {
        if (!status.equals("กำลังปรุง") || requestStatus.equals("รออนุมัติ")) {
            throw new IllegalStateException("ขอได้เฉพาะรายการกำลังปรุงที่ไม่มีคำขอค้าง");
        }
        if (!type.equals("ยกเลิก") && !type.equals("แก้หมายเหตุ"))
            throw new IllegalArgumentException("ชนิดคำขอไม่ถูกต้อง");
        if (reason.trim().isEmpty())
            throw new IllegalArgumentException("ต้องระบุเหตุผล");
        requestType = type;
        requestReason = reason;
        requestedNote = newNote;
        requestStatus = "รออนุมัติ";
        decisionReason = "";
    }

    public void decideRequest(boolean approve, String reason, Employee manager) {
        if (!manager.getRole().equals("ผู้จัดการ"))
            throw new IllegalArgumentException("ต้องเป็นผู้จัดการ");
        if (!requestStatus.equals("รออนุมัติ"))
            throw new IllegalStateException("ไม่มีคำขอค้าง");
        if (approve) {
            if (requestType.equals("ยกเลิก"))
                forceCancel();
            else
                note = requestedNote;
            requestStatus = "อนุมัติ";
        } else {
            if (reason.trim().isEmpty())
                throw new IllegalArgumentException("ต้องระบุเหตุผลปฏิเสธ");
            requestStatus = "ปฏิเสธ";
        }
        decisionReason = manager.getName() + ": " + reason;
    }

    public void destroy() {
        ingredients.clear();
        quantities.clear();
        optionNames.clear();
        menu = null;
        recipe = null;
        handledBy = null;
        destroyed = true;
    }

    public String getOrderItemId() {
        return orderItemId;
    }

    public Menu getMenu() {
        return menu;
    }

    public Recipe getRecipe() {
        return recipe;
    }

    public int getQuantity() {
        return quantity;
    }

    public double getPrice() {
        return unitPrice * quantity;
    }

    public String getSpice() {
        return spice;
    }

    public String getNote() {
        return note;
    }

    public void setNote(String note) {
        this.note = note;
    }

    public String getStatus() {
        return status;
    }

    public ArrayList<String> getOptionNames() {
        return optionNames;
    }

    public ArrayList<Ingredient> getIngredients() {
        return ingredients;
    }

    public double getStandardMinutes() {
        return standardMinutes;
    }

    public String getRequestStatus() {
        return requestStatus;
    }

    public String getRequestReason() {
        return requestReason;
    }

    public String getRequestType() {
        return requestType;
    }

    public String getDecisionReason() {
        return decisionReason;
    }

    public boolean isDestroyed() {
        return destroyed;
    }
}
