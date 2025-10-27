# 🎯 ROADMAP DE LA ESTRATEGIA MULTITIMEFRAME

## 📊 Visión Completa de la Estrategia

### Concepto Final (Target):
Estrategia multi-timeframe que combina múltiples confirmaciones:

**Análisis en 3 Timeframes**:
- **4H**: Identificar tendencia principal
- **1H**: Confirmar direccionalidad y estructura
- **15M**: Ejecución de trades con precisión

**Señales de Entrada**:
1. **Divergencias RSI** (precio vs RSI)
2. **Divergencias MACD** (precio vs MACD)
3. **Filtro de tendencia** (EMAs en 4H)
4. **Confirmación direccional** (estructura en 1H)
5. **Volumen** (confirmación de fuerza)
6. **Volatilidad** (ATR mínimo)

---

## ✅ ESTADO ACTUAL (v4.0 Híbrida)

### Componentes ACTIVOS:

**Timeframes**:
- ✅ 15M (ejecución)
- ⚠️ 1H (importado pero no usado aún)
- ⚠️ 4H (importado pero no usado aún)

**Filtros de Entrada**:
- ✅ RSI oversold/overbought (< 42 LONG, > 58 SHORT)
- ✅ MACD señal alcista/bajista
- ✅ Tendencia EMA50 vs EMA200 (solo en 15M)
- ✅ Precio vs EMA200 (solo en 15M)
- ✅ Volumen > promedio
- ✅ Volatilidad mínima (ATR)

**Gestión de Riesgo**:
- ✅ Stop-loss: ATR(14) x 1.8
- ✅ TP1: 1.5R (cerrar 50%)
- ✅ TP2: 3.0R (cerrar 30%)
- ✅ TP3: 6.0R (cerrar 20% final)
- ✅ Trailing stop después de TP2
- ✅ Límite diario: 3% pérdida máxima
- ✅ Cooldown: 60 minutos entre señales

### Componentes DESACTIVADOS (temporalmente):

**Pendientes de Activación**:
- ⏳ Divergencias alcistas RSI (_bullish_divergence)
- ⏳ Divergencias bajistas RSI (_bearish_divergence)
- ⏳ Análisis multi-timeframe (1H, 4H)
- ⏳ Filtro overextended (_not_overextended)

---

## 🚀 PLAN DE ACTIVACIÓN POR FASES

### FASE 1 (ACTUAL - v4.0): Fundamentos Sólidos ✅
**Objetivo**: Estrategia básica funcional con buenos filtros
**Estado**: ✅ COMPLETADO
- RSI + MACD + Tendencia + Volumen
- Sistema de cierre escalonado (TP1, TP2, TP3)
- Gestión de riesgo diaria

**Próximo paso**: Backtest v4.0 para establecer baseline

---

### FASE 2: Activar Divergencias RSI (v5.0)
**Objetivo**: Añadir detección de divergencias como filtro adicional
**Dependencias**: Resultados de v4.0

**Cambios**:
1. Activar  en should_long
2. Activar  en should_short
3. Ajustar lookback period según resultados
4. Backtest comparativo v4.0 vs v5.0

**Resultado esperado**: 
- Menos trades (más selectivo)
- Mayor win rate
- Mejor calidad de entradas

---

### FASE 3: Multi-timeframe 1H (v6.0)
**Objetivo**: Usar 1H para confirmar estructura/direccionalidad
**Dependencias**: v5.0 funcionando

**Cambios**:
1. Leer candles de 1H: 
2. Analizar estructura en 1H (swing highs/lows)
3. Confirmar dirección con RSI/MACD en 1H
4. Backtest v5.0 vs v6.0

**Resultado esperado**:
- Trades alineados con estructura mayor
- Reducción de whipsaws
- Mejor R:R ratio

---

### FASE 4: Multi-timeframe 4H (v7.0)
**Objetivo**: Usar 4H para filtro de tendencia principal
**Dependencias**: v6.0 funcionando

**Cambios**:
1. Leer candles de 4H
2. Identificar tendencia en 4H (EMA 50/200)
3. Solo operar LONG en uptrend 4H, SHORT en downtrend 4H
4. Backtest v6.0 vs v7.0

**Resultado esperado**:
- Trades alineados con tendencia mayor
- Menos trades contra-tendencia
- Mayor consistencia

---

### FASE 5: Optimización Final (v8.0)
**Objetivo**: Fine-tuning de todos los parámetros
**Dependencias**: v7.0 funcionando

**Optimizaciones**:
1. RSI thresholds (42/58 vs otros valores)
2. Cooldown (60min vs otros)
3. TP levels (1.5R, 3R, 6R vs otros)
4. ATR multiplier (1.8x vs otros)
5. Límite pérdida diaria (3% vs otros)

**Método**: Grid search o walk-forward optimization

---

## 📈 MÉTRICAS OBJETIVO POR FASE

| Fase | Trades/año | Win Rate | Profit Factor | Max DD | Sharpe |
|------|------------|----------|---------------|---------|--------|
| v4.0 Baseline | 50-150 | 40-45% | >1.2 | <20% | >0.8 |
| v5.0 Divergencias | 30-80 | 50-55% | >1.5 | <15% | >1.2 |
| v6.0 Multi 1H | 20-60 | 55-60% | >1.8 | <12% | >1.5 |
| v7.0 Multi 4H | 15-40 | 60-65% | >2.0 | <10% | >1.8 |
| v8.0 Optimizada | 20-50 | 65-70% | >2.5 | <8% | >2.0 |

---

## 🔧 ARCHIVO DE CÓDIGO

**Ubicación**: 

**Métodos por Estado**:

**ACTIVOS** ✅:
-  / 
-  / 
- 
-  / 
-  / 
-  / 
- 
- 
- 
- 

**INACTIVOS** ⏳ (para fases futuras):
-  → FASE 2
-  → FASE 2
-  → FASE 5 (optimización)

**ARCHIVADOS** 📦:
- Multi-timeframe analysis → FASE 3 y 4

---

## 📝 NOTAS IMPORTANTES

1. **No eliminar código inactivo**: Las divergencias y multi-timeframe son parte del plan
2. **Activación gradual**: Una fase a la vez, con backtests comparativos
3. **Baseline v4.0**: Establecer métricas base antes de añadir complejidad
4. **Documentación**: Cada fase debe registrarse en 

---

**Última actualización**: 2025-10-25
**Versión actual**: v4.0 Híbrida
**Próximo hito**: Backtest v4.0 baseline
