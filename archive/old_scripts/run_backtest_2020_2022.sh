#!/bin/bash
# Backtest TrendFollowing Strategy 2020-2022
# Ejecutar desde WSL

cd "/mnt/c/Users/ikerm/Desktop/Pruebas BOTTrading/TradingBot_Project"

echo "========================================================================"
echo "BACKTEST: TrendFollowing Strategy (v11.0-UNIVERSAL)"
echo "========================================================================"
echo "Periodo: 2020-01-01 → 2022-12-31 (3 años)"
echo "Exchange: Binance Perpetual Futures"
echo "Symbol: BTC-USDT"
echo "Timeframe: 15m"
echo "Strategy: TrendFollowing"
echo "========================================================================"
echo ""

# Asegurarse que Redis está corriendo
echo "🔄 Verificando Redis..."
sudo service redis-server start > /dev/null 2>&1
redis-cli ping > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Redis OK"
else
    echo "❌ Redis no disponible"
    exit 1
fi

echo ""
echo "⏳ Ejecutando backtest..."
echo "   (Esto puede tomar varios minutos)"
echo ""

# Ejecutar backtest
jesse run 2020-01-01 2022-12-31

echo ""
echo "✅ Backtest completado"
echo ""
