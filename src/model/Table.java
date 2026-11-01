package model;

// โต๊ะหนึ่งตัวเป็น object ที่มีรหัส QR จำนวนที่นั่ง และสถานะของตัวเอง
public class Table {
    private String tableId;
    private String qrCode;
    private int seatCapacity;
    private String status;

    // Constructor ถูกเรียกเมื่อใช้ new Table(...)
    public Table(String tableId, String qrCode, int seatCapacity) {
        this.tableId = tableId;
        this.qrCode = qrCode;
        this.seatCapacity = seatCapacity;
        this.status = "ว่าง";
    }

    public String getTableId() {
        return tableId;
    }

    public String getQrCode() {
        return qrCode;
    }

    public int getSeatCapacity() {
        return seatCapacity;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }
}
