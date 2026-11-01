package model;

import java.time.LocalDateTime;

// เก็บประวัติแต้มหนึ่งครั้ง พร้อมใบชำระเงินที่เกี่ยวข้อง (ถ้ามี)
public class PointTransaction {
    private String pointTransactionId;
    private LocalDateTime time;
    private String type;
    private int points;
    private int balance;
    private Payment payment;
    private boolean destroyed;

    public PointTransaction(String id, String type, int points, int balance, Payment payment) {
        this.pointTransactionId = id;
        this.time = LocalDateTime.now();
        this.type = type;
        this.points = points;
        this.balance = balance;
        this.payment = payment;
    }

    public void destroy() {
        destroyed = true;
        payment = null;
    }

    public String getPointTransactionId() {
        return pointTransactionId;
    }

    public LocalDateTime getTime() {
        return time;
    }

    public String getType() {
        return type;
    }

    public int getPoints() {
        return points;
    }

    public int getBalance() {
        return balance;
    }

    public Payment getPayment() {
        return payment;
    }

    public boolean isDestroyed() {
        return destroyed;
    }
}
