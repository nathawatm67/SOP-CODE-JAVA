package model;

// หนึ่งขั้นตอน เช่น เตรียมปลา ใช้เวลา 2 นาที
public class SOPStep {
    private String sopStepId;
    private int number;
    private String description;
    private double standardMinutes;
    private boolean destroyed;

    public SOPStep(String id, int number, String description, double minutes) {
        this.sopStepId = id;
        this.number = number;
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

    public String getSopStepId() {
        return sopStepId;
    }

    public int getNumber() {
        return number;
    }

    public String getDescription() {
        return description;
    }

    public double getStandardMinutes() {
        return standardMinutes;
    }

    public boolean isDestroyed() {
        return destroyed;
    }
}
