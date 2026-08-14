# Windows preflight for the EEL 4664 Webots environment.
$ErrorActionPreference = 'Stop'

$python = Get-Command python.exe -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Host '[FAIL] Python is not available on PATH.' -ForegroundColor Red
    Write-Host 'Install 64-bit Python 3.11 or newer from python.org, check "Add python.exe to PATH", open a new PowerShell window, and retry.'
    exit 1
}

$pythonPath = $python.Source
if ($pythonPath -like '*\WindowsApps\*') {
    Write-Host "[FAIL] 'python' resolves to the Microsoft Store/App Execution Alias: $pythonPath" -ForegroundColor Red
    Write-Host 'Install normal CPython from python.org, put it on PATH, and configure its full path in Webots Preferences.'
    exit 1
}

$versionOutput = & $pythonPath --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "[FAIL] Python was found at '$pythonPath' but could not run." -ForegroundColor Red
    Write-Host 'Repair the python.org installation, then verify with: python --version'
    exit 1
}

Write-Host "[PASS] $versionOutput"
Write-Host "[INFO] Python interpreter: $pythonPath"

& $pythonPath (Join-Path $PSScriptRoot 'verify_installation.py')
exit $LASTEXITCODE