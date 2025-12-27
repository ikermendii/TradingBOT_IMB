# 🤖 Jesse Trading Bot - Multi-Timeframe Strategy

Bot de trading automatizado para Bitcoin usando el framework Jesse con estrategia multi-timeframe optimizada mediante sensitivity analysis.

---

## 📊 Estado Actual

- **Versión:** v9.3-RSI36 🏆🏆🏆
- **Framework:** Jesse 1.11.0
- **Python:** 3.x
- **Exchange:** Binance Perpetual Futures
- **Símbolo:** BTC-USDT
- **Timeframe principal:** 15m
- **Timeframes adicionales:** 1h
- **Última actualización:** 2025-12-27
- **Estado:** ✅ VALIDADO - **CALIDAD ELITE** (Calmar 1.55)

---

## 🏆 Resultados v9.3-RSI36

**Periodo:** 2023-2025 (2.78 años) | **Capital inicial:** $10,000

```
Net Profit:      +$11,067 (+110.68%) 🏆🏆🏆
Annual Return:   30.8% 🏆
Max Drawdown:    -19.93% ✅ (EXCELENTE)
Sharpe Ratio:    1.09 ✅ (INSTITUCIONAL PREMIUM)
Calmar Ratio:    1.55 🏆 (ELITE - threshold >1.5)

Win Rate:        25.14%
Total Trades:    354
R:R Ratio:       3.63
Expectancy:      $31.26 por trade
Losing Streak:   14 trades
```

**Double Breakthrough:**
1. Break-even 1.25R → 1.35R (v9.2) = +39.7% mejora
2. RSI 38 → 36 (v9.3) = +15.9% mejora adicional

**Mejora total vs v9.1:** +62% profit, +49% annual return

---

## 🎯 Estrategia v9.3-RSI36

### Sistema de Puntuación Weighted (Score-based)

**Entrada LONG:** Requiere mínimo 3 puntos de 7 posibles

**Señales PREMIUM** (2 puntos cada una):
1. [1H] Divergencia alcista RSI = +2 puntos
2. [15M] Fair Value Gap alcista = +2 puntos

**Señales BASE** (1 punto cada una):
3. [1H] MACD alcista = +1 punto
4. [15M] RSI < 36 (oversold - OPTIMIZADO v9.3) = +1 punto
5. [15M] MACD alcista = +1 punto

**Entrada SHORT:** Requiere mínimo 2 puntos de 5 posibles
1. [1H] MACD bajista = +1 punto
2. [1H] Divergencia bajista RSI = +1 punto
3. [15M] RSI > 64 (overbought - OPTIMIZADO v9.3) = +1 punto
4. [15M] MACD bajista = +1 punto
5. [15M] Fair Value Gap bajista = +1 punto (BONUS)

### Gestión de Riesgo
- **Leverage:** 20x
- **Risk por trade:** 1.5% del balance
- **Stop Loss:** ATR(14) × 1.8
- **Take Profits:**
  - TP1: 1.2R (cierra 50%)
  - TP2: 2.5R (cierra 30%)
  - TP3: 4R (cierra 20% + trailing stop)
- **Cooldown:** 30 minutos entre señales
- **Daily loss limit:** 3% pérdida máxima diaria

---

## 📚 Documentación

### Documentos principales:
- **[📍 Estado Actual](docs/CURRENT_VERSION.md)** - Versión actual, parámetros, último backtest
- **[📖 Changelog](docs/CHANGELOG.md)** - Evolución completa v1.0 → v8.2
- **[📈 Resultados de Backtests](docs/BACKTEST_RESULTS.md)** - Todos los backtests ejecutados
- **[🔧 Workflow de Desarrollo](docs/WORKFLOW.md)** - Proceso obligatorio para modificar código
- **[⚙️ Guía de Instalación](docs/INSTALLATION.md)** - Setup completo del proyecto

### Documentos de referencia:
- **[📦 Archivo Histórico](docs/archive/)** - Reportes antiguos, bugs corregidos
- **[📚 Documentación Técnica](docs/reference/)** - Protocolos, troubleshooting

---

## 🚀 Quick Start

### 1. Instalación
Ver guía completa en [docs/INSTALLATION.md](docs/INSTALLATION.md)

```bash
# Instalar Jesse
pip install jesse

# Clonar proyecto
cd "c:\Users\ikerm\Desktop\Pruebas BOTTrading\TradingBot_Project"

# Importar datos históricos
jesse import-candles 'Binance Perpetual Futures' 'BTC-USDT' '2023-01-01'
```

### 2. Ejecutar Backtest
```bash
# Desde la interfaz web
http://localhost:9000

# O desde terminal
jesse backtest '2023-01-01' '2025-12-31'
```

### 3. Modificar Código
**IMPORTANTE:** Seguir siempre el [Workflow Obligatorio](docs/WORKFLOW.md) para evitar procesos zombie y caché corrupto.

---

## 📊 Evolución del Bot

### Versiones principales:
- **v1.0-v4.0:** Estrategia básica con filtros → Resultados pobres (0-6 trades)
- **v5.0-v5.5:** Divergencias RSI → Bug corregido, mejoras incrementales
- **v6.0-v6.9:** 972 trades, 24% WR, -30% return
- **v7.0-v7.6:** Overtrading masivo (-85% return, -85% DD)
- **v8.0-v8.1:** Filtros muy estrictos → 0 trades
- **v8.2-SMART:** Sistema de score inteligente → ⏳ PENDIENTE BACKTEST

Ver evolución completa en [docs/CHANGELOG.md](docs/CHANGELOG.md)

---

## 📈 Último Backtest

**Versión testeada:** v8.1-ADAPTIVE
**Resultado:** 0 trades (filtro EMA200 4H bloqueó todo)
**Próximo test:** v8.2-SMART (pendiente)

Ver todos los resultados en [docs/BACKTEST_RESULTS.md](docs/BACKTEST_RESULTS.md)

---

## 🗂️ Estructura del Proyecto

```
TradingBot_Project/
├── README.md                          # Este archivo
├── config.py                          # Configuración Jesse
├── routes.py                          # Rutas de trading
│
├── code/
│   └── strategies/
│       └── Multitimeframe/
│           └── __init__.py            # Estrategia principal v8.2-SMART
│
├── docs/
│   ├── CURRENT_VERSION.md             # Estado actual (auto-generado)
│   ├── CHANGELOG.md                   # Todas las versiones
│   ├── BACKTEST_RESULTS.md            # Resultados de backtests
│   ├── WORKFLOW.md                    # Workflow de desarrollo
│   ├── INSTALLATION.md                # Guía de instalación
│   │
│   ├── archive/                       # Historial
│   │   ├── BUG_REPORT_DIVERGENCIAS.md
│   │   ├── VERSIONES_v5_POST_BUGFIX.md
│   │   └── ...
│   │
│   └── reference/                     # Docs técnicos
│       ├── VERIFICATION_PROTOCOL.md
│       └── troubleshooting.md
│
└── storage/                           # Datos y logs de Jesse
    └── logs/
```

---

## 🔍 Problemas Conocidos

### ✅ Resueltos:
- Bug en detección de divergencias RSI (corregido en v5.5+)
- Procesos zombie de Jesse (workflow automático implementado)
- Trades eternos por falta de TP3 (corregido en v3.1+)

### ⏳ En investigación:
- Win rate consistentemente bajo (14-24%) a pesar de buen Win/Loss ratio (3.5-3.9)
- Filtros multi-timeframe demasiado restrictivos (0 trades en v8.0-v8.1)

---

## 🛠️ Comandos Útiles

```bash
# Verificar sintaxis
python3 -m py_compile code/strategies/Multitimeframe/__init__.py

# Limpiar caché (importante antes de modificar código)
wsl --shutdown
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
redis-cli FLUSHALL

# Ver procesos Jesse corriendo
ps aux | grep jesse

# Levantar servidor Jesse
jesse run
```

---

## 📞 Notas del Desarrollador

Este bot es un proyecto en desarrollo activo. La estrategia ha evolucionado desde filtros básicos (v1.0) hasta un sistema de puntuación multi-timeframe inteligente (v8.2).

**Filosofía actual:** Balance entre calidad y frecuencia de trades, evitando extremos de:
- Muy restrictivo → 0 trades (v8.0-v8.1)
- Muy permisivo → Overtrading y pérdidas (v7.6: -85%)

**Objetivo v8.2:** 200-400 trades en 3 años con >25% win rate y <20% drawdown.

---

## 📝 Licencia

Proyecto personal de trading automatizado.

---

**Última actualización:** 2025-12-26
**Versión actual:** v8.2-SMART
**Estado:** ⏳ Pendiente de backtest
