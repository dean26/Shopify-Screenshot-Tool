@echo off
echo Starting Shopify Screenshot Tool...

:: Create venv if not exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

:: Activate venv
call venv\Scripts\activate.bat

:: Install dependencies
echo Installing requirements...
pip install -r requirements.txt

:: Install Playwright browsers if not installed
echo Installing Playwright browsers...
playwright install

:: Run the Python script
echo Running the application...
python main.py

pause