@echo off
setlocal
chcp 65001 >nul
pytest -m "not external and not slow"
endlocal
