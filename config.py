"""
🚀 TRADING BOT CONFIG - Advanced Setup
=====================================

Configuración optimizada para:
- SimpleRSI (estrategia básica de aprendizaje)
- Multitimeframe (estrategia avanzada con divergencias)
- Balance inicial: $10,000
- Risk management profesional
- Backtesting con métricas detalladas
"""

# Configuración principal de Jesse
config = {
    # ============================================
    # TRADING ENVIRONMENT
    # ============================================
    'env': {
        'exchanges': {
            # Binance Spot - Para backtesting SPOT
            'Binance Spot': {
                'fee': 0.001,  # 0.1% fee (con descuento BNB)
            },
            # Binance Perpetual Futures - Para backtesting FUTURES
            'Binance Perpetual Futures': {
                'fee': 0.0004,  # 0.04% fee típico en perp futures
            },
        },
    },

    # ============================================
    # DATABASE CONFIGURATION (PostgreSQL)
    # ============================================
    'databases': {
        'postgres_host': '127.0.0.1',
        'postgres_name': 'jesse_db',
        'postgres_port': 5432,
        'postgres_username': 'jesse_user',
        'postgres_password': 'password',
    },

    # ============================================
    # LOGGING OPTIONS
    # ============================================
    'logging': {
        'order_submission': True,
        'order_cancellation': True,
        'order_execution': True,
        'position_opened': True,
        'position_increased': False,  # No usamos posiciones incrementales
        'position_reduced': False,    # No usamos posiciones reducidas
        'position_closed': True,
        'balance_update': True,
        'shorter_period_candles': False,
        'trading_candles': False,
    },

    # ============================================
    # NOTIFICATIONS
    # ============================================
    'notifications': {
        'enabled': False,  # Deshabilitado para backtesting
        'events': {
            'errors': True,
            'started_session': False,
            'terminated_session': False,
            'submitted_orders': False,
            'cancelled_orders': False,
            'executed_orders': False,
            'opened_position': False,
            'closed_position': False,
            'increased_position': False,
            'reduced_position': False,
        }
    },

    # ============================================
    # ADVANCED SETTINGS
    # ============================================

    # Warm-up candles - Crítico para indicadores complejos
    # 300 candles es suficiente para:
    # - EMA 200
    # - RSI con lookback
    # - MACD
    # - Detección de divergencias
    'warm_up_candles': 300,
}

# ============================================
# CONFIGURACIÓN ADICIONAL PARA DESARROLLO
# ============================================
# Estas configuraciones no son parte del config oficial de Jesse
# pero son útiles para documentar tu setup

BACKTEST_CONFIG = {
    'initial_balance': 10000,  # $10,000 capital inicial
    'risk_per_trade': 1.5,     # 1.5% del capital por trade
    'max_open_positions': 1,   # Solo 1 posición simultánea
    'max_daily_risk': 4.5,     # Máximo 4.5% riesgo diario (3 trades)
}

OPTIMIZATION_CONFIG = {
    'cpu_cores': 4,            # Usar 4 cores para optimización
    'population_size': 100,    # Tamaño población algoritmo genético
    'iterations': 200,         # Iteraciones para optimización
}

STRATEGIES_INFO = {
    'SimpleRSI': {
        'description': 'Estrategia básica RSI con EMA 200',
        'timeframes': ['15m'],
        'indicators': ['RSI(14)', 'EMA(200)'],
        'risk_reward': '1:2',
        'status': 'tested',  # tested, in_development, production
    },
    'Multitimeframe': {
        'description': 'Estrategia avanzada con divergencias RSI',
        'timeframes': ['15m', '1h', '4h'],
        'indicators': ['RSI', 'EMA', 'Volume', 'Divergences'],
        'risk_reward': '1:3',
        'status': 'in_development',
    }
}

# ============================================
# NOTAS DE DESARROLLO
# ============================================
"""
📝 Configuración de Exchanges:
- Jesse 1.11.0 usa 'Binance Spot' no 'Binance'
- El fee de 0.001 = 0.1% (fee con descuento BNB)
 - Para futuros usar 'Binance Perpetual Futures'

📝 Warm-up Candles:
- 300 candles en 15m = 75 horas = 3.1 días
- Suficiente para EMA 200 y detección de divergencias
- Si usas indicadores más largos, aumentar este valor

📝 Backtesting:
- Los resultados se guardan en storage/json-reports/
- Los gráficos en storage/charts/
- Los logs en storage/logs/

📝 Para Live Trading (futuro):
- Cambiar notifications.enabled a True
- Configurar Telegram/Discord webhooks
- Habilitar paper trading primero
- Nunca hacer live sin backtesting exhaustivo
"""
