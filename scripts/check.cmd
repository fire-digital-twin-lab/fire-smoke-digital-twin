@echo off
setlocal
chcp 65001 >nul
python -m compileall -q src dashboard\backend
if errorlevel 1 exit /b 1
where ruff >nul 2>&1
if not errorlevel 1 ruff check src tests dashboard\backend
endlocal
