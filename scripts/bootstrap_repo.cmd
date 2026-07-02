@echo off
setlocal EnableExtensions
chcp 65001 >nul
set "ROOT=%~1"
if "%ROOT%"=="" set "ROOT=%CD%"
set "EXTRA="
if /I "%~2"=="--force" set "EXTRA=--force"
if /I "%~2"=="--dry-run" set "EXTRA=--dry-run"

where py >nul 2>&1
if not errorlevel 1 (
  py -3 "%~dp0bootstrap_repo.py" --root "%ROOT%" %EXTRA%
  exit /b %errorlevel%
)
where python >nul 2>&1
if errorlevel 1 (
  echo Python 3 is required.
  exit /b 1
)
python "%~dp0bootstrap_repo.py" --root "%ROOT%" %EXTRA%
endlocal
