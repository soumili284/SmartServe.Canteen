@echo off
cd /d "%~dp0"
echo ========================================================
echo    Launching SmartServe Web Server on Localhost (5000)
echo ========================================================

set "PY_CMD="
if exist "C:\Program Files\Python315\python.exe" (
    set "PY_CMD=C:\Program Files\Python315\python.exe"
) else (
    where python >nul 2>nul && set "PY_CMD=python" || set "PY_CMD=py"
)

echo Using Python: %PY_CMD%
echo Starting web server at http://localhost:5000...
echo Opening browser...
start http://localhost:5000

"%PY_CMD%" server.py 5000
if %ERRORLEVEL% neq 0 (
    echo.
    echo [!] Server stopped or encountered an error.
)
pause
