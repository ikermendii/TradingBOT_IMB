# 🏆 Estrategia 8787% ROI - Implementación EXACTA

**Fuente:** [Medium Article - 8787% ROI Strategy](https://imbuedeskpicasso.medium.com/the-8787-roi-algo-strategy-unveiled-for-crypto-futures-22a5dd88c4a5)

**Autor:** Puranam Pradeep Picasso

**Resultado PROBADO:** +8787% ROI en 1024 días (2021-01-06 a 2023-10-27)

---

## 📊 Parámetros EXACTOS de la Estrategia Original

### Configuración Backtest

```
Período: 2021-01-06 a 2023-10-27 (1024 días = 2.8 años)
Capital inicial: 1000 USDT
Max trades abiertos: 4 simultáneos
Stake máximo: ~200 USDT por trade
Timeframe: 1H
Drawdown máximo: -1.78% (EXCELENTE)
```

### Resultados Reales

```
ROI Total: +8787%
Daily Average Profit: 2.02%
Daily Average Trades: 21.28
Win Days: 706
Loss Days: 309
Draw Days: 10
BTC Buy & Hold (mismo período): +25.75%
Ratio vs Hold: 341x mejor
```

---

## 🔧 Indicadores EXACTOS

### 1. RSI
```python
rsi_period = 14  # Estándar
```

### 2. Bollinger Bands
```python
bb_period = 20  # Estándar
bb_std = 2.0  # Implícito (estándar TA-Lib)
```

### 3. MACD
```python
macd_fast = 12  # Estándar (default TA-Lib)
macd_slow = 26  # Estándar
macd_signal = 9  # Estándar
```

### 4. ADX
```python
adx_period = 14  # Estándar
```

### 5. EMA
```python
# Para exit strategy
ema_period = ?  # No especificado, probablemente 20 o 50
```

### 6. ATR
```python
atr_period = 14  # Estándar
```

---

## 📝 ENTRY LOGIC - CÓDIGO ORIGINAL

### LONG Entry (del artículo)

```python
conditions_long = (
    (dataframe['RSI'] > 30) &  # RSI saliendo de oversold
    (dataframe['close'] > dataframe['lower_band']) &  # Price sobre BB inferior
    (dataframe['macd'] > dataframe['signal'])  # MACD bullish
)
```

**CON ADX Filter (código completo del artículo):**

```python
dataframe.loc[
    (
        (
            (dataframe['adx'] > self.adx_long_min_1.value) &  # ADX mínimo
            (dataframe['adx'] < self.adx_long_max_1.value)    # ADX máximo
        ) |
        (
            (dataframe['adx'] > self.adx_long_min_2.value) &  # ADX mínimo 2
            (dataframe['adx'] < self.adx_long_max_2.value)    # ADX máximo 2
        ) &
        (dataframe['signal'] > 0) &  # Signal LONG del trade_signal
        (dataframe['volume'] > dataframe['volume_mean']) &  # Volume filter
        (dataframe['volume'] > 0)
    ),
    'enter_long'] = 1
```

### SHORT Entry (del artículo)

```python
conditions_short = (
    (dataframe['RSI'] < 70) &  # RSI saliendo de overbought
    (dataframe['close'] < dataframe['upper_band']) &  # Price bajo BB superior
    (dataframe['macd'] < dataframe['signal'])  # MACD bearish
)
```

**CON ADX Filter:**

```python
dataframe.loc[
    (
        (
            (dataframe['adx'] > self.adx_short_min_1.value) &
            (dataframe['adx'] < self.adx_short_max_1.value)
        ) |
        (
            (dataframe['adx'] > self.adx_short_min_2.value) &
            (dataframe['adx'] < self.adx_short_max_2.value)
        ) &
        (dataframe['signal'] < 0) &  # Signal SHORT
        (dataframe['volume'] > dataframe['volume_mean_s'])
    ),
    'enter_short'] = 1
```

---

## 🚪 EXIT LOGIC - CÓDIGO ORIGINAL

### LONG Exit

```python
exit_long = (
    (dataframe['close'] < (dataframe['ema_l'] - (self.atr_long_mul.value * dataframe['atr']))) &
    (dataframe['volume'] > dataframe['volume_mean_exit'])
)
```

**Traducción:**
- Exit cuando: `close < (EMA - (ATR_multiplier * ATR))`
- Requiere volume confirmación

### SHORT Exit

```python
exit_short = (
    (dataframe['close'] > (dataframe['ema_s'] + (self.atr_short_mul.value * dataframe['atr']))) &
    (dataframe['volume'] > dataframe['volume_mean_exit_s'])
)
```

**Traducción:**
- Exit cuando: `close > (EMA + (ATR_multiplier * ATR))`
- Requiere volume confirmación

---

## 🎯 Parámetros Hyperoptimizables (del artículo)

**ADX LONG:**
- `adx_long_min_1` (valor no especificado, probablemente 15-25)
- `adx_long_max_1` (valor no especificado, probablemente 40-60)
- `adx_long_min_2` (alternativa)
- `adx_long_max_2` (alternativa)

**ADX SHORT:**
- `adx_short_min_1`
- `adx_short_max_1`
- `adx_short_min_2`
- `adx_short_max_2`

**ATR Multipliers:**
- `atr_long_mul` (probablemente 1.5-2.5)
- `atr_short_mul` (probablemente 1.5-2.5)

**EMA Periods:**
- `ema_l` (para LONG, probablemente 20-50)
- `ema_s` (para SHORT, probablemente 20-50)

---

## 🔑 Diferencias Críticas vs v2.0

| Aspecto | v2.0 (FALLA) | 8787% ORIGINAL |
|---------|--------------|----------------|
| **RSI Entry** | RSI < 40 (oversold) | **RSI > 30** (saliendo de oversold) ✅ |
| **Bollinger Entry** | Price TOCA banda (2%) | **Price > lower_band** ✅ |
| **MACD Entry** | MACD > Signal ✅ | MACD > Signal (igual) |
| **ADX Logic** | ADX > 20 (simple) | **ADX range (min, max) con OR** ✅ |
| **Volume Filter** | NO | **Volume > mean** ✅ |
| **Exit Logic** | TP fijo 3R | **EMA ± (ATR × multiplier)** ✅ |
| **Timeframe** | 15m | **1H** ✅ |
| **Max trades** | 1 | **4 simultáneos** ✅ |

---

## ⚠️ CRITICAL INSIGHTS

### 1. RSI > 30 (NO < 30)

**ERROR v2.0:** Esperaba RSI <40 (oversold)

**CORRECTO 8787%:** RSI >30 (SALIENDO de oversold)

**Por qué funciona:**
- RSI <30 = Todavía cayendo
- RSI >30 (después de <30) = **REVERSIÓN confirmada**

### 2. close > lower_band (NO touching)

**ERROR v2.0:** Price DEBE tocar banda (≤2%)

**CORRECTO 8787%:** Price > lower_band (cualquier distancia)

**Por qué funciona:**
- Touching banda es muy raro (pocas señales)
- "Sobre la banda" permite más oportunidades

### 3. ADX RANGE (min, max) con OR Logic

**ERROR v2.0:** ADX > 20 simple

**CORRECTO 8787%:**
```python
(ADX > min1 & ADX < max1) OR (ADX > min2 & ADX < max2)
```

**Por qué funciona:**
- ADX >50 = Tendencia muy fuerte, cerca de agotamiento
- ADX 15-35 = Tendencia óptima para entradas
- OR logic permite 2 rangos (flexibilidad)

### 4. Volume Filter OBLIGATORIO

**ERROR v2.0:** Sin volume filter

**CORRECTO 8787%:** `volume > volume_mean`

**Por qué funciona:**
- Evita señales en mercado sin liquidez
- Confirma que hay interés real

### 5. Exit con EMA + ATR (NO TP fijo)

**ERROR v2.0:** TP fijo 3R

**CORRECTO 8787%:** `close < (EMA - ATR × multiplier)`

**Por qué funciona:**
- Dinámico, se adapta a volatilidad
- Deja correr ganadores (trend following)
- Exit solo cuando tendencia cambia (EMA cross + ATR buffer)

### 6. Timeframe 1H (NO 15m)

**ERROR v2.0:** 15m

**CORRECTO 8787%:** **1H**

**Por qué funciona:**
- Menos ruido (noise)
- Señales más confiables
- Menos trades pero mejor calidad

### 7. Max Trades 4 (NO 1)

**ERROR v2.0:** Solo 1 trade simultáneo

**CORRECTO 8787%:** **4 trades simultáneos**

**Por qué funciona:**
- Diversificación temporal
- 21.28 trades/día promedio = Necesita múltiples slots
- Aprovecha más oportunidades

---

## 📋 Implementation Checklist

### Cambios CRÍTICOS para v3.0

- [ ] Cambiar timeframe 15m → **1H**
- [ ] RSI entry: `< 40` → `> 30`
- [ ] Bollinger entry: `touching (≤2%)` → `> lower_band`
- [ ] Añadir **Volume filter**: `volume > volume_mean`
- [ ] ADX: Simple `>20` → **ADX range (min, max) OR logic**
- [ ] Exit: TP fijo → **EMA ± (ATR × multiplier)**
- [ ] Max trades: 1 → **4 simultáneos** (si Jesse lo permite)

### Parámetros a Determinar (Hyperopt)

**ADX ranges:**
- Probar: min1=15, max1=35, min2=25, max2=45

**ATR multipliers:**
- Probar: 1.5, 2.0, 2.5

**EMA periods:**
- Probar: 20, 50

---

## 🎯 Expected Results con Implementación Exacta

**Si copiamos EXACTAMENTE la estrategia:**

```
Período test: 2020-2025 (5.88 años)
Esperado vs 2021-2023 original: Similar o mejor

Target CONSERVADOR (ajustado a período más largo):
- Annual Return: +50-150% (vs +300%+ original)
- Max Drawdown: <-10%
- Trades/año: 150-300+
- Win Rate: 30-40%
```

**Nota:**
- Original fue en 2021-2023 (bull + recovery)
- Nuestro test 2020-2025 incluye bear market 2022
- Esperamos performance algo menor pero AÚN EXCELENTE

---

## 📚 Source Code Reference

**Original Python Code (Freqtrade):**

```python
def trade_signal(dataframe, rsi_tp=14, bb_tp=20):
    # Indicators
    dataframe['RSI'] = ta.RSI(dataframe['close'], timeperiod=rsi_tp)
    dataframe['upper_band'], dataframe['middle_band'], dataframe['lower_band'] = ta.BBANDS(
        dataframe['close'], timeperiod=bb_tp
    )
    dataframe['macd'], dataframe['signal'], _ = ta.MACD(dataframe['close'])

    # LONG conditions
    conditions_long = (
        (dataframe['RSI'] > 30) &
        (dataframe['close'] > dataframe['lower_band']) &
        (dataframe['macd'] > dataframe['signal'])
    )

    # SHORT conditions
    conditions_short = (
        (dataframe['RSI'] < 70) &
        (dataframe['close'] < dataframe['upper_band']) &
        (dataframe['macd'] < dataframe['signal'])
    )

    dataframe.loc[conditions_long, 'signal'] = 1
    dataframe.loc[conditions_short, 'signal'] = -1

    return dataframe
```

**Full code available:** https://patreon.com/pppicasso (paid)

---

## ✅ Next Step

**Implementar UniversalRobustV3 con parámetros EXACTOS de la estrategia 8787% ROI.**

**NO inventar, NO "mejorar", solo COPIAR.**

**Fuente:** [8787% ROI Strategy Article](https://imbuedeskpicasso.medium.com/the-8787-roi-algo-strategy-unveiled-for-crypto-futures-22a5dd88c4a5)
