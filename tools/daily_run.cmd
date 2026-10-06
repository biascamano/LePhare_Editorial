@echo off
setlocal
cd /d "%~dp0.."
python tools\daily_run.py
