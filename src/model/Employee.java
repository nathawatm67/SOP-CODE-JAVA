package model;

// พนักงานแต่ละคนมีบทบาท เช่น ผู้จัดการ แคชเชียร์ หรือคนครัว
public class Employee {
    public enum Role { MANAGER, CASHIER, COOK }

    // ข้อมูลประจำตัวพนักงาน; station เปลี่ยนได้เมื่อรับหน้าที่ในครัว
    private String employeeId;
    private String name;
    private Role role;
    private String station;

    // สร้างพนักงานโดยระบุรหัส ชื่อ และบทบาท
    public Employee(String employeeId, String name, Role role) {
        this.employeeId = employeeId;
        this.name = name;
        this.role = role;
        this.station = "ยังไม่กำหนด";
    }

    // รับคำภาษาไทยจาก Main เพื่อให้อ่านตัวอย่างได้ง่าย
    public Employee(String employeeId, String name, String role) {
        this(employeeId, name, parseRole(role));
    }

    // แปลงคำบทบาทภาษาไทยจากหน้าจอเป็นค่า Role
    private static Role parseRole(String text) {
        if (text.equals("ผู้จัดการ")) return Role.MANAGER;
        if (text.equals("แคชเชียร์")) return Role.CASHIER;
        if (text.equals("คนครัว")) return Role.COOK;
        throw new IllegalArgumentException("บทบาทพนักงานไม่ถูกต้อง");
    }

    // ตรวจสิทธิ์ว่าบทบาทตรงกับงานที่กำหนดหรือไม่
    public boolean authenticateRole(Role requiredRole) {
        return role == requiredRole;
    }

    // บันทึกสถานีครัวที่พนักงานรับผิดชอบ
    public void assignStationDuty(String station) {
        this.station = station;
    }

    // เมธอดด้านล่างให้ Main อ่านรหัส ชื่อ บทบาท และสถานีของพนักงาน

    public String name() { return name; }
    public String roleName() {
        if (role == Role.MANAGER) return "ผู้จัดการ";
        if (role == Role.CASHIER) return "แคชเชียร์";
        return "คนครัว";
    }
    public String station() { return station; }
}
