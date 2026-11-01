@echo off
chcp 65001 > nul
cd /d "%~dp0"
if not exist "bin" mkdir bin
if defined JAVA_HOME (
    "%JAVA_HOME%\bin\javac" -encoding UTF-8 -d bin src\model\*.java src\Main.java
) else (
    javac -encoding UTF-8 -d bin src\model\*.java src\Main.java
)
if errorlevel 1 (
    echo กรุณาตรวจสอบ JDK 17+ หรือ JAVA_HOME
    exit /b 1
)
if defined JAVA_HOME (
    "%JAVA_HOME%\bin\java" -Dfile.encoding=UTF-8 -cp bin Main
) else (
    java -Dfile.encoding=UTF-8 -cp bin Main
)
