#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Full PDF Educational Guide Generator for Khao Tom Arom Dee (17 Java Classes).
Reads all 16 Model Classes + Main.java, formats them into a publication-grade
HTML manual, and renders it to a high-resolution PDF via Google Chrome headless.
"""

import os
import re
import html
import subprocess
from guide_data import CLASSES_INFO

WORKSPACE_DIR = "/run/media/liella/New Volume/SOP/OOAD-ข้าวต้มอารมณ์ดี-ล่าสุด-17คลาส/ชุดไฟล์แก้สไลด์-P1-P8/P9-Code-Java"
SRC_MODEL_DIR = os.path.join(WORKSPACE_DIR, "src", "model")
SRC_MAIN_FILE = os.path.join(WORKSPACE_DIR, "src", "Main.java")
OUTPUT_HTML = os.path.join(WORKSPACE_DIR, "P9-JAVA-OOP-17CLASSES-GUIDE.html")
OUTPUT_PDF = os.path.join(WORKSPACE_DIR, "P9-JAVA-OOP-17CLASSES-GUIDE.pdf")

def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

MAIN_SOURCE_LINES = read_file(SRC_MAIN_FILE).split("\n")

def get_main_method_code(name):
    """Extract full method code from Main.java by tracking matching braces."""
    start = -1
    for i, l in enumerate(MAIN_SOURCE_LINES):
        if f"static void {name}(" in l or f"public static void {name}(" in l:
            start = i
            break
    if start == -1:
        return ""
    brace = 0
    end = start
    for i in range(start, len(MAIN_SOURCE_LINES)):
        brace += MAIN_SOURCE_LINES[i].count("{") - MAIN_SOURCE_LINES[i].count("}")
        if brace == 0 and "{" in "".join(MAIN_SOURCE_LINES[start:i+1]):
            end = i
            break
    return "\n".join(MAIN_SOURCE_LINES[start:end+1])

def highlight_java(code):
    """Robust character-level lexer for Java syntax highlighting to HTML."""
    lines = code.split("\n")
    highlighted_lines = []
    
    keywords = {
        "package", "import", "public", "private", "protected", "class", "interface",
        "enum", "extends", "implements", "static", "final", "void", "return", "new",
        "this", "super", "if", "else", "for", "while", "do", "switch", "case",
        "default", "break", "continue", "throw", "throws", "try", "catch", "finally",
        "null", "true", "false", "int", "double", "float", "boolean", "char", "long", "short", "byte"
    }

    for line_idx, line in enumerate(lines, 1):
        line_parts = []
        pos = 0
        while pos < len(line):
            # 1. Line Comment: // ...
            if line[pos:pos+2] == '//':
                comment_text = html.escape(line[pos:])
                line_parts.append(f'<span class="tok-comment">{comment_text}</span>')
                break
            # 2. String literal: "..."
            elif line[pos] == '"':
                end_pos = pos + 1
                while end_pos < len(line):
                    if line[end_pos] == '\\':
                        end_pos += 2
                    elif line[end_pos] == '"':
                        end_pos += 1
                        break
                    else:
                        end_pos += 1
                str_text = html.escape(line[pos:end_pos])
                line_parts.append(f'<span class="tok-string">{str_text}</span>')
                pos = end_pos
            # 3. Identifiers & Keywords
            elif line[pos].isalpha() or line[pos] == '_':
                end_pos = pos + 1
                while end_pos < len(line) and (line[end_pos].isalnum() or line[end_pos] == '_'):
                    end_pos += 1
                word = line[pos:end_pos]
                word_escaped = html.escape(word)
                if word in keywords:
                    line_parts.append(f'<span class="tok-kw">{word_escaped}</span>')
                else:
                    line_parts.append(word_escaped)
                pos = end_pos
            # 4. Other characters
            else:
                line_parts.append(html.escape(line[pos]))
                pos += 1

        line_html = "".join(line_parts)
        highlighted_lines.append(f'<div class="code-line"><span class="line-num">{line_idx:3d}</span><span class="line-code">{line_html}</span></div>')
        
    return "\n".join(highlighted_lines)

def build_css():
    return """
    @page {
        size: A4 portrait;
        margin: 18mm 14mm 18mm 14mm;
        @bottom-right {
            content: counter(page);
            font-family: 'Noto Sans Thai', 'Leelawadee UI', sans-serif;
            font-size: 8pt;
            color: #64748b;
        }
        @bottom-left {
            content: "คู่มือเรียนรู้โค้ด Java OOP 17 คลาส - ระบบร้านข้าวต้มอารมณ์ดี";
            font-family: 'Noto Sans Thai', 'Leelawadee UI', sans-serif;
            font-size: 8pt;
            color: #64748b;
        }
    }
    
    * {
        box-sizing: border-box;
    }
    
    body {
        font-family: 'Noto Sans Thai', 'Leelawadee UI', 'Segoe UI', sans-serif;
        font-size: 9.8pt;
        line-height: 1.55;
        color: #1e293b;
        background: #ffffff;
        margin: 0;
        padding: 0;
    }
    
    .cover {
        min-height: 92vh;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        padding: 40px 30px;
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 50%, #0369a1 100%);
        color: #ffffff;
        border-radius: 12px;
        page-break-after: always;
    }
    
    .cover-top .tag {
        display: inline-block;
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(8px);
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 11pt;
        font-weight: 600;
        letter-spacing: 1px;
        border: 1px solid rgba(255, 255, 255, 0.25);
        margin-bottom: 25px;
    }
    
    .cover h1, .cover-top h1 {
        color: #ffffff !important;
        font-size: 26pt;
        line-height: 1.25;
        font-weight: 800;
        margin: 0 0 15px 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.4);
    }
    
    .cover-top .subtitle {
        font-size: 14pt;
        color: #93c5fd;
        font-weight: 400;
        line-height: 1.4;
        margin: 0 0 30px 0;
    }
    
    .cover-middle {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 22px;
        border-radius: 12px;
    }
    
    .cover-middle h3 {
        margin: 0 0 10px 0;
        font-size: 12.5pt;
        color: #38bdf8;
    }
    
    .cover-middle ul {
        margin: 0;
        padding-left: 20px;
        font-size: 10pt;
        line-height: 1.65;
    }
    
    .cover-bottom {
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
        border-top: 1px solid rgba(255, 255, 255, 0.2);
        padding-top: 20px;
        font-size: 9pt;
        color: #cbd5e1;
    }
    
    .page-break {
        page-break-before: always;
    }
    
    .no-break {
        page-break-inside: avoid;
    }
    
    h1, h2, h3, h4 {
        color: #0f172a;
        font-weight: 700;
        page-break-after: avoid;
    }
    
    h1.chapter-title {
        font-size: 17pt;
        color: #1e3a8a;
        border-bottom: 3px solid #2563eb;
        padding-bottom: 8px;
        margin-top: 0;
        margin-bottom: 18px;
    }
    
    h2.section-title {
        font-size: 13.5pt;
        color: #0369a1;
        border-bottom: 1px solid #bae6fd;
        padding-bottom: 5px;
        margin-top: 24px;
        margin-bottom: 12px;
    }
    
    h3.sub-title {
        font-size: 11pt;
        color: #334155;
        margin-top: 16px;
        margin-bottom: 8px;
    }
    
    p {
        margin: 0 0 10px 0;
        text-align: justify;
    }
    
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 12px 0 16px 0;
        font-size: 8.8pt;
        page-break-inside: avoid;
    }
    
    th {
        background: #f1f5f9;
        color: #0f172a;
        font-weight: 700;
        text-align: left;
        padding: 7px 9px;
        border: 1px solid #cbd5e1;
    }
    
    td {
        padding: 6px 9px;
        border: 1px solid #e2e8f0;
        vertical-align: top;
    }
    
    tr:nth-child(even) td {
        background: #f8fafc;
    }
    
    .card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 12px 14px;
        margin: 12px 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        page-break-inside: avoid;
    }
    
    .callout {
        padding: 10px 14px;
        border-radius: 6px;
        margin: 12px 0;
        font-size: 9pt;
        page-break-inside: avoid;
    }
    
    .callout-info {
        background: #f0f9ff;
        border-left: 4px solid #0284c7;
        color: #0369a1;
    }
    
    .callout-tip {
        background: #f0fdf4;
        border-left: 4px solid #16a34a;
        color: #15803d;
    }
    
    .callout-warn {
        background: #fffbeb;
        border-left: 4px solid #f59e0b;
        color: #b45309;
    }
    
    .callout-danger {
        background: #fef2f2;
        border-left: 4px solid #ef4444;
        color: #b91c1c;
    }
    
    .callout-title {
        font-weight: 700;
        margin-bottom: 3px;
    }
    
    .badge {
        display: inline-block;
        padding: 2px 7px;
        border-radius: 10px;
        font-size: 7.5pt;
        font-weight: 600;
        text-transform: uppercase;
        margin-right: 4px;
    }
    
    .badge-comp { background: #fee2e2; color: #991b1b; border: 1px solid #fca5a5; }
    .badge-assoc { background: #e0f2fe; color: #0369a1; border: 1px solid #7dd3fc; }
    .badge-enum { background: #fef3c7; color: #92400e; border: 1px solid #fde68a; }
    .badge-domain { background: #ede9fe; color: #5b21b6; border: 1px solid #c4b5fd; }
    
    .code-container {
        background: #f8fafc;
        border: 1px solid #cbd5e1;
        border-radius: 6px;
        margin: 10px 0 14px 0;
        font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace;
        font-size: 7.2pt;
        line-height: 1.4;
        overflow: hidden;
        page-break-inside: avoid;
    }
    
    .code-header {
        background: #e2e8f0;
        padding: 5px 12px;
        font-size: 7.5pt;
        font-weight: 600;
        color: #334155;
        display: flex;
        justify-content: space-between;
        border-bottom: 1px solid #cbd5e1;
    }
    
    .code-body {
        padding: 5px 0;
    }
    
    .code-line {
        display: flex;
        padding: 0 8px;
    }
    
    .code-line:hover {
        background: #f1f5f9;
    }
    
    .line-num {
        width: 30px;
        text-align: right;
        padding-right: 10px;
        color: #94a3b8;
        user-select: none;
        flex-shrink: 0;
    }
    
    .line-code {
        white-space: pre-wrap;
        word-break: break-all;
        flex-grow: 1;
    }
    
    .tok-kw { color: #0284c7; font-weight: bold; }
    .tok-string { color: #16a34a; }
    .tok-comment { color: #64748b; font-style: italic; }
    
    .toc {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 18px 24px;
        margin-bottom: 25px;
        page-break-after: always;
    }
    
    .toc h2 {
        color: #1e3a8a;
        border-bottom: 2px solid #3b82f6;
        padding-bottom: 6px;
        margin-top: 0;
    }
    
    .toc-list {
        list-style: none;
        padding-left: 0;
        margin: 0;
    }
    
    .toc-item {
        margin: 6px 0;
        font-size: 9.5pt;
    }
    
    .toc-item a {
        color: #1e293b;
        text-decoration: none;
        display: flex;
        justify-content: space-between;
        border-bottom: 1px dotted #cbd5e1;
        padding-bottom: 1px;
    }
    
    .toc-sub {
        list-style: none;
        padding-left: 18px;
        margin: 3px 0 6px 0;
        font-size: 8.8pt;
        color: #475569;
    }
    
    .toc-sub li {
        margin: 3px 0;
    }
    """

def generate_cover_html():
    return """
    <div class="cover">
        <div class="cover-top">
            <span class="tag">คู่มือสถาปัตยกรรมและการเขียนโค้ดเชิงวัตถุ (OOAD &amp; OOP)</span>
            <h1>คู่มือเจาะลึกและเรียนรู้โค้ด Java OOP 17 คลาส</h1>
            <div class="subtitle">ระบบบริหารจัดการร้านอาหาร "ข้าวต้มอารมณ์ดี" (Khao Tom Arom Dee)<br>
            เจาะลึก 16 คลาสโมเดล + Main Controller ตามมาตรฐาน OOAD P1–P9</div>
        </div>
        <div class="cover-middle">
            <h3>สาระสำคัญที่ครอบคลุมในเอกสารฉบับนี้:</h3>
            <ul>
                <li><strong>สถาปัตยกรรม OOP &amp; Clean Domain Design:</strong> เข้าใจลึกซึ้งถึง Class, Object, Encapsulation, State Management และ Invariants</li>
                <li><strong>ความสัมพันธ์เชิงโครงสร้าง (Relationships):</strong> จำแนกชัดเจนระหว่าง Association (has-a) และ Composition (owns-a) พร้อมหลักฐานการทำลายวงจรชีวิต (destroy cascade) ทั้ง 5 คู่</li>
                <li><strong>ผ่าซอร์สโค้ด 16 คลาสโมเดลแบบบรรทัดต่อบรรทัด:</strong> อธิบายบทบาท ฟิลด์ เมธอด Validation กฎการตัดสต็อก การคิดเงิน และระบบแต้มสะสม</li>
                <li><strong>เจาะลึก Main.java (Driver &amp; Presentation):</strong> ถอดรหัสการทำงาน 8 Use Cases (UC01–UC08), In-Memory Collections และตัวอย่างข้อมูลจริง</li>
                <li><strong>Life of an Order &amp; Defense Cheatsheet:</strong> ตามรอยการเดินทางของข้อมูลแบบ End-to-End พร้อมคลัง 15 คำถามปราบเซียนในการสอบและนำเสนอ</li>
            </ul>
        </div>
        <div class="cover-bottom">
            <div>
                <strong>จัดทำสำหรับ:</strong> นักศึกษาและนักพัฒนาซอฟต์แวร์สาย Object-Oriented Analysis &amp; Design (OOAD)<br>
                <strong>ชุดโครงงาน:</strong> ระบบบริหารร้านข้าวต้มอารมณ์ดี (ฉบับ 17 คลาส Java พื้นฐาน)
            </div>
            <div style="text-align: right;">
                <strong>วันที่จัดทำ:</strong> พฤศจิกายน 2026<br>
                <strong>เวอร์ชัน:</strong> P9 Release Candidate 1.0 (Comprehensive Edition)
            </div>
        </div>
    </div>
    """

def generate_toc_html():
    return """
    <div class="toc">
        <h2>สารบัญเนื้อหา (Table of Contents)</h2>
        <ul class="toc-list">
            <li class="toc-item">
                <a href="#ch1"><strong>บทที่ 1: สถาปัตยกรรมและมโนทัศน์พื้นฐาน OOP ของระบบร้านข้าวต้มอารมณ์ดี</strong> <span>หน้า 3</span></a>
                <ul class="toc-sub">
                    <li>1.1 ภาพรวมระบบและการจำลองการทำงานจริง (8 Use Cases: UC01–UC08)</li>
                    <li>1.2 มโนทัศน์ OOP ที่ประยุกต์ใช้ในระบบ (Encapsulation, Invariants, Static Scope, Collections)</li>
                    <li>1.3 Association vs Composition: กฎเกณฑ์และตารางเปรียบเทียบเชิงวิศวกรรม</li>
                    <li>1.4 หลักฐานเชิงประจักษ์ของ Composition ทั้ง 5 คู่ (destroy cascade)</li>
                </ul>
            </li>
            <li class="toc-item">
                <a href="#ch2"><strong>บทที่ 2: ผ่าโค้ดเจาะลึก 16 คลาสโมเดลใน src/model (The 16 Model Classes)</strong> <span>หน้า 7</span></a>
                <ul class="toc-sub">
                    <li><strong>ส่วนที่ 2.1: โดเมนบุคคลและสถานที่</strong> — Customer, Employee, Table, Member</li>
                    <li><strong>ส่วนที่ 2.2: โดเมนเมนู คู่มือ และสูตรอาหาร</strong> — Menu, Recipe, SOP, SOPStep</li>
                    <li><strong>ส่วนที่ 2.3: โดเมนคลังวัตถุดิบและการจัดซื้อ</strong> — Ingredient, StockMovement, Supplier, PurchaseOrder</li>
                    <li><strong>ส่วนที่ 2.4: โดเมนออเดอร์และการเงิน</strong> — OrderItem, Order, Payment, PointTransaction</li>
                </ul>
            </li>
            <li class="toc-item">
                <a href="#ch3"><strong>บทที่ 3: เจาะลึก Main.java ตัวควบคุมระบบและการทำงาน 8 Use Cases</strong> <span>หน้า 45</span></a>
                <ul class="toc-sub">
                    <li>3.1 โครงสร้างภาพรวมและบทบาท Presentation / Controller</li>
                    <li>3.2 ตัวแปรส่วนกลาง (Shared In-Memory Collections) และพนักงานตัวอย่าง</li>
                    <li>3.3 การสร้างข้อมูลตั้งต้น createSampleData() (ผัดกะเพราปลา, ยำหมูยอ, สต็อก)</li>
                    <li>3.4 เครื่องมือและ Helper Functions ในการรับและตรวจสอบอินพุต</li>
                    <li>3.5 เจาะลึกการทำงานของเมธอด Use Cases ทั้ง 8 งาน (uc01() ถึง uc08()) พร้อมซอร์สโค้ดประกอบ</li>
                </ul>
            </li>
            <li class="toc-item">
                <a href="#ch4"><strong>บทที่ 4: การเดินทางของข้อมูลแบบครบวงจร (Life of an Order: End-to-End Walkthrough)</strong> <span>หน้า 65</span></a>
                <ul class="toc-sub">
                    <li>4.1 ตามรอยออเดอร์ตั้งแต่เปิดโต๊ะจนถึงคิดเงินและตัดสต็อก (7 สเต็ปครบวงจร)</li>
                    <li>4.2 แผนภาพและตาราง State Machine Diagram ของ Order และ OrderItem</li>
                </ul>
            </li>
            <li class="toc-item">
                <a href="#ch5"><strong>บทที่ 5: คลังข้อสอบและแนวทางตอบคำถามสำหรับนำเสนอ (Defense &amp; Exam Cheatsheet)</strong> <span>หน้า 70</span></a>
                <ul class="toc-sub">
                    <li>รวบรวม 15 คำถามปราบเซียนที่อาจารย์มักถาม พร้อมคำตอบระดับเกียรตินิยม</li>
                </ul>
            </li>
            <li class="toc-item">
                <a href="#ch6"><strong>บทที่ 6: บทสรุปและแนวทางการพัฒนาต่อยอดสู่ระดับ Enterprise (Future Roadmap)</strong> <span>หน้า 76</span></a>
                <ul class="toc-sub">
                    <li>จาก In-Memory สู่ Relational Database (JPA / PostgreSQL) และ Spring Boot Web API</li>
                </ul>
            </li>
        </ul>
    </div>
    """

def generate_chapter1_html():
    return """
    <div id="ch1" class="page-break">
        <h1 class="chapter-title">บทที่ 1: สถาปัตยกรรมและมโนทัศน์พื้นฐาน OOP ของระบบร้านข้าวต้มอารมณ์ดี</h1>
        
        <h2 class="section-title">1.1 ภาพรวมระบบและการจำลองการทำงานจริง (8 Use Cases)</h2>
        <p>
            ระบบร้านอาหาร <strong>"ข้าวต้มอารมณ์ดี" (Khao Tom Arom Dee)</strong> เป็นโครงงานพัฒนาระบบตามระเบียบวิธีวิเคราะห์และออกแบบเชิงวัตถุ (Object-Oriented Analysis and Design: OOAD) ตั้งแต่ระยะ P1 ถึง P8 และถูกแปลงเป็นซอร์สโค้ดภาษา Java ในระยะ P9 โดยจำลองการทำงานผ่านคอนโซล (Text Mode Console) เพื่อให้ผู้เรียนสามารถทำความเข้าใจโครงสร้างเชิงวัตถุได้อย่างบริสุทธิ์โดยไม่มีความซับซ้อนของเฟรมเวิร์กเว็บหรือฐานข้อมูลมาบดบัง
        </p>
        <p>
            ระบบประกอบด้วยงานหลัก 8 ด้าน (Use Cases) ที่ครอบคลุมการดำเนินงานทั้งหมดของร้านอาหาร ได้แก่:
        </p>
        <table>
            <thead>
                <tr>
                    <th style="width: 12%;">รหัส UC</th>
                    <th style="width: 25%;">ชื่องาน (Use Case)</th>
                    <th style="width: 28%;">ผู้ใช้งานหลัก (Actors)</th>
                    <th>ความรับผิดชอบหลักของระบบ</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>UC01</strong></td>
                    <td>สั่งอาหารผ่าน QR โต๊ะ</td>
                    <td>ลูกค้า / พนักงานเสิร์ฟ</td>
                    <td>สแกนโต๊ะ, ผูกสมาชิก, เลือกเมนูและ Topping, ตรวจสอบสต็อก และยืนยันออเดอร์</td>
                </tr>
                <tr>
                    <td><strong>UC02</strong></td>
                    <td>จัดการคู่มือ SOP</td>
                    <td>ผู้จัดการ / เชฟใหญ่</td>
                    <td>สร้างคู่มือมาตรฐานการปรุงอาหาร, กำหนดขั้นตอนย่อยและเวลา, เผยแพร่ และปิดใช้งาน</td>
                </tr>
                <tr>
                    <td><strong>UC03</strong></td>
                    <td>ปรุงอาหารและเสิร์ฟ</td>
                    <td>คนครัว / พนักงานเสิร์ฟ</td>
                    <td>เลือกสถานีครัว, รับออเดอร์เข้าคิว, เริ่มปรุง, จับเวลาเทียบ SOP, เสิร์ฟถึงโต๊ะ</td>
                </tr>
                <tr>
                    <td><strong>UC04</strong></td>
                    <td>ชำระเงินและออกใบเสร็จ</td>
                    <td>แคชเชียร์ / ลูกค้า</td>
                    <td>เลือกโต๊ะที่เสิร์ฟครบ, แลกแต้มส่วนลด, คำนวณเงินทอน, ปิดบิล, แจกแต้มใหม่, ปล่อยโต๊ะว่าง</td>
                </tr>
                <tr>
                    <td><strong>UC05</strong></td>
                    <td>สต็อกและใบสั่งซื้อ</td>
                    <td>ผู้จัดการ / พนักงานคลัง</td>
                    <td>ตรวจสต็อกต่ำกว่าเกณฑ์, ออกใบสั่งซื้อ PO ให้ซัพพลายเออร์, รับของเข้าคลัง, ปรับยอดตรวจนับ</td>
                </tr>
                <tr>
                    <td><strong>UC06</strong></td>
                    <td>ภาพรวมและรายงานยอดขาย</td>
                    <td>ผู้จัดการ / เจ้าของร้าน</td>
                    <td>สรุปรายได้ตามช่วงวันที่, แยกยอดเงินสดและ QR, วิเคราะห์อันดับเมนูขายดี</td>
                </tr>
                <tr>
                    <td><strong>UC07</strong></td>
                    <td>จัดการเมนูและสูตรอาหาร</td>
                    <td>ผู้จัดการ / เชฟ</td>
                    <td>เพิ่มเมนู, ตั้งราคา, สร้างสูตรฉบับร่าง, ยืนยันสูตรสมบูรณ์, แตกเวอร์ชันสูตร, เพิ่มตัวเลือกเสริม</td>
                </tr>
                <tr>
                    <td><strong>UC08</strong></td>
                    <td>สมาชิกและแต้มสะสม</td>
                    <td>ลูกค้า / แคชเชียร์ / ผู้จัดการ</td>
                    <td>สมัครสมาชิก, ค้นหาประวัติแต้ม, ผู้จัดการอนุมัติคำขอยกเลิกอาหาร, ปรับกฎแต้มกลางของร้าน</td>
                </tr>
            </tbody>
        </table>

        <h2 class="section-title">1.2 มโนทัศน์ OOP ที่นำมาใช้ในระบบร้านข้าวต้มอารมณ์ดี</h2>
        <div class="card">
            <h3 style="margin-top:0; color:#1e3a8a;">1. Encapsulation (การห่อหุ้มและการซ่อนข้อมูล)</h3>
            <p>
                ฟิลด์ข้อมูลทั้งหมดใน 16 คลาสโมเดลถูกประกาศเป็น <code>private</code> อย่างเคร่งครัด เพื่อป้องกันไม่ให้อ็อบเจกต์ภายนอกหรือคลาส <code>Main</code> แก้ไขค่าได้โดยพลการ เช่น ยอดสต็อก <code>stockQty</code> ใน <code>Ingredient</code> ไม่สามารถถูกเขียนทับด้วยเครื่องหมายเท่ากับ (<code>=</code>) ได้ แต่จะต้องผ่านเมธอดทางธุรกิจ เช่น <code>deduct()</code>, <code>receive()</code> หรือ <code>adjustStock()</code> เท่านั้น ซึ่งแต่ละเมธอดจะมีเงื่อนไขตรวจสอบ (Validation) และจะสร้างประวัติ <code>StockMovement</code> เสมอ
            </p>
        </div>
        
        <div class="card">
            <h3 style="margin-top:0; color:#1e3a8a;">2. Invariants &amp; State Validation (การรักษาสภาวะความถูกต้องของระบบ)</h3>
            <p>
                ทุกอ็อบเจกต์มีหน้าที่รักษากฎความถูกต้องของตนเอง (Invariants) หากมีคำสั่งใดที่ขัดแย้งกับกฎ อ็อบเจกต์จะโยน Exception ออกมาทันที:
            </p>
            <ul>
                <li><strong>IllegalArgumentException:</strong> ใช้เมื่อพารามิเตอร์ที่ส่งเข้ามาไม่ถูกต้อง เช่น เบอร์โทรศัพท์ไม่ใช่ 10 หลัก (<code>!phone.matches("0[0-9]{9}")</code>), ปริมาณติดลบ, หรือราคาอาหารเท่ากับ 0</li>
                <li><strong>IllegalStateException:</strong> ใช้เมื่อพยายามทำงานที่ขัดกับสถานะปัจจุบันของอ็อบเจกต์ เช่น พยายามเปิดขายเมนูที่ยังไม่มีสูตรสมบูรณ์ (<code>currentRecipe() == null</code>), พยายามยกเลิกอาหารที่เริ่มปรุงไปแล้วโดยไม่ผ่านผู้จัดการ, หรือพยายามรับของซ้ำในใบสั่งซื้อที่รับไปแล้ว</li>
            </ul>
        </div>

        <div class="card">
            <h3 style="margin-top:0; color:#1e3a8a;">3. Class Scope (static) vs Instance Scope</h3>
            <p>
                ในคลาส <code>Member</code> มีการประยุกต์ใช้ <code>static</code> ได้อย่างชัดเจน:
            </p>
            <ul>
                <li><strong>Instance Variables:</strong> <code>memberId</code>, <code>name</code>, <code>phone</code>, <code>points</code> และ <code>transactions</code> เป็นของสมาชิกแต่ละคน (แต่ละอ็อบเจกต์มีค่าของตัวเอง)</li>
                <li><strong>Static Variables (Class Level):</strong> <code>bahtPerPoint</code> (50 บาท/แต้ม), <code>pointValue</code> (1 บาท/แต้ม), และ <code>minRedeem</code> (10 แต้ม) เป็นกฎกลางของร้านอาหาร เมื่อผู้จัดการแก้ไขผ่าน <code>Member.setRule()</code> จะมีผลบังคับใช้กับสมาชิกทุกคนในร้านทันทีโดยไม่ต้องไปแก้ในสมาชิกทีละคน</li>
            </ul>
        </div>

        <h2 class="section-title">1.3 Association (has-a) vs Composition (owns-a)</h2>
        <p>
            หนึ่งในหัวใจสำคัญที่สุดของการออกแบบเชิงวัตถุคือการทำความเข้าใจความสัมพันธ์แบบ <strong>has-a</strong> ซึ่งใน UML และ OOAD แบ่งออกเป็น 2 ประเภทหลัก:
        </p>
        <table>
            <thead>
                <tr>
                    <th style="width: 20%;">มิติการเปรียบเทียบ</th>
                    <th style="width: 40%;">Association (ความสัมพันธ์แบบรู้จักกัน / has-a)</th>
                    <th style="width: 40%;">Composition (ความเป็นเจ้าของส่วนประกอบ / owns-a)</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>สัญลักษณ์ UML</strong></td>
                    <td>เส้นตรงธรรมดา หรือเส้นมีหัวลูกศรทิศทางเดียว (──&gt;)</td>
                    <td>เส้นตรงที่มี <strong>สัญลักษณ์ข้าวหลามตัดทึบ (◆)</strong> อยู่ฝั่งเจ้าของ</td>
                </tr>
                <tr>
                    <td><strong>ความเป็นเจ้าของ</strong></td>
                    <td>ต่างฝ่ายต่างมีชีวิตเป็นของตัวเอง (Loose relationship)</td>
                    <td>ฝั่ง Composite เป็นเจ้าของส่วนประกอบย่อย (Part-of) โดยสมบูรณ์</td>
                </tr>
                <tr>
                    <td><strong>วงจรชีวิต (Lifecycle)</strong></td>
                    <td>เป็นอิสระต่อกัน การทำลายอ็อบเจกต์หนึ่งไม่ส่งผลต่ออีกอ็อบเจกต์</td>
                    <td><strong>ผูกติดกัน (Bound lifecycle)</strong> เมื่ออ็อบเจกต์แม่ถูกทำลาย ส่วนย่อยจะถูกทำลายตามไปด้วย</td>
                </tr>
                <tr>
                    <td><strong>ตัวอย่างในโปรเจกต์</strong></td>
                    <td><code>Order</code> อ้างถึง <code>Table</code><br><code>Customer</code> อ้างถึง <code>Member</code><br><code>PurchaseOrder</code> อ้างถึง <code>Supplier</code></td>
                    <td><code>Order</code> ◆── <code>OrderItem</code><br><code>Menu</code> ◆── <code>Recipe</code><br><code>SOP</code> ◆── <code>SOPStep</code><br><code>Ingredient</code> ◆── <code>StockMovement</code><br><code>Member</code> ◆── <code>PointTransaction</code></td>
                </tr>
            </tbody>
        </table>

        <h2 class="section-title">1.4 หลักฐานเชิงประจักษ์ของ Composition ทั้ง 5 คู่ในโค้ด Java</h2>
        <p>
            เนื่องจากภาษา Java มีระบบ Garbage Collection ที่จัดการคืนหน่วยความจำอัตโนมัติ การแสดงความเป็น Composition ในระดับโค้ดจึงแสดงออกผ่าน 3 ปัจจัยหลัก:
        </p>
        <ol>
            <li><strong>การถือครองข้อมูล:</strong> อ็อบเจกต์แม่เก็บ List ของอ็อบเจกต์ลูกไว้ภายใน</li>
            <li><strong>การให้กำเนิด:</strong> อ็อบเจกต์แม่มีเมธอดสร้างอ็อบเจกต์ลูกขึ้นมาเอง เช่น <code>order.addItem(...)</code> สร้าง <code>OrderItem</code>, <code>sop.addStep(...)</code> สร้าง <code>SOPStep</code></li>
            <li><strong>การทำลายวงจรชีวิต (Lifecycle Cascade):</strong> อ็อบเจกต์แม่มีเมธอด <code>destroy()</code> ที่จะวนลูปเรียก <code>destroy()</code> ของอ็อบเจกต์ลูกทุกตัวก่อนที่จะเคลียร์ List ทิ้ง</li>
        </ol>

        <table>
            <thead>
                <tr>
                    <th>อ็อบเจกต์แม่ (Composite)</th>
                    <th>อ็อบเจกต์ลูก (Part-of)</th>
                    <th>เมธอดสร้างลูก (Creation)</th>
                    <th>หลักฐานการทำลาย (destroy cascade) ในโค้ดจริง</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><span class="badge badge-comp">Order</span></td>
                    <td>OrderItem</td>
                    <td><code>order.addItem(...)</code></td>
                    <td><code>for (OrderItem item : items) item.destroy(); items.clear();</code></td>
                </tr>
                <tr>
                    <td><span class="badge badge-comp">Menu</span></td>
                    <td>Recipe</td>
                    <td><code>menu.addRecipe(...)</code></td>
                    <td><code>for (Recipe r : recipes) r.destroy(); recipes.clear();</code></td>
                </tr>
                <tr>
                    <td><span class="badge badge-comp">SOP</span></td>
                    <td>SOPStep</td>
                    <td><code>sop.addStep(...)</code></td>
                    <td><code>for (SOPStep s : steps) s.destroy(); steps.clear();</code></td>
                </tr>
                <tr>
                    <td><span class="badge badge-comp">Ingredient</span></td>
                    <td>StockMovement</td>
                    <td><code>ingredient.changeStock(...)</code></td>
                    <td><code>for (StockMovement m : movements) m.destroy(); movements.clear();</code></td>
                </tr>
                <tr>
                    <td><span class="badge badge-comp">Member</span></td>
                    <td>PointTransaction</td>
                    <td><code>member.addTransaction(...)</code></td>
                    <td><code>for (PointTransaction t : transactions) t.destroy(); transactions.clear();</code></td>
                </tr>
            </tbody>
        </table>
    </div>
    """

def generate_chapter2_html():
    html_parts = ["""
    <div id="ch2" class="page-break">
        <h1 class="chapter-title">บทที่ 2: ผ่าโค้ดเจาะลึก 16 คลาสโมเดลใน src/model</h1>
        <p>
            ในโฟลเดอร์ <code>src/model</code> ประกอบด้วยคลาสสาธารณะจำนวน 16 คลาสพอดี ไม่มีคลาสซ้อนภายนอก ไม่มีไฟล์ enum แยกย่อย และไม่มีคลาสอำนวยความสะดวกแปลกปลอม เพื่อให้คงความเรียบง่ายตามหลักการเรียนรู้ OOP พื้นฐาน โดยแบ่งออกเป็น 4 โดเมนธุรกิจหลัก ดังนี้:
        </p>
    """]
    
    for idx, c in enumerate(CLASSES_INFO, 1):
        class_name = c["name"]
        file_path = os.path.join(SRC_MODEL_DIR, c["file"])
        source_code = read_file(file_path)
        highlighted_code = highlight_java(source_code)
        
        fields_rows = ""
        for fname, ftype, fvis, fdesc in c["fields"]:
            fields_rows += f"""
            <tr>
                <td><code>{html.escape(fvis)} {html.escape(ftype)}</code></td>
                <td><strong>{html.escape(fname)}</strong></td>
                <td>{html.escape(fdesc)}</td>
            </tr>
            """
            
        methods_rows = ""
        for mname, mcat, mdesc in c["methods_desc"]:
            methods_rows += f"""
            <tr>
                <td style="width: 32%;"><code>{html.escape(mname)}</code></td>
                <td style="width: 18%;"><span class="badge badge-assoc">{html.escape(mcat)}</span></td>
                <td>{html.escape(mdesc)}</td>
            </tr>
            """
            
        class_html = f"""
        <div class="page-break">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 8px;">
                <h2 class="section-title" style="margin:0; border:none; padding:0;">
                    2.{idx} คลาส {class_name} ({c["file"]})
                </h2>
                <div>
                    <span class="badge badge-domain">{html.escape(c["domain"])}</span>
                </div>
            </div>
            
            <div class="card" style="margin-top: 5px;">
                <p><strong>บทบาทหน้าที่ (Responsibility):</strong> {c["purpose"]}</p>
                <p><strong>ความสัมพันธ์ UML:</strong> <code>{html.escape(c["uml"])}</code></p>
            </div>
            
            <h3 class="sub-title">ตารางฟิลด์และตัวแปรข้อมูล (Fields &amp; Attributes)</h3>
            <table>
                <thead>
                    <tr>
                        <th style="width: 30%;">ชนิดข้อมูลและการเข้าถึง</th>
                        <th style="width: 25%;">ชื่อตัวแปร (Field)</th>
                        <th>คำอธิบายหน้าที่ในระบบ</th>
                    </tr>
                </thead>
                <tbody>
                    {fields_rows}
                </tbody>
            </table>
            
            <h3 class="sub-title">ตารางเมธอดสำคัญ (Key Methods &amp; Operations)</h3>
            <table>
                <thead>
                    <tr>
                        <th>รูปแบบเมธอด (Signature)</th>
                        <th>หมวดหมู่การทำงาน</th>
                        <th>คำอธิบายรายละเอียดการทำงาน</th>
                    </tr>
                </thead>
                <tbody>
                    {methods_rows}
                </tbody>
            </table>
            
            <div class="callout callout-info">
                <div class="callout-title">จุดสังเกตการออกแบบเชิงวัตถุ (OOP Design Insight):</div>
                {c["design_notes"]}
            </div>
            
            <div class="callout callout-tip">
                <div class="callout-title">คำถาม-คำตอบยอดฮิตสำหรับการนำเสนอ (Defense Q&amp;A):</div>
                {c["qa"]}
            </div>
            
            <h3 class="sub-title">ซอร์สโค้ดฉบับสมบูรณ์ (Full Source Code: {c["file"]})</h3>
            <div class="code-container">
                <div class="code-header">
                    <span>src/model/{c["file"]}</span>
                    <span>Java Source Code</span>
                </div>
                <div class="code-body">
                    {highlighted_code}
                </div>
            </div>
        </div>
        """
        html_parts.append(class_html)
        
    html_parts.append("</div>")
    return "\n".join(html_parts)

def generate_chapter3_html():
    code_create_sample = highlight_java(get_main_method_code("createSampleData"))
    code_uc01 = highlight_java(get_main_method_code("uc01"))
    code_add_food = highlight_java(get_main_method_code("addFood"))
    code_uc02 = highlight_java(get_main_method_code("uc02"))
    code_uc03 = highlight_java(get_main_method_code("uc03"))
    code_uc04 = highlight_java(get_main_method_code("uc04"))
    code_uc05 = highlight_java(get_main_method_code("uc05"))
    code_uc06 = highlight_java(get_main_method_code("uc06"))
    code_print_sales = highlight_java(get_main_method_code("printSales"))
    code_uc07 = highlight_java(get_main_method_code("uc07"))
    code_uc08 = highlight_java(get_main_method_code("uc08"))

    return f"""
    <div id="ch3" class="page-break">
        <h1 class="chapter-title">บทที่ 3: เจาะลึก Main.java ตัวควบคุมระบบและการทำงาน 8 Use Cases</h1>
        
        <h2 class="section-title">3.1 สถาปัตยกรรมและบทบาทของ Main.java</h2>
        <p>
            ไฟล์ <code>src/Main.java</code> มีความยาว 1,445 บรรทัด ทำหน้าที่เป็นทั้ง <strong>Presentation Layer (ส่วนติดต่อผู้ใช้แบบคอนโซล Text Mode)</strong> และ <strong>Application Orchestrator (ตัวควบคุมการไหลของระบบ)</strong> ที่คอยรับคำสั่งจากแป้นพิมพ์ ส่งต่อให้อ็อบเจกต์ในแพ็กเกจ <code>model</code> ทำงาน และนำผลลัพธ์มาแสดงผล
        </p>
        <p>
            เหตุผลที่ <code>Main.java</code> มีความยาวมาก เกิดจากการที่ระบบต้องรวมหน้าจอเมนูและลอจิกการรับคำตอบของ Use Cases ทั้ง 8 งาน (UC01–UC08) ไว้ในไฟล์เดียวตามข้อกำหนด โดยไม่สร้างคลาสสนับสนุนในโฟลเดอร์ภายนอก (ไม่มี <code>ui/</code>, <code>data/</code> หรือ <code>util/</code>) เพื่อให้ไฟล์โมเดลทั้ง 16 คลาสคงความบริสุทธิ์ของกฎทางธุรกิจอย่างสมบูรณ์
        </p>
        
        <div class="callout callout-info">
            <div class="callout-title">หลักการแบ่งหน้าที่ (Separation of Concerns):</div>
            <strong>Main</strong> สนใจเรื่อง <em>"ผู้ใช้เลือกเมนูใด และจะพิมพ์อะไรออกทางหน้าจอ"</em> ในขณะที่ <strong>model</strong> สนใจเรื่อง <em>"สต็อกมีพอไหม, เงินทอนเท่าไร, สถานะเปลี่ยนได้หรือไม่"</em> ทำให้โค้ดมีความเป็นโมดูลาร์สูง แม้ <code>Main</code> จะยาวแต่ก็อ่านง่ายเพราะแบ่งเป็นเมธอด <code>uc01()</code> ถึง <code>uc08()</code> ชัดเจน
        </div>

        <h2 class="section-title">3.2 ฐานข้อมูลจำลองส่วนกลาง (Shared In-Memory Collections)</h2>
        <p>
            ด้านบนของคลาส <code>Main</code> มีการประกาศตัวแปรส่วนกลางแบบ <code>static ArrayList</code> หลายชุด ซึ่งทำหน้าที่เสมือนฐานข้อมูลจำลอง (In-Memory Database) ที่ทุก Use Case ใช้งานร่วมกันตลอดเวลาที่โปรแกรมเปิดอยู่:
        </p>
        <table>
            <thead>
                <tr>
                    <th style="width: 30%;">ตัวแปรใน Main</th>
                    <th style="width: 30%;">ชนิดข้อมูล</th>
                    <th>หน้าที่และความสำคัญ</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><code>tables</code></td>
                    <td><code>ArrayList&lt;Table&gt;</code></td>
                    <td>เก็บโต๊ะอาหาร T01 ถึง T04 เพื่อใช้สแกนเปิดออเดอร์ใน UC01 และเคลียร์โต๊ะใน UC04</td>
                </tr>
                <tr>
                    <td><code>menus</code></td>
                    <td><code>ArrayList&lt;Menu&gt;</code></td>
                    <td>เก็บเมนูอาหาร เช่น ผัดกะเพราปลา, ยำหมูยอ/แหนม สำหรับสั่งอาหารและคำนวณราคา</td>
                </tr>
                <tr>
                    <td><code>ingredients</code></td>
                    <td><code>ArrayList&lt;Ingredient&gt;</code></td>
                    <td>คลังวัตถุดิบกลาง (เนื้อปลา, ไข่ไก่, หมูยอ ฯลฯ) ที่ถูกตัดสต็อกใน UC01 และรับเข้าใน UC05</td>
                </tr>
                <tr>
                    <td><code>members</code></td>
                    <td><code>ArrayList&lt;Member&gt;</code></td>
                    <td>ทะเบียนสมาชิกของร้าน สำหรับค้นหาด้วยเบอร์โทรใน UC01/UC08 และใช้แลกแต้มใน UC04</td>
                </tr>
                <tr>
                    <td><code>suppliers</code></td>
                    <td><code>ArrayList&lt;Supplier&gt;</code></td>
                    <td>รายชื่อผู้จัดจำหน่ายวัตถุดิบ สำหรับการออกใบสั่งซื้อ PO ใน UC05</td>
                </tr>
                <tr>
                    <td><code>sops</code></td>
                    <td><code>ArrayList&lt;SOP&gt;</code></td>
                    <td>คู่มือการปรุงอาหารมาตรฐาน สำหรับให้คนครัวดูเวลาและขั้นตอนใน UC03</td>
                </tr>
                <tr>
                    <td><code>orders</code></td>
                    <td><code>ArrayList&lt;Order&gt;</code></td>
                    <td>ประวัติและคิวออเดอร์ทั้งหมดในร้าน ตั้งแต่ตะกร้า ปรุง เสิร์ฟ จนถึงชำระเงิน</td>
                </tr>
                <tr>
                    <td><code>purchaseOrders</code></td>
                    <td><code>ArrayList&lt;PurchaseOrder&gt;</code></td>
                    <td>รายการใบสั่งซื้อวัตถุดิบทั้งหมดของร้าน</td>
                </tr>
                <tr>
                    <td><code>manager, cashier, cook</code></td>
                    <td><code>Employee</code></td>
                    <td>พนักงานตัวแทน 3 บทบาทหลักที่ใช้แสดงและตรวจสอบสิทธิ์ในระบบ</td>
                </tr>
            </tbody>
        </table>

        <h2 class="section-title">3.3 การสร้างข้อมูลตั้งต้น createSampleData()</h2>
        <p>
            เมื่อโปรแกรมเริ่มทำงาน เมธอด <code>main()</code> จะเรียก <code>createSampleData()</code> เป็นลำดับแรก เพื่อจำลองสภาพแวดล้อมจริงของร้านข้าวต้มอารมณ์ดี:
        </p>
        <div class="card">
            <h4 style="margin-top:0; color:#1e3a8a;">รายละเอียดข้อมูลตัวอย่าง P4:</h4>
            <ul>
                <li><strong>โต๊ะอาหาร (4 โต๊ะ):</strong> T01 (4 ที่นั่ง), T02 (4 ที่นั่ง), T03 (2 ที่นั่ง), T04 (6 ที่นั่ง)</li>
                <li><strong>วัตถุดิบเริ่มต้น:</strong> เนื้อปลา 5.3 กก., ไข่ไก่ 3 ฟอง, หมูยอ 2 แท่ง, แหนม 2 แท่ง, น้ำยำ 2 ลิตร</li>
                <li><strong>เมนูอาหาร:</strong> ผัดกะเพราปลา (69 บาท) พร้อมออปชันเพิ่มไข่ดาว (15 บาท), ยำหมูยอ/แหนม (65 บาท)</li>
                <li><strong>สมาชิกตัวอย่าง:</strong> คุณอารมณ์ดี แจ่มใส (0812345678) แต้มสะสม 46 แต้ม</li>
            </ul>
        </div>
        
        <div class="code-container">
            <div class="code-header">
                <span>src/Main.java &rarr; createSampleData()</span>
                <span>Pre-seeded Business Data</span>
            </div>
            <div class="code-body">
                {code_create_sample}
            </div>
        </div>

        <h2 class="section-title">3.4 เครื่องมือรับคำสั่งและดักจับความผิดพลาด (Input Helpers)</h2>
        <p>
            ใน <code>Main.java</code> มีเมธอดสำหรับอ่านและตรวจสอบอินพุตจากผู้ใช้ เพื่อป้องกันไม่ให้เกิด <code>InputMismatchException</code> หรือโปรแกรมแครชเมื่อผู้ใช้พิมพ์ข้อมูลผิด:
        </p>
        <ul>
            <li><code>readText(String question)</code>: อ่านข้อความ 1 บรรทัด พร้อมตัดช่องว่าง (trim)</li>
            <li><code>readRequired(String question)</code>: วนลูปถามซ้ำจนกว่าผู้ใช้จะพิมพ์ข้อความที่ไม่ใช่ค่าว่าง</li>
            <li><code>readInt(String question, int min, int max)</code>: อ่านตัวเลขจำนวนเต็มในช่วง [min, max] หากพิมพ์ตัวอักษรจะพิมพ์แจ้งเตือนและให้กรอกใหม่</li>
            <li><code>readNumber(String question, double min, double max)</code>: อ่านตัวเลขทศนิยมในช่วงที่กำหนด</li>
            <li><code>confirm(String question)</code>: รับคำตอบ 1 (ใช่) หรือ 0 (ไม่ใช่) คืนค่าเป็น <code>boolean</code></li>
            <li><code>chooseMenu(), chooseIngredient(), chooseOrder()</code>: แสดงรายการอ็อบเจกต์เป็นเมนูตัวเลข 1, 2, 3... และแปลงค่าที่ผู้ใช้เลือกกลับเป็น Index ของ <code>ArrayList</code> (ใช้ <code>choice - 1</code>)</li>
        </ul>

        <div class="callout callout-warn">
            <div class="callout-title">กลไก Global Exception Handling ใน main():</div>
            ในลูปเมนูหลักของ <code>main()</code> มีการครอบบล็อก <code>try-catch</code> รับ <code>IllegalArgumentException</code> และ <code>IllegalStateException</code> เอาไว้เสมอ เมื่อคลาสใน <code>model</code> ตรวจพบว่าสต็อกไม่พอหรือเงินไม่พอและโยน Exception ออกมา <code>Main</code> จะจับข้อความไปพิมพ์เตือนบนหน้าจออย่างสุภาพ เช่น <em>"ทำรายการไม่ได้: วัตถุดิบไม่พอ: เนื้อปลา"</em> โดยไม่ทำให้โปรแกรมปิดตัวลงกลางคัน
        </div>

        <h2 class="section-title">3.5 ผ่าโค้ดการทำงานของ Use Cases (uc01 ถึง uc08)</h2>
        
        <div class="page-break">
            <h3 class="sub-title" style="color:#0369a1;">3.5.1 UC01: สั่งอาหารผ่าน QR โต๊ะและติดตามออเดอร์ (uc01 &amp; addFood)</h3>
            <p>
                <strong>ขั้นตอนการทำงาน:</strong> สแกนโต๊ะ (<code>scanTableQRCode</code>) &rarr; สร้าง Customer &rarr; ค้นหาและผูกสมาชิก &rarr; สร้าง Order สถานะ CART &rarr; วนลูปเพิ่มอาหารและ Topping ผ่าน <code>addFood</code> &rarr; ยืนยันออเดอร์ <code>order.confirm()</code> ตรวจสต็อกครบทุกตัวแล้วตัดสต็อกอะตอมมิก &rarr; โต๊ะเปลี่ยนเป็น "ใช้งาน"
            </p>
            <div class="code-container">
                <div class="code-header">
                    <span>src/Main.java &rarr; uc01() &amp; addFood()</span>
                    <span>Order Placement Workflow</span>
                </div>
                <div class="code-body">
                    {code_uc01}
                </div>
            </div>
            <div class="code-container">
                <div class="code-header">
                    <span>src/Main.java &rarr; addFood()</span>
                    <span>Add Item &amp; Option Logic</span>
                </div>
                <div class="code-body">
                    {code_add_food}
                </div>
            </div>
        </div>

        <div class="page-break">
            <h3 class="sub-title" style="color:#0369a1;">3.5.2 UC02: จัดการคู่มือ SOP (uc02)</h3>
            <p>
                <strong>ขั้นตอนการทำงาน:</strong> สร้าง SOP ใหม่ ผูกกับเมนู &rarr; เพิ่มขั้นตอนย่อยทีละข้อพร้อมเวลามาตรฐาน &rarr; คำนวณเวลารวมด้วย <code>getTotalMinutes()</code> &rarr; เผยแพร่คู่มือ <code>publish()</code> เพื่อให้ครัวนำไปใช้ หรือปิดใช้ <code>disable()</code>
            </p>
            <div class="code-container">
                <div class="code-header">
                    <span>src/Main.java &rarr; uc02()</span>
                    <span>SOP Management</span>
                </div>
                <div class="code-body">
                    {code_uc02}
                </div>
            </div>
        </div>

        <div class="page-break">
            <h3 class="sub-title" style="color:#0369a1;">3.5.3 UC03: ปรุงอาหารและเสิร์ฟ (uc03)</h3>
            <p>
                <strong>ขั้นตอนการทำงาน:</strong> คนครัวเลือกสถานีครัว &rarr; ดึงคิว OrderItem &rarr; เรียก <code>item.startCooking()</code> บันทึกเวลาเริ่ม &rarr; เมื่อทำเสร็จเรียก <code>item.markReady()</code> บันทึกเวลาจบและคำนวณเปรียบเทียบกับ SOP &rarr; บริกรเรียก <code>item.serve()</code> เปลี่ยนเป็นเสิร์ฟแล้ว &rarr; สั่ง <code>order.refreshStatus()</code>
            </p>
            <div class="code-container">
                <div class="code-header">
                    <span>src/Main.java &rarr; uc03()</span>
                    <span>Kitchen &amp; Serving Workflow</span>
                </div>
                <div class="code-body">
                    {code_uc03}
                </div>
            </div>
        </div>

        <div class="page-break">
            <h3 class="sub-title" style="color:#0369a1;">3.5.4 UC04: ชำระเงินและออกใบเสร็จ (uc04)</h3>
            <p>
                <strong>ขั้นตอนการทำงาน:</strong> แสดงออเดอร์ที่เสิร์ฟครบทุกจานแล้ว (<code>isServed() == true</code>) &rarr; ดึงแต้มสมาชิกมาแสดง &rarr; สมาชิกขอแลกแต้มส่วนลด (ขั้นต่ำ 10 แต้ม) &rarr; เลือกจ่ายเงินสดหรือ QR &rarr; เรียก <code>payment.pay(...)</code> เตรียมบิล &rarr; กดยืนยัน <code>payment.confirm()</code> หักแต้มที่ใช้ แจกแต้มใหม่ ปิดออเดอร์ &rarr; พิมพ์ใบเสร็จ &rarr; ปล่อยโต๊ะว่าง
            </p>
            <div class="code-container">
                <div class="code-header">
                    <span>src/Main.java &rarr; uc04()</span>
                    <span>Settlement &amp; Receipt Workflow</span>
                </div>
                <div class="code-body">
                    {code_uc04}
                </div>
            </div>
        </div>

        <div class="page-break">
            <h3 class="sub-title" style="color:#0369a1;">3.5.5 UC05: สต็อกและใบสั่งซื้อ (uc05)</h3>
            <p>
                <strong>ขั้นตอนการทำงาน:</strong> ตรวจสอบยอดสต็อกคงเหลือ แจ้งเตือนเมื่อต่ำกว่า <code>minQty</code> &rarr; ออกใบสั่งซื้อ PO เลือกซัพพลายเออร์ &rarr; เมื่อสินค้ามาส่ง เรียก <code>po.receive(qtys)</code> รับของเข้าคลังและบันทึก StockMovement อัตโนมัติ หรือปรับยอดตรวจนับด้วย <code>adjustStock</code>
            </p>
            <div class="code-container">
                <div class="code-header">
                    <span>src/Main.java &rarr; uc05()</span>
                    <span>Inventory &amp; PO Workflow</span>
                </div>
                <div class="code-body">
                    {code_uc05}
                </div>
            </div>
        </div>

        <div class="page-break">
            <h3 class="sub-title" style="color:#0369a1;">3.5.6 UC06: ภาพรวมและรายงานยอดขาย (uc06 &amp; printSales)</h3>
            <p>
                <strong>ขั้นตอนการทำงาน:</strong> รับช่วงวันที่เริ่มต้นและสิ้นสุด &rarr; วนลูปอ่าน Order ทั้งหมด กรองเฉพาะบิลที่จ่ายเงินแล้ว &rarr; รวมยอดสุทธิ แยกเงินสดและ QR &rarr; นับจำนวนจานที่ขายได้ของแต่ละเมนู &rarr; จัดอันดับเมนูยอดนิยมด้วย Simple Sort Algorithm
            </p>
            <div class="code-container">
                <div class="code-header">
                    <span>src/Main.java &rarr; uc06() &amp; printSales()</span>
                    <span>Sales Reporting &amp; Ranking</span>
                </div>
                <div class="code-body">
                    {code_uc06}
                </div>
            </div>
            <div class="code-container">
                <div class="code-header">
                    <span>src/Main.java &rarr; printSales()</span>
                    <span>Sales Aggregation Logic</span>
                </div>
                <div class="code-body">
                    {code_print_sales}
                </div>
            </div>
        </div>

        <div class="page-break">
            <h3 class="sub-title" style="color:#0369a1;">3.5.7 UC07: จัดการเมนูและสูตรอาหาร (uc07)</h3>
            <p>
                <strong>ขั้นตอนการทำงาน:</strong> สร้างเมนูใหม่ (สถานะเริ่ม OFF_SALE) &rarr; สร้างสูตรฉบับร่าง DRAFT ผูกวัตถุดิบและปริมาณ &rarr; เรียก <code>complete()</code> ยืนยันสูตรสมบูรณ์ &rarr; สั่ง <code>openSale()</code> เปิดขาย &rarr; แตกเวอร์ชันสูตรใหม่ <code>createNewVersion()</code> &rarr; เพิ่ม Topping ตัวเลือกเสริม
            </p>
            <div class="code-container">
                <div class="code-header">
                    <span>src/Main.java &rarr; uc07()</span>
                    <span>Menu Engineering Workflow</span>
                </div>
                <div class="code-body">
                    {code_uc07}
                </div>
            </div>
        </div>

        <div class="page-break">
            <h3 class="sub-title" style="color:#0369a1;">3.5.8 UC08: สมาชิกและแต้มสะสม (uc08)</h3>
            <p>
                <strong>ขั้นตอนการทำงาน:</strong> สมัครสมาชิกใหม่ด้วยเบอร์โทร 10 หลัก &rarr; ค้นหาและดูประวัติ Statement แต้ม &rarr; ผู้จัดการพิจารณาคำขอยกเลิกอาหารที่กำลังปรุงจากครัว (<code>approveRequests</code>) อนุมัติหรือปฏิเสธ &rarr; ผู้จัดการปรับเปลี่ยนกฎแต้มกลางของร้าน (<code>Member.setRule</code>)
            </p>
            <div class="code-container">
                <div class="code-header">
                    <span>src/Main.java &rarr; uc08()</span>
                    <span>Member &amp; Manager Approval Workflow</span>
                </div>
                <div class="code-body">
                    {code_uc08}
                </div>
            </div>
        </div>
    </div>
    """

def generate_chapter4_html():
    return """
    <div id="ch4" class="page-break">
        <h1 class="chapter-title">บทที่ 4: การเดินทางของข้อมูลแบบครบวงจร (Life of an Order)</h1>
        
        <h2 class="section-title">4.1 จำลองสถานการณ์จริง: โต๊ะ T01 สั่งอาหารและคิดเงิน</h2>
        <p>
            เพื่อความเข้าใจที่แจ่มชัดที่สุด ให้เราพิจารณากรณีศึกษาตัวอย่าง P4 ตามเอกสาร: ลูกค้าโต๊ะ T01 (ซึ่งเป็นสมาชิก คุณอารมณ์ดี มี 46 แต้ม) สั่งอาหาร 2 รายการ:
        </p>
        <ul>
            <li><strong>ผัดกะเพราปลา (M01):</strong> 2 จาน @ 69 บาท พร้อมตัวเลือก "เพิ่มไข่ดาว" ทั้ง 2 จาน @ 15 บาท = 2 × (69 + 15) = 168 บาท</li>
            <li><strong>ยำหมูยอ/แหนม (M02):</strong> 1 จาน @ 65 บาท = 65 บาท</li>
            <li><strong>ยอดรวมทั้งสิ้น:</strong> 168 + 65 = 233 บาท</li>
        </ul>

        <div class="card">
            <h3 style="margin-top:0; color:#1e3a8a;">การไหลของข้อมูลในระบบทีละสเต็ป (Step-by-Step Flow):</h3>
            
            <p><strong>สเต็ปที่ 1: สแกนโต๊ะและผูกสมาชิก (UC01)</strong><br>
            <code>Table t01</code> ถูกสแกน (<code>qrScanned = true</code>) &rarr; สร้าง <code>Customer cus</code> &rarr; ค้นพบสมาชิก <code>cus.linkMember(member)</code> &rarr; สร้าง <code>Order ord = new Order("ORD-1", t01, cus)</code> ในสถานะ <code>CART</code></p>
            
            <p><strong>สเต็ปที่ 2: หยิบอาหารใส่ตะกร้า (UC01)</strong><br>
            เรียก <code>ord.addItem(kaprao, 2, "เผ็ดกลาง", "ไม่ใส่ชูรส")</code> &rarr; สร้าง <code>OrderItem item1</code> พร้อมคัดลอกสูตรปลา 0.15 กก. ต่อจาน &rarr; เรียก <code>item1.addOption(0)</code> เพิ่มไข่ดาว บวกราคาเพิ่ม 15 บาท และเพิ่มไข่ไก่ 1 ฟองในสูตร Snapshot<br>
            เรียก <code>ord.addItem(yam, 1, "เผ็ดน้อย", "")</code> &rarr; สร้าง <code>OrderItem item2</code> คัดลอกสูตรหมูยอ 0.5 แท่ง, แหนม 0.5 แท่ง, น้ำยำ 0.1 ลิตร</p>
            
            <p><strong>สเต็ปที่ 3: ตรวจสอบสต็อกและยืนยันออเดอร์ (Two-Pass Confirmation)</strong><br>
            เมื่อผู้ใช้กดยืนยัน เรียก <code>ord.confirm()</code>:<br>
            &bull; <em>Pass 1 (ตรวจสอบ):</em> รวมวัตถุดิบทั้งหมด: ปลาต้องใช้ 0.15 × 2 = 0.30 กก. (มี 5.3 กก. พอ), ไข่ไก่ต้องใช้ 1 × 2 = 2 ฟอง (มี 3 ฟอง พอ), หมูยอ 0.5 แท่ง (พอ), แหนม 0.5 แท่ง (พอ), น้ำยำ 0.1 ลิตร (พอ)<br>
            &bull; <em>Pass 2 (ตัดสต็อก):</em> เรียก <code>deduct()</code> ของทุกวัตถุดิบ: ปลาเหลือ 5.0 กก., ไข่ไก่เหลือ 1 ฟอง, หมูยอเหลือ 1.5 แท่ง &rarr; แต่ละตัวสร้าง <code>StockMovement</code> ประเภท "ขาย"<br>
            &bull; ออเดอร์เปลี่ยนสถานะเป็น <code>CONFIRMED</code> และโต๊ะ T01 เปลี่ยนสถานะเป็น <code>ใช้งาน</code></p>
            
            <p><strong>สเต็ปที่ 4: ครัวปรุงอาหาร (UC03)</strong><br>
            คนครัวรับ <code>item1</code> เข้าสถานีครัวร้อน เรียก <code>item1.startCooking(cook, 5.0)</code> จดเวลาเริ่ม &rarr; ปรุงเสร็จเรียก <code>item1.markReady()</code> จดเวลาจบ<br>
            สถานีครัวยำทำ <code>item2</code> จนพร้อมเสิร์ฟเช่นเดียวกัน</p>
            
            <p><strong>สเต็ปที่ 5: เสิร์ฟอาหาร (UC03)</strong><br>
            พนักงานเสิร์ฟ <code>item1.serve(cashier)</code> และ <code>item2.serve(cashier)</code> &rarr; เรียก <code>ord.refreshStatus()</code> พบว่าอาหารเสิร์ฟครบทุกจาน ออเดอร์เปลี่ยนสถานะเป็น <code>SERVED</code></p>
            
            <p><strong>สเต็ปที่ 6: ชำระเงิน คิดแต้ม และปิดบิล (UC04)</strong><br>
            แคชเชียร์เลือกออเดอร์ ORD-1 (ยอดรวม 233 บาท) &rarr; ลูกค้าใช้ 10 แต้มแลกส่วนลด 10 บาท (ยอดสุทธิเหลือ 223 บาท) &rarr; ลูกค้าจ่ายเงินสด 250 บาท (เงินทอน 27 บาท)<br>
            เมื่อกดยืนยันชำระเงิน <code>payment.confirm()</code>:<br>
            &bull; แต้มสมาชิกถูกหัก 10 แต้ม: 46 - 10 = เหลือ 36 แต้ม (สร้าง PointTransaction ประเภท "แลก")<br>
            &bull; คำนวณแต้มสะสมใหม่จากยอดสุทธิ: 223 ÷ 50 = 4 แต้ม (ปัดเศษทิ้ง)<br>
            &bull; แต้มสะสมเพิ่ม 4 แต้ม: 36 + 4 = <strong>ยอดสุทธิสุดท้าย 40 แต้ม</strong> (สร้าง PointTransaction ประเภท "สะสม")<br>
            &bull; ออเดอร์เปลี่ยนสถานะเป็น <code>PAID</code> และโต๊ะ T01 เปลี่ยนสถานะกลับเป็น <code>ว่าง</code></p>
            
            <p><strong>สเต็ปที่ 7: รายงานผลการขาย (UC06)</strong><br>
            เมื่อผู้จัดการเปิดรายงานยอดขาย ยอดเงินสด 223 บาทจะถูกบันทึกเข้ารายรับของวัน และผัดกะเพราปลาจะถูกนับยอดขาย 2 จาน, ยำหมูยอถูกนับ 1 จานในการจัดอันดับเมนูยอดนิยม</p>
        </div>

        <h2 class="section-title">4.2 แผนภาพสถานะ (State Transition Diagram)</h2>
        <table>
            <thead>
                <tr>
                    <th style="width: 20%;">เอนทิตี</th>
                    <th style="width: 25%;">สถานะที่เป็นไปได้</th>
                    <th style="width: 25%;">เหตุการณ์ที่ทำให้เปลี่ยน (Trigger)</th>
                    <th>เงื่อนไขสำคัญที่ต้องผ่าน (Guards)</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Order</strong></td>
                    <td>CART &rarr; CONFIRMED &rarr; COOKING &rarr; READY &rarr; SERVED &rarr; PAID</td>
                    <td>สแกนโต๊ะ &rarr; confirm() &rarr; ครัวเริ่มปรุงจานแรก &rarr; ปรุงเสร็จครบ &rarr; เสิร์ฟครบ &rarr; payment.confirm()</td>
                    <td>ตะกร้าต้องมีอาหาร, สต็อกต้องพอทุกตัว, การชำระเงินต้องทำได้เมื่ออาหารเสิร์ฟครบทุกจานแล้วเท่านั้น</td>
                </tr>
                <tr>
                    <td><strong>OrderItem</strong></td>
                    <td>WAITING &rarr; COOKING &rarr; READY &rarr; SERVED (หรือ CANCELLED)</td>
                    <td>confirm ออเดอร์ &rarr; startCooking() &rarr; markReady() &rarr; serve() (หรือ cancel() / decideRequest())</td>
                    <td>ต้องเคยตัดสต็อกจริง, ต้องไม่มีคำขอค้างที่รอผู้จัดการอนุมัติ, หากกำลังปรุงอยู่ต้องผ่านผู้จัดการเท่านั้น</td>
                </tr>
                <tr>
                    <td><strong>PurchaseOrder</strong></td>
                    <td>DRAFT &rarr; ORDERED &rarr; RECEIVED</td>
                    <td>สร้างเอกสาร &rarr; markOrdered() &rarr; receive(qtys)</td>
                    <td>ต้องมีรายการสั่ง, ซัพพลายเออร์ต้องส่งวัตถุดิบนั้นได้, จำนวนรับจริงต้องเป็นตัวเลขครบทุกรายการ</td>
                </tr>
                <tr>
                    <td><strong>Table</strong></td>
                    <td>ว่าง &rarr; ใช้งาน &rarr; ว่าง</td>
                    <td>เปิดร้าน &rarr; order.confirm() &rarr; payment.confirm()</td>
                    <td>โต๊ะต้องผ่านการสแกน QR ก่อนนำรหัสไปเปิดบิล</td>
                </tr>
            </tbody>
        </table>
    </div>
    """

def generate_chapter5_html():
    return """
    <div id="ch5" class="page-break">
        <h1 class="chapter-title">บทที่ 5: คลังข้อสอบและแนวทางตอบคำถามสำหรับนำเสนอ (Defense Cheatsheet)</h1>
        <p>
            รวบรวม 15 คำถามสำคัญที่คณะกรรมการสอบ อาจารย์ผู้ทรงคุณวุฒิ หรือผู้ตรวจประเมินโปรเจกต์มักจะถาม พร้อมแนวทางการตอบที่ถูกต้องตามหลักการวิเคราะห์และออกแบบเชิงวัตถุ (OOAD) และมาตรฐานสถาปัตยกรรมซอฟต์แวร์:
        </p>
        
        <div class="card">
            <h4 style="margin-top:0; color:#1e3a8a;">คำถามที่ 1: ทำไมระบบนี้จึงแยก Main ออกจาก 16 คลาสในแพ็กเกจ model?</h4>
            <p><strong>แนวทางการตอบ:</strong> เป็นไปตามหลักการ Separation of Concerns (SoC) และ Single Responsibility Principle (SRP) คลาสใน <code>model</code> มีหน้าที่ดูแลข้อมูล กฎเกณฑ์ทางธุรกิจ และความถูกต้องของตนเอง โดยไม่ขึ้นกับว่าผู้ใช้จะติดต่อผ่านหน้าจอแบบใด ส่วน <code>Main</code> ทำหน้าที่เป็น Presentation และ Orchestrator หากในอนาคตเราต้องการเปลี่ยนหน้าจอจากคอนโซล Text Mode ไปเป็นหน้าเว็บ หรือแอปมือถือ เราสามารถนำคลาสทั้ง 16 ใน <code>model</code> ไปใช้งานต่อได้ทันทีโดยไม่ต้องแก้ไขโค้ดตรรกะธุรกิจเลย</p>
        </div>

        <div class="card">
            <h4 style="margin-top:0; color:#1e3a8a;">คำถามที่ 2: ทำไมจึงไม่มีการใช้ Inheritance (extends) ระหว่าง 16 คลาสนี้เลย?</h4>
            <p><strong>แนวทางการตอบ:</strong> เพราะคลาสทั้ง 16 ในระบบร้านอาหารนี้มีความสัมพันธ์เชิงธุรกิจแบบ <em>has-a (เป็นเจ้าของหรือรู้จักกัน)</em> ไม่ใช่ความสัมพันธ์แบบ <em>is-a (เป็นชนิดย่อยของกันและกัน)</em> เช่น โต๊ะไม่ได้เป็นลูกค้า, ลูกค้าไม่ได้เป็นออเดอร์, และออเดอร์ไม่ได้เป็นอาหาร การฝืนใช้ Inheritance จะทำให้เกิดสถาปัตยกรรมที่ผิดเพี้ยนและเกิด Coupling สูง เราจึงยึดหลักการสากล "Composition over Inheritance" ตามแนวทางของ Clean OOP</p>
        </div>

        <div class="card">
            <h4 style="margin-top:0; color:#1e3a8a;">คำถามที่ 3: ทำไมใน Order.confirm() ถึงต้องตรวจสต็อก 2 รอบ (Two-Pass Loop)?</h4>
            <p><strong>แนวทางการตอบ:</strong> เพื่อรักษาความเป็น Atomic Transaction (All-or-Nothing) หากออเดอร์ต้องใช้เนื้อปลาและไข่ไก่ แต่เราวนลูปตรวจเนื้อปลาแล้วตัดเนื้อปลาทันที ก่อนจะไปพบว่าไข่ไก่หมด จะทำให้คำสั่งซื้อล้มเหลวแต่เนื้อปลาถูกตัดไปแล้ว เกิดความเสียหายต่อสต็อกสินค้า ดังนั้นเราจึงต้องใช้ Loop ที่ 1 ตรวจสอบวัตถุดิบทุกชนิดให้มั่นใจว่าพอครบ 100% ก่อน เมื่อผ่านหมดแล้วจึงค่อยเข้า Loop ที่ 2 เพื่อตัดสต็อกจริง</p>
        </div>

        <div class="card">
            <h4 style="margin-top:0; color:#1e3a8a;">คำถามที่ 4: ทำไม OrderItem ต้องคัดลอกราคาและสูตรมาจาก Menu มาเก็บไว้เอง (Snapshot Pattern)?</h4>
            <p><strong>แนวทางการตอบ:</strong> เพื่อรักษาประวัติศาสตร์และความถูกต้องทางบัญชี หากร้านเปิดมา 1 ปีแล้วผู้จัดการขึ้นราคาผัดกะเพราจาก 69 บาทเป็น 80 บาท หรือเชฟปรับสูตรลดเนื้อปลาลง บิลและประวัติออเดอร์ของลูกค้าเก่าที่เคยสั่งไปเมื่อสัปดาห์ก่อนจะต้องไม่เปลี่ยนราคาและสูตรตามไปด้วย การทำ Snapshot ไว้ใน <code>OrderItem</code> ทำให้ข้อมูลในอดีตคงเดิมอย่างถาวร</p>
        </div>

        <div class="card">
            <h4 style="margin-top:0; color:#1e3a8a;">คำถามที่ 5: ในภาษา Java มี Garbage Collection อยู่แล้ว ทำไมเรายังต้องเขียนเมธอด destroy() ขึ้นมาเอง?</h4>
            <p><strong>แนวทางการตอบ:</strong> Garbage Collector (GC) ของ Java จะลบอ็อบเจกต์ออกจากหน่วยความจำก็ต่อเมื่อ <em>ไม่มีใครอ้างถึงอ็อบเจกต์นั้นแล้ว</em> แต่ในระดับการออกแบบเชิงตรรกะ (Domain Modeling) เมธอด <code>destroy()</code> ที่เราเขียนขึ้นทำหน้าที่เป็น <strong>Lifecycle Cascade Hook</strong> เพื่อสะท้อนกฎ Composition อย่างชัดเจน เช่น เมื่อ <code>Order.destroy()</code> ถูกเรียก มันจะสั่ง <code>item.destroy()</code> ทุกตัว และเคลียร์ลิงก์ต่าง ๆ ทิ้ง ทำให้ไม่มีการอ้างอิงค้างอยู่ และช่วยให้ GC สามารถเก็บกวาดหน่วยความจำได้อย่างรวดเร็วและปลอดภัย</p>
        </div>

        <div class="card">
            <h4 style="margin-top:0; color:#1e3a8a;">คำถามที่ 6: ทำไมฟิลด์กฎแต้มใน Member ถึงประกาศเป็น static แต่ยอดแต้มสะสมเป็นธรรมดา?</h4>
            <p><strong>แนวทางการตอบ:</strong> ยอดแต้มสะสม (<code>points</code>) เป็นของสมาชิกแต่ละคน สมาชิก A มี 40 แต้ม สมาชิก B มี 10 แต้ม จึงต้องเป็น Instance Variable แต่กฎเกณฑ์การคำนวณ เช่น อัตรา 50 บาทได้ 1 แต้ม (<code>bahtPerPoint</code>) หรือ 1 แต้มเท่ากับ 1 บาท (<code>pointValue</code>) เป็นนโยบายการตลาดของร้านที่สมาชิกทุกคนต้องปฏิบัติตามเหมือนกันหมด จึงประกาศเป็น <code>static</code> (Class Variable) ทำให้เมื่อผู้จัดการแก้ไขกฎผ่าน <code>Member.setRule()</code> จะมีผลต่อสมาชิกทุกคนทั้งร้านทันที</p>
        </div>

        <div class="card">
            <h4 style="margin-top:0; color:#1e3a8a;">คำถามที่ 7: ทำไมใน Recipe ถึงใช้ List 2 ชุด (ingredients และ quantities) แทนที่จะใช้ Map?</h4>
            <p><strong>แนวทางการตอบ:</strong> ตามหลักสูตรการสอนและการอธิบาย OOP ขั้นพื้นฐาน การใช้ List สองชุดที่ตรงกันด้วย Index (Parallel Lists) เช่น ตำแหน่งที่ 0 คือวัตถุดิบปลา และตำแหน่งที่ 0 ของอีก List คือปริมาณปลา 0.15 กก. ช่วยให้ผู้เรียนสามารถไล่ติดตามค่าด้วยลูป <code>for (int i = 0; i &lt; size; i++)</code> ได้อย่างตรงไปตรงมา และไม่ก่อให้เกิดปัญหาเรื่องการเรียงลำดับของ Key เหมือนในโครงสร้าง Map ทั่วไป</p>
        </div>

        <div class="card">
            <h4 style="margin-top:0; color:#1e3a8a;">คำถามที่ 8: มี Constructor แล้ว ทำไมคลาสต่าง ๆ ยังต้องมีเมธอดอ่านข้อมูล (เช่น name(), stockQty())?</h4>
            <p><strong>แนวทางการตอบ:</strong> เพราะ Constructor ทำงานเพียง <em>ครั้งเดียวตอนสร้างอ็อบเจกต์ (ตอน new)</em> แต่หลังจากสร้างอ็อบเจกต์ขึ้นมาแล้ว โปรแกรมยังต้องมีการทำงานต่อเนื่องอีกยาวนาน เช่น หน้าจอ <code>Main</code> ต้องการนำชื่ออาหาร ราคา ยอดเงิน สถานะ และสต็อกคงเหลือไปแสดงผลให้ผู้ใช้ดู จึงจำเป็นต้องมีเมธอดอ่านข้อมูลเพื่อเปิดช่องทางให้ภายนอกอ่านค่าฟิลด์ที่เป็น <code>private</code> ได้โดยไม่ละเมิด Encapsulation</p>
        </div>

        <div class="card">
            <h4 style="margin-top:0; color:#1e3a8a;">คำถามที่ 9: ทำไมในคลาสของแพ็กเกจ model ถึงไม่มีคำสั่ง System.out.println() แม้แต่บรรทัดเดียว?</h4>
            <p><strong>แนวทางการตอบ:</strong> เพราะคลาสใน <code>model</code> เป็น Business Entity ที่ไม่ควรผูกติดกับอุปกรณ์แสดงผล (Output Device) หากคลาสโมเดลมีคำสั่งพิมพ์หน้าจอคอนโซล เมื่อนำคลาสนี้ไปใช้งานบนเว็บหรือแอปพลิเคชัน ข้อความเหล่านั้นจะกลายเป็นข้อความขยะในเซิร์ฟเวอร์ หน้าที่การแสดงผลและการจัดรูปแบบข้อความจึงเป็นหน้าที่ของคลาส <code>Main</code> เพียงผู้เดียว</p>
        </div>

        <div class="card">
            <h4 style="margin-top:0; color:#1e3a8a;">คำถามที่ 10: enum ที่อยู่ในคลาส เช่น OrderStatus หรือ Role ทำให้มีจำนวนคลาสเกิน 16 หรือไม่?</h4>
            <p><strong>แนวทางการตอบ:</strong> ไม่เกินครับ เพราะโครงสร้างไฟล์ในระบบมี 16 ไฟล์ Java ใน <code>src/model</code> พอดี โดย <code>enum</code> ถูกประกาศเป็นสมาชิกภายในคลาสของตนเอง (Nested Enum) เช่น <code>Order.OrderStatus</code> หรือ <code>Employee.Role</code> ทำให้ขอบเขตของ enum ผูกอยู่กับคลาสนั้นอย่างสมเหตุสมผล และไม่มีไฟล์คลาสสนับสนุนแยกย่อยภายนอก</p>
        </div>

        <div class="card">
            <h4 style="margin-top:0; color:#1e3a8a;">คำถามที่ 11: ทำไมลูกค้าถึงกดยกเลิกอาหารเองไม่ได้เมื่ออาหารเริ่มปรุงแล้ว?</h4>
            <p><strong>แนวทางการตอบ:</strong> เป็นการสะท้อน Business Logic จริงของร้านอาหาร เมื่ออาหารอยู่ในสถานะ <code>WAITING</code> (รอปรุง) พนักงานยังไม่ได้นำวัตถุดิบไปปรุง ลูกค้าจึงยกเลิกได้ทันทีและสต็อกจะถูกคืนเข้าคลัง แต่หากอาหารเปลี่ยนเป็น <code>COOKING</code> (กำลังปรุง) วัตถุดิบได้ถูกใช้ลงกระทะไปแล้ว หากลูกค้ายกเลิกโดยพลการร้านจะขาดทุน จึงต้องออกแบบให้ส่งคำขอพิเศษ (<code>requestChange</code>) ไปยังหน้าจอของผู้จัดการเพื่อให้ผู้จัดการพิจารณาอนุมัติหรือปฏิเสธเป็นกรณีพิเศษ</p>
        </div>

        <div class="card">
            <h4 style="margin-top:0; color:#1e3a8a;">คำถามที่ 12: การสแกน QR Code โต๊ะใน Terminal ทำงานอย่างไร ทั้งที่ไม่มีกล้องจริง?</h4>
            <p><strong>แนวทางการตอบ:</strong> เป็นการจำลอง (Simulation) โดยในคลาส <code>Table</code> จะมีเมธอด <code>scanTableQRCode()</code> ซึ่งทำหน้าที่ตั้งค่าแฟล็ก <code>qrScanned = true</code> เมื่อผู้ใช้เลือกโต๊ะในหน้าจอ UC01 ระบบจะจำลองว่าลูกค้าได้นำกล้องมาสแกนแล้ว และเมธอด <code>identifyTableNumber()</code> จะยอมคืนรหัสโต๊ะให้เปิดออเดอร์ได้เฉพาะเมื่อแฟล็กนี้เป็นจริงเท่านั้น หากไม่ได้สแกนจะโยน <code>IllegalStateException</code> ออกมาทันที</p>
        </div>

        <div class="card">
            <h4 style="margin-top:0; color:#1e3a8a;">คำถามที่ 13: ทำไม Customer จึงไม่ถูกลบเมื่อ Order ถูกลบ?</h4>
            <p><strong>แนวทางการตอบ:</strong> เพราะความสัมพันธ์ระหว่าง <code>Order</code> กับ <code>Customer</code> เป็นแบบ Association ลูกค้าเป็นบุคคลภายนอกที่เข้ามาใช้บริการ ในขณะที่ Order เป็นเพียงเอกสารการสั่งอาหาร 1 ครั้ง เมื่อบิลอาหารสิ้นสุดลง ข้อมูลตัวแทนลูกค้ายังคงสามารถคงอยู่ได้เพื่อใช้วิเคราะห์หรือเชื่อมโยงกับบัญชีสมาชิก</p>
        </div>

        <div class="card">
            <h4 style="margin-top:0; color:#1e3a8a;">คำถามที่ 14: ปัญหา Floating Point ป้องกันอย่างไรตอนตัดสต็อกและคำนวณเงิน?</h4>
            <p><strong>แนวทางการตอบ:</strong> ในการเปรียบเทียบสต็อกของ <code>Ingredient.hasEnough(qty)</code> มีการบวกค่าเผื่อความคลาดเคลื่อน (Epsilon) <code>0.000001</code> เข้าไปก่อนเทียบ เพื่อป้องกันข้อผิดพลาดการปัดเศษของเลขฐานสองในชนิดข้อมูล double ส่วนในการคำนวณเงินทอนและยอดสต็อก มีการใช้ฟังก์ชัน <code>Math.round(...)</code> ปัดทศนิยมให้ตรงกับหน่วยสตางค์และหน่วยกรัมอย่างแม่นยำ</p>
        </div>

        <div class="card">
            <h4 style="margin-top:0; color:#1e3a8a;">คำถามที่ 15: หากระบบไฟดับหรือปิดโปรแกรม ข้อมูลในร้านจะหายหรือไม่ เพราะเหตุใด?</h4>
            <p><strong>แนวทางการตอบ:</strong> ข้อมูลจะหายและกลับไปเริ่มต้นที่ข้อมูลตัวอย่างใหม่ครับ เพราะระบบฉบับนี้เป็นการจำลองสถาปัตยกรรม OOP เชิงตรรกะแบบ In-Memory Collections (เก็บใน RAM ผ่าน ArrayList) เพื่อวัตถุประสงค์ในการศึกษาโครงสร้างอ็อบเจกต์ โดยยังไม่ได้เชื่อมต่อกับระบบจัดเก็บข้อมูลถาวร (Persistent Storage) เช่น ฐานข้อมูล SQL ซึ่งเป็นสเต็ปการต่อยอดในระยะต่อไป</p>
        </div>
    </div>
    """

def generate_chapter6_html():
    return """
    <div id="ch6" class="page-break">
        <h1 class="chapter-title">บทที่ 6: บทสรุปและแนวทางการพัฒนาต่อยอดสู่ระดับ Enterprise</h1>
        
        <h2 class="section-title">6.1 สรุปสาระสำคัญของโครงสร้างระบบ (Project Summary)</h2>
        <p>
            ระบบบริหารจัดการร้านอาหาร <strong>"ข้าวต้มอารมณ์ดี"</strong> ในฉบับ Java OOP 17 คลาสนี้ ได้บรรลุเป้าหมายสำคัญทางวิศวกรรมซอฟต์แวร์และการออกแบบเชิงวัตถุอย่างสมบูรณ์แบบ:
        </p>
        <ul>
            <li><strong>ความสอดคล้องกับระเบียบวิธี OOAD:</strong> สามารถแปลงโมเดลเชิงแนวคิดจากสไลด์และ Use Cases (P1–P8) สู่อ็อบเจกต์จริงในภาษา Java ได้อย่างถูกต้องครบถ้วนทั้ง 8 งาน</li>
            <li><strong>การปฏิบัติตามหลักการ Encapsulation:</strong> ข้อมูลทั้งหมดถูกปกป้องและเปลี่ยนแปลงผ่านเมธอดที่มีการตรวจสอบกฎเกณฑ์ทางธุรกิจอย่างเข้มงวด</li>
            <li><strong>ความชัดเจนของ Composition ทั้ง 5 คู่:</strong> มีหลักฐานการทำลายวงจรชีวิต (destroy cascade) ที่พิสูจน์ได้จริงในระดับซอร์สโค้ด</li>
            <li><strong>ความปลอดภัยในการทำธุรกรรม:</strong> ใช้รูปแบบ Two-Pass Validation ในการตัดสต็อกและการตรวจรับสินค้า เพื่อป้องกันสภาวะข้อมูลไม่สอดคล้องกัน</li>
        </ul>

        <h2 class="section-title">6.2 แผนที่การพัฒนาต่อยอดสู่ระบบจริง (Enterprise Modernization Roadmap)</h2>
        <p>
            หากต้องการนำระบบนี้ไปพัฒนาต่อยอดเพื่อใช้งานในร้านอาหารจริงในเชิงพาณิชย์ สามารถดำเนินตามขั้นตอนวิศวกรรมซอฟต์แวร์สมัยใหม่ได้ดังนี้:
        </p>
        
        <div class="card">
            <h3 style="margin-top:0; color:#1e3a8a;">ระยะที่ 1: การเปลี่ยน In-Memory สู่ Relational Database (JPA / PostgreSQL)</h3>
            <p>
                เปลี่ยน <code>ArrayList</code> ใน <code>Main</code> ไปเป็นตารางในฐานข้อมูลเชิงสัมพันธ์ โดยใช้ <strong>Spring Data JPA / Hibernate</strong>:
            </p>
            <ul>
                <li>คลาสโมเดลทั้ง 16 จะถูกใส่คำอธิบายประกอบ (Annotations) เช่น <code>@Entity</code>, <code>@Table</code>, <code>@Id</code></li>
                <li>ความสัมพันธ์ Composition จะถูกแปลงเป็น <code>@OneToMany(cascade = CascadeType.ALL, orphanRemoval = true)</code> ซึ่งจะทำหน้าที่เหมือนเมธอด <code>destroy()</code> โดยอัตโนมัติในระดับฐานข้อมูล</li>
                <li>ความสัมพันธ์ Association จะถูกแปลงเป็น <code>@ManyToOne(fetch = FetchType.LAZY)</code> เพื่อเพิ่มประสิทธิภาพในการสืบค้น</li>
            </ul>
        </div>

        <div class="card">
            <h3 style="margin-top:0; color:#1e3a8a;">ระยะที่ 2: การพัฒนา RESTful API และ Layered Architecture</h3>
            <p>
                ปรับเปลี่ยนสถาปัตยกรรมจากไฟล์ <code>Main</code> เดี่ยว ให้เป็น <strong>3-Tier Layered Architecture</strong>:
            </p>
            <ul>
                <li><strong>Controller Layer:</strong> สร้าง <code>@RestController</code> เช่น <code>OrderController</code>, <code>MenuController</code> เพื่อให้บริการรับส่งข้อมูลในรูปแบบ JSON</li>
                <li><strong>Service Layer:</strong> ย้ายตรรกะการประสานงาน Use Cases จาก <code>uc01()</code> ถึง <code>uc08()</code> ไปอยู่ใน <code>OrderService</code>, <code>PaymentService</code>, <code>StockService</code> พร้อมใส่ <code>@Transactional</code> เพื่อควบคุมความปลอดภัยของธุรกรรม</li>
                <li><strong>Repository Layer:</strong> อินเทอร์เฟซ <code>JpaRepository</code> สำหรับจัดการบันทึกและสืบค้นข้อมูลจากฐานข้อมูล</li>
            </ul>
        </div>

        <div class="card">
            <h3 style="margin-top:0; color:#1e3a8a;">ระยะที่ 3: ส่วนติดต่อผู้ใช้สมัยใหม่ (Modern UI / UX)</h3>
            <p>
                สร้างเว็บแอปพลิเคชันและแอปพลิเคชันบนอุปกรณ์พกพา:
            </p>
            <ul>
                <li><strong>Customer Mobile Web (React / Vue):</strong> ให้ลูกค้าสแกน QR Code จริงบนโต๊ะผ่านกล้องมือถือ ดูเมนูรูปภาพสวยงาม สั่งอาหาร และติดตามสถานะแบบเรียลไทม์ผ่าน WebSocket</li>
                <li><strong>Kitchen Display System (KDS):</strong> หน้าจอแท็บเล็ตสำหรับคนครัวในแต่ละสถานี แสดงคิวอาหาร จับเวลา และกดแจ้งพร้อมเสิร์ฟ</li>
                <li><strong>POS Cashier Terminal:</strong> หน้าจอสัมผัสสำหรับแคชเชียร์ คิดเงิน สแกนจ่าย Thai QR PromptPay และพิมพ์ใบเสร็จผ่านเครื่องพิมพ์ความร้อน (Thermal Printer)</li>
            </ul>
        </div>
        
        <div style="text-align: center; margin-top: 40px; padding: 20px; border-top: 1px solid #cbd5e1; color: #64748b; font-size: 9pt;">
            --- สิ้นสุดคู่มือการเรียนรู้และเจาะลึกโค้ด Java OOP 17 คลาส ระบบร้านข้าวต้มอารมณ์ดี ---
        </div>
    </div>
    """

def main():
    print("Generating comprehensive HTML...")
    html_content = f"""<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <title>คู่มือเจาะลึกและเรียนรู้โค้ด Java OOP 17 คลาส - ระบบร้านข้าวต้มอารมณ์ดี</title>
    <style>
        {build_css()}
    </style>
</head>
<body>
    {generate_cover_html()}
    {generate_toc_html()}
    {generate_chapter1_html()}
    {generate_chapter2_html()}
    {generate_chapter3_html()}
    {generate_chapter4_html()}
    {generate_chapter5_html()}
    {generate_chapter6_html()}
</body>
</html>
"""

    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Saved HTML to {OUTPUT_HTML} (Size: {len(html_content):,} bytes)")

    print("Rendering PDF via Google Chrome headless...")
    cmd = [
        "google-chrome-stable",
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--no-pdf-header-footer",
        f"--print-to-pdf={OUTPUT_PDF}",
        OUTPUT_HTML
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("Chrome error:", res.stderr)
        sys.exit(1)

    pdf_size = os.path.getsize(OUTPUT_PDF)
    print(f"PDF successfully generated: {OUTPUT_PDF} (Size: {pdf_size:,} bytes)")

if __name__ == "__main__":
    main()
