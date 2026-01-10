# 🚀 TREND-FOLLOWING STRATEGY - Diseño Técnico Completo

**Versión:** v11.0-TrendFollowing
**Fecha:** 2025-12-28
**Objetivo:** Capturar mega trends en mercados parabólicos (2020-2021 style)

---

## 🎯 Filosofía de la Estrategia

### Concepto Central: RIDE THE TREND

```
MEAN-REVERSION (v9.3)          vs          TREND-FOLLOWING (v11.0)
═══════════════════════════════════════════════════════════════════

Entrada: Dips (oversold)                    Entrada: Breakouts
         ↓                                           ↓
         RSI < 36                                    Precio > High(20)

Objetivo: Reversión                         Objetivo: Continuación
          ↓                                          ↓
          Precio rebota                              Precio continúa

TP: 3R (movimiento corto)                   TP: 6R (mega trend)

BE: 1.35R (proteger rápido)                 BE: 3.0R (dar espacio)

Trailing: NO                                Trailing: SÍ (2R desde high)

Óptimo: Alta volatilidad                    Óptimo: Bull parabólico
        Reversiones frecuentes                      Trends largos
```

---

## 📊 Performance Esperada

### Target (2020-2021 - Bull Parabólico)

```
BTC: $7,000 → $64,000 (+814% en 18 meses)

Estrategia Mean-Reversion:
- Entra en dips, expulsado en BE
- Win rate: 17-20%
- Net Profit: -50% a -70% ❌

Estrategia Trend-Following:
- Entra en breakouts, sigue trend
- Win rate: 18-25%
- Net Profit: +40-60% ✅ (TARGET)
```

---

## 🔧 Componentes de la Estrategia

### 1. SCORE SYSTEM (Más Selectivo que v9.3)

**Minimum Score: 4 puntos** (vs 3 en Mean-Reversion)

```python
Score Components:
├─ Breakout de Resistencia (2 puntos) - SEÑAL PREMIUM
│  └─ Precio > High(20) × 1.01 (breakout >1%)
│
├─ MACD Alcista 1H (2 puntos) - SEÑAL PREMIUM
│  └─ MACD > Signal AND MACD > 0
│
├─ Momentum Alcista 15M (1 punto)
│  └─ Precio > EMA50
│
├─ Volumen Confirmación (1 punto)
│  └─ Volume > Avg(20) × 1.3
│
└─ ADX Trending (1 punto)
   └─ ADX > 25

Total posible: 7 puntos
Mínimo requerido: 4 puntos (57% threshold)
```

**Ejemplo de entrada válida:**
```
Breakout (2) + MACD 1H (2) = 4 puntos ✅ ENTRA
Breakout (2) + Momentum (1) + Volumen (1) = 4 puntos ✅ ENTRA
Breakout (2) + MACD 1H (2) + ADX (1) = 5 puntos ✅ ENTRA (ALTA CALIDAD)
```

---

### 2. ENTRADA LONG (Breakout Alcista)

**Condiciones:**

```python
def should_long_trend():
    score = 0

    # 1. BREAKOUT de resistencia (2 puntos)
    high_20 = max(candles[-20:]['high'])
    if close > high_20 * 1.01:  # >1% breakout
        score += 2

    # 2. MACD alcista 1H (2 puntos)
    macd_1h, signal_1h = get_macd_1h()
    if macd_1h > signal_1h and macd_1h > 0:
        score += 2

    # 3. Momentum (precio > EMA50) (1 punto)
    if close > ema_50:
        score += 1

    # 4. Volumen alto (1 punto)
    if volume > avg_volume_20 * 1.3:
        score += 1

    # 5. ADX trending (1 punto)
    if adx > 25:
        score += 1

    # Score mínimo: 4 puntos
    if score >= 4:
        return True

    return False
```

**Filtros adicionales:**
- Cooldown: 60 minutos entre trades
- Daily loss limit: 3%
- Volatilidad mínima: ATR >0.4%

---

### 3. ENTRADA SHORT (Breakdown Bajista)

**Condiciones:**

```python
def should_short_trend():
    score = 0

    # 1. BREAKDOWN de soporte (2 puntos)
    low_20 = min(candles[-20:]['low'])
    if close < low_20 * 0.99:  # >1% breakdown
        score += 2

    # 2. MACD bajista 1H (2 puntos)
    macd_1h, signal_1h = get_macd_1h()
    if macd_1h < signal_1h and macd_1h < 0:
        score += 2

    # 3. Momentum bajista (1 punto)
    if close < ema_50:
        score += 1

    # 4. Volumen alto (1 punto)
    if volume > avg_volume_20 * 1.3:
        score += 1

    # 5. ADX trending (1 punto)
    if adx > 25:
        score += 1

    # Score mínimo: 4 puntos
    if score >= 4:
        return True

    return False
```

---

### 4. GESTIÓN DE POSICIÓN (Trailing Stop)

**Reglas:**

```python
def update_position_trend():
    """
    Trend-Following: Dejar correr ganancias
    """
    if not position.is_open:
        return

    initial_risk = vars['initial_risk_distance']
    current_profit = close - entry_price  # LONG
    r_ratio = current_profit / initial_risk

    # REGLA 1: Break-even a 3.0R (MÁS RELAJADO que Mean-Reversion)
    if r_ratio >= 3.0 and not vars['be_activated']:
        vars['be_activated'] = True
        vars['sl_price'] = entry_price
        print(f"Break-even activado en 3.0R")

    # REGLA 2: Trailing stop DESPUÉS de 3.0R
    if r_ratio >= 3.0:
        # Track highest price
        if 'highest_price' not in vars:
            vars['highest_price'] = close
        else:
            vars['highest_price'] = max(vars['highest_price'], close)

        # Trailing stop: 2R desde el high
        trailing_sl = vars['highest_price'] - (initial_risk * 2.0)

        # Solo mover SL hacia arriba, nunca hacia abajo
        if trailing_sl > vars['sl_price']:
            vars['sl_price'] = trailing_sl
            print(f"Trailing stop actualizado: {trailing_sl:.2f}")

    # REGLA 3: TP final en 6.0R (captura mega trends)
    if r_ratio >= 6.0:
        liquidate()
        print(f"TP final 6.0R alcanzado - Profit: {current_profit:.2f}")
        return

    # REGLA 4: Stop loss manual
    if close <= vars['sl_price']:
        liquidate()
        print(f"Stop loss ejecutado en {vars['sl_price']:.2f}")
        return
```

**Ejemplo de gestión:**
```
Entry: $10,000
Initial SL: $9,650 (risk: $350 = 1R)

Precio sube a $11,050 (+3.0R):
└─ Break-even activado → SL = $10,000

Precio sube a $12,000 (+5.7R):
└─ Highest = $12,000
└─ Trailing SL = $12,000 - (2 × $350) = $11,300

Precio hace pullback a $11,500:
└─ SL sigue en $11,300 (no baja)

Precio continúa a $12,100 (+6.0R):
└─ TP final ejecutado → Profit: $2,100 (6R) ✅
```

---

## 📈 Parámetros de la Estrategia

```python
# TREND-FOLLOWING PARAMETERS
class TrendFollowing(Strategy):

    # Breakout detection
    breakout_lookback = 20       # Velas para detectar high/low
    breakout_threshold = 0.01    # 1% mínimo breakout

    # Score system
    minimum_score = 4            # Más selectivo que Mean-Reversion (3)

    # Position management
    break_even_ratio = 3.0       # Más relajado que Mean-Reversion (1.35)
    tp_final_ratio = 6.0         # Más ambicioso que Mean-Reversion (3.0)
    trailing_stop_ratio = 2.0    # Trailing 2R desde high

    # Risk management
    risk_percent = 1.5           # 1.5% risk per trade
    stop_multiplier = 3.5        # SL = ATR × 3.5

    # Filters
    signal_cooldown_minutes = 60
    min_atr_pct = 0.004          # 0.4% mínimo
    adx_threshold = 25           # Trending market
    volume_multiplier = 1.3      # 30% más volumen

    # Daily limits
    max_daily_loss_pct = 3.0     # 3% max loss per day
```

---

## 🧪 Testing Strategy

### Test 1: Bull Parabólico (2020-2021)

**Periodo:** 2020-01-01 → 2021-12-31
**BTC:** $7,200 → $46,000 (+539%)

**Criterios de éxito:**
- ✅ Net Profit > +30%
- ✅ Win Rate > 18%
- ✅ Max DD < -40%
- ✅ Calmar > 0.8
- ✅ Avg Win > $200
- ✅ R:R > 3.0

**Expectativa realista:**
```
Trades: 150-200 (menos que Mean-Reversion)
Win Rate: 20-25%
Net Profit: +35-55%
Max DD: -30-35%
Avg Win: $250-350
R:R: 4.0-5.0
Calmar: 1.0-1.5
```

---

### Test 2: Validation en Alta Volatilidad (2022-2024)

**Periodo:** 2022-01-01 → 2024-12-31

**Expectativa:**
- Funcionará peor que Mean-Reversion
- Net Profit: -5% a +15% (vs +80% Mean-Reversion)
- Esto es OK - no está diseñado para este régimen

**Criterio:**
- ⚠️ No perder >20% en periodo volátil
- ⚠️ Win rate >15%
- ✅ Sistema híbrido usará Mean-Reversion aquí anyway

---

## 🔄 Diferencias vs Mean-Reversion

| Aspecto | Mean-Reversion (v9.3) | Trend-Following (v11.0) |
|---------|----------------------|------------------------|
| **Entrada** | Dips (RSI oversold) | Breakouts (High×1.01) |
| **Señal Premium** | Divergencias + FVG | Breakout + MACD 1H |
| **Score Mínimo** | 3 puntos | 4 puntos (más selectivo) |
| **Break-Even** | 1.35R (agresivo) | 3.0R (relajado) |
| **Take Profit** | 3.0R (fijo) | 6.0R (fijo) |
| **Trailing Stop** | NO | SÍ (2R desde high) |
| **Objetivo** | Capturar reversiones | Capturar continuación |
| **Óptimo en** | Alta volatilidad | Bull parabólico |
| **Performance** | +110% (2023-25) | +40-60% (2020-21) |

---

## 💡 Ventajas de Trend-Following

**1. Captura mega movimientos**
- Mean-Reversion cierra en 3R
- Trend-Following puede capturar 6R-10R+ con trailing

**2. No lucha contra la tendencia**
- Mean-Reversion entra contra trend (dips)
- Trend-Following entra a favor de trend (breakouts)

**3. Trailing stop protege ganancias**
- Mean-Reversion: BE fijo en 1.35R
- Trend-Following: Trailing 2R desde high

**4. Más selectivo (score 4 vs 3)**
- Menos trades
- Mayor calidad promedio

---

## ⚠️ Riesgos Identificados

**1. Falsos breakouts**
- **Riesgo:** Precio rompe resistencia pero revierte
- **Mitigación:** MACD 1H confirmación (2 puntos)

**2. Whipsaws en ranging**
- **Riesgo:** Breakout en mercado lateral
- **Mitigación:** ADX >25 (trending market)

**3. Trailing stop expulsa muy temprano**
- **Riesgo:** Pullback normal toca trailing SL
- **Mitigación:** 2R de espacio desde high

**4. No funciona en alta volatilidad**
- **Riesgo:** Reversiones frecuentes
- **Mitigación:** Regime Detector usa Mean-Reversion en ese caso

---

## 🎯 Métricas de Monitoreo

**Durante backtesting:**
1. Trades por año
2. Win rate por año
3. Avg holding time (esperamos >3 días vs <2 días Mean-Reversion)
4. % de trades que alcanzan 6R
5. % de trades cerrados en trailing vs TP

**Idealmente:**
- 30-40% trades alcanzan 6R TP
- 40-50% trades cerrados en trailing (3R-5.9R)
- 20-30% trades cerrados en SL o BE

---

## 📋 Próximos Pasos

1. **Implementar código completo** (Día 3-4)
   - Crear `code/strategies/TrendFollowing/__init__.py`
   - Implementar score system
   - Implementar trailing stop logic

2. **Backtest 2020-2021** (Día 5-6)
   - Ejecutar en Jesse
   - Analizar métricas
   - Iterar si necesario

3. **Validación** (Día 7)
   - Walk-forward test
   - Confirmar no overfitting
   - Aprobar para integración

---

**Creado:** 2025-12-28
**Próximo:** Implementar código TrendFollowing
**Estado:** Diseño completo - Listo para implementar
