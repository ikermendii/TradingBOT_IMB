# 🔬 Plan de Re-Optimización v10.0-ROBUST

**Fecha inicio:** 2025-12-28
**Objetivo:** Crear v10.0-ROBUST que funcione en AMBOS regímenes de mercado
**Periodo target:** 2019-2025 (6+ años, incluye bull parabólico + alta volatilidad)

---

## 🎯 Objetivo Final

**v10.0-ROBUST debe cumplir:**
- ✅ Net Profit positivo en 2019-2025 completo
- ✅ Net Profit positivo en 2020-2021 específicamente (actualmente -80%)
- ✅ Max DD <40% en 2019-2025
- ✅ Calmar Ratio >0.8 (vs 1.55 actual en 2023-2025)
- ✅ Win Rate >22% (mínimo viable)

**Trade-off aceptado:**
- ⚠️ Performance en 2023-2025 bajará de +110% a ~+60-80%
- ⚠️ Annual Return bajará de 30.8% a ~18-22%
- ✅ Pero ROBUSTEZ garantizada en cualquier régimen

---

## 📊 Fase 1: Análisis de Baseline (v9.3-RSI36 en 2019-2025)

### Objetivo
Entender el breakdown año por año para identificar dónde exactamente colapsa.

### Tests a Ejecutar

**Test 1.1: Baseline Completo 2019-2025**
```bash
jesse backtest '2019-01-01' '2025-10-17'
```
**Métrica esperada:** -50% a -70% (ya sabemos que falla)
**Uso:** Baseline de referencia

---

**Test 1.2: Breakdown por Año Individual**
```bash
# 2019 - Pre-parabólico
jesse backtest '2019-01-01' '2019-12-31'

# 2020 - Bull parabólico inicio
jesse backtest '2020-01-01' '2020-12-31'

# 2021 - Bull parabólico peak
jesse backtest '2021-01-01' '2021-12-31'

# 2022 - Bear market (ya testeado: +3.72%)
jesse backtest '2022-01-01' '2022-12-31'

# 2023 - Recovery bull (ya testeado: +62.86%)
jesse backtest '2023-01-01' '2023-12-31'

# 2024 - Consolidación (ya testeado en walk-forward)
jesse backtest '2024-01-01' '2024-12-31'

# 2025 - Actual
jesse backtest '2025-01-01' '2025-10-17'
```

**Uso:** Identificar EXACTAMENTE en qué año/s el bot pierde más dinero

---

### Resultados Esperados

| Año | Contexto BTC | Net Profit Esperado v9.3 | Análisis |
|-----|--------------|--------------------------|----------|
| 2019 | +94% (BTC $3.7k→$7.2k) | -10% a +5% | Recuperación post-bear, moderado |
| 2020 | +305% (BTC $7.2k→$29k) | **-40% a -60%** | Bull parabólico 🔴 CRÍTICO |
| 2021 | +60% (BTC $29k→$46k) | **-30% a -50%** | Bull parabólico peak 🔴 CRÍTICO |
| 2022 | -64% (BTC $46k→$16.5k) | +3.72% ✅ (ya testeado) | Bear, bot sobrevive |
| 2023 | +155% (BTC $16.5k→$42k) | +62.86% ✅ (ya testeado) | Recovery, bot excelente |
| 2024 | +35% (BTC $42k→$57k) | +15-25% ✅ | Consolidación, bot bueno |
| 2025 | Variable | Variable | YTD |

**Conclusión esperada:** 2020-2021 generan el -80% del daño total.

---

## 📊 Fase 2: Hipótesis de Parámetros Robustos

Basado en el análisis de causa raíz, estos parámetros deberían funcionar mejor en AMBOS regímenes:

### Hipótesis v10.0-ROBUST (Primera Iteración)

```python
# CAMBIOS RESPECTO A v9.3-RSI36:

# 1. RSI Thresholds - MÁS CONSERVADOR
rsi_long_threshold = 32   # Era 36 - Entradas más selectivas
rsi_short_threshold = 68  # Era 64 - Simétrico

# 2. Break-Even - MÁS RELAJADO
break_even_ratio = 2.0    # Era 1.35 - Da más espacio a mega trends

# 3. Take Profit - MÁS AMBICIOSO
tp_final_ratio = 4.0      # Era 3.0 - Captura más upside en parabólicos

# 4. Score System - SIN CAMBIOS
minimum_score = 3         # Mantener

# JUSTIFICACIÓN:
# - RSI=32: Reduce overtrading en bull parabólico (menos entradas falsas)
# - BE=2.0R: No expulsa posiciones en pullbacks de bull parabólico
# - TP=4.0R: Captura más movimiento en trends largas (2020-2021)
# - Trade-off: En alta volatilidad (2022-2025) capturará menos trades pero más seguros
```

### Hipótesis Alternativa v10.1-ROBUST (Segunda Iteración)

```python
# Más conservador aún:

rsi_long_threshold = 30   # Muy conservador
rsi_short_threshold = 70
break_even_ratio = 2.5    # Muy relajado
tp_final_ratio = 5.0      # Muy ambicioso

# Justificación:
# Priorizar CAPTURA de mega trends vs frecuencia de trades
# Win rate puede bajar a 20-22% pero expectancy sube
```

---

## 📊 Fase 3: Testing de Hipótesis

### Test 3.1: v10.0-ROBUST (RSI=32, BE=2.0, TP=4.0)

**Paso 1:** Modificar código
```bash
# Editar code/strategies/Multitimeframe/__init__.py
# Cambiar parámetros a v10.0-ROBUST
```

**Paso 2:** Backtest 2019-2025 completo
```bash
jesse backtest '2019-01-01' '2025-10-17'
```

**Criterios de éxito:**
- ✅ Net Profit >+30% (vs -66.9% de v9.3)
- ✅ Max DD <-40% (vs -84.47% de v9.3)
- ✅ Profit positivo en 2020-2021 (al menos break-even)
- ✅ Calmar >0.8

**Si falla:** Probar v10.1-ROBUST

---

**Paso 3:** Breakdown por año
```bash
# Si v10.0 pasa el test completo, validar por año:
jesse backtest '2020-01-01' '2020-12-31'  # Debe ser positivo
jesse backtest '2021-01-01' '2021-12-31'  # Debe ser positivo
jesse backtest '2023-01-01' '2023-12-31'  # Comparar con v9.3
```

**Trade-off esperado:**
- 2020-2021: De -60% a +10-20% ✅ MEJORA
- 2023-2025: De +110% a +60-80% ⚠️ DEGRADACIÓN (aceptable)

---

### Test 3.2: v10.1-ROBUST (RSI=30, BE=2.5, TP=5.0)

Solo ejecutar si v10.0 no cumple criterios.

**Mismo proceso que 3.1**

---

### Test 3.3: Walk-Forward Validation

Una vez encontremos parámetros que funcionen en 2019-2025:

**Walk-forward 1: 2019-2022 → Test 2023-2025**
- Train: 2019-2022 (3 años)
- Test: 2023-2025 (2.78 años)
- Criterio: Test debe tener profit positivo

**Walk-forward 2: 2019-2023 → Test 2024-2025**
- Train: 2019-2023 (4 años)
- Test: 2024-2025 (1.77 años)
- Criterio: Test debe tener profit positivo

**Si ambos walk-forwards pasan:** v10.0-ROBUST está validado

---

## 📊 Fase 4: Grid Search Refinamiento (Opcional)

Si v10.0 y v10.1 no cumplen, hacer grid search limitado:

### Parámetros a Optimizar

```python
# RSI Long Threshold
rsi_candidates = [28, 30, 32, 34]  # 4 valores

# Break-Even Ratio
be_candidates = [1.8, 2.0, 2.2, 2.5]  # 4 valores

# TP Final Ratio
tp_candidates = [3.5, 4.0, 4.5, 5.0]  # 4 valores

# Total combinaciones: 4 × 4 × 4 = 64 backtests
```

### Método de Evaluación

**Scoring function:**
```python
def robustness_score(results):
    """
    Prioriza:
    1. Profit positivo en TODOS los periodos
    2. Max DD controlado
    3. Calmar ratio
    """
    # Profit en 2019-2025
    profit_2019_2025 = results['net_profit_pct']

    # Profit en 2020-2021 (crítico)
    profit_2020_2021 = results['net_profit_2020_2021']

    # Max DD
    max_dd = results['max_drawdown']

    # Penalizar si algún periodo es negativo
    if profit_2019_2025 < 0 or profit_2020_2021 < 0:
        return -1000  # Descalificar

    # Penalizar DD extremo
    if max_dd < -50:
        return -1000

    # Score: profit total + profit en 2020-2021 - max_dd
    score = profit_2019_2025 + (profit_2020_2021 * 2) + max_dd

    return score
```

**Ejecutar:**
```bash
# Usar herramienta de optimización de Jesse
jesse optimize '2019-01-01' '2025-10-17'
```

**Seleccionar:** Parámetros con mayor robustness_score

---

## 📊 Fase 5: Validación Final

### Test 5.1: Robustness Testing en v10.0-ROBUST

Una vez tengamos parámetros finales, ejecutar TODOS los tests de robustez:

1. **Test 1: Diferentes Periodos** (7 tests)
   - 2019, 2020, 2021, 2022, 2023, 2024, 2025
   - **Criterio:** Máximo 2 años con profit negativo

2. **Test 2: Altcoins**
   - ETH-USDT 2019-2025
   - **Criterio:** Profit >-20% (mejorado vs -59% de v9.3)

3. **Test 3: Stress Testing**
   - Luna Crash (Mayo 2022)
   - FTX Collapse (Nov 2022)
   - Banking Crisis (Mar 2023)
   - **Criterio:** Máximo 1 evento con profit negativo

4. **Test 4: Walk-Forward Multi-Régimen**
   - Train 2019-2022 → Test 2023-2025
   - **Criterio:** Test profit >+30%

---

### Test 5.2: Comparación v9.3 vs v10.0

| Métrica | v9.3-RSI36 (2023-2025) | v10.0-ROBUST (2023-2025) | v10.0-ROBUST (2019-2025) |
|---------|------------------------|--------------------------|--------------------------|
| Net Profit | +110.68% 🏆 | ??? (esperado: +60-80%) | ??? (esperado: +30-50%) |
| Annual Return | 30.8% 🏆 | ??? (esperado: 18-22%) | ??? (esperado: 8-12%) |
| Max DD | -19.93% | ??? (esperado: -25-30%) | ??? (esperado: -30-40%) |
| Calmar | 1.55 🏆 | ??? (esperado: 0.9-1.2) | ??? (esperado: 0.8-1.0) |
| Win Rate | 25.14% | ??? (esperado: 22-24%) | ??? (esperado: 20-23%) |
| Robustez | ⚠️ Solo 2022-2025 | ✅ Multi-régimen | ✅ Multi-régimen |

**Decisión final:**
- Si v10.0 cumple criterios → Migrar Freqtrade a v10.0
- Si v9.3 sigue mejor en 2025 actual → Mantener v9.3 con circuit breakers

---

## ⏱️ Timeline Estimado

### Semana 1 (Días 1-7)
- ✅ **Día 1:** Fase 1 completa (análisis baseline 2019-2025)
- ✅ **Día 2-3:** Fase 2 + Fase 3.1 (test v10.0-ROBUST)
- ✅ **Día 4-5:** Fase 3.2 y 3.3 si es necesario (walk-forward)
- ✅ **Día 6-7:** Fase 4 (grid search) si v10.0/v10.1 fallan

### Semana 2 (Días 8-14)
- ✅ **Día 8-10:** Fase 5 (validación final)
- ✅ **Día 11-12:** Documentación de v10.0-ROBUST
- ✅ **Día 13-14:** Migración a Freqtrade si es necesario

---

## 📋 Criterios de Éxito Final

**v10.0-ROBUST se considera EXITOSO si:**

1. ✅ Net Profit 2019-2025 >+30%
2. ✅ Net Profit 2020-2021 >+0% (al menos break-even)
3. ✅ Max DD 2019-2025 <-40%
4. ✅ Calmar 2019-2025 >0.8
5. ✅ Máximo 2 años de 7 con profit negativo
6. ✅ Pasa walk-forward validation
7. ✅ Sobrevive 2/3 stress tests

**Si cumple 7/7:** v10.0-ROBUST listo para production

**Si cumple 5-6/7:** v10.0-ROBUST aceptable, considerar deployment conservador

**Si cumple <5/7:** Iterar o considerar Opción 3 (regime detection)

---

## 🎯 Próximo Paso Inmediato

**AHORA:** Ejecutar Fase 1 - Análisis de baseline

```bash
cd "c:\Users\ikerm\Desktop\Pruebas BOTTrading\TradingBot_Project"

# Test baseline completo
jesse backtest '2019-01-01' '2025-10-17'

# Breakdown por año
jesse backtest '2019-01-01' '2019-12-31'
jesse backtest '2020-01-01' '2020-12-31'
jesse backtest '2021-01-01' '2021-12-31'
# (2022-2025 ya testeados)
```

---

**Creado:** 2025-12-28
**Objetivo:** v10.0-ROBUST funcional en 2 semanas
**Versión actual:** v9.3-RSI36 (corriendo en Freqtrade paper trading)
**Próximo milestone:** Fase 1 completa en 24 horas
