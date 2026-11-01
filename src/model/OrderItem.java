package model;

import java.time.LocalDateTime;
import java.time.Duration;
import java.util.ArrayList;

// อาหารหนึ่งรายการ เก็บราคาและสูตร ณ ตอนสั่ง เพื่อไม่ให้เมนูที่แก้ภายหลังเปลี่ยนบิลเก่า
public class OrderItem {
    public enum ItemStatus { WAITING, COOKING, READY, SERVED, CANCELLED }
    public enum RequestType { CANCEL, CHANGE_NOTE }
    public enum RequestStatus { NONE, PENDING, APPROVED, REJECTED }
    // ราคาและส่วนผสมเป็นสำเนาตอนสั่ง บิลเก่าจึงไม่เปลี่ยนเมื่อแก้ Menu/Recipe
    private String orderItemId;
    // has-a (Association): อาหารอ้างถึง Menu และ Recipe ที่มีอยู่แล้ว
    // OrderItem เก็บสำเนาราคา/ปริมาณ แต่ไม่ทำลาย Menu หรือ Recipe
    private Menu menu;
    private Recipe recipe;
    private int qty;
    private double price;
    private String spiceLevel;
    private String note;
    private String option;
    private ItemStatus status;
    private LocalDateTime startTime;
    private LocalDateTime endTime;
    private double standardMinutes;
    // has-a (Association): พนักงานผู้จัดการรายการ ไม่ได้ถูก OrderItem เป็นเจ้าของ
    private Employee handledBy;
    private String requestReason;
    private RequestType requestType;
    private RequestStatus requestStatus;
    private String decisionReason;
    private String requestedNote;
    private LocalDateTime requestedAt;
    private String decidedBy;
    // ธงนี้ช่วยคืนสต็อกเฉพาะรายการที่เคยตัดจริง
    private boolean stockDeducted;
    private boolean destroyed;
    private ArrayList<String> optionNames;
    private ArrayList<Ingredient> ingredients;
    private ArrayList<Double> quantities;

    // สร้างอาหารหนึ่งบรรทัดและคัดลอกราคา/สูตร ณ เวลาที่สั่ง
    public OrderItem(String orderItemId, Menu menu, int qty, Recipe recipe) {
        this(orderItemId, menu, qty, "ไม่ระบุ", "");
        if (recipe != null && recipe != this.recipe)
            throw new IllegalArgumentException("สูตรไม่ตรงกับเมนูที่เลือก");
    }

    // สร้างอาหารหนึ่งบรรทัดและคัดลอกราคา/สูตร ณ เวลาที่สั่ง
    public OrderItem(String orderItemId, Menu menu, int qty, String spiceLevel, String note) {
        if (qty <= 0)
            throw new IllegalArgumentException("จำนวนต้องมากกว่า 0");
        this.orderItemId = orderItemId;
        this.menu = menu;
        this.recipe = menu.currentRecipe();
        if (recipe == null)
            throw new IllegalArgumentException("เมนูยังไม่มีสูตรสมบูรณ์");
        this.qty = qty;
        this.price = menu.price();
        this.spiceLevel = spiceLevel;
        this.note = note;
        this.status = ItemStatus.WAITING;
        this.requestStatus = RequestStatus.NONE;
        this.optionNames = new ArrayList<String>();
        this.ingredients = new ArrayList<Ingredient>();
        this.quantities = new ArrayList<Double>();
        for (int i = 0; i < recipe.ingredients().size(); i++) {
            ingredients.add(recipe.ingredients().get(i));
            quantities.add(recipe.quantity(i));
        }
    }

    // เพิ่มตัวเลือก ราคา และวัตถุดิบที่ใช้เพิ่มก่อนส่งครัว
    public void addOption(int index) {
        if (stockDeducted)
            throw new IllegalStateException("แก้ตัวเลือกหลังส่งครัวไม่ได้");
        String name = menu.optionNames().get(index);
        if (optionNames.contains(name))
            throw new IllegalArgumentException("เลือกตัวเลือกนี้แล้ว");
        optionNames.add(name);
        option = String.join(", ", optionNames);
        price += menu.optionPrice(index);
        for (int i = 0; i < menu.extraCount(); i++) {
            if (menu.extraOptionIndex(i) == index) {
                ingredients.add(menu.extraIngredient(i));
                quantities.add(menu.extraQuantity(i));
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
    void changeQuantity(int qty) {
        this.qty = qty;
    }

    // จำว่าสต็อกถูกตัดแล้วและเมนูนี้เคยถูกสั่ง
    void markConfirmed() {
        stockDeducted = true;
        menu.noteOrdered();
    }

    // เปลี่ยนจากรอปรุงเป็นกำลังปรุง และจดเวลาเริ่ม
    public void startCooking(Employee cook, double standardMinutes) {
        if (!stockDeducted || status != ItemStatus.WAITING)
            throw new IllegalStateException("ต้องยืนยันและยังรอปรุงอยู่");
        this.status = ItemStatus.COOKING;
        this.startTime = LocalDateTime.now();
        this.standardMinutes = standardMinutes;
        this.handledBy = cook;
    }

    // เปลี่ยนจากรอปรุงเป็นกำลังปรุง และจดเวลาเริ่ม
    public void startCooking(Employee cook) {
        startCooking(cook, 0);
    }

    // จดเวลาจบเมื่อปรุงเสร็จ และห้ามข้ามคำขอที่รออนุมัติ
    public void markReady() {
        if (requestStatus == RequestStatus.PENDING)
            throw new IllegalStateException("ให้ผู้จัดการพิจารณาคำขอก่อนปรุงเสร็จ");
        if (status != ItemStatus.COOKING)
            throw new IllegalStateException("ต้องกำลังปรุง");
        status = ItemStatus.READY;
        endTime = LocalDateTime.now();
    }

    // เปลี่ยนจากพร้อมเสิร์ฟเป็นเสิร์ฟแล้ว
    public void serve(Employee by) {
        if (status != ItemStatus.READY)
            throw new IllegalStateException("ต้องพร้อมเสิร์ฟ");
        status = ItemStatus.SERVED;
        handledBy = by;
    }

    // หานาทีจริงจากเวลาเริ่มถึงเวลาจบ
    public double cookingMinutes() {
        if (startTime == null || endTime == null)
            return 0;
        return Duration.between(startTime, endTime).getSeconds() / 60.0;
    }

    // เทียบเวลาจริงกับเวลามาตรฐาน; ค่าบวกหมายถึงเกินเวลา
    public int compareTime() {
        return (int) Math.round(cookingMinutes() - standardMinutes);
    }

    // เปลี่ยนสถานะเฉพาะเส้นทางที่ไม่ข้ามกฎการปรุง
    public void changeStatus(ItemStatus s) {
        if (s == ItemStatus.CANCELLED) { cancel(); return; }
        if (s == ItemStatus.READY) { markReady(); return; }
        throw new IllegalStateException("ใช้ขั้นตอนปรุงและเสิร์ฟที่กำหนดเพื่อเปลี่ยนสถานะ");
    }

    // ยกเลิกอาหารที่ยังรอปรุง
    public void cancel() {
        if (status != ItemStatus.WAITING)
            throw new IllegalStateException("เริ่มปรุงแล้วต้องส่งคำขอผู้จัดการ");
        forceCancel();
    }

    // คืนสต็อกเฉพาะรายการที่เคยตัดจริง แล้วตั้งสถานะยกเลิก
    private void forceCancel() {
        if (status == ItemStatus.CANCELLED)
            return;
        // คืนเฉพาะสต็อกที่เคยตัดจริง ตะกร้าที่ยังไม่ยืนยันจึงไม่ทำให้สต็อกเพิ่ม
        if (stockDeducted) {
            for (int i = 0; i < ingredients.size(); i++) {
                ingredients.get(i).restore(quantities.get(i) * qty, orderItemId);
            }
            stockDeducted = false;
        }
        status = ItemStatus.CANCELLED;
    }

    // บันทึกคำขอและเหตุผลเพื่อรอผู้จัดการพิจารณา
    public void requestChange(String type, String reason, String newNote) {
        if (status != ItemStatus.COOKING || requestStatus == RequestStatus.PENDING) {
            throw new IllegalStateException("ขอได้เฉพาะรายการกำลังปรุงที่ไม่มีคำขอค้าง");
        }
        if (!type.equals("ยกเลิก") && !type.equals("แก้หมายเหตุ"))
            throw new IllegalArgumentException("ชนิดคำขอไม่ถูกต้อง");
        if (reason.trim().isEmpty())
            throw new IllegalArgumentException("ต้องระบุเหตุผล");
        requestType = type.equals("ยกเลิก") ? RequestType.CANCEL : RequestType.CHANGE_NOTE;
        requestReason = reason;
        requestedNote = newNote;
        requestStatus = RequestStatus.PENDING;
        decisionReason = "";
        requestedAt = LocalDateTime.now();
    }

    // บันทึกคำขอและเหตุผลเพื่อรอผู้จัดการพิจารณา
    public void requestChange(RequestType type, String reason) {
        requestChange(type == RequestType.CANCEL ? "ยกเลิก" : "แก้หมายเหตุ", reason, note);
    }

    // ตรวจบทบาทผู้จัดการแล้วอนุมัติหรือปฏิเสธคำขอ
    public void decideRequest(boolean approve, String reason, Employee manager) {
        if (!manager.roleName().equals("ผู้จัดการ"))
            throw new IllegalArgumentException("ต้องเป็นผู้จัดการ");
        if (requestStatus != RequestStatus.PENDING)
            throw new IllegalStateException("ไม่มีคำขอค้าง");
        if (approve) {
            if (requestType == RequestType.CANCEL)
                forceCancel();
            else
                note = requestedNote;
            requestStatus = RequestStatus.APPROVED;
        } else {
            if (reason.trim().isEmpty())
                throw new IllegalArgumentException("ต้องระบุเหตุผลปฏิเสธ");
            requestStatus = RequestStatus.REJECTED;
        }
        decisionReason = manager.name() + ": " + reason;
        decidedBy = manager.name();
    }

    // ชื่อสั้นตาม P7 สำหรับอนุมัติคำขอ
    public void approve(Employee by) { decideRequest(true, "", by); }

    // ชื่อสั้นตาม P7 สำหรับปฏิเสธพร้อมเหตุผล
    public void reject(Employee by, String why) { decideRequest(false, why, by); }

    public void destroy() {
        ingredients.clear();
        quantities.clear();
        optionNames.clear();
        menu = null;
        recipe = null;
        handledBy = null;
        destroyed = true;
    }

    // เมธอดอ่านข้อมูลรายการอาหารและสถานะสำหรับหน้าจอ

    public Menu menu() {
        return menu;
    }

    public Recipe recipe() {
        return recipe;
    }

    public int quantity() {
        return qty;
    }

    // คืนราคารวมของรายการนี้: ราคาต่อจานคูณจำนวน
    public double price() {
        return price * qty;
    }

    public String spice() {
        return spiceLevel;
    }

    public String note() {
        return note;
    }

    public void changeNote(String note) {
        this.note = note;
    }

    public String statusText() {
        switch (status) {
            case WAITING: return "รอปรุง";
            case COOKING: return "กำลังปรุง";
            case READY: return "พร้อมเสิร์ฟ";
            case SERVED: return "เสิร์ฟแล้ว";
            default: return "ยกเลิก";
        }
    }

    public ArrayList<String> optionNames() {
        return optionNames;
    }

    public ArrayList<Ingredient> ingredients() {
        return ingredients;
    }

    public double standardMinutes() {
        return standardMinutes;
    }

    public String requestStatus() {
        switch (requestStatus) {
            case NONE: return "ไม่มี";
            case PENDING: return "รออนุมัติ";
            case APPROVED: return "อนุมัติ";
            default: return "ปฏิเสธ";
        }
    }

    public String requestReason() {
        return requestReason;
    }

    public String requestType() {
        if (requestType == null) return null;
        return requestType == RequestType.CANCEL ? "ยกเลิก" : "แก้หมายเหตุ";
    }

    public String decisionReason() {
        return decisionReason;
    }



    public boolean isDestroyed() {
        return destroyed;
    }
}
