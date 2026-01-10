# 🚀 EJECUTAR BACKTEST v3.1 - Instrucciones Rápidas

**Fecha:** 2025-12-29
**Versión:** v3.1 (Risk Optimized)

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
Start Date:       2020-01-14  ⚠️ MISMO que v3.0
End Date:         2025-12-27
Strategy:         UniversalRobustV3_1  ⚠️ NUEVA VERSIÓN
Starting Balance: 10000
```

### 3. Click "Start Backtest"

Esperar 2-5 minutos.

---

## 📊 Qué Esperar

### v3.0 Baseline (para comparar)

```
Net Profit:      +1517.58%
Annual Return:   59.57%
Max Drawdown:    -62.31% ⚠️ (TOO HIGH)
Sharpe Ratio:    1.05
Win Rate:        33.46%
Trades/año:      89.8
```

### v3.1 Expected Results

```
Net Profit:      +500-900% (menos que v3.0)
Annual Return:   35-45% (target >30%)
Max Drawdown:    -35% to -45% (target <-45%)
Sharpe Ratio:    1.1-1.3 (mejor risk-adjusted)
Win Rate:        ~33% (similar)
Trades/año:      ~90 (similar)
```

---

## ✅ Criterios de ÉXITO v3.1

| Métrica | v3.0 | v3.1 Target | Prioridad |
|---------|------|-------------|-----------|
| **Annual Return** | 59.57% | **>30%** | ALTA |
| **Max Drawdown** | -62.31% | **<-45%** | CRÍTICA |
| **Sharpe Ratio** | 1.05 | **>0.9** | ALTA |

**Si pasa los 3 targets:** ✅ PROCEDER a Walk-forward Validation

**Si NO pasa Max DD:** ❌ Crear v3.2 con más reducción (Leverage 2x, Risk 0.8%)

---

## 🔑 Cambios v3.0 → v3.1

**ÚNICAMENTE Risk Management:**

| Parámetro | v3.0 | v3.1 |
|-----------|------|------|
| Leverage | 5x | **3x** |
| Risk per trade | 1.5% | **1.0%** |

**TODO LO DEMÁS (RSI, MACD, Bollinger, ADX, EMA, ATR, Volume) SIN CAMBIOS**

---

## 📝 Template para Documentar Resultados

Copiar y completar después del backtest:

```markdown
# v3.1 BACKTEST RESULTS - 2025-12-29

## Resultados

- Net Profit: XXX%
- Annual Return: XXX%
- Max Drawdown: -XXX%
- Sharpe Ratio: XXX
- Calmar Ratio: XXX
- Win Rate: XXX%
- Trades/año: XXX

## Comparación vs v3.0

| Métrica | v3.0 | v3.1 | Cambio | Target | Status |
|---------|------|------|--------|--------|--------|
| Annual Return | 59.57% | XXX% | XXX% | >30% | ✅/❌ |
| Max DD | -62.31% | -XXX% | XXX% | <-45% | ✅/❌ |
| Sharpe | 1.05 | XXX | XXX | >0.9 | ✅/❌ |

## Decisión

- [ ] ✅ APROBAR v3.1 → Proceder a Walk-forward Validation
- [ ] ⚠️ AJUSTAR → Crear v3.2 con parámetros intermedios
- [ ] ❌ RECHAZAR → Revertir a v3.0 y aceptar DD alto
```

---

## 🎯 Próximos Pasos según Resultado

### Si v3.1 PASA (Annual >30%, DD <-45%)

1. Documentar resultados completos en `V3.1_BACKTEST_RESULTS.md`
2. **Walk-forward Validation:**
   - Train: 2020-01-14 to 2023-12-31
   - Test: 2024-01-01 to 2025-12-27
   - Comparar performance test vs train
3. Si validation pasa → **Paper trading 4-8 semanas**

### Si v3.1 NO PASA (DD aún >-45%)

1. Analizar por qué DD no mejoró suficiente
2. Opciones:
   - **v3.2 más conservador:** Leverage 2x, Risk 0.8%
   - **v3.2 intermedio:** Leverage 4x, Risk 1.25%
   - **Circuit breaker:** Stop trading si DD >-40%
3. Re-testear v3.2

---

## ⚠️ IMPORTANTE: Comparación Justa

**Para comparar v3.0 vs v3.1 correctamente:**

- Mismo período: 2020-01-14 to 2025-12-27
- Mismo timeframe: 1h
- Mismo capital inicial: $10,000
- Misma configuración de exchange

**La ÚNICA diferencia debe ser:** UniversalRobustV3 vs UniversalRobustV3_1

---

## 💡 Qué Analizar en los Resultados

### 1. Max Drawdown

**Target:** <-45%

```
v3.0: -62.31%
v3.1: -XXX%
Mejora: XXX%

¿Suficiente reducción? Si no, considerar v3.2 más conservador.
```

### 2. Annual Return

**Target:** >30%

```
v3.0: 59.57%
v3.1: XXX%
Reducción: XXX%

¿Trade-off aceptable? 35-45% anual con -40% DD es EXCELENTE.
```

### 3. Sharpe Ratio

**Target:** >0.9 (mejor >1.1)

```
v3.0: 1.05
v3.1: XXX

¿Mejora risk-adjusted return? Si Sharpe sube = mejor balance risk/return.
```

### 4. Calmar Ratio

**Target:** >0.8 (mejor >1.0)

```
Calmar = Annual Return / |Max DD|

v3.0: 59.57% / 62.31% = 0.96
v3.1: XXX% / XXX% = ???

Calmar >1.0 = ELITE quality strategy
```

---

## 🔗 Documentos Relacionados

- [V3.0_BACKTEST_RESULTS.md](V3.0_BACKTEST_RESULTS.md) - Resultados v3.0 baseline
- [V3.1_IMPLEMENTATION_NOTES.md](V3.1_IMPLEMENTATION_NOTES.md) - Detalles técnicos v3.1
- [V3_IMPLEMENTATION_SUMMARY.md](V3_IMPLEMENTATION_SUMMARY.md) - Resumen estrategia 8787%
- [code/strategies/UniversalRobustV3_1/__init__.py](code/strategies/UniversalRobustV3_1/__init__.py) - Código v3.1

---

**Estado:** ✅ v3.1 READY FOR BACKTEST

**Acción inmediata:** Ejecutar backtest en Jesse Web UI con configuración de arriba

**Tiempo estimado:** 2-5 minutos de ejecución

---

**¡Buena suerte con v3.1!**

Objetivo: Reducir DD de -62% a -35-45% manteniendo >30% anual.
