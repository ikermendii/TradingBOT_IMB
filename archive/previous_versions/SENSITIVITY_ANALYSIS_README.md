# 🔬 Sensitivity Analysis - v9.1-TP1

**Fecha**: 2025-12-27
**Versión base**: v9.1-TP1 (primera versión rentable: +68.32% en periodo completo)
**Periodo de validación**: 2024-07-01 a 2025-10-17 (walk-forward)

---

## 🎯 Objetivo

Mejorar el +2.36% profit del walk-forward test mediante optimización de parámetros críticos.

**Parámetros actuales (v9.1-TP1)**:
- Break-even: 1.25R
- RSI threshold LONG: 38 (SHORT: 62)
- TP final: 3.0R

**Resultados actuales (walk-forward)**:
- 186 trades
- 21.51% win rate
- +2.36% net profit
- -32.33% max drawdown

---

## 📊 Metodología: Optimización por Fases

En lugar de probar todas las combinaciones (80 backtests), usamos enfoque **secuencial**:

### Fase 1: Break-Even Optimization
**Objetivo**: Encontrar el punto óptimo para mover SL a break-even

**Valores a testear**: [1.2R, 1.25R, 1.3R, 1.35R]

**Hipótesis**:
- 1.25R actual puede ser demasiado temprano (limita winners)
- O muy tardío (expone a reversiones)

**Mantener fijo**: RSI=38, TP=3.0R

---

### Fase 2: RSI Threshold Optimization
**Objetivo**: Ajustar sensibilidad de entradas RSI

**Valores a testear**: [36, 37, 38, 39, 40]

**Hipótesis**:
- RSI 38 puede estar perdiendo entradas tempranas (36-37)
- O permitiendo entradas prematuras (39-40)

**Usar**: Mejor break-even de Fase 1
**Mantener fijo**: TP=3.0R

**Nota**: RSI SHORT se ajusta simétricamente (100 - RSI_LONG)
- Si RSI LONG = 36 → RSI SHORT = 64
- Si RSI LONG = 40 → RSI SHORT = 60

---

### Fase 3: Take Profit Optimization
**Objetivo**: Optimizar objetivo de profit final

**Valores a testear**: [2.5R, 3.0R, 3.5R, 4.0R]

**Hipótesis**:
- TP 3.0R puede ser muy conservador (cierra winners prematuros)
- O muy ambicioso (deja profit sobre la mesa en reversiones)

**Usar**: Mejor break-even + RSI de Fases 1 y 2

---

## 🔢 Total de Backtests

**Enfoque Full Grid** (todas combinaciones):
- 4 BE × 5 RSI × 4 TP = **80 backtests**
- Tiempo estimado: 4-5 horas

**Enfoque por Fases** (secuencial):
- Fase 1: 4 backtests
- Fase 2: 5 backtests
- Fase 3: 4 backtests
- **Total: 13 backtests**
- Tiempo estimado: 45-60 minutos

**Ventaja**: Reduce tiempo 83% manteniendo eficacia de optimización

---

## 📈 Métricas a Evaluar

Para cada configuración, medimos:

1. **Net Profit %** (principal)
2. **Win Rate %**
3. **Max Drawdown %**
4. **Total Trades** (debe estar en 150-250 para walk-forward)
5. **R:R Ratio** (mantener >3.5)
6. **Expectancy** ($ por trade)
7. **Sharpe Ratio**

---

## ✅ Criterios de Éxito

Una configuración es **mejor que v9.1-TP1** si:

1. **Net Profit > 2.36%** (baseline walk-forward)
2. **Win Rate ≥ 21%** (no empeorar calidad)
3. **Max DD ≤ -35%** (no aumentar riesgo significativamente)
4. **Trades entre 150-250** (no overtrading ni muy restrictivo)
5. **R:R Ratio ≥ 3.5** (mantener calidad de wins)

**Ideal**:
- Net Profit > 5%
- Win Rate > 23%
- Max DD < -30%

---

## 🚀 Proceso de Ejecución

### Script: `quick_sensitivity.py`

**Funcionamiento**:
1. Crea backup de estrategia actual
2. **FASE 1**: Modifica break-even, ejecuta 4 backtests
3. Identifica mejor break-even
4. **FASE 2**: Con mejor BE, modifica RSI, ejecuta 5 backtests
5. Identifica mejor RSI
6. **FASE 3**: Con mejor BE+RSI, modifica TP, ejecuta 4 backtests
7. Identifica mejor configuración completa
8. Restaura estrategia original
9. Guarda resultados en `sensitivity_quick_results.json`

**Seguridad**:
- ✅ Backup automático antes de modificar
- ✅ Restauración automática al finalizar
- ✅ Restauración automática si hay error (try/finally)

---

## 📁 Outputs Generados

### `sensitivity_quick_results.json`
```json
{
  "timestamp": "2025-12-27T...",
  "period": "2024-07-01 to 2025-10-17",
  "baseline": {
    "breakeven": 1.25,
    "rsi": 38,
    "tp": 3.0
  },
  "optimal": {
    "breakeven": X.XX,
    "rsi": XX,
    "tp": X.X
  },
  "all_results": [...]
}
```

### Console Output
- Progreso en tiempo real de cada backtest
- Tabla comparativa al final
- Mejoras vs baseline
- Configuración óptima recomendada

---

## 🔍 Próximos Pasos Después del Análisis

### Si encontramos mejora significativa (>5% profit):
1. Implementar v9.2-OPTIMIZED con nuevos parámetros
2. Re-ejecutar backtest completo (2023-2025)
3. Validar en walk-forward nuevamente
4. Documentar en CHANGELOG.md

### Si mejora es marginal (2.5-5% profit):
1. Evaluar si vale la pena el cambio
2. Considerar otros parámetros (cooldown, min_atr_pct, score weights)
3. Analizar periodos específicos del equity curve

### Si no hay mejora:
1. Los parámetros v9.1-TP1 ya están bien calibrados
2. Buscar mejoras en otras áreas:
   - Filtros de volatilidad
   - Timeframes adicionales
   - Gestión de capital dinámica
   - Filtros de market regime

---

## 📝 Notas Técnicas

### Modificación de Estrategia

El script modifica 3 puntos en `__init__.py`:

**1. RSI Long Threshold**
```python
@property
def rsi_long_threshold(self):
    return 38  # Modificado a valor de test
```

**2. RSI Short Threshold**
```python
@property
def rsi_short_threshold(self):
    return 62  # Calculado como 100 - rsi_long
```

**3. Break-Even en update_position()**
```python
if r_ratio >= 1.25 and not self.vars['tp1_hit']:  # Modificado
    self.vars['tp1_hit'] = True
    self.vars['sl_price'] = self.vars['entry_price']
```

**4. TP Final en update_position()**
```python
if r_ratio >= 3.0:  # Modificado
    self.liquidate()
```

### Consideraciones

- Cada backtest toma ~2-4 minutos
- Total de 13 backtests = 26-52 minutos
- Jesse debe estar instalado en WSL
- Datos de BTC-USDT deben existir para 2024-2025

---

## 🎯 Expectativas Realistas

**Escenario Optimista**:
- Encontramos configuración con +8-10% profit en walk-forward
- Win rate sube a 24-25%
- Drawdown se mantiene en -30%

**Escenario Moderado**:
- Mejora a +4-6% profit
- Win rate sube a 22-23%
- Parámetros ligeramente mejores

**Escenario Conservador**:
- Mejora marginal a +3-4%
- v9.1-TP1 ya estaba bien calibrado
- Cambios mínimos justificables

**Peor Caso**:
- No hay mejora significativa
- Parámetros actuales son óptimos
- Necesitamos buscar mejoras en otro lado (ej: score system, filtros)

---

**Análisis iniciado**: 2025-12-27
**Estado**: En ejecución (13 backtests)
**Tiempo estimado**: 45-60 minutos
