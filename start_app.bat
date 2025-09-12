@echo off
echo Starting AQI Analyzer UI with Backend Integration...
echo ====================================================

cd /d "C:\Users\Admin\OneDrive\Desktop\LAB_oops\AQI_Analyser\app"

echo Testing backend integration first...
"C:\Users\Admin\OneDrive\Desktop\LAB_oops\AQI_Analyser\.venv\Scripts\python.exe" test_integration.py

echo.
echo Starting UI application...
"C:\Users\Admin\OneDrive\Desktop\LAB_oops\AQI_Analyser\.venv\Scripts\python.exe" main.py

pause
