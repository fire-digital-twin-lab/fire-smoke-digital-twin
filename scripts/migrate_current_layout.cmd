@echo off
setlocal EnableExtensions
chcp 65001 >nul

if not exist ".git" (
  echo ERROR: Run this script from the current repository root.
  exit /b 1
)

set "BRANCH=chore/restructure-repo"
git rev-parse --verify "%BRANCH%" >nul 2>&1
if errorlevel 1 (
  git checkout -b "%BRANCH%"
  if errorlevel 1 exit /b 1
) else (
  echo Branch %BRANCH% already exists. Checking it out.
  git checkout "%BRANCH%"
  if errorlevel 1 exit /b 1
)

if not exist "src\fire_smoke_dt" mkdir "src\fire_smoke_dt"

call :move_dir "src\bim_graph" "src\fire_smoke_dt\bim_graph"
call :move_dir "src\scenario" "src\fire_smoke_dt\scenario"
call :move_dir "src\cfast_sim" "src\fire_smoke_dt\cfast_sim"
call :move_dir "src\fds_sim" "src\fire_smoke_dt\fds_sim"
call :move_dir "src\comparison" "src\fire_smoke_dt\comparison"
call :move_dir "src\iot_sim" "src\fire_smoke_dt\iot_sim"
call :move_dir "src\dataset" "src\fire_smoke_dt\dataset"
call :move_dir "src\models" "src\fire_smoke_dt\models"
call :move_dir "src\training" "src\fire_smoke_dt\training"
call :move_dir "src\common" "src\fire_smoke_dt\shared"

if exist "configs\iot_presets.yaml" if not exist "configs\noise_presets.yaml" (
  git mv "configs\iot_presets.yaml" "configs\noise_presets.yaml"
)

call "%~dp0bootstrap_repo.cmd" "%CD%"
if errorlevel 1 exit /b 1

if exist "Makefile" for %%F in ("Makefile") do if %%~zF==0 (
  echo Empty Makefile kept for manual review. Remove it if the team uses Windows CMD only.
)

echo.
echo Migration scaffold finished. Review before committing:
git status --short
echo.
echo Recommended next commands:
echo   scripts\check.cmd
echo   scripts\test.cmd
echo   git add -A
echo   git commit -m "chore: establish project contracts and module scaffold"
exit /b 0

:move_dir
set "SRC=%~1"
set "DST=%~2"
if not exist "%SRC%" exit /b 0
if exist "%DST%" (
  echo SKIP: target already exists: %DST%
  exit /b 0
)
git mv "%SRC%" "%DST%"
if errorlevel 1 exit /b 1
exit /b 0
