package model;

// หนึ่งขั้นตอน เช่น เตรียมปลา ใช้เวลา 2 นาที
public class SOPStep {
    // หนึ่ง object คือหนึ่งขั้นตอน; no เริ่มจาก 1 ตามลำดับที่เห็นบนหน้าจอ
    private String sopStepId;
    private int no;
    private String description;
    private double standardMinutes;
    private boolean destroyed;

    // สร้างขั้นตอนหนึ่งลำดับพร้อมเวลาเป้าหมาย
    public SOPStep(String sopStepId, int no, String description, double minutes) {
        this.sopStepId = sopStepId;
        this.no = no;
        update(description, minutes);
    }

    public void update(String description, double minutes) {
        if (!Double.isFinite(minutes) || minutes <= 0)
            throw new IllegalArgumentException("เวลาต้องมากกว่า 0");
        this.description = description;
        this.standardMinutes = minutes;
    }

    public void destroy() {
        destroyed = true;
    }

    // เมธอดอ่านลำดับ คำอธิบาย และเวลามาตรฐานของขั้นตอน

    public int number() {
        return no;
    }

    public String description() {
        return description;
    }

    public double standardMinutes() {
        return standardMinutes;
    }

    public boolean isDestroyed() {
        return destroyed;
    }
}
