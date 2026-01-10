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
- Multitimeframe: Mean-Reversion (v9.3) - Alta volatilidad
- TrendFollowing: Trend-Following (v11.0) - Bull parabólico
"""

# ==============================================
# CONFIGURACIÓN PRINCIPAL DE RUTAS
# ==============================================

routes = [
    # ========================================================================
    # ESTRATEGIA ACTIVA
    # ========================================================================

    # Universal Robust V3.0 - AGRESIVO (8787% ROI Strategy)
    # Walk-Forward Validation: Testing v3.0 TRAIN period (2020-2023)
    # v3.0: Leverage 5x, Risk 1.5% | Full: +1517% ROI, 59.57% annual, -62.31% DD
    # Timeframe: 1H (CRITICAL - original used 1H, not 15m)
    # Source: https://imbuedeskpicasso.medium.com/the-8787-roi-algo-strategy-unveiled-for-crypto-futures-22a5dd88c4a5
    ('Binance Perpetual Futures', 'BTC-USDT', '1h', 'UniversalRobustV3'),

    # ========================================================================
    # ESTRATEGIAS ANTIGUAS (Archivadas)
    # ========================================================================

    # Universal Robust V3.1 - Conservador (+807% ROI, 44.8% anual, -47.35% DD)
    # ('Binance Perpetual Futures', 'BTC-USDT', '1h', 'UniversalRobustV3_1'),

    # Universal Robust V3.0 - ÉXITO pero DD alto (+1517% ROI, 59.57% anual, -62.31% DD)
    # ('Binance Perpetual Futures', 'BTC-USDT', '1h', 'UniversalRobustV3'),

    # Universal Robust V2.0 - FALLA (-0.76% anual, 19.2 trades/año)
    # ('Binance Perpetual Futures', 'BTC-USDT', '15m', 'UniversalRobustV2'),

    # Universal Robust v1.0 - DESCARTADO (solo 8.48% en 6 años)
    # ('Binance Perpetual Futures', 'BTC-USDT', '15m', 'UniversalRobust'),

    # v9.3-RSI36 - DESCARTADO (overfitted, -66.9% en 2020-2025)
    # ('Binance Perpetual Futures', 'BTC-USDT', '15m', 'Multitimeframe'),
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
    ('Binance Perpetual Futures', 'BTC-USDT', '1D'),   # Regime detection (v6)
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
