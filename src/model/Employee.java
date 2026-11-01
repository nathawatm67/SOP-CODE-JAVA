package model;

// พนักงานแต่ละคนมีบทบาท เช่น ผู้จัดการ แคชเชียร์ หรือคนครัว
public class Employee {
    private String employeeId;
    private String name;
    private String role;
    private String station;

    public Employee(String employeeId, String name, String role) {
        this.employeeId = employeeId;
        this.name = name;
        this.role = role;
        this.station = "ยังไม่กำหนด";
    }

    public String getEmployeeId() { return employeeId; }
    public String getName() { return name; }
    public String getRole() { return role; }
    public String getStation() { return station; }
    public void setStation(String station) { this.station = station; }
}
