@ECHO OFF
CD "%~dp0%"
TITLE Setup

REM When text file of packages to install doesnt exist
IF NOT EXIST requirements.txt GOTO NoRequirements

REM Checks that python is installed
python --version > tmpFile.txt
IF ERRORLEVEL 1 GOTO NoPython

REM Temp file allows version to be in a variable
SET /p full_version=<tmpFile.txt
DEL tmpFile.txt
REM The last part of the version is not needed
SET version=%full_version:~0,10%

IF NOT "%version%"=="Python 3.8" (
	ECHO You are currently running %version%
	ECHO Version other than 3.8 have not been tested and may be cause instability

	:Continue
	SET /p choice="Do you want to continue [y/n]: "
	IF /I "%choice%"=="y" GOTO Setup
	IF /I "%choice%"=="n" GOTO CommonExit
	GOTO Continue
)

REM When all checks are satisfied
GOTO Setup

:NoPython
ECHO Python is not installed, please install Python 3.8
GOTO CommonExit

:NoRequirements
ECHO Missing file: requirements.txt
GOTO CommonExit

:Setup
REM Creates .env file with your discord bot token in it
SET /p token="Enter your discord bot token: "
ECHO DISCORD_TOKEN=%token% > .env

REM Generates file structure
IF NOT EXIST Data/ MKDIR Data
IF NOT EXIST Graphs/ MKDIR Graphs

ECHO Creating virtual environment...
python -m venv venv\

ECHO Creating scheduled task to run stocks.py daily at 4pm...
SCHTASKS /Create /SC DAILY /ST 16:00 /F /TN Custom\Stocks /TR "%~dp0%\run_python.cmd stocks.py"

REM Installs all the required modules to a virtual environment
.\venv\Scripts\activate && pip install -r requirements.txt && deactivate && ECHO Setup complete && GOTO CommonExit

:CommonExit
PAUSE