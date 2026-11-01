package model;

import java.time.LocalDateTime;

// Payment คำนวณเงินและแต้ม ส่วน Main รับคำตอบจากผู้ใช้และแสดงใบเสร็จ
public class Payment {
    public enum PayMethod { CASH, QR }
    // เก็บยอดและวิธีชำระของหนึ่งบิล; confirm() จะเปลี่ยนข้อมูลสมาชิกและออเดอร์
    private String paymentId;
    // has-a (Association): Payment อ้างถึง Order และ Employee ผู้รับเงิน
    private Order order;
    private Employee receivedBy;
    private PayMethod method;
    private double received;
    private double change;
    private double discount;
    private double netAmount;
    private int pointsToRedeem;
    private int earnedPoints;
    private LocalDateTime time;
    private String receiptNo;
    private boolean confirmed;

    // ผูกการชำระกับออเดอร์และผู้รับเงิน พร้อมสร้างเลขใบเสร็จ
    public Payment(String paymentId, Order order, Employee by) {
        this.paymentId = paymentId;
        this.order = order;
        this.receivedBy = by;
        this.receiptNo = "RCT-" + paymentId;
    }

    // ตรวจสิทธิ์แลกแต้มและคืนมูลค่าส่วนลด
    public double calculateDiscount(int points) {
        if (points < 0) throw new IllegalArgumentException("แต้มต้องไม่ติดลบ");
        Member member = order.linkedMember();
        if (points > 0 && (member == null || points < Member.minimumRedeem()
                || points > member.points()
                || points * Member.pointValue() > order.calculateTotal()))
            throw new IllegalArgumentException("สมาชิกหรือจำนวนแต้มไม่ผ่านเงื่อนไข");
        pointsToRedeem = points;
        return points * Member.pointValue();
    }

    // คำนวณเงินทอนจากเงินรับลบยอดสุทธิ
    public double calculateChange() {
        if (method == null) throw new IllegalStateException("ยังไม่ได้เลือกวิธีชำระ");
        return Math.round((received - netAmount) * 100.0) / 100.0;
    }

    // ตรวจวิธีชำระ แต้ม และเงินรับ แล้วคำนวณยอดสุทธิ
    public void pay(PayMethod method, double received) {
        if (method == null) throw new IllegalArgumentException("ต้องเลือกวิธีชำระ");
        pay(method == PayMethod.CASH ? "เงินสด" : "QR", received, pointsToRedeem);
    }

    // ตรวจวิธีชำระ แต้ม และเงินรับ แล้วคำนวณยอดสุทธิ
    public void pay(String method, double received, int points) {
        // pay() คำนวณและเตรียมบิลก่อน ยังไม่หักแต้มและยังไม่ปิดออเดอร์
        if (confirmed || order.payment() != null || !order.isServed()) {
            throw new IllegalStateException("ต้องเสิร์ฟครบและยังไม่ชำระ");
        }
        if (!method.equals("เงินสด") && !method.equals("QR"))
            throw new IllegalArgumentException("ช่องทางไม่ถูกต้อง");
        if (points < 0 || !Double.isFinite(received))
            throw new IllegalArgumentException("เงินหรือแต้มไม่ถูกต้อง");
        Member member = order.linkedMember();
        if (points > 0) {
            if (member == null || points < Member.minimumRedeem() || points > member.points()) {
                throw new IllegalArgumentException("สมาชิกหรือจำนวนแต้มไม่ผ่านเงื่อนไข");
            }
        }
        double total = order.calculateTotal();
        double reduction = points * Member.pointValue();
        if (reduction > total)
            throw new IllegalArgumentException("ส่วนลดเกินยอดบิล");
        double due = Math.round((total - reduction) * 100.0) / 100.0;
        if (method.equals("เงินสด") && received < due)
            throw new IllegalArgumentException("เงินไม่พอ");
        this.method = method.equals("เงินสด") ? PayMethod.CASH : PayMethod.QR;
        this.pointsToRedeem = points;
        this.discount = reduction;
        this.netAmount = due;
        if (method.equals("QR"))
            this.received = due;
        else
            this.received = received;
        this.change = calculateChange();
    }

    // หักแต้มที่ใช้ เพิ่มแต้มที่ได้ และปิดออเดอร์ครั้งเดียว
    public void confirm() {
        if (confirmed || order.payment() != null || method == null || !order.isServed()) {
            throw new IllegalStateException("ยังไม่พร้อมชำระ หรือยืนยันไปแล้ว");
        }
        Member member = order.linkedMember();
        // เปลี่ยนยอดแต้มจริงที่นี่ เมื่อผู้ใช้ยืนยันชำระแล้วเท่านั้น
        if (pointsToRedeem > 0) {
            if (member == null || pointsToRedeem > member.points() || pointsToRedeem < Member.minimumRedeem()) {
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

    // เมธอดอ่านยอดชำระที่คำนวณแล้วเพื่อแสดงใบเสร็จและรายงาน

    public String receiptNo() {
        return receiptNo;
    }

    public Order order() {
        return order;
    }

    public Employee employee() {
        return receivedBy;
    }

    public String method() {
        if (method == null) return null;
        return method == PayMethod.CASH ? "เงินสด" : "QR";
    }

    public double received() {
        return received;
    }

    public double change() {
        return change;
    }

    public double discount() {
        return discount;
    }

    public double netAmount() {
        return netAmount;
    }

    public int pointsToRedeem() {
        return pointsToRedeem;
    }

    public int earnedPoints() {
        return earnedPoints;
    }

    public LocalDateTime time() {
        return time;
    }

    public boolean isConfirmed() {
        return confirmed;
    }

    // สร้างข้อความใบเสร็จหลังยืนยันการชำระ
    public String printReceipt() {
        if (!confirmed) throw new IllegalStateException("ต้องยืนยันการชำระก่อนพิมพ์ใบเสร็จ");
        return "ใบเสร็จ " + receiptNo + "\nออเดอร์ " + order.orderId()
                + "\nยอดสุทธิ " + String.format("%.2f", netAmount)
                + " บาท\nรับเงิน " + String.format("%.2f", received)
                + " บาท\nเงินทอน " + String.format("%.2f", change) + " บาท";
    }
}
