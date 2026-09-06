# PowerShell Quick Launcher for WikiAgent Terminal CLI
$ErrorActionPreference = "Stop"

$env:PYTHONIOENCODING = "utf-8"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$VenvPython = Join-Path $ScriptDir ".venv\Scripts\python.exe"
$AgentScript = Join-Path $ScriptDir "agent.py"

if (-not (Test-Path $VenvPython)) {
    Write-Error "Virtual environment not found at '$VenvPython'. Run 'python -m venv .venv' first."
    exit 1
}

Write-Host "Starting Wikipedia Chatbot Terminal Agent..." -ForegroundColor Cyan
& $VenvPython $AgentScript
