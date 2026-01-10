#!/bin/bash
# Training period test: 2018-2022

cd /mnt/c/Users/ikerm/Desktop/Pruebas\ BOTTrading/TradingBot_Project

echo "======================================================================"
echo "WALK-FORWARD TRAINING: 2018-01-01 to 2022-12-31"
echo "Strategy: UniversalRobust v1.0"
echo "======================================================================"

/root/.local/bin/jesse import-candles "Binance Perpetual Futures" BTC-USDT 2018-01-01

echo ""
echo "Running backtest..."
/root/.local/bin/jesse -m backtest 2018-01-01 2022-12-31
