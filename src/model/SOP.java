package model;

import java.util.ArrayList;

// คู่มือหนึ่งฉบับผูกกับหนึ่งเมนู และเป็นเจ้าของขั้นตอนย่อย
public class SOP {
    private String sopId;
    private String name;
    private String status;
    private Menu menu;
    private ArrayList<SOPStep> steps;
    private boolean destroyed;

    public SOP(String sopId, String name, Menu menu) {
        this.sopId = sopId;
        this.name = name;
        this.menu = menu;
        this.status = "ร่าง";
        this.steps = new ArrayList<SOPStep>();
    }

    public void addStep(String description, double minutes) {
        int number = steps.size() + 1;
        SOPStep step = new SOPStep(sopId + "-STP-" + number, number, description, minutes);
        steps.add(step);
    }

    public double getTotalMinutes() {
        double total = 0;
        for (int i = 0; i < steps.size(); i++)
            total += steps.get(i).getStandardMinutes();
        return total;
    }

    public void publish() {
        if (!status.equals("ร่าง") || steps.isEmpty()) {
            throw new IllegalStateException("เผยแพร่ได้เฉพาะฉบับร่างที่มีขั้นตอน");
        }
        status = "เผยแพร่";
    }

    public void disable() {
        if (!status.equals("เผยแพร่"))
            throw new IllegalStateException("ต้องเผยแพร่ก่อน");
        status = "ปิดใช้";
    }

    public void enable() {
        if (!status.equals("ปิดใช้"))
            throw new IllegalStateException("ต้องปิดใช้อยู่ก่อน");
        status = "เผยแพร่";
    }

    public boolean isDeletable() {
        return status.equals("ร่าง");
    }

    public void destroy() {
        for (int i = 0; i < steps.size(); i++)
            steps.get(i).destroy();
        steps.clear();
        menu = null;
        destroyed = true;
    }

    public String getSopId() {
        return sopId;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getStatus() {
        return status;
    }

    public Menu getMenu() {
        return menu;
    }

    public ArrayList<SOPStep> getSteps() {
        return steps;
    }

    public boolean isDestroyed() {
        return destroyed;
    }
}
