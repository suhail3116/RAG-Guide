@echo off
title Wikipedia Chatbot Terminal Agent
chcp 65001 > nul
set PYTHONIOENCODING=utf-8
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo Error: Virtual environment not found. Please setup .venv first.
    pause
    exit /b 1
)

echo Starting Wikipedia Chatbot Terminal Agent...
.venv\Scripts\python.exe agent.py
pause
