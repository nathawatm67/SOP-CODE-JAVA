#!/usr/bin/env python3
"""เทียบชื่อ/ชนิด field และลายเซ็น method กับกล่อง P7 จาก Canva ล่าสุด."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SNAPSHOT = Path(__file__).with_name("P7-CANVA-LATEST.json")


def split_params(text):
    parts = []
    current = ""
    depth = 0
    for char in text:
        if char == "<":
            depth += 1
        elif char == ">":
            depth -= 1
        if char == "," and depth == 0:
            parts.append(current.strip())
            current = ""
        else:
            current += char
    if current.strip():
        parts.append(current.strip())
    return parts


def compact(text):
    return re.sub(r"\s+", "", text)


source = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
problems = []
for diagram in source["diagrams"]:
    raw = diagram["raw"]
    class_name = raw.splitlines()[0].strip()
    java = (ROOT / "src/model" / (class_name + ".java")).read_text(encoding="utf-8")

    expected_fields = {
        name: compact(kind)
        for name, kind in re.findall(
            r"-\s*([A-Za-z]\w*)\s*:\s*([A-Za-z]\w*(?:<[^>]+>)?)", raw
        )
    }
    actual_fields = {
        name: compact(kind)
        for kind, name in re.findall(
            r"(?m)^\s*private\s+(?:static\s+)?([\w<>?, ]+?)\s+(\w+)\s*(?:=|;)",
            java,
        )
    }
    for name, expected_type in expected_fields.items():
        if name not in actual_fields:
            problems.append(f"{class_name}: ขาด field {name}")
        elif actual_fields[name] != expected_type:
            problems.append(
                f"{class_name}.{name}: P7={expected_type}, Java={actual_fields[name]}"
            )

    actual_methods = []
    pattern = r"\b(public|private|protected)\s+(?:static\s+)?(?:([\w<>?, ]+?)\s+)?(\w+)\s*\(([^)]*)\)\s*\{"
    for match in re.finditer(pattern, java, re.S):
        params = []
        for part in split_params(match.group(4)):
            kind, name = part.rsplit(" ", 1)
            params.append((compact(kind), name))
        actual_methods.append((match.group(3), compact(match.group(2) or ""), params))

    operation_count = 0
    for match in re.finditer(
        r"\+\s*([A-Za-z]\w*)\s*\((.*?)\)\s*(?::\s*([\w<>]+))?", raw, re.S
    ):
        operation_count += 1
        method_name, raw_params, return_type = match.groups()
        expected_params = []
        for part in split_params(raw_params):
            name, kind = part.split(":", 1)
            expected_params.append((compact(kind), name.strip()))
        expected_return = return_type or ""
        if not any(
            name == method_name and kind == expected_return and params == expected_params
            for name, kind, params in actual_methods
        ):
            problems.append(
                f"{class_name}.{method_name}({raw_params}): ลายเซ็นหรือชื่อพารามิเตอร์ไม่ตรง P7"
            )
    print(f"{class_name}: {len(expected_fields)} fields, {operation_count} operations")

print(f"\nจุดต่าง {len(problems)} รายการ")
for problem in problems:
    print("-", problem)
