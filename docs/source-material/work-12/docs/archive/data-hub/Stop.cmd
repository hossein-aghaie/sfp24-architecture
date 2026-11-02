@echo off
pwsh -NoProfile -File "%~dp0scripts\Stop-Lab.ps1" %*
exit /b %errorlevel%
