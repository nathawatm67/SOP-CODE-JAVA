package model;

// ลูกค้าไม่จำเป็นต้องเป็นสมาชิก จึงให้ member เป็น null ได้
public class Customer {
    private String customerId;
    private Member member;

    public Customer(String customerId) {
        this.customerId = customerId;
    }

    public String getCustomerId() {
        return customerId;
    }

    public Member getMember() {
        return member;
    }

    public void setMember(Member member) {
        this.member = member;
    }

    public boolean isMember() {
        return member != null;
    }
}
