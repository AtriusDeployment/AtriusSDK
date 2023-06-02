@echo off

rem Set prompt for this session
set PROMPT=AtriusSDK$g

rem Activate a Python virtualenv if present
call .venv\Scripts\Activate >nul 2>&1 || echo No Virtual Environment detected

rem Check for python version
python --version

rem If Python is missing or the wrong version, try these commands to locate python.exe
rem where python
rem dir c:\python.exe /s
rem Then add that path to the front of your PATH in windows or in this script:
rem set PATH=c:\path\to\python.exe\;%PATH%

rem Install dependencies
pip install -r requirements.txt

rem List the available python scripts
echo.
dir /b *.py

echo.
echo Example: python eclypse_firmware_version.py host_list.csv

rem Launch a persistant windows terminal and turn command echoing back on
cmd /k @echo on 
