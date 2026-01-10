# 🚀 EJECUTAR BACKTEST v3.2 - Intermediate Balance

**Fecha:** 2025-12-29
**Versión:** v3.2 (Intermediate Balance)

---

## 🎯 Objetivo v3.2

**Encontrar el balance óptimo entre profit y drawdown:**

| Versión | Leverage | Risk % | Annual Return | Max DD |
|---------|----------|--------|---------------|--------|
| v3.0 | 5x | 1.5% | 59.57% | -62.31% ⚠️ |
| v3.1 | 3x | 1.0% | 44.8% | -47.35% ⚠️ |
| **v3.2** | **4x** | **1.25%** | **~50-52%?** | **~-53-55%?** |

**v3.2 = Punto medio entre v3.0 y v3.1**

---

## ⚡ QUICK START

### 1. Abrir Jesse Web UI

```
http://localhost:9000
```

### 2. Configurar Backtest (EXACTO)

**Tab:** Backtest

```
Exchange:         Binance Perpetual Futures
Symbol:           BTC-USDT
Timeframe:        1h  ⚠️ CRITICAL (no 15m)
Start Date:       2020-01-14  ⚠️ MISMO que v3.0 y v3.1
End Date:         2025-12-27
Strategy:         UniversalRobustV3_2  ⚠️ NUEVA VERSIÓN
Starting Balance: 10000
```

### 3. Click "Start Backtest"

Esperar 2-5 minutos.

---

## 📊 Expectativas v3.2

### Proyección Matemática

**Leverage:**
```
v3.0 (5x) → v3.1 (3x) = -40% exposure
v3.2 (4x) = -20% exposure vs v3.0
        = +33% exposure vs v3.1
```

**Risk per trade:**
```
v3.0 (1.5%) → v3.1 (1.0%) = -33% risk
v3.2 (1.25%) = -16.7% risk vs v3.0
             = +25% risk vs v3.1
```

**Expected Results:**
```
Annual Return:
  v3.0: 59.57%
  v3.1: 44.8% (-24.8% vs v3.0)
  v3.2: ~50-52% (-12-16% vs v3.0)

Max Drawdown:
  v3.0: -62.31%
  v3.1: -47.35% (+24.0% mejora)
  v3.2: ~-53-55% (+12-15% mejora)
```

---

## ✅ Criterios de ÉXITO v3.2

### Target Principal

**Encontrar el mejor balance profit/DD:**

```
Calmar Ratio = Annual Return / |Max DD|

v3.0: 59.57% / 62.31% = 0.96
v3.1: 44.8% / 47.35% = 0.95
v3.2 target: >0.95 (igual o mejor que v3.0/v3.1)
```

### Targets Mínimos

| Métrica | v3.2 Target | Prioridad |
|---------|-------------|-----------|
| **Annual Return** | >45% | ALTA |
| **Max Drawdown** | <-55% | ALTA |
| **Calmar Ratio** | >0.95 | CRÍTICA |
| **Sharpe Ratio** | >1.0 | MEDIA |

---

## 🔍 Análisis Post-Backtest

### Comparación Completa

```markdown
# v3.2 BACKTEST RESULTS

## Comparación Triple

| Métrica | v3.0 | v3.1 | v3.2 | Best |
|---------|------|------|------|------|
| **Leverage** | 5x | 3x | 4x | - |
| **Risk %** | 1.5% | 1.0% | 1.25% | - |
| **Net Profit** | +1517.58% | +807.0% | XXX% | ? |
| **Annual Return** | 59.57% | 44.8% | XXX% | ? |
| **Max DD** | -62.31% | -47.35% | -XXX% | ? |
| **Sharpe** | 1.05 | 1.08 | XXX | ? |
| **Calmar** | 0.96 | 0.95 | XXX | ? |
| **Sortino** | 1.85 | 1.90 | XXX | ? |

## Calmar Ratio Analysis

v3.0 Calmar: XXX% / XX.XX% = X.XX
v3.1 Calmar: XXX% / XX.XX% = X.XX
v3.2 Calmar: XXX% / XX.XX% = X.XX

Winner: ???
```

---

## 🎯 Decisión según Resultados

### Escenario A: v3.2 tiene MEJOR Calmar que v3.0 y v3.1 ✅

**Si:**
- Calmar v3.2 > 0.97 (mejor que ambos)
- Annual Return: 48-55%
- Max DD: -50-57%

**Acción:**
1. ✅ **v3.2 APROBADO como versión final**
2. Documentar como "sweet spot" entre profit y riesgo
3. Proceder a **Walk-forward Validation**

---

### Escenario B: v3.2 similar a v3.0 o v3.1 ⚠️

**Si Calmar v3.2 ≈ v3.0 o v3.1 (±0.05):**

**Decisión:** Elegir basado en preferencia:

**Preferir v3.0 si:**
- Toleras -62% DD
- Quieres 59.57% anual
- Calmar 0.96

**Preferir v3.1 si:**
- Prefieres menos riesgo
- 44.8% anual es suficiente
- Calmar 0.95, DD -47%

**Preferir v3.2 si:**
- Balance intermedio
- ~50% anual con ~-53% DD
- Similar Calmar

---

### Escenario C: v3.2 PEOR Calmar que v3.0 y v3.1 ❌

**Si Calmar v3.2 < 0.90:**

**Acción:**
1. ❌ Descartar v3.2
2. Elegir entre v3.0 o v3.1 basado en preferencia
3. No crear más versiones intermedias (evitar overfitting)

---

## 💡 Qué Analizar en Detalle

### 1. Calmar Ratio (CRÍTICO)

**Por qué Calmar es la métrica clave:**
```
Calmar = Profit / Riesgo (en forma de DD)
Calmar >1.0 = ELITE (profit > DD)
Calmar >0.95 = Excelente
Calmar <0.90 = Revisar estrategia
```

**Comparar:**
```
v3.0: 59.57% / 62.31% = 0.96
v3.1: 44.8% / 47.35% = 0.95
v3.2: XXX% / XXX% = ???

¿v3.2 supera 0.96? → Mejor que v3.0
¿v3.2 entre 0.95-0.96? → Similar a v3.0/v3.1
¿v3.2 < 0.95? → Peor balance
```

### 2. Effective Risk per Trade

```
Effective Risk = Leverage × Risk %

v3.0: 5x × 1.5% = 7.5%
v3.1: 3x × 1.0% = 3.0%
v3.2: 4x × 1.25% = 5.0%

v3.2 está exactamente en el medio (3.0% ← 5.0% → 7.5%)
```

### 3. Sharpe/Sortino Improvement

```
Sharpe compara return vs volatilidad total
Sortino compara return vs downside volatility (mejor métrica)

v3.0 Sortino: 1.85
v3.1 Sortino: 1.90

¿v3.2 mejora Sortino? → Mejor downside protection
```

---

## 📝 Template Documentación

Después del backtest, completar:

```markdown
# v3.2 RESULTS - 2025-12-29

## Métricas Principales

- Net Profit: XXX%
- Annual Return: XXX%
- Max Drawdown: -XXX%
- Sharpe Ratio: XXX
- Calmar Ratio: XXX
- Sortino Ratio: XXX
- Win Rate: XXX%
- Trades/año: XXX

## Triple Comparison

### Effective Risk
- v3.0: 5x × 1.5% = 7.5%
- v3.1: 3x × 1.0% = 3.0%
- v3.2: 4x × 1.25% = 5.0%

### Calmar Ratio (Winner)
- v3.0: 0.96
- v3.1: 0.95
- v3.2: XXX ← GANADOR: ???

### Annual/DD Balance
- v3.0: 59.57% / -62.31%
- v3.1: 44.8% / -47.35%
- v3.2: XXX% / -XXX%

## Decisión Final

- [ ] v3.0: Más profit, más DD
- [ ] v3.1: Menos profit, menos DD
- [ ] v3.2: Balance intermedio

Elegida: ??? → Proceder a Walk-forward Validation
```

---

## 🚦 Próximos Pasos

### Si v3.2 es la elegida:

1. **Documentar resultados completos** en `V3.2_BACKTEST_RESULTS.md`
2. **Walk-forward Validation:**
   ```
   Train: 2020-01-14 to 2023-12-31
   Test:  2024-01-01 to 2025-12-27

   Criterio: Test Annual Return > 50% del training
   ```
3. Si validation pasa → **Paper trading 4-8 semanas**

### Si v3.0 o v3.1 son mejores:

1. Descartar v3.2
2. Documentar análisis comparativo
3. Proceder con la versión elegida (v3.0 o v3.1)

---

## 🔑 Puntos Clave

**1. v3.2 NO es necesariamente mejor**
- Es un experimento para encontrar el balance óptimo
- Puede ser igual o peor que v3.0/v3.1

**2. Usar Calmar Ratio como métrica principal**
- Calmar incorpora profit Y riesgo
- Más objetivo que solo mirar Annual Return o Max DD

**3. Evitar overfitting**
- Si v3.2 no supera claramente v3.0/v3.1, elegir uno de ellos
- NO crear v3.3, v3.4, etc.

**4. Todos usan la MISMA lógica de trading**
- v3.0, v3.1, v3.2 = EXACTA estrategia 8787% ROI
- Solo cambia risk management (leverage + risk%)

---

## 📊 Teoría del Balance Óptimo

```
         Profit ↑
            │
            │     v3.0 (59.57%, -62.31%)
            │      ●
            │
            │         v3.2? (~50%, ~-53%)
            │          ●
            │
            │             v3.1 (44.8%, -47.35%)
            │              ●
            │
            └─────────────────────────► DD (menos riesgo →)
```

**El "sweet spot" es donde:**
- Calmar Ratio es MÁXIMO
- Balance óptimo profit/riesgo
- Puede ser v3.0, v3.1 o v3.2

**Solo el backtest revelará cuál es el mejor.**

---

**Estado:** ✅ v3.2 READY FOR BACKTEST

**Acción inmediata:** Ejecutar backtest en http://localhost:9000

**Tiempo estimado:** 2-5 minutos

---

**¡Vamos a descubrir si v3.2 es el sweet spot! 🎯**
