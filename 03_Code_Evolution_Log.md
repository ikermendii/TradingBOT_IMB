# Log de Evolución del Código

## Formato de Entrada:

Cada cambio significativo en el código debe documentarse así:

---

### [FECHA] - [VERSIÓN] - [DESCRIPCIÓN CORTA]

**Cambios realizados**:
- Cambio 1
- Cambio 2
- Cambio 3

**Razón**:
[Por qué se hizo este cambio]

**Resultados**:
[Mejora/Empeora - Métricas clave afectadas]

**Código modificado**:
```python
# Pegar snippet del cambio clave aquí
```

**Ubicación archivo**: `code/strategies/vX_nombre.py`

---

## EJEMPLO DE ENTRADA:

### 2024-01-15 - v2.0 - Añadida detección de divergencias

**Cambios realizados**:
- Implementada función `check_bullish_divergence()`
- Implementada función `check_bearish_divergence()`
- Añadido lookback period de 20 velas
- Integrado filtro de divergencias en `should_long()` y `should_short()`

**Razón**:
Mejorar precisión de entradas filtrando solo operaciones con divergencias RSI confirmadas, reduciendo señales falsas y aumentando calidad de trades.

**Resultados**:
✅ Win rate aumentó de 51% a 58%
✅ Profit factor mejoró de 1.2 a 1.6
✅ Trades reducidos de 145 a 68 (mayor selectividad)
✅ Drawdown mejoró de -18.5% a -12.3%

**Código modificado**:
```python
def check_bullish_divergence(self):
    """
    Buscar divergencia alcista:
    - Precio hace mínimo más bajo
    - RSI hace mínimo más alto
    """
    indicators = self.indicators(self.candles)
    current_price = self.close
    current_rsi = indicators['rsi']
    
    for i in range(5, self.lookback_period):
        past_price = self.candles[-i, 3]  # Low
        past_rsi = indicators['rsi'][-i]
        
        if current_price < past_price and current_rsi > past_rsi:
            return True
    
    return False
```

**Ubicación archivo**: `code/strategies/v2_divergence.py`

---

## [AÑADIR NUEVAS VERSIONES AQUÍ]
### 2025-10-25 - v1.0 - Estrategia Multitimeframe inicial (SPOT)

**Cambios realizados**:
- Estrategia inicial con divergencias RSI/MACD
- Configurado para Binance Spot
- Stop-loss manual (sin self.stop_loss automático)
- Take profits escalonados: TP1 (1.5R 50%), TP2 (3R 30%)
- RSI < 35 para LONG, RSI > 65 para SHORT
- Filtro de tendencia: precio > EMA 200 Y EMA 50 > EMA 200

**Razón**:
Implementar estrategia multi-timeframe avanzada con filtros de divergencias para mejorar precisión de entradas.

**Resultados**:
❌ Solo 2 trades en 3 años (demasiado restrictivo)
❌ 0% win rate
❌ Problema: SPOT no permite SHORT

**Código clave**:


**Ubicación**: 

---

### 2025-10-25 - v2.0 - Migración a Binance Futures

**Cambios realizados**:
- Cambio de Binance Spot → Binance Futures
- Reactivación de should_short() y go_short()
- Implementado self.stop_loss con tupla (qty, price) para FUTURES
- Permitir operaciones LONG y SHORT

**Razón**:
SPOT trading limita la estrategia a solo LONG. Futures permite operar en ambas direcciones para aprovechar mercados alcistas y bajistas.

**Resultados**:
✅ SHORT activo (50% LONG / 50% SHORT)
✅ 4 trades vs 2 trades anteriores
❌ Sigue siendo muy restrictivo (solo 4 trades en 3 años)
❌ 0% win rate

**Código clave**:


**Ubicación**: , 

---

### 2025-10-25 - v3.0 - Condiciones relajadas

**Cambios realizados**:
- RSI umbral LONG: < 35 → < 45
- RSI umbral SHORT: > 65 → > 55
- Tiempo entre señales: 4h → 30 minutos
- Filtro tendencia simplificado: solo EMA 50 vs EMA 200 (sin requisito precio)

**Razón**:
Condiciones demasiado restrictivas generaban solo 4 trades en 3 años. Relajar umbrales para generar más oportunidades de trading.

**Resultados**:
✅ Condiciones más permisivas
❌ BUG CRÍTICO: trade se mantuvo abierto 1,017 días
❌ Ganancia de +493% pero completamente irrealista
❌ Problema: 20% final de posición nunca se cierra

**Código clave**:


**Ubicación**: 

---

### 2025-10-25 - v3.1 - Fix: TP3 implementado (EN PRUEBAS)

**Cambios realizados**:
- Añadido TP3 en 6R que cierra el 20% final con self.liquidate()
- Estructura completa: TP1(1.5R, 50%) → TP2(3R, 30%) → TP3(6R, 20%)
- Trailing stop dinámico entre TP2 y TP3

**Razón**:
Bug detectado: el 20% restante nunca se cerraba, causando trades de 2+ años. TP3 asegura cierre completo de posición.

**Resultados**:
❌ Backtest negativo (ver 04_Backtest_results.md v3.1)
- 575 trades, Win rate 20%
- Net Profit -41.16%, Max DD -46.11%
- Comisiones altas ($3,199.55) → sobreoperación

**Código clave**:


**Ubicación**:  (línea ~210)

---

## [VERSIONES FUTURAS AQUÍ]
### 2025-10-25 - v3.2 - Reducción de sobreoperación y filtros (EN PRUEBAS)

**Cambios realizados**:
- Cooldown entre señales: 30 min → 90 min.
- RSI: LONG < 40 (antes 45), SHORT > 60 (antes 55).
- Filtro de tendencia más estricto: precio y EMA50 respecto a EMA200.
- Requerir confirmación de volumen y volatilidad mínima ATR/close ≥ 0.3%.
- Límite de entradas por día: 8 (reset diario automático).
- Logs al alcanzar TP1/TP2/TP3 para trazabilidad.

**Razón**:
Reducir churn y comisiones, aumentar selectividad de señales y calidad de entradas para mejorar win rate/expectancy.

**Resultados**:
⏳ Pendiente de backtest v3.2.

**Código clave**:
```python
# Nuevos @property de control (cooldown, thresholds, min_atr_pct, max_daily_trades)
# Filtros en should_long/should_short: tendencia, volatilidad, volumen
# Guardián de límite diario: _can_trade_today()
```

**Ubicación**: `code/strategies/Multitimeframe/__init__.py`


### 2025-10-25 - v4.0 HÍBRIDA - Gestión de riesgo inteligente + Balance de condiciones

**Cambios realizados**:
- **LÍMITE DIARIO POR PÉRDIDA** (no por número): Bot se detiene si pierde 3% del capital en un día
- RSI híbrido: LONG < 42, SHORT > 58 (balance entre permisivo y restrictivo)
- Cooldown: 60 minutos entre señales (balance)
- Filtro de tendencia ESTRICTO: Precio Y EMA50 respecto a EMA200
- Filtro de volumen: Obligatorio (volumen > promedio)
- Mantenido: initial_risk_distance, TP3 en 6R
- Eliminado: Prints de debug, límite numérico de trades

**Razón**:
Combinar lo mejor de ambas aproximaciones:
1. Copilot tenía buena idea con filtros estrictos pero límite numérico muy bajo
2. Versión anterior era muy permisiva (575 trades, -41%)
3. Híbrida: Filtros de calidad + libertad para operar si va bien

**Fórmula de Límite Diario**:


**Parámetros finales v4.0**:
- RSI LONG: < 42
- RSI SHORT: > 58  
- Cooldown: 60 min
- Pérdida diaria máx: 3%
- Filtro tendencia: precio Y EMA50 vs EMA200
- Filtro volumen: SÍ
- TP1: 1.5R (50%), TP2: 3R (30%), TP3: 6R (20%)

**Resultados**:
⏳ PENDIENTE - Ejecutar backtest

**Ubicación**: 



---

### 2025-10-25 - v5.0 PHASE 2 - DIVERGENCIAS RSI + LEVERAGE 20x

**Cambios realizados**:
- ✅ **ACTIVADAS DIVERGENCIAS RSI**: _bullish_divergence() y _bearish_divergence() como SEÑAL PRINCIPAL
- ✅ **LEVERAGE 20x**: Configurado apalancamiento en futuros
- ✅ **Cálculo de posición actualizado**: Usa leverage 20x manteniendo riesgo 1.5% sobre balance real
- ✅ **RSI relajado**: LONG < 45 (era 42), SHORT > 55 (era 58) → Más permisivo para capturar divergencias
- ✅ **Arquitectura PHASE 2**: 
  - Divergencias = Señal principal
  - Tendencia/volumen/volatilidad = Filtros de contexto
  - MACD removido de condiciones (conflicto con divergencias)

**Razón**:
v4.0 fue solo el "esqueleto" (PHASE 1) sin su "cerebro" principal. Las divergencias RSI son la ESENCIA de la estrategia Multitimeframe. 

Problemas v4.0:
- Solo 6 trades en 3 años (filtros demasiado restrictivos sin señal principal)
- Win rate 16.67% (sin divergencias, trades de baja calidad)
- 100% shorts (RSI < 42 demasiado extremo en mercado alcista)

Solución v5.0:
- Divergencias detectan reversiones de alta probabilidad
- RSI relajado (45/55) permite capturar más oportunidades válidas
- Leverage 20x aumenta rentabilidad manteniendo riesgo controlado al 1.5%

**Parámetros v5.0**:
- **Señal principal**: Divergencias RSI (alcista/bajista)
- **Leverage**: 20x
- **RSI**: LONG < 45, SHORT > 55
- **Cooldown**: 60 minutos
- **Risk**: 1.5% del balance real (sin apalancar)
- **Daily loss limit**: 3% pérdida máxima
- **Filtros**: Tendencia + Volumen + Volatilidad (ATR ≥ 0.3%)
- **TPs**: 1.5R (50%), 3R (30%), 6R (20%)

**Código clave**:


**Expectativa de resultados**:
- Trades esperados: 20-40 en 3 años (calidad > cantidad)
- Win rate objetivo: 50-60% (divergencias tienen alta precisión)
- Profit factor esperado: >1.5
- Drawdown objetivo: <15%
- Return anual objetivo: 30-80% (con leverage 20x)

**Comparación con v4.0**:
| Métrica | v4.0 | v5.0 (esperado) |
|---------|------|-----------------|
| Señal principal | RSI extremo | Divergencias RSI |
| Trades/año | 2 | 10-15 |
| Win rate | 16.67% | 50-60% |
| Leverage | 1x | 20x |
| Filtros | Muy restrictivos | Balanceados |

**Resultados**:
⏳ PENDIENTE - Ejecutar backtest v5.0

**Ubicación**:  (543 líneas)



---

### 2025-10-25 - v5.0 PHASE 2 - DIVERGENCIAS RSI + LEVERAGE 20x

**Cambios realizados**:
- ACTIVADAS DIVERGENCIAS RSI: _bullish_divergence() y _bearish_divergence() como SEÑAL PRINCIPAL
- LEVERAGE 20x: Configurado apalancamiento en futuros
- Cálculo de posición actualizado: Usa leverage 20x manteniendo riesgo 1.5% sobre balance real
- RSI relajado: LONG < 45 (era 42), SHORT > 55 (era 58) para capturar más divergencias
- Arquitectura PHASE 2: Divergencias = señal principal, otros = filtros de contexto
- MACD removido de condiciones (conflicto con divergencias)

**Razón**:
v4.0 fue solo el "esqueleto" (PHASE 1) sin su "cerebro" principal. Las divergencias RSI son la ESENCIA de la estrategia Multitimeframe.

Problemas v4.0:
- Solo 6 trades en 3 años (filtros demasiado restrictivos sin señal principal)
- Win rate 16.67% (sin divergencias, trades de baja calidad)
- 100% shorts (RSI < 42 demasiado extremo en mercado alcista)

Solución v5.0:
- Divergencias detectan reversiones de alta probabilidad
- RSI relajado (45/55) permite capturar más oportunidades válidas
- Leverage 20x aumenta rentabilidad manteniendo riesgo controlado al 1.5%

**Parámetros v5.0**:
- Señal principal: Divergencias RSI (alcista/bajista)
- Leverage: 20x
- RSI: LONG < 45, SHORT > 55
- Cooldown: 60 minutos
- Risk: 1.5% del balance real (sin apalancar)
- Daily loss limit: 3% pérdida máxima
- Filtros: Tendencia + Volumen + Volatilidad (ATR >= 0.3%)
- TPs: 1.5R (50%), 3R (30%), 6R (20%)

**Expectativa de resultados**:
- Trades esperados: 20-40 en 3 años (calidad > cantidad)
- Win rate objetivo: 50-60% (divergencias tienen alta precisión)
- Profit factor esperado: >1.5
- Return anual objetivo: 30-80% (con leverage 20x)

**Resultados**:
PENDIENTE - Ejecutar backtest v5.0

**Ubicación**: `code/strategies/Multitimeframe/__init__.py` (543 líneas)
