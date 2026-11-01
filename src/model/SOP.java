package model;

import java.util.ArrayList;
import java.util.List;

// คู่มือหนึ่งฉบับผูกกับหนึ่งเมนู และเป็นเจ้าของขั้นตอนย่อย
public class SOP {
    public enum SopStatus { DRAFT, PUBLISHED, DISABLED }

    // SOP ผูกกับ Menu หนึ่งรายการ และเก็บขั้นตอนตามลำดับ
    private String sopId;
    private String name;
    private SopStatus status;
    // has-a (Association): SOP ใช้ Menu เดิมของร้าน ไม่ได้ทำลายเมนูเมื่อคู่มือถูกลบ
    private Menu menu;
    // has-a (Composition): SOP เป็นเจ้าของ SOPStep; ลบ SOP แล้วลบขั้นตอนด้วย
    private List<SOPStep> steps;
    private boolean destroyed;

    // สร้างคู่มือฉบับร่างที่ผูกกับเมนูหนึ่งรายการ
    public SOP(String sopId, String name, Menu menu) {
        this.sopId = sopId;
        this.name = name;
        this.menu = menu;
        this.status = SopStatus.DRAFT;
        this.steps = new ArrayList<SOPStep>();
    }

    // เพิ่มขั้นตอนพร้อมลำดับและเวลามาตรฐาน
    public void addStep(String description, double minutes) {
        int number = steps.size() + 1;
        SOPStep step = new SOPStep(sopId + "-STP-" + number, number, description, minutes);
        steps.add(step);
    }

    // รวมเวลาของทุกขั้นตอนเพื่อใช้เทียบเวลาปรุง
    public double getTotalMinutes() {
        double total = 0;
        for (int i = 0; i < steps.size(); i++)
            total += steps.get(i).standardMinutes();
        return total;
    }

    // เผยแพร่ได้เมื่อฉบับร่างมีขั้นตอนแล้ว
    public void publish() {
        if (status != SopStatus.DRAFT || steps.isEmpty()) {
            throw new IllegalStateException("เผยแพร่ได้เฉพาะฉบับร่างที่มีขั้นตอน");
        }
        status = SopStatus.PUBLISHED;
    }

    // ปิดใช้คู่มือที่เผยแพร่แล้ว
    public void disable() {
        if (status != SopStatus.PUBLISHED)
            throw new IllegalStateException("ต้องเผยแพร่ก่อน");
        status = SopStatus.DISABLED;
    }

    // เปิดใช้คู่มือที่ถูกปิด
    public void enable() {
        if (status != SopStatus.DISABLED)
            throw new IllegalStateException("ต้องปิดใช้อยู่ก่อน");
        status = SopStatus.PUBLISHED;
    }

    // อนุญาตให้ลบได้เฉพาะคู่มือฉบับร่าง
    public boolean isDeletable() {
        return status == SopStatus.DRAFT;
    }

    public void destroy() {
        for (int i = 0; i < steps.size(); i++)
            steps.get(i).destroy();
        steps.clear();
        menu = null;
        destroyed = true;
    }

    // เมธอดอ่านข้อมูลคู่มือและขั้นตอนสำหรับแสดงผล

    public String name() {
        return name;
    }

    // แก้ชื่อคู่มือ
    public void update(String name) {
        this.name = name;
    }

    public String statusText() {
        if (status == SopStatus.DRAFT) return "ร่าง";
        if (status == SopStatus.PUBLISHED) return "เผยแพร่";
        return "ปิดใช้";
    }

    public Menu menu() {
        return menu;
    }

    public List<SOPStep> steps() {
        return steps;
    }

    public boolean isDestroyed() {
        return destroyed;
    }
}
