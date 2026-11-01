package model;

import java.util.ArrayList;

// ข้อมูลสมาชิกเป็นของแต่ละ object แต่กฎแต้มเป็น static จึงใช้ร่วมกันทั้งร้าน
public class Member {
    private String memberId;
    private String name;
    private String phone;
    private int points;
    private ArrayList<PointTransaction> transactions;
    private boolean destroyed;
    private static int bahtPerPoint = 50;
    private static double pointValue = 1;
    private static int minRedeem = 10;

    public Member(String id, String name, String phone) {
        this.memberId = id;
        this.name = name;
        setPhone(phone);
        this.transactions = new ArrayList<PointTransaction>();
    }

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

    public void redeemPoints(int use, Payment payment) {
        if (use < minRedeem || use > points)
            throw new IllegalArgumentException("แต้มไม่พอหรือไม่ถึงขั้นต่ำ");
        points -= use;
        addTransaction("แลก", use, payment);
    }

    private void addTransaction(String type, int amount, Payment payment) {
        String id = memberId + "-PTX-" + (transactions.size() + 1);
        transactions.add(new PointTransaction(id, type, amount, points, payment));
    }

    public static void setRule(int baht, double value, int minimum) {
        if (baht <= 0 || !Double.isFinite(value) || value <= 0 || minimum <= 0)
            throw new IllegalArgumentException("ค่ากฎแต้มต้องมากกว่า 0");
        bahtPerPoint = baht;
        pointValue = value;
        minRedeem = minimum;
    }

    public void destroy() {
        for (int i = 0; i < transactions.size(); i++)
            transactions.get(i).destroy();
        transactions.clear();
        destroyed = true;
    }

    public String getMemberId() {
        return memberId;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getPhone() {
        return phone;
    }

    public void setPhone(String phone) {
        if (!phone.matches("0[0-9]{9}"))
            throw new IllegalArgumentException("เบอร์โทรต้องมี 10 หลักขึ้นต้นด้วย 0");
        this.phone = phone;
    }

    public int getPoints() {
        return points;
    }

    public ArrayList<PointTransaction> getTransactions() {
        return transactions;
    }

    public static int getBahtPerPoint() {
        return bahtPerPoint;
    }

    public static double getPointValue() {
        return pointValue;
    }

    public static int getMinRedeem() {
        return minRedeem;
    }

    public boolean isDestroyed() {
        return destroyed;
    }
}
