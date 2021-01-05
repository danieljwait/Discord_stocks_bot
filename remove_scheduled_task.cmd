@ECHO OFF
CD "%~dp0%"
TITLE Scheduled Task Remover

REM If command fails, task does not exist. So script is exited
SCHTASKS /DELETE /TN Custom\Stocks
GOTO CommonExit

:CommonExit
PAUSE
EXIT /b