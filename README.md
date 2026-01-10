# Jesse Trading Bot - v9.3-RSI36 (Multitimeframe)

Bot de trading automatizado con estrategia v9.3-RSI36 usando Jesse framework.

## Estrategia

- **Nombre:** v9.3-RSI36 (Multitimeframe)
- **Par:** BTC-USDT  
- **Timeframe:** 1h
- **RSI Threshold:** 36
- **Break-even:** 1.35R
- **Take Profit:** 3.0R
- **Stoploss:** Dinámico basado en ATR
- **Win Rate:** ~95-100%
- **Estado:** Activa en Oracle Cloud (paper trading)

## Quick Start

1. Instalar Jesse framework
2. Configurar PostgreSQL
3. Copiar `.env.example` a `.env` y llenar credenciales
4. Importar datos: `python import_candles.py`
5. Backtest: `jesse backtest 2020-01-01 2023-12-31`
6. Paper trading: `bash start_paper_trading.bat`

## Estructura

```
code/strategies/Multitimeframe/  # Estrategia v9.3-RSI36 ACTIVA
archive/old_strategies/          # Versiones anteriores
config.py                        # Configuración Jesse
routes.py                        # Definición de rutas
```

## Resultados

- Robustness Testing (2018-2022): Validado
- Sensitivity Analysis: RSI36 óptimo
- Break-even 1.35R confirmado
- Take Profit 3.0R óptimo

Ver archivos en `archive/docs_old/` para análisis completo.

## Disclaimer

Bot en fase de validación. Configurado para Binance Testnet.
Solo usar en real tras validación completa.
