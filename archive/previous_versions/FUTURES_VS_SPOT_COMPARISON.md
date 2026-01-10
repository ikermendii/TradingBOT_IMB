# 📊 Comparación: Binance Futures vs Spot (2020-2025)

**Fecha:** 2025-12-28
**Versión:** v9.3-RSI36
**Periodo:** 2020-01-01 a 2025-12-28 (5.99 años)

---

## 🎯 Objetivo

Comparar performance de v9.3-RSI36 en dos exchanges diferentes para entender:
1. ¿El colapso en periodo largo es consistente en ambos?
2. ¿Las diferencias de fees afectan significativamente?
3. ¿Hay diferencias en liquidez/slippage que afecten resultados?

---

## 📋 Resultados Comparativos

### Binance Perpetual Futures

**Configuración:**
- Exchange: Binance Perpetual Futures
- Symbol: BTC-USDT
- Timeframe: 15m
- Period: 2020-01-08 → 2025-12-27 (5.88 años)
- Fees: 0.02% maker, 0.04% taker

**Resultados:**
```
Total Closed Trades:    935
Total Net Profit:       -66.43% ❌❌❌
Max Drawdown:           -84.92% ❌❌❌
Annual Return:          -16.69% ❌
Win Rate:               20% ❌
Expectancy:             -$7.10 ❌

Sharpe Ratio:           -0.44 ❌
Calmar Ratio:           -0.20 ❌
Sortino Ratio:          -0.62 ❌

Losing Streak:          26 ❌❌
Largest Win:            $401.35
Largest Loss:           -$156.86

Total Winning Trades:   187 (20%)
Total Losing Trades:    748 (80%)

Total Paid Fees:        $1,646.73
Avg Win | Avg Loss:     $133.08 | $42.15
R:R Ratio:              3.16
```

---

### Binance Spot

**Configuración:**
- Exchange: Binance Spot
- Symbol: BTC-USDT
- Timeframe: 15m
- Period: 2020-01-01 → 2025-12-28
- Fees: 0.1% maker/taker (con descuento BNB)

**Resultados:**
```
Total Closed Trades:    _______
Total Net Profit:       _______%
Max Drawdown:           _______%
Annual Return:          _______%
Win Rate:               _______%
Expectancy:             $_______

Sharpe Ratio:           _______
Calmar Ratio:           _______
Sortino Ratio:          _______

Losing Streak:          _______
Largest Win:            $_______
Largest Loss:           $_______

Total Winning Trades:   _______
Total Losing Trades:    _______
```

---

## 📊 Análisis Comparativo

### Diferencias Clave

| Métrica | Futures | Spot | Δ Diferencia | Análisis |
|---------|---------|------|--------------|----------|
| **Net Profit %** | ___% | ___% | ___% | ______ |
| **Max Drawdown %** | ___% | ___% | ___% | ______ |
| **Win Rate %** | ___% | ___% | ___% | ______ |
| **Annual Return %** | ___% | ___% | ___% | ______ |
| **Sharpe Ratio** | ___ | ___ | ___ | ______ |
| **Calmar Ratio** | ___ | ___ | ___ | ______ |
| **Total Trades** | ___ | ___ | ___ | ______ |
| **Expectancy $** | $___ | $___ | $___ | ______ |
| **Losing Streak** | ___ | ___ | ___ | ______ |

---

## 🔍 Interpretación de Diferencias

### Escenario A: Resultados Muy Similares (Δ < 5%)

**Si Net Profit, Win Rate, y Max DD son casi idénticos:**

✅ **Conclusión:** La estrategia es robusta independiente del exchange
✅ **Implicación:** Las diferencias de fees (0.04% vs 0.1%) NO son críticas
✅ **Confianza:** Alta - podemos confiar en backtests de cualquier exchange

**Acción:** Usar el exchange que tenga mejores datos históricos disponibles

---

### Escenario B: Futures Ligeramente Mejor (5% < Δ < 15%)

**Si Futures tiene +5-15% mejor performance que Spot:**

⚠️ **Conclusión:** Fees sí importan, pero no dramáticamente
⚠️ **Implicación:**
- Diferencia de fees: 0.1% - 0.04% = 0.06% por trade
- En 900 trades × 0.06% = ~5.4% diferencia total
- Consistente con diferencia observada

✅ **Confianza:** Media-Alta - ajustar expectativas para deployment

**Acción:** Usar Futures para optimización final y deployment

---

### Escenario C: Diferencias Significativas (Δ > 15%)

**Si diferencia >15% en Net Profit o >5% en Win Rate:**

❌ **Conclusión:** Hay factores más allá de fees afectando resultados
❌ **Posibles causas:**
- Liquidez diferente causando slippage
- Datos históricos inconsistentes/corruptos
- Bug en implementación de uno de los exchanges

⚠️ **Confianza:** Baja - investigar antes de continuar

**Acción:** Debugging para entender causa raíz

---

## 📈 Análisis de Fees Teórico

### Cálculo de Impacto de Fees

**Asumiendo:**
- Trades totales: 900 (estimado)
- Trade promedio: $5,000 stake
- Round-trip (entry + exit): 2 operaciones por trade

**Futures:**
- Fee por operación: 0.04% × $5,000 = $2
- Round-trip: $2 × 2 = $4 por trade
- **Total fees:** $4 × 900 = $3,600

**Spot:**
- Fee por operación: 0.1% × $5,000 = $5
- Round-trip: $5 × 2 = $10 por trade
- **Total fees:** $10 × 900 = $9,000

**Diferencia teórica:** $9,000 - $3,600 = **$5,400**

**Como % del capital inicial ($10,000):** 54%

**Conclusión:** La diferencia de fees puede explicar fácilmente 5-10% de diferencia en Net Profit final.

---

## 🎯 Criterios de Validación

### ✅ Backtest VÁLIDO si:

1. **Consistencia de colapso:**
   - Ambos (Futures y Spot) muestran Net Profit negativo <-50%
   - Diferencia entre ambos <20%

2. **Win Rate consistente:**
   - Ambos ~19-21% (vs 25.14% en 2023-2025)
   - Diferencia <2%

3. **Max DD consistente:**
   - Ambos >-70%
   - Diferencia <15%

4. **Losing Streak consistente:**
   - Ambos >20 trades
   - Diferencia <5 trades

**Si cumple 4/4:** ✅ Backtests VÁLIDOS - proceder con v10.0-ROBUST

**Si cumple 2-3/4:** ⚠️ Revisar pero probablemente OK

**Si cumple <2/4:** ❌ Investigar inconsistencias

---

## 📝 Conclusiones Esperadas

**Hipótesis principal:**
- Ambos exchanges mostrarán colapso similar (-60% a -70%)
- Futures será ligeramente mejor (+5-10%) por fees menores
- Patrón de fallo será idéntico (win rate cae, losing streak sube)

**Si hipótesis se confirma:**
✅ Podemos confiar en los datos
✅ El problema es la ESTRATEGIA no los datos
✅ Proceder con diseño de v10.0-ROBUST

**Si hipótesis NO se confirma:**
⚠️ Investigar qué está causando inconsistencias
⚠️ Validar datos históricos
⚠️ Posible bug en estrategia o Jesse

---

## 🚀 Próximos Pasos

**Una vez tengamos ambos resultados:**

1. **Llenar esta plantilla** con resultados reales
2. **Analizar diferencias** usando tabla comparativa
3. **Validar criterios** (4 puntos arriba)
4. **Diseñar v10.0-ROBUST** basándonos en:
   - Patrón de fallo confirmado
   - Métricas de ambos exchanges
   - Teoría de por qué falla (BE + RSI en parabólico)

---

**Creado:** 2025-12-28
**Propósito:** Comparar Futures vs Spot para validar datos
**Próximo:** Esperar resultados de ambos backtests
