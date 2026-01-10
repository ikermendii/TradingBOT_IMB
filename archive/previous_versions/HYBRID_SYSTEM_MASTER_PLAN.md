# 🚀 MASTER PLAN: Sistema Híbrido Universal (v11.0-UNIVERSAL)

**Fecha:** 2025-12-28
**Objetivo:** Bot que funcione ÓPTIMAMENTE en CUALQUIER régimen de mercado
**Timeline:** 3-4 semanas
**Versión final:** v11.0-UNIVERSAL

---

## 🎯 Visión del Sistema

### Concepto Central: DUAL-STRATEGY con REGIME DETECTION

```
┌─────────────────────────────────────────────────────────────┐
│                   v11.0-UNIVERSAL SYSTEM                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────┐         ┌──────────────────┐         │
│  │ REGIME DETECTOR  │────────▶│  STRATEGY SWITCH │         │
│  │                  │         │                  │         │
│  │ • ADX 4H         │         │  IF parabolic:   │         │
│  │ • Price Momentum │         │    → Trend Bot   │         │
│  │ • RSI 1D         │         │                  │         │
│  │ • Volatility ATR │         │  ELSE:           │         │
│  └──────────────────┘         │    → Mean Bot    │         │
│                                └──────────────────┘         │
│                                                              │
│  ┌────────────────────────┐   ┌────────────────────────┐  │
│  │  STRATEGY A:           │   │  STRATEGY B:           │  │
│  │  MEAN-REVERSION        │   │  TREND-FOLLOWING       │  │
│  │  (v9.3 actual)         │   │  (nuevo)               │  │
│  ├────────────────────────┤   ├────────────────────────┤  │
│  │ • RSI oversold/bought  │   │ • Breakout entries     │  │
│  │ • Divergencias         │   │ • Trailing stop        │  │
│  │ • Fair Value Gaps      │   │ • Momentum confirm     │  │
│  │ • TP: 3.0R             │   │ • TP: 6-8R             │  │
│  │ • BE: 1.35R            │   │ • BE: 3.0R             │  │
│  │                         │   │                         │  │
│  │ Óptimo: Volatilidad    │   │ Óptimo: Parabólico     │  │
│  │ Result: +110% (2023)   │   │ Result: +60%? (2020)   │  │
│  └────────────────────────┘   └────────────────────────┘  │
│                                                              │
└─────────────────────────────────────────────────────────────┘

PERFORMANCE ESPERADA:
- Bull Parabólico (2020-2021): +50-80% (Trend Bot)
- Alta Volatilidad (2022-2025): +80-110% (Mean Bot)
- Periodo completo (2020-2025): +70-100% ✅
- Calmar Ratio: >1.2 (ELITE universal)
```

---

## 📋 FASE A: Mantener v9.3 Paper Trading (ACTUAL)

### Status Quo - YA EN MARCHA

**Bot activo:**
- Versión: v9.3-RSI36
- Exchange: Binance Futures Testnet
- Paper trading: SÍ
- Performance esperada: +110% anual en mercado actual

**Monitoreo continuo:**
1. Revisar trades diarios
2. Verificar que funciona como esperado
3. Acumular data de paper trading (mínimo 50 trades)
4. Detectar cualquier anomalía

**Sin cambios hasta que v11.0-UNIVERSAL esté listo.**

---

## 📋 FASE B: Desarrollo v11.0-UNIVERSAL (3-4 semanas)

### Roadmap Completo

```
SEMANA 1: Regime Detection + Trend Strategy Design
├─ Día 1-2: Diseñar algoritmo de detección de régimen
├─ Día 3-4: Implementar Trend-Following strategy
└─ Día 5-7: Backtest Trend strategy en 2020-2021

SEMANA 2: Integración + Backtesting
├─ Día 8-10: Integrar ambas strategies en Jesse
├─ Día 11-12: Backtest sistema completo 2020-2025
└─ Día 13-14: Walk-forward validation

SEMANA 3: Optimización + Refinamiento
├─ Día 15-17: Ajustar parámetros basándose en resultados
├─ Día 18-19: Stress testing (eventos extremos)
└─ Día 20-21: Finalizar código Jesse

SEMANA 4: Migración a Freqtrade + Deployment
├─ Día 22-24: Portar código a Freqtrade
├─ Día 25-26: Testing en Testnet
└─ Día 27-28: Deployment en paper trading
```

---

## 🔧 COMPONENTE 1: Regime Detection

### Objetivo
Detectar automáticamente si el mercado está en:
1. **BULL PARABOLIC** → Usar Trend-Following
2. **HIGH VOLATILITY** → Usar Mean-Reversion
3. **RANGING** → No tradear

### Algoritmo de Detección

```python
def detect_market_regime():
    """
    Detecta régimen de mercado usando múltiples indicadores

    Returns:
        'parabolic' | 'volatile' | 'ranging'
    """
    # Calcular indicadores
    adx_4h = ta.adx(candles_4h, period=14)
    rsi_1d = ta.rsi(candles_1d, period=14)
    atr_pct = ta.atr(candles_15m, 14) / close * 100

    # Precio vs EMAs
    ema_50_4h = ta.ema(candles_4h, 50)
    ema_200_4h = ta.ema(candles_4h, 200)
    ema_diff_pct = ((ema_50_4h - ema_200_4h) / ema_200_4h) * 100

    # Momentum 30 días
    price_30d_ago = candles_1d[-30]['close']
    momentum_30d = ((close - price_30d_ago) / price_30d_ago) * 100

    # RÉGIMEN 1: BULL PARABOLIC
    if (
        adx_4h > 30 and              # Tendencia fuerte
        ema_diff_pct > 3.0 and       # EMA50 >> EMA200 (>3%)
        rsi_1d > 60 and              # RSI alto sostenido
        momentum_30d > 15            # +15% en 30 días
    ):
        return 'parabolic'

    # RÉGIMEN 2: HIGH VOLATILITY
    elif (
        atr_pct > 0.008 and          # ATR >0.8% (volátil)
        adx_4h > 15 and              # Algo de tendencia
        abs(momentum_30d) < 15       # Movimiento moderado
    ):
        return 'volatile'

    # RÉGIMEN 3: RANGING
    else:
        return 'ranging'
```

### Parámetros de Detección

| Indicador | Parabolic | Volatile | Ranging |
|-----------|-----------|----------|---------|
| **ADX 4H** | >30 | 15-30 | <15 |
| **EMA Diff %** | >3% | 0-3% | <1% |
| **RSI 1D** | >60 | 40-60 | 30-70 |
| **Momentum 30d** | >+15% | ±15% | <±5% |
| **ATR %** | <0.8% | >0.8% | <0.4% |

### Testing del Detector

**Backtest con datos históricos:**
```
2020 Q1-Q2: Debería detectar 'parabolic' → BTC $7k → $29k
2022 Q1-Q2: Debería detectar 'volatile' → BTC -50% crash
2023 Q4: Debería detectar 'parabolic' → BTC $27k → $44k
2024: Debería detectar 'volatile' → BTC oscillating
```

**Validación:**
- ✅ Si detecta correctamente >80% del tiempo → APROBAR
- ❌ Si falla >20% → ITERAR parámetros

---

## 🔧 COMPONENTE 2: Strategy A - Mean-Reversion (v9.3)

### Ya Implementada y Testeada

**Código:** `code/strategies/Multitimeframe/__init__.py` (versión v9.3-RSI36)

**Parámetros óptimos:**
```python
# v9.3-RSI36 (ELITE en alta volatilidad)
rsi_long_threshold = 36
rsi_short_threshold = 64
break_even_ratio = 1.35
tp_final_ratio = 3.0
minimum_score = 3
```

**Performance validada:**
```
Periodo: 2023-2025 (Alta volatilidad)
Net Profit: +110.68% 🏆
Win Rate: 25.14%
Max DD: -19.93%
Calmar: 1.55 (ELITE)
```

**Condición de activación:**
```python
if market_regime == 'volatile':
    use_strategy = 'mean_reversion'
```

**Sin cambios necesarios - ya está optimizada.**

---

## 🔧 COMPONENTE 3: Strategy B - Trend-Following (NUEVO)

### Diseño Completo

**Filosofía:**
- Entrar en breakouts (NO en dips)
- Dejar correr las ganancias (trailing stop)
- TP largo (6-8R para capturar mega trends)
- Score system similar a v9.3

### Lógica de Entrada LONG

```python
def should_long_trend():
    """
    Trend-Following: Entrar en BREAKOUTS alcistas

    Score mínimo: 4 puntos (más selectivo que mean-reversion)
    """
    score = 0

    # 1. BREAKOUT de resistencia (2 puntos)
    high_20 = max(candles[-20:, 'high'])
    if close > high_20 * 1.01:  # Breakout >1%
        score += 2

    # 2. MACD alcista 1H (2 puntos - señal fuerte)
    macd_1h, signal_1h, _ = ta.macd(candles_1h, 15, 30, 9)
    if macd_1h > signal_1h and macd_1h > 0:
        score += 2

    # 3. Momentum alcista (1 punto)
    # Precio > EMA50 15M
    ema_50 = ta.ema(candles, 50)
    if close > ema_50:
        score += 1

    # 4. Volumen confirmación (1 punto)
    avg_volume_20 = np.mean(candles[-20:, 'volume'])
    if volume > avg_volume_20 * 1.3:
        score += 1

    # 5. ADX trending (1 punto)
    adx = ta.adx(candles, 14)
    if adx > 25:
        score += 1

    # Score mínimo: 4 puntos
    return score >= 4
```

### Lógica de Entrada SHORT

```python
def should_short_trend():
    """
    Trend-Following: Entrar en BREAKDOWNS bajistas
    """
    score = 0

    # 1. BREAKDOWN de soporte (2 puntos)
    low_20 = min(candles[-20:, 'low'])
    if close < low_20 * 0.99:  # Breakdown >1%
        score += 2

    # 2. MACD bajista 1H (2 puntos)
    macd_1h, signal_1h, _ = ta.macd(candles_1h, 15, 30, 9)
    if macd_1h < signal_1h and macd_1h < 0:
        score += 2

    # 3. Momentum bajista (1 punto)
    ema_50 = ta.ema(candles, 50)
    if close < ema_50:
        score += 1

    # 4. Volumen confirmación (1 punto)
    avg_volume_20 = np.mean(candles[-20:, 'volume'])
    if volume > avg_volume_20 * 1.3:
        score += 1

    # 5. ADX trending (1 punto)
    adx = ta.adx(candles, 14)
    if adx > 25:
        score += 1

    return score >= 4
```

### Gestión de Posición Trend-Following

```python
def update_position_trend():
    """
    TREND-FOLLOWING: Dejar correr ganancias, trailing stop
    """
    if not position.is_open:
        return

    initial_risk = vars['initial_risk_distance']
    current_profit = (close - entry_price) if is_long else (entry_price - close)
    r_ratio = current_profit / initial_risk

    # REGLA 1: Break-even a 3.0R (MÁS RELAJADO que mean-reversion)
    if r_ratio >= 3.0 and not vars['tp1_hit']:
        vars['tp1_hit'] = True
        vars['sl_price'] = entry_price

    # REGLA 2: Trailing stop después de 3.0R
    if r_ratio >= 3.0:
        # Trailing stop: 2R desde el high
        if is_long:
            highest_price = max(highest_price, close)
            new_sl = highest_price - (initial_risk * 2.0)
            vars['sl_price'] = max(vars['sl_price'], new_sl)
        else:
            lowest_price = min(lowest_price, close)
            new_sl = lowest_price + (initial_risk * 2.0)
            vars['sl_price'] = min(vars['sl_price'], new_sl)

    # REGLA 3: TP final en 6.0R (para capturar mega trends)
    # Pero trailing puede cerrar antes si hay reversión
    if r_ratio >= 6.0:
        liquidate()
        return
```

### Parámetros Trend-Following

```python
# Strategy B: Trend-Following
breakout_lookback = 20      # Velas para detectar breakout
breakout_threshold = 0.01   # 1% breakout mínimo
minimum_score = 4           # Más selectivo que mean-reversion
break_even_ratio = 3.0      # Más relajado
tp_final_ratio = 6.0        # Más ambicioso
trailing_stop_ratio = 2.0   # Trailing 2R desde high
```

---

## 🧪 Testing Strategy - Fase por Fase

### Test 1: Trend Strategy Solo (2020-2021)

**Objetivo:** Validar que Trend-Following funciona en parabólico

**Backtest:**
```
Exchange: Binance Futures
Period: 2020-01-01 → 2021-12-31
Strategy: Trend-Following ONLY (sin regime detection)
```

**Criterios de éxito:**
- ✅ Net Profit > +30%
- ✅ Win Rate > 18%
- ✅ Max DD < -40%
- ✅ Calmar > 0.8

**Si falla:** Iterar parámetros (score, BE, TP)

---

### Test 2: Mean Strategy Solo (2022-2025)

**Objetivo:** Re-validar que Mean-Reversion sigue funcionando

**Backtest:**
```
Exchange: Binance Futures
Period: 2022-01-01 → 2025-12-27
Strategy: Mean-Reversion ONLY (v9.3)
```

**Criterios de éxito:**
- ✅ Net Profit > +80%
- ✅ Win Rate > 24%
- ✅ Max DD < -25%
- ✅ Calmar > 1.3

**Si falla:** Verificar si algo cambió vs v9.3 original

---

### Test 3: Regime Detector Accuracy (2020-2025)

**Objetivo:** Validar que detector clasifica correctamente

**Backtest:**
```
Exchange: Binance Futures
Period: 2020-01-01 → 2025-12-27
Test: Regime detection vs manual classification
```

**Manual classification esperada:**
```
2020 Q1-Q2: Parabolic (BTC $7k → $12k)
2020 Q3-Q4: Parabolic (BTC $10k → $29k)
2021 Q1-Q2: Parabolic (BTC $29k → $64k)
2021 Q3-Q4: Volatile (BTC crash -50%)
2022 Q1-Q4: Volatile (bear market)
2023 Q1-Q2: Volatile (recovery)
2023 Q3-Q4: Parabolic (BTC $27k → $44k)
2024 Q1-Q4: Volatile (consolidation)
2025 Q1: Parabolic/Volatile (mixed)
```

**Accuracy target:**
- ✅ >80% correct classification → APROBAR
- ⚠️ 70-80% → ITERAR parámetros
- ❌ <70% → RE-DISEÑAR detector

---

### Test 4: HYBRID SYSTEM Complete (2020-2025)

**Objetivo:** Validar sistema completo con switching automático

**Backtest:**
```
Exchange: Binance Futures
Period: 2020-01-01 → 2025-12-27 (5.88 años)
Strategy: v11.0-UNIVERSAL (regime detection + dual strategy)
```

**Criterios de éxito (7/7 para deployment):**

**Periodo completo 2020-2025:**
- ✅ Net Profit > +60%
- ✅ Win Rate > 20%
- ✅ Max DD < -35%
- ✅ Calmar > 1.0

**Periodo 2023-2025 (no degradar mucho vs v9.3):**
- ✅ Net Profit > +80% (toleramos -30% vs v9.3)
- ✅ Max DD < -25%
- ✅ Calmar > 1.2

**Resultado:**
- **7/7:** ✅ DEPLOYMENT APROBADO
- **5-6/7:** ⚠️ Iterar a v11.1
- **<5/7:** ❌ Re-diseñar

---

## 📊 Performance Esperada v11.0-UNIVERSAL

### Proyección Realista

| Periodo | Régimen | Strategy Activa | Net Profit | Win Rate | Max DD | Calmar |
|---------|---------|-----------------|------------|----------|--------|--------|
| **2020** | Parabolic | Trend | +40% | 18% | -25% | 1.6 |
| **2021** | Parabolic | Trend | +35% | 17% | -30% | 1.2 |
| **2022** | Volatile | Mean | -5% | 22% | -28% | -0.2 |
| **2023** | Volatile | Mean | +60% | 26% | -18% | 3.3 |
| **2024** | Volatile | Mean | +35% | 24% | -22% | 1.6 |
| **2025** | Mixed | Both | +15% | 21% | -15% | 1.0 |
| **TOTAL** | - | Hybrid | **+80-100%** | **21%** | **-35%** | **~1.3** |

**Comparación:**

| Versión | Profit 2020-2025 | Profit 2023-2025 | Calmar | Robustez |
|---------|------------------|------------------|--------|----------|
| **v9.3-RSI36** | -66.43% ❌ | +110.68% 🏆 | -0.20 / 1.55 | ❌ Solo volátil |
| **v10.0-ROBUST** | -60.2% ❌ | +70-90%? | -0.18 / 1.0-1.3? | ❌ Falla igual |
| **v11.0-UNIVERSAL** | **+80-100% ✅** | **+80-100% ✅** | **~1.3 ✅** | ✅ Universal |

**Mejora:**
- +146-166% profit vs v9.3 en periodo completo
- Ligeramente menos profit en 2023-2025 (-10-30%) pero GANA robustez
- Calmar consistente >1.0 en TODOS los regímenes

---

## 📁 Estructura de Código

### Jesse Framework (para backtesting)

```
TradingBot_Project/
├── code/
│   └── strategies/
│       ├── Multitimeframe/
│       │   └── __init__.py  (v9.3 - Mean-Reversion)
│       └── MultitimeframeTrend/
│           └── __init__.py  (NEW - Trend-Following)
│       └── UniversalHybrid/
│           └── __init__.py  (NEW - v11.0 Sistema completo)
```

### Freqtrade (para deployment)

```
Freqtrade_Project/
├── user_data/
│   └── strategies/
│       ├── Multitimeframe_v93_Complete.py  (ACTUAL)
│       ├── TrendFollowing_v11.py           (NEW)
│       └── Universal_v11_Hybrid.py         (NEW - Final)
```

---

## ⏱️ Timeline Detallado

### SEMANA 1: Regime Detection + Trend Design

**Día 1 (Hoy - 2025-12-28):**
- [x] Analizar fallo v10.0
- [x] Diseñar master plan v11.0
- [ ] Crear estructura de archivos

**Día 2 (2025-12-29):**
- [ ] Implementar algoritmo regime detection
- [ ] Testear detector en datos históricos
- [ ] Validar accuracy >80%

**Día 3 (2025-12-30):**
- [ ] Diseñar lógica Trend-Following completa
- [ ] Implementar score system para breakouts
- [ ] Crear función update_position_trend()

**Día 4 (2025-12-31):**
- [ ] Implementar código completo Trend strategy
- [ ] Code review y debugging
- [ ] Preparar backtest

**Día 5-7 (2026-01-01 a 01-03):**
- [ ] Backtest Trend strategy 2020-2021
- [ ] Analizar resultados
- [ ] Iterar parámetros si necesario
- [ ] Validar criterios de éxito (Test 1)

---

### SEMANA 2: Integración + Backtesting Completo

**Día 8-10 (2026-01-04 a 01-06):**
- [ ] Integrar regime detector + ambas strategies
- [ ] Crear sistema de switching automático
- [ ] Testing unitario de componentes
- [ ] Code review completo

**Día 11-12 (2026-01-07 a 01-08):**
- [ ] Backtest sistema completo 2020-2025
- [ ] Analizar métricas vs criterios
- [ ] Documentar resultados

**Día 13-14 (2026-01-09 a 01-10):**
- [ ] Walk-forward validation
- [ ] Train: 2020-2022, Test: 2023-2025
- [ ] Verificar no overfitting
- [ ] Validar robustez

---

### SEMANA 3: Optimización + Refinamiento

**Día 15-17 (2026-01-11 a 01-13):**
- [ ] Ajustar parámetros basándose en backtests
- [ ] Re-testear con nuevos parámetros
- [ ] Optimización fina

**Día 18-19 (2026-01-14 a 01-15):**
- [ ] Stress testing eventos extremos
- [ ] Luna crash, FTX, Banking crisis
- [ ] Validar que sobrevive

**Día 20-21 (2026-01-16 a 01-17):**
- [ ] Finalizar código Jesse
- [ ] Documentación completa
- [ ] Preparar migración a Freqtrade

---

### SEMANA 4: Migración a Freqtrade + Deployment

**Día 22-24 (2026-01-18 a 01-20):**
- [ ] Portar código a Freqtrade
- [ ] Adaptar sintaxis Jesse → Freqtrade
- [ ] Testing local

**Día 25-26 (2026-01-21 a 01-22):**
- [ ] Deploy en Binance Testnet
- [ ] Monitorear primeros trades
- [ ] Validar funcionamiento

**Día 27-28 (2026-01-23 a 01-24):**
- [ ] Detener v9.3 paper trading
- [ ] Iniciar v11.0 paper trading
- [ ] Monitoreo intensivo primeros 50 trades
- [ ] ✅ DEPLOYMENT COMPLETO

---

## ✅ Criterios de Decisión en Cada Fase

### Checkpoints de Validación

**Checkpoint 1 (Fin Semana 1):**
- ¿Trend strategy funciona en 2020-2021?
- **SI:** Continuar a Semana 2
- **NO:** Iterar diseño Trend strategy

**Checkpoint 2 (Fin Semana 2):**
- ¿Sistema híbrido pasa criterios 2020-2025?
- **SI:** Continuar a Semana 3
- **NO:** Ajustar parámetros, repetir backtests

**Checkpoint 3 (Fin Semana 3):**
- ¿Walk-forward validation exitosa?
- **SI:** Continuar a Semana 4 (migración)
- **NO:** Re-diseñar approach

**Checkpoint 4 (Fin Semana 4):**
- ¿Primeros trades en paper trading exitosos?
- **SI:** ✅ DEPLOYMENT COMPLETO
- **NO:** Debugging y monitoreo extendido

---

## 📋 Próxima Acción Inmediata

### Hoy (2025-12-28) - Resto del día

1. **Crear archivos base:**
   - [ ] `regime_detector.py` (módulo independiente)
   - [ ] `TrendFollowing_v11.py` (estrategia nueva)
   - [ ] `SEMANA1_PROGRESS.md` (tracking)

2. **Empezar diseño Regime Detector:**
   - [ ] Implementar función `detect_market_regime()`
   - [ ] Preparar datos para testing

3. **Mantener v9.3 corriendo:**
   - [ ] Verificar que sigue en paper trading
   - [ ] Revisar últimos trades

**Tiempo estimado:** 2-3 horas

---

## 🎯 Objetivo Final

```
v11.0-UNIVERSAL DEPLOYED
├─ Paper trading activo en Binance Testnet
├─ Regime detection automático funcionando
├─ Mean-Reversion activa en mercado actual
├─ Trend-Following lista para cuando mercado cambie
├─ Performance proyectada: +80-100% anual universal
└─ Calmar ratio >1.2 en CUALQUIER régimen
```

**Estado actual:** 📍 Semana 1, Día 1 - Master Plan completado

**Próximo hito:** Implementar Regime Detector (Día 2)

---

**Creado:** 2025-12-28
**Timeline:** 3-4 semanas
**Objetivo:** Bot universal que funciona ÓPTIMAMENTE en cualquier condición
**Probabilidad de éxito:** 80-90% (con iteración)
