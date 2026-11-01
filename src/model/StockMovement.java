package model;

import java.time.LocalDateTime;

// ประวัติหนึ่งครั้ง: เปลี่ยนเท่าไร เหลือเท่าไร เพราะอะไร และใครทำ
public class StockMovement {
    private String stockMovementId;
    private LocalDateTime time;
    private String type;
    private double quantity;
    private double balance;
    private String reference;
    private String reason;
    private Employee employee;
    private boolean destroyed;

    public StockMovement(String id, String type, double quantity, double balance,
            String reference, String reason, Employee employee) {
        this.stockMovementId = id;
        this.time = LocalDateTime.now();
        this.type = type;
        this.quantity = quantity;
        this.balance = balance;
        this.reference = reference;
        this.reason = reason;
        this.employee = employee;
    }

    public void destroy() {
        destroyed = true;
        employee = null;
    }

    public String getStockMovementId() {
        return stockMovementId;
    }

    public LocalDateTime getTime() {
        return time;
    }

    public String getType() {
        return type;
    }

    public double getQuantity() {
        return quantity;
    }

    public double getBalance() {
        return balance;
    }

    public String getReference() {
        return reference;
    }

    public String getReason() {
        return reason;
    }

    public Employee getEmployee() {
        return employee;
    }

    public boolean isDestroyed() {
        return destroyed;
    }
}
