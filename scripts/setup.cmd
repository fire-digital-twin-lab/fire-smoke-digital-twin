@echo off
setlocal EnableExtensions
chcp 65001 >nul
cd /d "%~dp0\.."

if not exist ".venv\Scripts\python.exe" (
    where py >nul 2>&1
    if not errorlevel 1 (
        py -3.11 -m venv .venv
    ) else (
        python -m venv .venv
    )
    if errorlevel 1 exit /b 1
)

call ".venv\Scripts\activate.bat"
python -m pip install --upgrade pip
if errorlevel 1 exit /b 1
python -m pip install -e ".[dev]"
if errorlevel 1 exit /b 1

echo Environment ready.
echo Activate later with:
echo   call .venv\Scripts\activate.bat
endlocal
