@echo off
pwsh -NoProfile -File "%~dp0scripts\Start-Lab.ps1" %*
exit /b %errorlevel%
