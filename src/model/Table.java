package model;

// โต๊ะหนึ่งตัวเป็น object ที่มีรหัส QR จำนวนที่นั่ง และสถานะของตัวเอง
public class Table {
    // QR ระบุตัวโต๊ะ ส่วนสถานะใช้บอกว่าว่างหรือกำลังใช้งาน
    private String tableId;
    private String qrCode;
    private int seatCapacity;
    private String status;
    private boolean qrScanned;

    // สร้างโต๊ะพร้อม QR และจำนวนที่นั่ง; สถานะเริ่มเป็นว่าง
    public Table(String tableId, String qrCode) {
        this(tableId, qrCode, 4);
    }

    // Constructor ถูกเรียกเมื่อใช้ new Table(...)
    public Table(String tableId, String qrCode, int seatCapacity) {
        this.tableId = tableId;
        this.qrCode = qrCode;
        this.seatCapacity = seatCapacity;
        this.status = "ว่าง";
    }

    // เมธอดอ่านข้อมูลโต๊ะสำหรับแสดงบนหน้าจอ
    public String tableId() {
        return tableId;
    }

    public String qrCode() {
        return qrCode;
    }

    // Terminal จำลองการสแกน: ไม่มีการเปิดกล้องจริง
    public void scanTableQRCode() {
        qrScanned = true;
    }

    // คืนรหัสโต๊ะเมื่อสแกน QR แล้วเท่านั้น
    public String identifyTableNumber() {
        if (!qrScanned) throw new IllegalStateException("ยังไม่ได้สแกน QR ของโต๊ะ");
        return tableId;
    }


    public String statusText() {
        return status;
    }

    // เปลี่ยนสถานะโต๊ะเมื่อเปิดหรือปิดการใช้งาน
    public void changeTableStatus(String status) {
        this.status = status;
    }
}
