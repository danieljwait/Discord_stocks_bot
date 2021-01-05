@ECHO OFF
CD "%~dp0%"
TITLE Run

REM When there is no virtual environment
IF NOT EXIST venv\ GOTO NoVenv

REM Gets the .py file from arguments
SET file=%1

REM Checks the argument passed
IF NOT DEFINED file GOTO NoArg

REM Checks that .py file is valid
IF "%file%"=="stocks.py" GOTO Run
IF "%file%"=="bot.py" GOTO Run
ECHO Invalid argument: .py was invalid
GOTO CommonExit

:NoVenv
ECHO Missing virtual environment: Run setup.cmd
GOTO CommonExit

:NoArg
ECHO Missing argument: .py file to run
GOTO CommonExit

:Run
REM Runs the .py file in the virtual environment
.\venv\Scripts\activate && .\%file% && deactivate
REM .\venv\Scripts\activate && stocks.py && deactivate
GOTO CommonExit

:CommonExit
PAUSE