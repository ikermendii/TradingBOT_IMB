# BUG CRÍTICO - Detección de Divergencias

**Fecha**: 2025-10-26
**Versiones afectadas**: v5.0, v5.1, v5.2, v5.3, v5.4
**Severidad**: CRÍTICA - Impedía completamente la detección de divergencias

---

## Descripción del Bug

Las funciones `_bullish_divergence()` y `_bearish_divergence()` tenían un bug que impedía la correcta detección de divergencias RSI, causando que TODAS las versiones generaran **0 trades**.

---

## Código Incorrecto (v5.0 - v5.4)

### Función `_bullish_divergence()` - LÍNEA 472:

```python
for i in range(5, min(lookback, len(self.candles) - 5)):
    idx = -(i + 1)

    if (self.candles[idx, 3] <= self.candles[idx-1, 3] and
        self.candles[idx, 3] <= self.candles[idx-2, 3] and
        self.candles[idx, 3] <= self.candles[idx+1, 3] and
        self.candles[idx, 3] <= self.candles[idx+2, 3]):

        # ❌ BUG: Guardaba el ARRAY completo de RSI, no el valor en ese índice
        price_lows.append((i, self.candles[idx, 3], rsi))
```

### Función `_bearish_divergence()` - LÍNEA 527:

```python
for i in range(5, min(lookback, len(self.candles) - 5)):
    idx = -(i + 1)

    if (self.candles[idx, 2] >= self.candles[idx-1, 2] and
        self.candles[idx, 2] >= self.candles[idx-2, 2] and
        self.candles[idx, 2] >= self.candles[idx+1, 2] and
        self.candles[idx, 2] >= self.candles[idx+2, 2]):

        # ❌ BUG: Guardaba el ARRAY completo de RSI, no el valor en ese índice
        price_highs.append((i, self.candles[idx, 2], rsi))
```

---

## Causa Raíz

Cuando se intentaba comparar los valores RSI para detectar divergencias:

```python
idx_recent, price_recent, rsi_recent = price_lows[j]
idx_old, price_old, rsi_old = price_lows[k]

# Esta comparación FALLABA porque rsi_recent y rsi_old eran ARRAYS, no números
if price_recent < price_old and rsi_recent > rsi_old:
    # Esta condición NUNCA era True
```

**Problema**:
- `rsi_recent` era un **numpy array completo** (ej: `[45.2, 44.8, 43.1, ...]`)
- `rsi_old` era otro **numpy array completo**
- Python **NO puede comparar arrays directamente** con `>`
- La comparación siempre retornaba `False` o causaba excepciones silenciosas
- **Resultado**: Las divergencias NUNCA se detectaban

---

## Código Corregido (v5.5+)

### Función `_bullish_divergence()` - CORREGIDA:

```python
for i in range(5, min(lookback, len(self.candles) - 5)):
    idx = -(i + 1)

    if (self.candles[idx, 3] <= self.candles[idx-1, 3] and
        self.candles[idx, 3] <= self.candles[idx-2, 3] and
        self.candles[idx, 3] <= self.candles[idx+1, 3] and
        self.candles[idx, 3] <= self.candles[idx+2, 3]):

        # ✅ CORREGIDO: Guarda el VALOR de RSI en ese índice específico
        price_lows.append((i, self.candles[idx, 3], rsi[idx]))
```

### Función `_bearish_divergence()` - CORREGIDA:

```python
for i in range(5, min(lookback, len(self.candles) - 5)):
    idx = -(i + 1)

    if (self.candles[idx, 2] >= self.candles[idx-1, 2] and
        self.candles[idx, 2] >= self.candles[idx-2, 2] and
        self.candles[idx, 2] >= self.candles[idx+1, 2] and
        self.candles[idx, 2] >= self.candles[idx+2, 2]):

        # ✅ CORREGIDO: Guarda el VALOR de RSI en ese índice específico
        price_highs.append((i, self.candles[idx, 2], rsi[idx]))
```

---

## Impacto

### Versiones Afectadas y Resultados:

| Versión | Trades | Win Rate | Causa |
|---------|--------|----------|-------|
| v5.0 | 0 | N/A | Bug divergencias + 7 filtros AND |
| v5.1 | 333 | 22.52% | **Bug divergencias NO afectó** (usaba OR logic con RSI/MACD) |
| v5.2 | 0 | N/A | Bug divergencias + 7 filtros AND + 2R check |
| v5.3 | 0 | N/A | Bug divergencias + 4 filtros AND + 2R check |
| v5.4 | 0 | N/A | Bug divergencias + 2 filtros AND |
| **v5.5** | **?** | **?** | **BUG CORREGIDO** ✅ |

**NOTA IMPORTANTE**: v5.1 generó 333 trades porque usaba **lógica OR** permitiendo trades sin divergencias (solo RSI o solo MACD). El bug existía pero no impedía trades porque las divergencias NO eran obligatorias.

---

## Lecciones Aprendidas

1. **Validación de tipos**: Cuando trabajas con numpy arrays, siempre indexar correctamente
2. **Testing incremental**: Debimos probar la detección de divergencias AISLADA primero
3. **Debugging**: 4 versiones con 0 trades debió activar debugging de divergencias inmediatamente
4. **Logs**: Agregar logging para confirmar cuando se detectan divergencias

---

## Solución Aplicada

**Versión corregida**: v5.5
**Cambio**: `rsi` → `rsi[idx]` en ambas funciones
**Impacto esperado**: Las divergencias ahora se detectarán correctamente
**Próximos pasos**: Re-testear versiones anteriores (v5.2, v5.3) con el bug corregido

---

## Recomendación

**VOLVER A TESTEAR v5.2 (Professional Trader con 2R)** ahora que el bug está corregido:
- v5.2 tenía la mejor lógica profesional (2R mínimo + RSI extremo + todos filtros alineados)
- El bug impedía que funcionara
- Con el bug corregido, v5.2 podría ser la mejor versión

---

**Responsable**: Claude Code AI Assistant
**Estado**: CORREGIDO en v5.5+
**Prioridad**: CRÍTICA - Bloqueo total de funcionalidad
