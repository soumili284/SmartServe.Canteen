@echo off
cd /d "%~dp0"
echo ========================================================
echo    Launching SmartServe Web Server on Localhost (8080)
echo ========================================================

set "PY_CMD="
if exist "C:\Program Files\Python315\python.exe" (
    set "PY_CMD=C:\Program Files\Python315\python.exe"
) else (
    where python >nul 2>nul && set "PY_CMD=python" || set "PY_CMD=py"
)

echo Using Python: %PY_CMD%
echo Starting web server at http://localhost:8080...
echo Opening browser...
start http://localhost:8080

"%PY_CMD%" server.py 8080
if %ERRORLEVEL% neq 0 (
    echo.
    echo [!] Server stopped or encountered an error.
)
pause
