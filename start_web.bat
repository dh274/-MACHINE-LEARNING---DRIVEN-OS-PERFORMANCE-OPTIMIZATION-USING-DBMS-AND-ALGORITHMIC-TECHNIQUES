@echo off
echo 🌐 Starting ML Performance Monitor Web Interface
echo ================================================

echo Installing dependencies...
pip install flask flask-cors streamlit plotly requests

echo.
echo Starting web services...
python run_web.py

pause