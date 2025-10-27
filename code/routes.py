"""
🚀 TRADING BOT ROUTES
=====================

Define qué estrategias ejecutar en qué pares/timeframes

Formato para Jesse 1.11.0:
    routes = [
        ('Exchange', 'Symbol', 'Timeframe', 'StrategyName'),
    ]

Estrategias disponibles:
- SimpleRSI: Estrategia básica con RSI y EMA 200
- Multitimeframe: Estrategia avanzada con divergencias
"""

# ==============================================
# CONFIGURACIÓN PRINCIPAL DE RUTAS
# ==============================================

routes = [
    # Simple RSI Strategy
    # ('Binance Perpetual Futures', 'BTC-USDT', '15m', 'SimpleRSI'),

    # Multitimeframe Strategy (avanzada con divergencias)
    ('Binance Perpetual Futures', 'BTC-USDT', '15m', 'Multitimeframe'),
]

# ==============================================
# TIMEFRAMES ADICIONALES (opcional)
# ==============================================
# Si tu estrategia usa multi-timeframe analysis,
# define aquí los timeframes adicionales que necesita

extra_candles = [
    # Timeframes adicionales para análisis multi-timeframe
    ('Binance Perpetual Futures', 'BTC-USDT', '1h'),   # Timeframe intermedio
    ('Binance Perpetual Futures', 'BTC-USDT', '4h'),   # Tendencia principal
]

# ==============================================
# NOTAS
# ==============================================
"""
📝 Para cambiar de estrategia:
   Comenta/descomenta las líneas en routes[]

📝 Exchange names en Jesse 1.11.0:
    - 'Binance Spot' (spot)
    - 'Binance Perpetual Futures' (futuros/perpetuos)

📝 Timeframes soportados:
   1m, 3m, 5m, 15m, 30m, 45m, 1h, 2h, 3h, 4h, 6h, 8h, 12h, 1D, 3D, 1W

📝 Para backtesting:
   Solo necesitas definir el timeframe principal
   Los extra_candles son opcionales
"""
