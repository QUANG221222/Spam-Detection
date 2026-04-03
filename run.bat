@echo off
REM QUICK START GUIDE - Spam Detection System (Windows)
REM Run this file to set up and start the Spam Detection system

echo ==================================
echo ^|   SPAM DETECTION SYSTEM - SETUP
echo ==================================
echo.

REM Check Python
echo Kiem tra Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo LOIX Python chua duoc cai dat!
    echo Vui long cai dat Python 3.8+ tu https://www.python.org
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set python_version=%%i
echo [OK] Phien ban Python: %python_version%
echo.

REM Install dependencies
echo Cai dat dependencies...
pip install -r requirements.txt -q

if errorlevel 1 (
    echo [LOI] Loi cai dat dependencies
    pause
    exit /b 1
)
echo [OK] Dependencies cai dat thanh cong
echo.

REM Train model
echo Huan luyen mo hinh Naive Bayes...
python train_model.py

if errorlevel 1 (
    echo [LOI] Loi huan luyen mo hinh
    pause
    exit /b 1
)
echo [OK] Mo hinh huan luyen thanh cong
echo.

REM Start API
echo Khoi dong API...
echo API se chay tai: http://localhost:5000
echo Giao dien web: Mo file frontend\index.html trong trinh duyet
echo.
echo Nhan Ctrl+C de tat API
echo.

python app.py

pause
