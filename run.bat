@echo off

cd /d "%-dp0"
python -m pip install -q -r requirements.txt
python test1.py
pause