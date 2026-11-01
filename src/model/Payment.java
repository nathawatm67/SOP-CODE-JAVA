package model;

import java.time.LocalDateTime;

// Payment คำนวณเงินและแต้ม ส่วน Main รับคำตอบจากผู้ใช้และแสดงใบเสร็จ
public class Payment {
    private String paymentId;
    private Order order;
    private Employee employee;
    private String method;
    private double received;
    private double change;
    private double discount;
    private double netAmount;
    private int pointsToRedeem;
    private int earnedPoints;
    private LocalDateTime time;
    private boolean confirmed;

    public Payment(String paymentId, Order order, Employee employee) {
        this.paymentId = paymentId;
        this.order = order;
        this.employee = employee;
    }

    public void pay(String method, double received, int points) {
        if (confirmed || order.getPayment() != null || !order.isServed()) {
            throw new IllegalStateException("ต้องเสิร์ฟครบและยังไม่ชำระ");
        }
        if (!method.equals("เงินสด") && !method.equals("QR"))
            throw new IllegalArgumentException("ช่องทางไม่ถูกต้อง");
        if (points < 0 || !Double.isFinite(received))
            throw new IllegalArgumentException("เงินหรือแต้มไม่ถูกต้อง");
        Member member = order.getMember();
        if (points > 0) {
            if (member == null || points < Member.getMinRedeem() || points > member.getPoints()) {
                throw new IllegalArgumentException("สมาชิกหรือจำนวนแต้มไม่ผ่านเงื่อนไข");
            }
        }
        double total = order.calculateTotal();
        double reduction = points * Member.getPointValue();
        if (reduction > total)
            throw new IllegalArgumentException("ส่วนลดเกินยอดบิล");
        double due = Math.round((total - reduction) * 100.0) / 100.0;
        if (method.equals("เงินสด") && received < due)
            throw new IllegalArgumentException("เงินไม่พอ");
        this.method = method;
        this.pointsToRedeem = points;
        this.discount = reduction;
        this.netAmount = due;
        if (method.equals("QR"))
            this.received = due;
        else
            this.received = received;
        this.change = Math.round((this.received - due) * 100.0) / 100.0;
    }

    public void confirm() {
        if (confirmed || order.getPayment() != null || method == null || !order.isServed()) {
            throw new IllegalStateException("ยังไม่พร้อมชำระ หรือยืนยันไปแล้ว");
        }
        Member member = order.getMember();
        if (pointsToRedeem > 0) {
            if (member == null || pointsToRedeem > member.getPoints() || pointsToRedeem < Member.getMinRedeem()) {
                throw new IllegalStateException("แต้มเปลี่ยน กรุณาคำนวณการชำระใหม่");
            }
            member.redeemPoints(pointsToRedeem, this);
        }
        if (member != null)
            earnedPoints = member.earnPoints(netAmount, this);
        time = LocalDateTime.now();
        confirmed = true;
        order.markPaid(this);
    }

    public String getPaymentId() {
        return paymentId;
    }

    public String getReceiptNo() {
        return "RCT-" + paymentId;
    }

    public Order getOrder() {
        return order;
    }

    public Employee getEmployee() {
        return employee;
    }

    public String getMethod() {
        return method;
    }

    public double getReceived() {
        return received;
    }

    public double getChange() {
        return change;
    }

    public double getDiscount() {
        return discount;
    }

    public double getNetAmount() {
        return netAmount;
    }

    public int getPointsToRedeem() {
        return pointsToRedeem;
    }

    public int getEarnedPoints() {
        return earnedPoints;
    }

    public LocalDateTime getTime() {
        return time;
    }

    public boolean isConfirmed() {
        return confirmed;
    }
}
