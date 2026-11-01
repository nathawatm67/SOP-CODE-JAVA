package model;

import java.util.ArrayList;
import java.util.List;

// ข้อมูลสมาชิกเป็นของแต่ละ object แต่กฎแต้มเป็น static จึงใช้ร่วมกันทั้งร้าน
public class Member {
    // ข้อมูลและประวัติเป็นของสมาชิกแต่ละคน
    private String memberId;
    private String name;
    private String phone;
    private int points;
    // has-a (Composition): Member เป็นเจ้าของประวัติ PointTransaction
    // เมื่อทำลาย Member จะทำลายประวัติแต้มของสมาชิกคนนี้ด้วย
    private List<PointTransaction> transactions;
    private boolean destroyed;
    // กฎ static ใช้ร่วมกันทุกสมาชิก เมื่อผู้จัดการเปลี่ยนจึงมีผลทั้งร้าน
    private static int bahtPerPoint = 50;
    private static double pointValue = 1;
    private static int minRedeem = 10;

    // สร้างสมาชิกพร้อมตรวจรูปแบบเบอร์โทร
    public Member(String memberId, String name, String phone) {
        this.memberId = memberId;
        this.name = name;
        changePhone(phone);
        this.transactions = new ArrayList<PointTransaction>();
    }

    // คำนวณแต้มจากยอดสุทธิ เพิ่มยอด และบันทึกประวัติ
    public int earnPoints(double netAmount, Payment payment) {
        if (!Double.isFinite(netAmount) || netAmount < 0)
            throw new IllegalArgumentException("ยอดติดลบไม่ได้");
        int earned = (int) (netAmount / bahtPerPoint);
        if (earned > 0) {
            points += earned;
            addTransaction("สะสม", earned, payment);
        }
        return earned;
    }

    // คำนวณแต้มจากยอดสุทธิ เพิ่มยอด และบันทึกประวัติ
    public int earnPoints(double amount) {
        return earnPoints(amount, null);
    }

    // ตรวจขั้นต่ำและแต้มคงเหลือก่อนหักแต้ม
    public void redeemPoints(int use, Payment payment) {
        if (use < minRedeem || use > points)
            throw new IllegalArgumentException("แต้มไม่พอหรือไม่ถึงขั้นต่ำ");
        points -= use;
        addTransaction("แลก", use, payment);
    }

    // ตรวจขั้นต่ำและแต้มคงเหลือก่อนหักแต้ม
    public void redeemPoints(int points) {
        redeemPoints(points, null);
    }

    // ตรวจเกณฑ์ส่วนลดกลางของร้าน; จำนวนแต้มคงเหลืออยู่ที่สมาชิกแต่ละคน
    public static boolean validateRedeem(int points, double amount) {
        return points >= minRedeem && Double.isFinite(amount)
                && amount >= 0 && points * pointValue <= amount;
    }

    private void addTransaction(String type, int amount, Payment payment) {
        String id = memberId + "-PTX-" + (transactions.size() + 1);
        transactions.add(new PointTransaction(id, type, amount, points, payment));
    }

    // เปลี่ยนกฎกลางของร้านที่สมาชิกทุกคนใช้ร่วมกัน
    public static void setRule(int b, double v, int m) {
        if (b <= 0 || !Double.isFinite(v) || v <= 0 || m <= 0)
            throw new IllegalArgumentException("ค่ากฎแต้มต้องมากกว่า 0");
        bahtPerPoint = b;
        pointValue = v;
        minRedeem = m;
    }

    public void destroy() {
        for (int i = 0; i < transactions.size(); i++)
            transactions.get(i).destroy();
        transactions.clear();
        destroyed = true;
    }

    // เมธอดอ่านข้อมูลสมาชิกและกฎแต้มเพื่อแสดงหน้าจอ
    public String memberId() {
        return memberId;
    }

    public String name() {
        return name;
    }

    // เปลี่ยนชื่อสมาชิกหลังสมัคร
    public void rename(String name) {
        this.name = name;
    }

    public String phone() {
        return phone;
    }

    // ตรวจเบอร์ 10 หลักก่อนเปลี่ยนข้อมูลสมาชิก
    public void changePhone(String phone) {
        if (!phone.matches("0[0-9]{9}"))
            throw new IllegalArgumentException("เบอร์โทรต้องมี 10 หลักขึ้นต้นด้วย 0");
        this.phone = phone;
    }

    public int points() {
        return points;
    }

    public List<PointTransaction> transactions() {
        return transactions;
    }

    public static int bahtPerPoint() {
        return bahtPerPoint;
    }

    public static double pointValue() {
        return pointValue;
    }

    public static int minimumRedeem() {
        return minRedeem;
    }

    public boolean isDestroyed() {
        return destroyed;
    }
}
