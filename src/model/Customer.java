package model;

// ลูกค้าไม่จำเป็นต้องเป็นสมาชิก จึงให้ member เป็น null ได้
public class Customer {
    // ลูกค้าทั่วไปมี member เป็น null; ผูกสมาชิกเมื่อแจ้งเบอร์โทร
    private String customerId;
    // has-a (Association): Customer ผูกกับ Member ได้ แต่ไม่ได้เป็นเจ้าของ Member
    private Member member;

    // สร้างลูกค้าใหม่; member เริ่มเป็น null จนกว่าจะผูกสมาชิก
    public Customer(String customerId) {
        this.customerId = customerId;
    }

    // อ่านบัญชีสมาชิกที่ลูกค้าเชื่อมไว้ เพื่อใช้คำนวณแต้มตอนชำระเงิน
    public Member linkedMember() {
        return member;
    }

    // ผูกสมาชิกภายหลังได้ เพราะลูกค้าเริ่มสั่งอาหารโดยยังไม่เป็นสมาชิก
    public void linkMember(Member member) {
        this.member = member;
    }

    // P7: + checkCustomerStatus() : boolean
    // คืน true เมื่อเชื่อมบัญชีสมาชิกแล้ว และคืน false เมื่อยังไม่ได้เชื่อม
    public boolean checkCustomerStatus() {
        if (member == null) {
            return false;
        }
        return true;
    }
}
