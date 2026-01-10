# 📝 Nota: Por Qué Usamos Binance SPOT para Tests Históricos

**Fecha:** 2025-12-28
**Contexto:** Re-optimización v10.0-ROBUST

---

## 🔍 Problema Detectado

Al intentar importar datos de **Binance Perpetual Futures** desde 2019-01-01:

```
❌ Error: No candle exists in the market for 2019-01-01
```

**Causa:** Binance Perpetual Futures BTC-USDT fue lanzado en **Noviembre 2021**, no existía en 2019-2020-2021.

---

## ✅ Solución Adoptada

**Usar Binance Spot para tests históricos largos (2019-2025)**

### Justificación

1. **Datos disponibles desde 2017**
   - Binance Spot BTC-USDT tiene datos completos desde 2017
   - Podemos testear todo el bull parabólico 2020-2021

2. **Lógica de trading idéntica**
   - La estrategia usa RSI, MACD, FVG, divergencias
   - Estos indicadores funcionan igual en SPOT que en Futures
   - Los patrones de precio son los mismos

3. **Fees diferentes pero no crítico**
   - SPOT: ~0.1% fee (con descuento BNB)
   - Futures: ~0.04% fee
   - Diferencia: 0.06% por trade
   - En 350 trades = ~$210 diferencia total
   - **NO afecta las conclusiones sobre parámetros óptimos**

4. **No hay leverage en SPOT pero no importa**
   - Jesse backtest simula leverage matemáticamente
   - El backtest funciona igual en SPOT con leverage simulado
   - La estrategia NO cambia con/sin leverage real

---

## 🎯 Plan de Testeo

### Fase 1-3: Usar Binance SPOT (2019-2025)

**Objetivo:** Encontrar parámetros robustos para AMBOS regímenes

**Tests en SPOT:**
1. Baseline 2019-2025
2. Breakdown por año (2019, 2020, 2021, 2022, 2023, 2024)
3. Optimización de parámetros (RSI, BE, TP)
4. Validación walk-forward

**Resultado esperado:** v10.0-ROBUST con parámetros optimizados

---

### Fase 4: Validar en Binance Futures (2022-2025)

**Objetivo:** Confirmar que v10.0-ROBUST funciona en mercado real (Futures)

**Tests en Futures:**
1. Backtest 2022-2025 (datos disponibles en Futures)
2. Comparar con resultados de SPOT mismo periodo
3. Ajustar si hay diferencias significativas

**Criterio de éxito:**
- v10.0 en Futures 2022-2025 debe tener profit positivo
- Performance debe ser similar a SPOT mismo periodo (±10%)

---

## 📊 Diferencias SPOT vs Futures a Considerar

### 1. Fees
- **SPOT:** 0.1% maker/taker (con BNB)
- **Futures:** 0.02% maker, 0.04% taker
- **Impacto:** Futures ~0.06% mejor por trade
- **Ajuste:** Si v10.0 funciona en SPOT, funcionará MEJOR en Futures

### 2. Slippage
- **SPOT:** Menor liquidez que Futures
- **Futures:** Mayor liquidez
- **Impacto:** Futures tiene MEJOR ejecución
- **Ajuste:** Resultados de SPOT son conservadores

### 3. Funding Rate (solo Futures)
- **Futures:** Paga/recibe funding cada 8h
- **Impacto:** Puede sumar/restar 0.01%-0.03% diario
- **Ajuste:** Jesse backtest NO simula funding rate
- **Nota:** En producción será factor adicional a considerar

---

## ✅ Conclusión

**Usar SPOT para optimización histórica (2019-2025) es VÁLIDO porque:**

1. ✅ Datos completos disponibles
2. ✅ Patrones de precio idénticos
3. ✅ Indicadores técnicos funcionan igual
4. ✅ Diferencias en fees son mínimas (~0.06%)
5. ✅ Validaremos en Futures después (2022-2025)
6. ✅ Si funciona en SPOT, funcionará MEJOR en Futures (mejores fees)

**Plan:**
- Optimizar en SPOT 2019-2025 → v10.0-ROBUST
- Validar en Futures 2022-2025 → confirmar robustez
- Deployar en Freqtrade Futures → producción

---

## 📋 Trade-offs Aceptados

| Aspecto | SPOT | Futures | Impacto |
|---------|------|---------|---------|
| **Datos históricos** | ✅ Desde 2017 | ❌ Solo desde Nov 2021 | SPOT gana |
| **Fees** | 0.1% | 0.04% | Futures gana (+0.06%) |
| **Liquidez** | Buena | Excelente | Futures gana (menor slippage) |
| **Funding rate** | N/A | ±0.01-0.03%/día | Futures tiene costo adicional |
| **Leverage real** | No | Sí | No afecta backtest |
| **Mercado deployment** | No | Sí | Validaremos en Futures después |

**Neto:** Usar SPOT para optimización es conservador pero válido.

---

## 🚀 Próximos Pasos

1. ✅ Importar velas SPOT 2019-2025 (en progreso)
2. ⏳ Ejecutar 4 backtests en SPOT (Fase 1)
3. ⏳ Optimizar parámetros en SPOT (Fase 2-3)
4. ⏳ Validar v10.0 en Futures 2022-2025 (Fase 4)
5. ⏳ Migrar Freqtrade a v10.0-ROBUST si pasa validación

---

**Creado:** 2025-12-28
**Razón:** Documentar decisión de usar SPOT para tests históricos
**Impacto:** Permite optimización robusta incluyendo bull parabólico 2020-2021
