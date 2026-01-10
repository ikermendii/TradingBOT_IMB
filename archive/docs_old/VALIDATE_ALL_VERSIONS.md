# 🔬 Walk-Forward Validation - TODAS LAS VERSIONES

**Objetivo:** Comparar walk-forward de v3.0, v3.1, v3.2 para ver si el overfitting es universal o específico.

---

## 📊 Resultados v3.2 (YA COMPLETADO)

| Período | Annual Return | Calmar | Ratio |
|---------|---------------|--------|-------|
| TRAIN (2020-2023) | 77.32% | 1.40 | - |
| TEST (2024-2025) | 13.97% | 0.27 | 0.18 ❌ |
| **Veredicto** | **FAIL** | Degradación 82% | Need ≥0.5 |

---

## 🎯 PLAN DE VALIDACIÓN

### Secuencia de Tests

```
1. v3.1 TRAIN (2020-2023)  ← PRIMERO
2. v3.1 TEST (2024-2025)
3. v3.0 TRAIN (2020-2023)
4. v3.0 TEST (2024-2025)
5. Comparar las 3 versiones
```

**Tiempo total:** ~15 minutos (6 backtests)

---

## ⚡ TEST 1: v3.1 TRAIN Period

**ACTUAL - Ejecutar ahora:**

### Configuración

```
http://localhost:9000 → Backtest

Exchange:     Binance Perpetual Futures
Symbol:       BTC-USDT
Timeframe:    1h
Start Date:   2020-01-14  ← TRAIN
End Date:     2023-12-31  ← TRAIN (3.88 años)
Strategy:     UniversalRobustV3_1  ⚠️ (YA configurado en routes.py)
Balance:      10000

→ Start Backtest
```

### Qué Esperar

**v3.1 Full baseline (2020-2025):**
- Annual Return: 44.8%
- Max DD: -47.35%
- Sharpe: 1.08
- Calmar: 0.95

**Expected TRAIN (2020-2023):**
- Annual Return: ~50-60% (mejor que full, como v3.2)
- Max DD: ~-45-50%
- Calmar: ~1.0-1.2

---

## ⚡ TEST 2: v3.1 TEST Period

**Después de completar TEST 1:**

### Configuración

```
http://localhost:9000 → Backtest

Exchange:     Binance Perpetual Futures
Symbol:       BTC-USDT
Timeframe:    1h
Start Date:   2024-01-01  ← TEST
End Date:     2025-12-27  ← TEST (1.99 años)
Strategy:     UniversalRobustV3_1
Balance:      10000

→ Start Backtest
```

### Target v3.1

```
TRAIN Annual: ???% (de TEST 1)
Target TEST: ≥50% de TRAIN

Si TRAIN = 55% → TEST debe ser ≥27.5%
```

---

## ⚡ TEST 3-4: v3.0 TRAIN + TEST

**Después de completar v3.1, cambiar routes.py:**

```python
# En routes.py cambiar a:
('Binance Perpetual Futures', 'BTC-USDT', '1h', 'UniversalRobustV3'),
```

**Luego ejecutar:**
1. TRAIN: 2020-01-14 to 2023-12-31
2. TEST: 2024-01-01 to 2025-12-27

### v3.0 Baseline

- Annual Return: 59.57%
- Max DD: -62.31%
- Sharpe: 1.05
- Calmar: 0.96

---

## 📋 Template para Anotar Resultados

### v3.1 Walk-Forward

```
TRAIN (2020-2023):
  Annual Return: ____%
  Max DD: -____%
  Calmar: ____

TEST (2024-2025):
  Annual Return: ____%
  Max DD: -____%
  Calmar: ____

Ratio TEST/TRAIN: ____ (need ≥0.5)
Veredicto: PASS / FAIL
```

### v3.0 Walk-Forward

```
TRAIN (2020-2023):
  Annual Return: ____%
  Max DD: -____%
  Calmar: ____

TEST (2024-2025):
  Annual Return: ____%
  Max DD: -____%
  Calmar: ____

Ratio TEST/TRAIN: ____ (need ≥0.5)
Veredicto: PASS / FAIL
```

---

## 🎯 Posibles Escenarios

### Escenario A: TODAS fallan walk-forward ❌

```
v3.0: FAIL
v3.1: FAIL
v3.2: FAIL (ya confirmado)
```

**Conclusión:**
- Estrategia 8787% ROI tiene overfitting temporal UNIVERSAL
- Funciona SOLO en bull/bear markets (2020-2023)
- NO funciona en sideways (2024-2025)
- **Acción:** Descartar v3.x, buscar estrategia nueva

---

### Escenario B: v3.1 o v3.0 PASA ✅

```
v3.0: PASS (ratio ≥0.5)
v3.1: PASS (ratio ≥0.5)
v3.2: FAIL
```

**Conclusión:**
- Overfitting es específico de v3.2
- v3.0 o v3.1 son robustos
- **Acción:** Proceder a paper trading con la versión que pasó

---

### Escenario C: Solo UNA pasa ⚠️

```
v3.0: PASS
v3.1: FAIL
v3.2: FAIL
```

**Conclusión:**
- v3.0 (más agresivo) es más robusto
- Leverage menor (v3.1, v3.2) degradó robustez
- **Acción:** Proceder con v3.0 a paper trading

---

## 📊 Comparación Final

**Después de completar TODOS los tests:**

| Versión | Leverage | Risk % | TRAIN Annual | TEST Annual | Ratio | Status |
|---------|----------|--------|--------------|-------------|-------|--------|
| **v3.0** | 5x | 1.5% | ???% | ???% | ??? | ✅/❌ |
| **v3.1** | 3x | 1.0% | ???% | ???% | ??? | ✅/❌ |
| **v3.2** | 4x | 1.25% | 77.32% | 13.97% | 0.18 | ❌ |

---

## 💡 Hipótesis a Validar

### Hipótesis 1: Todas fallan (más probable)

**Razón:**
- Las 3 versiones usan MISMA lógica de trading
- Solo difieren en leverage/risk (position sizing)
- Si la lógica está overfitted, todas fallarán

**Si se confirma:**
→ Problema es la estrategia 8787% ROI base, no el risk management

---

### Hipótesis 2: v3.0 pasa, v3.1/v3.2 fallan

**Razón:**
- v3.0 (5x leverage) captura movimientos mejor
- v3.1/v3.2 (3x-4x leverage) son muy conservadores para TEST period
- Position sizing menor → Ganancias muy pequeñas

**Si se confirma:**
→ Más agresivo = más robusto en este caso

---

### Hipótesis 3: Todas pasan (menos probable)

**Razón:**
- v3.2 falló por casualidad
- Otras versiones son más robustas

**Si se confirma:**
→ Problema específico de v3.2, proceder con v3.0 o v3.1

---

## 🚀 PRÓXIMO PASO INMEDIATO

### Ejecutar v3.1 TRAIN Period

**Ir a:** http://localhost:9000

**Configurar:**
- Start: 2020-01-14
- End: 2023-12-31
- Strategy: UniversalRobustV3_1 (ya configurado)
- Balance: 10000

**Click:** Start Backtest

**Compartir:** Annual Return y Calmar de TRAIN

---

**Tiempo:** 2-3 minutos por backtest × 4 tests = ~10-15 minutos total

**¡Vamos a validar todas las versiones!** 🔬
