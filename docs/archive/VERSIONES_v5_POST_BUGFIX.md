# Versiones Disponibles - Post Bug Fix Divergencias

**Fecha**: 2025-10-26
**Bug corregido**: Detección de divergencias RSI (líneas 472 y 527)

Todas las versiones ahora tienen el bug de divergencias CORREGIDO y pueden detectar divergencias correctamente.

---

## v5.2-FIXED - PROFESSIONAL TRADER ⭐ (ACTUAL EN SERVIDOR)

**Filosofía**: Quality over Quantity - Trading profesional con máxima selectividad

### Filtros activos (6 filtros AND):
1. ✅ Divergencias RSI (alcista/bajista) - **BUG CORREGIDO**
2. ✅ **2R mínimo disponible** (Regla profesional obligatoria)
3. ✅ RSI extremo (<40 LONG, >60 SHORT)
4. ✅ Tendencia confirmada (precio + EMA50 vs EMA200)
5. ✅ Volatilidad ≥ 0.3%
6. ✅ Volumen confirmado (>1.2x promedio)

### Parámetros:
- Cooldown: 60 minutos
- Leverage: 20x
- Risk: 1.5% por trade
- Daily loss limit: 3%
- TPs: 1.2R (50%), 2.5R (30%), 4R (20%)

### Expectativa:
- **Trades**: 30-80 en 3 años (10-27/año)
- **Win Rate**: 55-60%+
- **Profit Factor**: >1.8
- **Trades/semana**: 0.5-1.5

### Ventajas:
- ✅ Cumple TODAS las reglas profesionales investigadas
- ✅ Solo abre trades con 2R garantizado
- ✅ Filtros múltiples = alta calidad
- ✅ Win rate esperado más alto

### Desventajas:
- ⚠️ Puede generar MUY pocos trades
- ⚠️ Requiere paciencia
- ⚠️ Si genera <30 trades, difícil evaluar estadísticamente

---

## v5.3-FIXED - BALANCED PROFESSIONAL

**Filosofía**: Balance entre calidad y frecuencia

### Filtros activos (4 filtros AND):
1. ✅ Divergencias RSI - **BUG CORREGIDO**
2. ✅ **2R mínimo disponible**
3. ✅ Tendencia confirmada (precio + EMA50 vs EMA200)
4. ✅ Volatilidad ≥ 0.3%

### Eliminado vs v5.2:
- ❌ RSI extremo obligatorio
- ❌ Volumen confirmado

### Parámetros:
- Cooldown: 60 minutos
- Leverage: 20x
- Risk: 1.5% por trade
- Daily loss limit: 3%
- TPs: 1.2R (50%), 2.5R (30%), 4R (20%)

### Expectativa:
- **Trades**: 50-120 en 3 años (17-40/año)
- **Win Rate**: 52-57%
- **Profit Factor**: 1.5-1.8
- **Trades/semana**: 1-2

### Ventajas:
- ✅ Mantiene regla 2R profesional
- ✅ Más trades que v5.2
- ✅ Balance calidad/frecuencia

### Desventajas:
- ⚠️ Win rate puede ser ligeramente menor
- ⚠️ Menos selectivo que v5.2

---

## v5.5 - SIMPLE DIVERGENCES

**Filosofía**: Maximum Frequency - Evaluar win rate puro de divergencias

### Filtros activos (2 filtros AND):
1. ✅ Divergencias RSI - **BUG CORREGIDO**
2. ✅ Tendencia simple (solo EMA50 vs EMA200)

### Eliminado vs v5.2:
- ❌ 2R mínimo obligatorio
- ❌ RSI extremo
- ❌ Precio vs EMA200
- ❌ Volatilidad mínima
- ❌ Volumen confirmado

### Parámetros:
- Cooldown: 60 minutos
- Leverage: 20x
- Risk: 1.5% por trade
- Daily loss limit: 3%
- TPs: 1.2R (50%), 2.5R (30%), 4R (20%)

### Expectativa:
- **Trades**: 100-200 en 3 años (33-67/año)
- **Win Rate**: 50-55%
- **Profit Factor**: 1.3-1.6
- **Trades/semana**: 2-4

### Ventajas:
- ✅ MÁXIMA frecuencia de trades
- ✅ Evalúa win rate puro de divergencias
- ✅ Más datos para análisis estadístico
- ✅ Divergencias ocurren en pullbacks (no requiere precio extremo)

### Desventajas:
- ⚠️ Win rate probablemente más bajo
- ⚠️ Puede abrir trades sin 2R disponible
- ⚠️ Menos selectivo = más trades mediocres

---

## COMPARACIÓN RÁPIDA

| Métrica | v5.2-FIXED | v5.3-FIXED | v5.5 Simple |
|---------|------------|------------|-------------|
| **Filtros AND** | 6 | 4 | 2 |
| **Trades esperados** | 30-80 | 50-120 | 100-200 |
| **Win Rate esperado** | 55-60% | 52-57% | 50-55% |
| **Profit Factor** | >1.8 | 1.5-1.8 | 1.3-1.6 |
| **Filosofía** | Quality | Balance | Frequency |
| **2R obligatorio** | ✅ Sí | ✅ Sí | ❌ No |
| **RSI extremo** | ✅ Sí | ❌ No | ❌ No |
| **Volumen** | ✅ Sí | ❌ No | ❌ No |
| **Trades/semana** | 0.5-1.5 | 1-2 | 2-4 |

---

## RECOMENDACIÓN DE TESTING

### Orden sugerido:

1. **v5.2-FIXED PRIMERO** ⭐
   - La más profesional
   - Si genera 30-80 trades con 55%+ → PERFECTA
   - Si genera <30 trades → Probar v5.5

2. **v5.5 Simple SEGUNDO** (si v5.2 muy restrictiva)
   - Máxima frecuencia
   - Evalúa win rate puro de divergencias
   - Si genera 100-200 trades con 50-55% → ACEPTABLE

3. **v5.3-FIXED TERCERO** (si ninguna anterior funciona)
   - Punto medio
   - Solo si v5.2 muy restrictiva y v5.5 muy permisiva

---

## CÓMO CAMBIAR ENTRE VERSIONES

Todas las versiones están documentadas en este archivo. Para cambiar, necesitas:

1. **Modificar `should_long()` y `should_short()`**
2. **Limpiar caché** (`__pycache__`, `.pyc`, Redis)
3. **WSL shutdown**
4. **Reiniciar Jesse**

**Claude puede hacer esto automáticamente en 2-3 minutos.**

---

## CRITERIOS DE ÉXITO

### v5.2-FIXED será exitosa si:
- ✅ Genera 30-80 trades en 3 años
- ✅ Win rate ≥ 55%
- ✅ Profit Factor > 1.5
- ✅ Max Drawdown < 20%

### v5.5 Simple será exitosa si:
- ✅ Genera 100-200 trades en 3 años
- ✅ Win rate ≥ 50%
- ✅ Profit Factor > 1.3
- ✅ Max Drawdown < 25%

### Cualquier versión será FALLIDA si:
- ❌ Genera 0 trades (divergencias no funcionan)
- ❌ Win rate < 45%
- ❌ Profit Factor < 1.2
- ❌ Max Drawdown > 30%

---

**Versión actual en servidor**: v5.2-FIXED
**Fecha**: 2025-10-26
**Bug divergencias**: CORREGIDO ✅
