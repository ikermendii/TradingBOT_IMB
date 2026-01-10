# 🔬 Diseño v10.0-ROBUST: Estrategia Multi-Régimen

**Fecha:** 2025-12-28
**Versión anterior:** v9.3-RSI36
**Objetivo:** Funcionar en AMBOS regímenes (parabólico + alta volatilidad)

---

## 🎯 Problema a Resolver

### v9.3-RSI36 Rendimiento por Régimen

| Régimen | Periodo | Net Profit | Calmar | Status |
|---------|---------|------------|--------|--------|
| **Alta Volatilidad** | 2023-2025 | +110.68% 🏆 | 1.55 🏆 | ELITE |
| **Largo Plazo** | 2020-2025 | -67.56% ❌ | -0.21 ❌ | COLAPSO |

**Hipótesis:** 2020-2021 bull parabólico destruye v9.3 por:
1. RSI=36 → Overtrading en dips pequeños
2. BE=1.35R → Expulsa posiciones antes de mega trends
3. TP=3.0R → Deja 70% del movimiento en la mesa

---

## 🧠 Análisis de Causa Raíz

### Régimen 1: Bull Parabólico (2020-2021)

**Características:**
- BTC: +590% en 18 meses ($7k → $69k)
- Movimientos largos sin pullbacks significativos
- Volatilidad BAJA relativa (trend suave hacia arriba)
- Movimientos de 10R, 20R, 30R+ comunes
- Reversiones pequeñas y poco frecuentes

**Por qué v9.3 falla:**
```
Ejemplo: BTC @ $10,000
1. RSI=36 señala LONG en micro-dip a $9,800
2. Bot entra LONG @ $9,800, SL @ $9,500
3. Precio sube a $10,100 (+1.35R) → BE activa, SL @ $9,800
4. Precio pullback a $9,900 (-0.9R desde high)
5. Bot cerrado en BE @ $9,800 (0% profit) ❌
6. BTC continúa a $15,000 (+53% sin el bot)
```

**Resultado:** Win rate colapsa, bot entra/sale en BE constantemente

---

### Régimen 2: Alta Volatilidad (2022-2025)

**Características:**
- BTC: -64% en 2022, luego +150% en 2023
- Movimientos cortos con reversiones frecuentes
- Volatilidad ALTA (ATR >1% común)
- Movimientos de 3R-5R típicos
- Reversiones constantes

**Por qué v9.3 funciona:**
```
Ejemplo: BTC @ $30,000
1. RSI=36 señala LONG en dip a $28,000
2. Bot entra LONG @ $28,000, SL @ $27,000
3. Precio sube a $29,350 (+1.35R) → BE activa
4. Precio continúa a $31,000 (+3.0R) → TP ejecutado ✅
5. Profit: +$300 (3.0R) 🏆
```

**Resultado:** Win rate aceptable (25%), bot captura movimientos completos

---

## 💡 Hipótesis de Solución: Parámetros Adaptativos

### Opción A: Parámetros Universales (v10.0-ROBUST Single Set)

**Concepto:** Un solo set de parámetros que funcione decentemente en AMBOS regímenes

**Trade-off:**
- ⚠️ Menor performance en cada régimen individual
- ✅ Mayor robustez y simplicidad
- ✅ No requiere detection de régimen

**Parámetros propuestos:**
```python
# RSI Thresholds - MÁS CONSERVADOR
rsi_long_threshold = 32   # Era 36 - Reduce entradas falsas
rsi_short_threshold = 68  # Era 64 - Simetría

# Break-Even - MÁS RELAJADO
break_even_ratio = 2.0    # Era 1.35 - Da espacio a trends largas

# Take Profit - MÁS AMBICIOSO
tp_final_ratio = 4.0      # Era 3.0 - Captura más upside

# Score System - SIN CAMBIOS
minimum_score = 3         # Mantener
```

**Justificación:**

**1. RSI=32 (vs 36 anterior):**
- **En bull parabólico:** Menos entradas falsas en micro-dips
  - Reduce overtrading
  - Solo entra en dips REALES
  - Win rate esperado: +3-5%
- **En alta volatilidad:** Ligeramente más conservador
  - Menos trades pero mayor calidad
  - Win rate esperado: -2-3%
- **Neto:** +0-2% win rate global

**2. BE=2.0R (vs 1.35R anterior):**
- **En bull parabólico:** No expulsa posiciones en pullbacks normales
  - Captura mega trends de 10R+
  - Profit esperado: +30-40%
- **En alta volatilidad:** Más riesgo de reversiones
  - Puede perder profit parcial en reversiones
  - Profit esperado: -10-15%
- **Neto:** +15-25% profit global

**3. TP=4.0R (vs 3.0R anterior):**
- **En bull parabólico:** Captura más movimiento
  - De 3R → 4R = +33% más profit por winner
  - Profit esperado: +20-30%
- **En alta volatilidad:** Puede no alcanzar 4R frecuentemente
  - Profit esperado: -5-10%
- **Neto:** +10-20% profit global

**Expectativa total v10.0-ROBUST:**
- **2020-2025:** De -67% → +15-30% (mejora +82-97%) ✅
- **2023-2025:** De +110% → +70-90% (degradación -20-40%) ⚠️

**Trade-off aceptable:** Sacrificamos performance ELITE en 2023-2025 para tener robustez universal

---

### Opción B: Parámetros Dinámicos (v10.1-ADAPTIVE)

**Concepto:** Detectar régimen automáticamente y cambiar parámetros

**Regímenes:**

**1. High Volatility Mode:**
- **Detección:** ATR% >0.6%, ADX >25, movimientos cortos
- **Parámetros:** RSI=36, BE=1.35R, TP=3.0R (v9.3 actual)

**2. Trending Parabolic Mode:**
- **Detección:** ATR% <0.5%, ADX <20, movimientos largos
- **Parámetros:** RSI=30, BE=2.5R, TP=5.0R (más relajado)

**Ventajas:**
- ✅ Mejor de ambos mundos
- ✅ Mantiene ELITE en alta volatilidad
- ✅ Funciona en parabólico

**Desventajas:**
- ❌ Complejidad alta
- ❌ Riesgo de mal detection
- ❌ Necesita 2-3 semanas desarrollo + testing

---

## 🎯 Recomendación: v10.0-ROBUST (Opción A)

**Razones:**
1. **Simplicidad:** Un solo set de parámetros
2. **Tiempo:** Listo para testear en 1-2 días
3. **Robustez:** Funciona en cualquier régimen
4. **Trade-off aceptable:** -20-40% en 2023-2025 pero +82-97% en 2020-2025

**v10.1-ADAPTIVE** queda como mejora futura si v10.0 funciona.

---

## 📊 Plan de Testing v10.0-ROBUST

### Fase 1: Modificar Código

```python
# Editar: code/strategies/Multitimeframe/__init__.py

# Línea ~80: RSI thresholds
self.rsi_long_threshold = 32   # Cambiar de 36
self.rsi_short_threshold = 68  # Cambiar de 64

# Línea ~95: Break-even ratio
self.break_even_ratio = 2.0    # Cambiar de 1.35

# Línea ~100: Take profit
self.tp_final_ratio = 4.0      # Cambiar de 3.0
```

---

### Fase 2: Backtest 2020-2025

**Test v10.0 en periodo completo:**
```
Exchange: Binance Perpetual Futures
Symbol: BTC-USDT
Start: 2020-01-01
End: 2025-12-28
Strategy: Multitimeframe (con parámetros v10.0)
```

**Criterios de éxito:**
- ✅ Net Profit >+20% (vs -67% de v9.3)
- ✅ Max DD <-40% (vs -84% de v9.3)
- ✅ Win Rate >22% (vs 19.8% de v9.3)
- ✅ Calmar >0.8 (vs -0.21 de v9.3)

**Si cumple 4/4:** ✅ v10.0-ROBUST es éxito

---

### Fase 3: Backtest 2023-2025 (Validación)

**Test v10.0 en periodo conocido:**
```
Start: 2023-01-01
End: 2025-12-28
```

**Criterios de aceptación:**
- ✅ Net Profit >+60% (toleramos degradación de +110%)
- ✅ Max DD <-30% (toleramos degradación de -19.93%)
- ✅ Win Rate >22% (toleramos degradación de 25.14%)
- ✅ Calmar >1.0 (toleramos degradación de 1.55)

**Si cumple 4/4:** ✅ Trade-off es aceptable

---

### Fase 4: Walk-Forward Validation

**Train: 2020-2022 → Test: 2023-2025**
- Test debe tener profit positivo (+30%+)

**Train: 2020-2023 → Test: 2024-2025**
- Test debe tener profit positivo (+15%+)

**Si ambos pasan:** ✅ NO hay overfitting

---

### Fase 5: Comparación Final

| Métrica | v9.3 (2020-2025) | v10.0 (2020-2025) | Δ Mejora |
|---------|------------------|-------------------|----------|
| Net Profit | -67.56% ❌ | +??% | +??? |
| Max DD | -84.92% ❌ | -??% | +??? |
| Win Rate | 19.8% ❌ | ??% | +??? |
| Calmar | -0.21 ❌ | ??? | +??? |
| **Status** | COLAPSO | ??? | ??? |

| Métrica | v9.3 (2023-2025) | v10.0 (2023-2025) | Δ Trade-off |
|---------|------------------|-------------------|-------------|
| Net Profit | +110.68% 🏆 | +??% | -??? |
| Max DD | -19.93% ✅ | -??% | -??? |
| Win Rate | 25.14% ✅ | ??% | -??? |
| Calmar | 1.55 🏆 | ??? | -??? |
| **Status** | ELITE | ??? | ??? |

---

## 🚀 Timeline de Implementación

### Hoy (2025-12-28):
- ✅ Esperar resultados backtests v9.3 (Futures + Spot)
- ✅ Confirmar hipótesis de colapso
- ⏳ Modificar código a v10.0-ROBUST
- ⏳ Testear v10.0 en 2020-2025

### Mañana (2025-12-29):
- ⏳ Testear v10.0 en 2023-2025 (validación)
- ⏳ Walk-forward validation
- ⏳ Decisión: ¿v10.0 es aceptable?

### Día 3 (2025-12-30):
- ⏳ Si v10.0 pasa: Migrar a Freqtrade
- ⏳ Si v10.0 falla: Iterar o considerar v10.1-ADAPTIVE

---

## 📝 Parámetros Alternativos (Si v10.0 Falla)

### v10.1-CONSERVATIVE (Más Conservador)

```python
rsi_long_threshold = 30   # Muy conservador
rsi_short_threshold = 70
break_even_ratio = 2.5    # Muy relajado
tp_final_ratio = 5.0      # Muy ambicioso
```

**Cuándo usar:** Si v10.0 aún tiene win rate <22% o overtrading

---

### v10.2-MODERATE (Menos Cambio)

```python
rsi_long_threshold = 34   # Cambio moderado
rsi_short_threshold = 66
break_even_ratio = 1.8    # Cambio moderado
tp_final_ratio = 3.5      # Cambio moderado
```

**Cuándo usar:** Si v10.0 degrada demasiado en 2023-2025 (>-40%)

---

## ✅ Criterios de Decisión Final

**Deployar v10.0-ROBUST si:**
1. ✅ Net Profit 2020-2025 >+20%
2. ✅ Net Profit 2023-2025 >+60%
3. ✅ Max DD 2020-2025 <-40%
4. ✅ Pasa walk-forward validation

**Iterar a v10.1 si:**
- ⚠️ Cumple 2-3 de 4 criterios arriba

**Volver a v9.3 + Circuit Breakers si:**
- ❌ Cumple <2 de 4 criterios

---

**Creado:** 2025-12-28
**Próximo:** Esperar backtests v9.3, luego implementar v10.0
**Objetivo:** v10.0-ROBUST funcional en 2-3 días
