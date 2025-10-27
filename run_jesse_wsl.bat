@echo off
REM Helper script to run Jesse commands in WSL
REM Usage: run_jesse_wsl.bat [jesse command]
REM Example: run_jesse_wsl.bat run

cd /d "%~dp0"
wsl bash -c "export PATH=\"$HOME/.local/bin:$PATH\" && cd /mnt/c/Users/ikerm/Desktop/Pruebas\ BOTTrading/TradingBot_Project && jesse %*"
