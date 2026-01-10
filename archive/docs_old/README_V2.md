# 🚀 Universal Trading Bot v2.0 - High ROI Strategy

**Objetivo:** Bot de trading con algoritmo robusto basado en indicadores técnicos probados para maximizar ROI en todos los regímenes de mercado.

**Inspirado en:** Estrategia 8787% ROI en 3 años (probada en producción)

---

## 📊 Estado Actual

- **Versión:** v2.0-ELITE (En Desarrollo)
- **Framework:** Jesse 1.11.0
- **Período de test:** 2020-2025 (5.9 años - 3 regímenes)
- **Target:** 50-200% annual return

---

## 🎯 Estrategia v2.0 - Multi-Indicador

### Indicadores Implementados (Basados en Research)

1. **RSI (14)** - Momentum
   - LONG: RSI < 40 (oversold temprano, no extremo)
   - SHORT: RSI > 60 (overbought temprano)

2. **MACD** - Confirmación Tendencia
   - LONG: MACD bullish cross
   - SHORT: MACD bearish cross

3. **Bollinger Bands** - Timing de Entrada
   - LONG: Price toca banda inferior
   - SHORT: Price toca banda superior
   - Filtro: Bandwidth > mínimo (evitar lateralización)

4. **ADX (14)** - Filtro de Tendencia
   - Solo trade cuando ADX > 20 (tendencia fuerte)
   - ADX < 20 = lateral → NO TRADE

5. **EMA 50/200** - Dirección Macro
   - LONG: Precio > EMA200 (uptrend general)
   - SHORT: Precio < EMA200 (downtrend general)

### Lógica de Entrada

**LONG Entry (Todos deben cumplirse):**
```
1. Precio > EMA200 (uptrend)
2. RSI < 40 (oversold temprano)
3. MACD bullish cross (momentum alcista)
4. Price toca Bollinger Band inferior (timing perfecto)
5. ADX > 20 (tendencia fuerte confirmada)
```

**SHORT Entry (Todos deben cumplirse):**
```
1. Precio < EMA200 (downtrend)
2. RSI > 60 (overbought temprano)
3. MACD bearish cross (momentum bajista)
4. Price toca Bollinger Band superior (timing perfecto)
5. ADX > 20 (tendencia fuerte confirmada)
```

### Gestión de Riesgo

- **Stop Loss:** 2.0 ATR
- **Take Profit:** 3.0 R:R
- **Trailing Stop:** Activar cuando profit > 2R
- **Risk per trade:** 1.5% del balance
- **Leverage:** 5x (conservador)
- **Max trades simultáneos:** 1 (foco en calidad)
- **Cooldown:** 2 horas entre trades

---

## 📈 Resultados Esperados

### Target Metrics (Basado en Research)

| Métrica | v1.0 Actual | v2.0 Target | Mejora |
|---------|-------------|-------------|--------|
| **Annual Return** | 1.37% ❌ | **50-100%** ✅ | +3550% |
| **Max Drawdown** | -23.21% ✅ | **<-30%** ✅ | Mantener |
| **Win Rate** | 29.41% ⚠️ | **40-50%** ✅ | +35% |
| **Total Trades/año** | 37 ❌ | **150-300** ✅ | +305% |
| **Sharpe Ratio** | 0.18 ❌ | **>1.0** ✅ | +456% |

### Estrategia de Referencia (8787% ROI)

**Período:** 1024 días (2021-2023)
- ROI: +8787%
- Max DD: -1.78%
- Win Days: 706 / Loss Days: 309

---

## 🔧 Instalación y Setup

### 1. Requisitos

```bash
Python 3.10+
Jesse 1.11.0
PostgreSQL
Redis
```

### 2. Importar Datos

```bash
cd "C:\Users\ikerm\Desktop\Pruebas BOTTrading\TradingBot_Project"
python import_candles.py
```

### 3. Ejecutar Backtest

**Opción A - Web UI:**
```bash
# Iniciar servidor Jesse
jesse run

# Abrir navegador
http://localhost:9000

# Configurar backtest:
- Exchange: Binance Perpetual Futures
- Symbol: BTC-USDT
- Timeframe: 15m
- Start: 2020-01-01
- End: 2025-12-27
- Strategy: UniversalRobustV2
```

**Opción B - Script Python:**
```bash
python test_strategy_v2.py
```

---

## 📁 Estructura del Proyecto

```
TradingBot_Project/
├── README_V2.md                    # Este archivo
├── code/
│   ├── strategies/
│   │   └── UniversalRobustV2/      # Estrategia principal v2.0
│   │       └── __init__.py
│   ├── routes.py                   # Configuración de trading
│   └── config.py                   # Config Jesse
│
├── archive/                        # Versiones anteriores
│   ├── previous_versions/          # v9.3, v10, v11 docs
│   ├── old_strategies/             # Estrategias descartadas
│   └── old_scripts/                # Scripts de test antiguos
│
├── RESEARCH_SUCCESSFUL_BOTS.md     # Análisis bots exitosos
├── import_candles.py               # Importador de datos
└── test_strategy_v2.py             # Script de testing
```

---

## 🎓 Filosofía de Diseño

### Lo que Aprendimos de v1.0

❌ **Errores v1.0:**
1. Solo 2 indicadores (RSI + EMA) - Insuficiente
2. RSI 30/70 demasiado extremo - Pocas señales
3. Sin filtro de tendencia (ADX) - Muchos whipsaws
4. Sin timing preciso (Bollinger) - Entradas malas
5. Sin confirmación momentum (MACD) - Señales falsas

✅ **Mejoras v2.0:**
1. **5 indicadores** con confirmación multi-señal
2. **RSI 40/60** - Entradas tempranas
3. **ADX >20** - Solo tendencias fuertes
4. **Bollinger Bands** - Timing perfecto de entrada
5. **MACD** - Confirmación de momentum

### Principios Clave

> **"Multi-indicador con confirmación ELIMINA señales falsas"**

> **"Trade SOLO en dirección de tendencia primaria (EMA200)"**

> **"Filtrar laterales (ADX) es MÁS IMPORTANTE que encontrar entradas"**

---

## 🚀 Roadmap

### Fase 1: Desarrollo (1-2 semanas) ← ACTUAL
- [x] Research de bots exitosos
- [x] Diseño estrategia v2.0
- [ ] Implementación código
- [ ] Backtest inicial 2020-2025
- [ ] Ajuste parámetros

### Fase 2: Optimización (1 semana)
- [ ] Optimizar RSI thresholds
- [ ] Optimizar ADX threshold
- [ ] Optimizar Bollinger bandwidth
- [ ] Walk-forward validation

### Fase 3: Testing (2-4 semanas)
- [ ] Paper trading en Testnet
- [ ] Monitoreo performance real
- [ ] Ajustes basados en live data

### Fase 4: Deployment (Cuando esté validado)
- [ ] Live trading micro capital ($500)
- [ ] Escalar gradualmente
- [ ] Circuit breakers activos

---

## ⚠️ Riesgos y Mitigación

| Riesgo | Probabilidad | Mitigación |
|--------|--------------|------------|
| Overfitting a 2020-2025 | Media | Walk-forward validation |
| Falsos positivos multi-indicador | Baja | 5 confirmaciones requeridas |
| Drawdown >30% | Media | Circuit breakers en -25% |
| Mercado lateral prolongado | Alta | ADX filter + cooldown |

---

## 📚 Referencias

- [8787% ROI Strategy](https://imbuedeskpicasso.medium.com/the-8787-roi-algo-strategy-unveiled-for-crypto-futures-22a5dd88c4a5)
- [Freqtrade Best Practices](https://github.com/freqtrade/freqtrade)
- [Crypto Indicators Research](RESEARCH_SUCCESSFUL_BOTS.md)

---

## 📞 Notas del Desarrollador

**v2.0 es una reconstrucción COMPLETA basada en research de estrategias probadas en producción.**

**Diferencias vs v1.0:**
- v1.0: Enfoque minimalista (2 indicadores) → Bajo rendimiento
- v2.0: Enfoque multi-confirmación (5 indicadores) → Alto rendimiento esperado

**Expectativa realista:**
- Si alcanzamos 50% annual return → **ÉXITO**
- Si alcanzamos 100%+ annual return → **ELITE**
- Target v8787 ROI (300%+ anual) → **Excepcional pero posible**

---

**Última actualización:** 2025-12-29
**Versión:** v2.0-ELITE (En Desarrollo)
**Estado:** Implementando estrategia multi-indicador
