package model;

import java.time.LocalDateTime;

// เก็บประวัติแต้มหนึ่งครั้ง พร้อมใบชำระเงินที่เกี่ยวข้อง (ถ้ามี)
public class PointTransaction {
    public enum PointType { EARN, REDEEM }
    // หนึ่ง object คือแต้มเพิ่มหรือแต้มลดหนึ่งครั้ง พร้อมยอดหลังทำรายการ
    private String pointTransactionId;
    private LocalDateTime date;
    private PointType type;
    private int points;
    private int balance;
    // has-a (Association): ประวัติแต้มอาจอ้างถึง Payment แต่ไม่ได้เป็นเจ้าของใบชำระ
    private Payment payment;
    private boolean destroyed;

    // สร้างประวัติแต้มหนึ่งรายการพร้อมยอดคงเหลือหลังรายการ
    public PointTransaction(String pointTransactionId, PointType type, int points, int balance) {
        this.pointTransactionId = pointTransactionId;
        this.date = LocalDateTime.now();
        this.type = type;
        this.points = points;
        this.balance = balance;
    }

    // สร้างประวัติแต้มหนึ่งรายการพร้อมยอดคงเหลือหลังรายการ
    public PointTransaction(String pointTransactionId, String type, int points, int balance, Payment payment) {
        this(pointTransactionId, type.equals("สะสม") ? PointType.EARN : PointType.REDEEM, points, balance);
        this.payment = payment;
    }

    // บันทึกชนิด จำนวน และใบชำระเงินที่เกี่ยวข้อง
    public void recordPointTransaction(PointType type, int points, int balance, Payment payment) {
        if (this.payment != null) throw new IllegalStateException("บันทึกรายการแต้มแล้ว");
        this.type = type;
        this.points = points;
        this.balance = balance;
        this.payment = payment;
        this.date = LocalDateTime.now();
    }

    public void destroy() {
        destroyed = true;
        payment = null;
    }

    // เมธอดอ่านประวัติแต้ม; typeText() แปลง enum เป็นคำภาษาไทย

    public LocalDateTime time() {
        return date;
    }

    public String typeText() {
        return type == PointType.EARN ? "สะสม" : "แลก";
    }

    public int points() {
        return points;
    }

    public int balance() {
        return balance;
    }

    public Payment payment() {
        return payment;
    }

    public boolean isDestroyed() {
        return destroyed;
    }
}
