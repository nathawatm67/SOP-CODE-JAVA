#!/bin/bash
# คอมไพล์ Main และ model 16 คลาส แล้วเปิดเมนู
set -e
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
JAVAC_CMD="javac"
JAVA_CMD="java"
if [ -n "${JAVA_HOME:-}" ]; then
    JAVAC_CMD="$JAVA_HOME/bin/javac"
    JAVA_CMD="$JAVA_HOME/bin/java"
elif ! command -v javac > /dev/null 2>&1; then
    if [ -x "/home/liella/.gemini/antigravity-ide/scratch/jdk/bin/javac" ]; then
        JAVAC_CMD="/home/liella/.gemini/antigravity-ide/scratch/jdk/bin/javac"
        JAVA_CMD="/home/liella/.gemini/antigravity-ide/scratch/jdk/bin/java"
    else
        echo "กรุณาติดตั้ง JDK 17+ หรือกำหนด JAVA_HOME"
        exit 1
    fi
fi
mkdir -p bin
"$JAVAC_CMD" -encoding UTF-8 -d bin src/model/*.java src/Main.java
"$JAVA_CMD" -Dfile.encoding=UTF-8 -cp bin Main
