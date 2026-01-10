# 📅 SEMANA 1: Regime Detection + Trend Strategy Design

**Fecha inicio:** 2025-12-28
**Objetivo:** Implementar Regime Detector y diseñar estrategia Trend-Following
**Timeline:** 7 días (Día 1-7)

---

## 🎯 Objetivos de la Semana

1. ✅ Implementar algoritmo Regime Detection
2. ✅ Testear detector con datos históricos
3. ✅ Diseñar lógica Trend-Following completa
4. ✅ Implementar código Trend strategy
5. ✅ Backtest Trend strategy en 2020-2021
6. ✅ Validar criterios de éxito

**Meta final:** Trend strategy funcionando en bull parabólico (+30-50% profit en 2020-2021)

---

## 📋 Checklist Día por Día

### ✅ Día 1 (2025-12-28) - COMPLETADO

**Tareas:**
- [x] Analizar fallo v10.0-ROBUST
- [x] Diseñar master plan v11.0-UNIVERSAL
- [x] Crear estructura de archivos
- [x] Implementar Regime Detector base
- [x] Revertir Jesse a v9.3-RSI36

**Archivos creados:**
- [HYBRID_SYSTEM_MASTER_PLAN.md](HYBRID_SYSTEM_MASTER_PLAN.md) - Plan completo 3-4 semanas
- [code/utils/regime_detector.py](code/utils/regime_detector.py) - Detector de régimen
- [V10_FAILURE_ANALYSIS.md](V10_FAILURE_ANALYSIS.md) - Análisis causa raíz

**Archivos modificados:**
- [code/strategies/Multitimeframe/__init__.py](code/strategies/Multitimeframe/__init__.py) - Revertido a v9.3

**Decisiones clave:**
- ✅ Mantener v9.3 en paper trading (sin cambios)
- ✅ Crear sistema híbrido con dual-strategy + regime detection
- ✅ Timeline: 3-4 semanas para v11.0-UNIVERSAL completo

**Estado:** ✅ DÍA 1 COMPLETADO

---

### ⏳ Día 2 (2025-12-29) - EN PROGRESO

**Tareas:**
- [ ] Implementar test del Regime Detector con datos históricos
- [ ] Validar accuracy >80% en clasificación
- [ ] Crear función de testing histórico
- [ ] Documentar resultados del detector

**Archivos a crear:**
- `REGIME_DETECTOR_TESTS.md` - Resultados de testing
- `test_regime_detector.py` - Script de testing

**Criterios de éxito:**
- ✅ Detector clasifica correctamente 2020 como 'parabolic'
- ✅ Detector clasifica correctamente 2022-2024 como 'volatile'
- ✅ Accuracy >80% en clasificación manual

**Estado:** ⏳ PENDIENTE

---

### ⏳ Día 3 (2025-12-30) - PENDIENTE

**Tareas:**
- [ ] Diseñar lógica completa Trend-Following
- [ ] Implementar score system para breakouts
- [ ] Crear función `should_long_trend()`
- [ ] Crear función `should_short_trend()`

**Archivos a crear:**
- `TREND_STRATEGY_DESIGN.md` - Documentación técnica
- Empezar código en nueva estrategia

**Criterios:**
- Score system claramente definido
- Entrada en breakouts (NO dips)
- Lógica diferente a Mean-Reversion

**Estado:** ⏳ PENDIENTE

---

### ⏳ Día 4 (2025-12-31) - PENDIENTE

**Tareas:**
- [ ] Implementar función `update_position_trend()` (trailing stop)
- [ ] Crear clase completa `TrendFollowing` en Jesse
- [ ] Code review y debugging
- [ ] Preparar configuración de backtest

**Archivos a crear:**
- `code/strategies/TrendFollowing/__init__.py` - Estrategia completa

**Criterios:**
- Trailing stop 2R implementado
- TP 6R implementado
- BE 3R implementado

**Estado:** ⏳ PENDIENTE

---

### ⏳ Día 5-7 (2026-01-01 a 01-03) - PENDIENTE

**Tareas:**
- [ ] Backtest Trend strategy 2020-2021 (bull parabólico)
- [ ] Analizar resultados vs criterios
- [ ] Iterar parámetros si necesario
- [ ] Documentar resultados finales

**Archivos a crear:**
- `TREND_BACKTEST_2020-2021.md` - Resultados completos

**Criterios de éxito (Test 1):**
- ✅ Net Profit > +30%
- ✅ Win Rate > 18%
- ✅ Max DD < -40%
- ✅ Calmar > 0.8

**Decisión checkpoint:**
- **SI pasa 4/4:** ✅ Continuar a Semana 2 (Integración)
- **NO pasa:** ⚠️ Iterar diseño Trend strategy

**Estado:** ⏳ PENDIENTE

---

## 📊 Progreso General Semana 1

```
Días completados: 1 / 7 (14%)

[█░░░░░░] 14%

Tareas completadas: 5 / 18 (28%)
```

---

## 🔧 Componentes Implementados

### 1. Regime Detector ✅

**Estado:** Implementado (básico)

**Archivo:** `code/utils/regime_detector.py`

**Funcionalidad:**
```python
detector = RegimeDetector()
regime = detector.detect(candles_15m, candles_1h, candles_4h, candles_1d)
# Returns: 'parabolic' | 'volatile' | 'ranging'
```

**Indicadores usados:**
- ADX 4H (tendencia)
- RSI 1D (momentum)
- ATR % 15M (volatilidad)
- EMA 50/200 4H (tendencia)
- Momentum 30 días

**Thresholds:**
- Parabolic: ADX>30, EMA_diff>3%, RSI>60, Momentum>15%
- Volatile: ATR>0.8%, ADX>15, Momentum<15%
- Ranging: ADX<15, ATR<0.4%, Momentum<5%

**Próximo paso:** Testing con datos históricos (Día 2)

---

### 2. Mean-Reversion Strategy (v9.3) ✅

**Estado:** Revertido y funcionando

**Archivo:** `code/strategies/Multitimeframe/__init__.py`

**Parámetros:**
```python
rsi_long_threshold = 36
rsi_short_threshold = 64
break_even_ratio = 1.35
tp_final_ratio = 3.0
minimum_score = 3
```

**Performance validada:**
- 2023-2025: +110.68%, Calmar 1.55 🏆

**Uso:** Activa en régimen 'volatile'

---

### 3. Trend-Following Strategy ⏳

**Estado:** PENDIENTE (Día 3-4)

**Archivo:** `code/strategies/TrendFollowing/__init__.py` (a crear)

**Diseño planeado:**
- Entrada: Breakouts de resistencia
- Score: MACD + Momentum + Volumen + ADX
- Gestión: Trailing stop 2R, TP 6R, BE 3R
- Uso: Activa en régimen 'parabolic'

**Próximo paso:** Implementar (Día 3-4)

---

## 📝 Notas de Desarrollo

### Decisiones Técnicas

**1. Por qué usar módulo separado para Regime Detector:**
- ✅ Reutilizable en ambas strategies
- ✅ Testing independiente más fácil
- ✅ Fácil de ajustar thresholds sin tocar strategies

**2. Por qué mantener v9.3 separado de Trend:**
- ✅ Lógica completamente diferente (mean-reversion vs trend-following)
- ✅ Parámetros diferentes
- ✅ Permite testing individual de cada estrategia

**3. Timeline conservador (7 días para Semana 1):**
- ✅ Buffer para debugging
- ✅ Tiempo para iteración si detector falla
- ✅ Testing exhaustivo de Trend strategy

---

### Riesgos Identificados

**Riesgo 1: Detector accuracy baja (<80%)**
- **Probabilidad:** Media
- **Impacto:** Alto - Sistema hybrid no funcionaría
- **Mitigación:** Testing exhaustivo Día 2, iterar thresholds si necesario

**Riesgo 2: Trend strategy falla en 2020-2021**
- **Probabilidad:** Media
- **Impacto:** Alto - Volver a diseño
- **Mitigación:** Diseño cuidadoso, basado en research de breakout strategies

**Riesgo 3: Overtrading en transitions de régimen**
- **Probabilidad:** Baja
- **Impacto:** Medio - Fees altos
- **Mitigación:** Cooldown entre cambios de régimen (a implementar)

---

## 🎯 Metas de Checkpoints

### Checkpoint 1 (Fin Día 2)
**Pregunta:** ¿Regime detector funciona?
- **SI:** Continuar a Día 3 (diseño Trend)
- **NO:** Iterar thresholds, repetir testing

### Checkpoint 2 (Fin Día 4)
**Pregunta:** ¿Código Trend strategy compilado y sin errores?
- **SI:** Continuar a Día 5 (backtesting)
- **NO:** Debugging, fix errores

### Checkpoint 3 (Fin Día 7 - FIN SEMANA 1)
**Pregunta:** ¿Trend strategy pasa criterios 2020-2021?
- **SI:** ✅ SEMANA 1 COMPLETADA → Continuar a Semana 2
- **NO:** ⚠️ Iterar diseño, extender Semana 1

---

## 📁 Estructura de Archivos Actual

```
TradingBot_Project/
├── code/
│   ├── strategies/
│   │   ├── Multitimeframe/
│   │   │   └── __init__.py  ✅ (v9.3 - Mean-Reversion)
│   │   └── TrendFollowing/
│   │       └── __init__.py  ⏳ (PENDIENTE - Día 3-4)
│   └── utils/
│       └── regime_detector.py  ✅ (Implementado)
│
├── HYBRID_SYSTEM_MASTER_PLAN.md  ✅
├── V10_FAILURE_ANALYSIS.md  ✅
├── V10_BACKTEST_RESULTS.md  ✅
├── SEMANA1_PROGRESS.md  ✅ (este archivo)
│
└── (a crear):
    ├── REGIME_DETECTOR_TESTS.md  ⏳ (Día 2)
    ├── TREND_STRATEGY_DESIGN.md  ⏳ (Día 3)
    └── TREND_BACKTEST_2020-2021.md  ⏳ (Día 5-7)
```

---

## 💡 Ideas y Mejoras Futuras

1. **Regime confidence score:** Agregar nivel de confianza a la detección
2. **Transition smoothing:** Evitar cambios bruscos entre strategies
3. **Hybrid mode:** Permitir ambas strategies activas con diferente % de capital
4. **Alert system:** Notificar cambios de régimen

---

## 🚀 Próxima Acción Inmediata

**Mañana (Día 2 - 2025-12-29):**

1. Crear datos sintéticos históricos para testing
2. Implementar función `test_historical_accuracy()`
3. Clasificar manualmente periodos históricos:
   - 2020 Q1-Q4: Parabolic
   - 2021 Q1-Q2: Parabolic
   - 2021 Q3-Q4: Volatile
   - 2022 Q1-Q4: Volatile
   - 2023 Q1-Q4: Volatile/Parabolic (mixto)
   - 2024 Q1-Q4: Volatile
4. Correr detector y calcular accuracy
5. Ajustar thresholds si accuracy <80%

**Tiempo estimado:** 2-3 horas

---

**Última actualización:** 2025-12-28 23:45
**Status general:** ✅ Día 1 completado, en track para Semana 1
**Próximo milestone:** Regime Detector testing (Día 2)
