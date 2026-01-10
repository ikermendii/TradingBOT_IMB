@echo off
echo ============================================================
echo JESSE PAPER TRADING - v9.3-RSI36
echo ============================================================
echo.
echo IMPORTANTE: Antes de ejecutar, asegurate de:
echo 1. Tener configurado .env con API keys de Binance Testnet
echo 2. Haber importado datos recientes (import_recent_data.py)
echo 3. Haber leido PAPER_TRADING_SETUP.md
echo.
echo ============================================================
echo.

cd /d "C:\Users\ikerm\Desktop\Pruebas BOTTrading\TradingBot_Project"

echo Iniciando Jesse dashboard...
echo.
echo Una vez que Jesse inicie:
echo 1. Abre tu navegador en: http://localhost:9000
echo 2. Ve a la tab "Live"
echo 3. Configura Paper Trading = ON
echo 4. Ingresa tus API keys de Testnet
echo 5. Click "Start"
echo.
echo Presiona Ctrl+C para detener Jesse
echo ============================================================
echo.

jesse run

pause
