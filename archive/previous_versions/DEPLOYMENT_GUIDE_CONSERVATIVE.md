# 🚀 Deployment Guide - v9.3-RSI36 (CONSERVADOR)

**Versión:** v9.3-RSI36
**Estado:** ELITE en 2022-2025 (Calmar 1.55, +110.68% profit)
**Advertencia:** Overfitting temporal detectado - Falla en régimen 2020-2021

---

## ⚠️ ADVERTENCIA CRÍTICA

**v9.3-RSI36 está optimizado específicamente para el régimen de mercado 2022-2025 (post-crash, alta volatilidad).**

✅ **Excelente en:** Bull/bear volátiles, crashes, alta volatilidad (ATR >0.6%)
❌ **FALLA en:** Bull parabólico 2020-2021 style (baja volatilidad, tendencias largas)

**Este deployment es CONSERVADOR con circuit breakers estrictos para detectar cambio de régimen.**

---

## 📋 Pre-requisitos OBLIGATORIOS

### 1. ✅ Completar ANTES de Deployar

- [ ] Leer y entender [CRITICAL_FINDING_2020-2021.md](CRITICAL_FINDING_2020-2021.md)
- [ ] Aceptar riesgo de fallo si mercado cambia a régimen parabólico
- [ ] Tener plan de respuesta si circuit breakers se activan
- [ ] Capital que puedes permitirte perder COMPLETAMENTE
- [ ] Tiempo para monitoring DIARIO obligatorio

### 2. Infraestructura

- [ ] VPS con uptime >99.9% (recomendado: Digital Ocean, AWS, Vultr)
- [ ] Conexión estable (backup 4G/5G opcional)
- [ ] Jesse framework actualizado
- [ ] Binance account con API keys
- [ ] Telegram bot para alertas (OBLIGATORIO)

---

## 🎯 Estrategia de Deployment (4 Fases)

### FASE 1: Paper Trading (OBLIGATORIO - 1-2 meses) 📝

**Objetivo:** Validar ejecución sin riesgo real

**Configuración:**
```python
# config.py
'exchanges': {
    'Binance Futures': {
        'testnet': True,  # ← PAPER TRADING
        'futures_leverage': 2,
        'fee': 0.04,  # 0.04% taker fee
    }
}
```

**Duración mínima:** 1 mes (2 meses recomendado)
**Capital virtual:** $10,000

**Checklist de validación:**
- [ ] Bot ejecuta trades sin errores
- [ ] Órdenes se llenan correctamente
- [ ] Stop loss funciona como esperado
- [ ] Take profit ejecuta en 3.0R
- [ ] Break-even activa en 1.35R
- [ ] Métricas dentro ±20% del backtest
- [ ] Sin crashes ni desconexiones >1h

**Criterio para pasar a Fase 2:**
- ✅ Paper trading 1+ mes exitoso
- ✅ Win rate 20-30% (±20% del baseline 25.14%)
- ✅ No errores críticos de ejecución
- ✅ Max DD <-30%

---

### FASE 2: Live Micro (1-2 meses) 💰

**Capital:** $500-1,000 (que puedas perder)
**Leverage:** 1x (conservador, NO 2x todavía)
**Risk per trade:** 1% del capital

**Configuración:**
```python
# config.py
'exchanges': {
    'Binance Futures': {
        'testnet': False,  # ← LIVE TRADING
        'futures_leverage': 1,  # Conservador
        'fee': 0.04,
    }
}
```

**Circuit Breakers Fase 2 (MÁS ESTRICTOS):**

🔴 **STOP INMEDIATO si:**
1. DD alcanza -15% (vs -20% normal)
2. 5+ errores de ejecución consecutivos
3. Losing streak >18 trades
4. Win rate cae <15% por 2 semanas

⚠️ **PAUSE y REVIEW si:**
1. DD alcanza -10%
2. 2 semanas consecutivas con profit negativo
3. Win rate <18% por 1 semana
4. Sharpe mensual <0.3

**Monitoring Diario OBLIGATORIO:**
- [ ] Check de trades ejecutados
- [ ] Equity curve trending up/down/flat
- [ ] Current drawdown level
- [ ] Win rate rolling 30 días
- [ ] **RÉGIMEN DE MERCADO** (ver abajo)

**Criterio para pasar a Fase 3:**
- ✅ 1-2 meses sin activar circuit breakers críticos
- ✅ Profit >0% o breakeven
- ✅ DD <-20%
- ✅ Régimen de mercado NO cambió

---

### FASE 3: Live Pequeño (3-6 meses) 📈

**Capital:** $5,000-10,000
**Leverage:** 2x (como en backtest)
**Risk per trade:** 1.5% del capital

**Configuración:**
```python
'exchanges': {
    'Binance Futures': {
        'testnet': False,
        'futures_leverage': 2,  # Según backtest
    }
}
```

**Circuit Breakers Fase 3 (NORMALES):**

🔴 **STOP INMEDIATO si:**
1. DD alcanza -20%
2. Losing streak >20 trades
3. 3 meses consecutivos con profit negativo
4. **⚠️ CAMBIO DE RÉGIMEN detectado** (ver sección abajo)

⚠️ **PAUSE y REVIEW si:**
1. DD alcanza -15%
2. Win rate <20% por 1 mes
3. Sharpe mensual <0.5 por 2 meses
4. Volatilidad (ATR) cae <0.4% por 3 semanas

**Monitoring:**
- [ ] Diario: Equity, DD, alertas
- [ ] Semanal: P&L, win rate, análisis de trades
- [ ] Mensual: Sharpe, Calmar, comparación vs backtest
- [ ] **Semanal: RÉGIMEN DE MERCADO**

**Criterio para pasar a Fase 4:**
- ✅ 3-6 meses exitosos
- ✅ Sharpe >0.8 mantenido
- ✅ Calmar >1.0 mantenido
- ✅ Régimen de mercado estable (2022-2025 style)

---

### FASE 4: Live Full (Indefinido) 🏆

**Capital:** $10,000-50,000+ (según tu capital)
**Leverage:** 2x (máximo recomendado, NO exceder)
**Risk per trade:** 1.5% del capital

**Circuit Breakers Fase 4 (PRODUCCIÓN):**

🔴 **STOP INMEDIATO si:**
1. DD alcanza -25% (hard stop)
2. Losing streak >25 trades
3. 3 meses consecutivos con profit negativo
4. **🚨 CAMBIO DE RÉGIMEN CONFIRMADO** (ver abajo)

⚠️ **PAUSE y REVIEW si:**
1. DD alcanza -20%
2. Win rate <22% por 2 meses
3. Sharpe <0.7 por 3 meses
4. Calmar <1.0 por 3 meses
5. **⚠️ SIGNOS de cambio de régimen** (ver abajo)

---

## 🔍 MONITORING DE RÉGIMEN DE MERCADO (CRÍTICO)

**Esto es ÚNICO de este deployment debido al hallazgo 2020-2021.**

### Indicadores de Régimen Actual (2022-2025 Style) - FAVORABLE

✅ **Tu bot funciona EXCELENTE si:**
- ATR% promedio mensual >0.6%
- BTC tiene pullbacks >-10% al menos 1 vez por mes
- Movimientos típicos: 3-7R
- Alta volatilidad intraday
- Reversiones frecuentes

### 🚨 ALERTAS de Cambio a Régimen Parabólico (2020-2021 Style) - PELIGROSO

**ALERTA TEMPRANA (⚠️ MONITOREAR):**
1. ATR% promedio mensual cae <0.5% por 4 semanas
2. BTC sube >30% en 2 meses SIN pullback >-8%
3. Losing streak alcanza 15+ (puede indicar BE/TP inadecuados)
4. Win rate cae <20% por 3 semanas (señales prematuras en tendencia)

**ALERTA CRÍTICA (🔴 CONSIDERAR PAUSE):**
1. ATR% <0.4% por 6 semanas consecutivas
2. BTC sube >50% en 3 meses SIN pullback >-10%
3. Bot tiene 3+ trades cerrados en BE consecutivos (tendencia larga lo expulsa)
4. Losing streak >18 (patrón 2020-2021)
5. Win rate <18% por 1 mes

**ACCIÓN si ALERTA CRÍTICA:**
1. ⏸️ PAUSE trading inmediatamente
2. 📊 Analizar últimos 50 trades (¿muchos BE? ¿TP deja mucho en la mesa?)
3. 📈 Confirmar régimen: ¿BTC en tendencia parabólica sin pullbacks?
4. ✅ Si régimen cambió → STOP trading, esperar v10.0-ROBUST
5. ❌ Si falsa alarma → Reanudar con monitoring más estricto

### Herramientas de Monitoring de Régimen

**Script Python (ejecutar semanalmente):**
```python
# regime_monitor.py
import ccxt
import pandas as pd
import numpy as np

exchange = ccxt.binance()
candles = exchange.fetch_ohlcv('BTC/USDT', '1d', limit=90)
df = pd.DataFrame(candles, columns=['time', 'open', 'high', 'low', 'close', 'volume'])

# Calcular ATR%
df['tr'] = df['high'] - df['low']
df['atr'] = df['tr'].rolling(14).mean()
df['atr_pct'] = (df['atr'] / df['close']) * 100

# ATR promedio último mes
atr_30d = df['atr_pct'].tail(30).mean()

# Pullback máximo último mes
high_30d = df['high'].tail(30).max()
low_30d = df['low'].tail(30).min()
pullback_30d = ((low_30d - high_30d) / high_30d) * 100

# BTC % change último mes
btc_change_30d = ((df['close'].iloc[-1] - df['close'].iloc[-30]) / df['close'].iloc[-30]) * 100

print(f"🔍 REGIME MONITOR - {pd.Timestamp.now().strftime('%Y-%m-%d')}")
print(f"=" * 60)
print(f"ATR% (30d avg):        {atr_30d:.2f}% {'✅' if atr_30d > 0.6 else '⚠️' if atr_30d > 0.4 else '🔴'}")
print(f"Max Pullback (30d):    {pullback_30d:.2f}% {'✅' if pullback_30d < -8 else '⚠️'}")
print(f"BTC Change (30d):      {btc_change_30d:+.2f}%")
print(f"=" * 60)

# Alertas
if atr_30d < 0.4:
    print("🔴 ALERT: ATR muy bajo - Posible régimen parabólico")
elif atr_30d < 0.5:
    print("⚠️ WARNING: ATR bajando - Monitorear de cerca")

if btc_change_30d > 30 and pullback_30d > -8:
    print("🔴 ALERT: Tendencia fuerte sin pullbacks - Régimen puede estar cambiando")
```

**Ejecutar SEMANALMENTE y documentar resultados.**

---

## 📊 Alertas de Telegram (Configuración)

**Eventos a notificar:**

**Prioridad CRÍTICA (🔴):**
- Trade perdedor >2.5%
- DD alcanza -10%, -15%, -20%
- Losing streak alcanza 15, 18, 20
- Error de ejecución
- **ALERTA DE RÉGIMEN CRÍTICA**

**Prioridad ALTA (⚠️):**
- Todos los trades (entry/exit)
- Win rate semanal <20%
- **ALERTA DE RÉGIMEN TEMPRANA**

**Prioridad INFO (ℹ️):**
- Resumen diario de P&L
- Resumen semanal de métricas

**Configuración en Jesse:**
```python
'notifications': {
    'telegram': {
        'enabled': True,
        'token': os.environ.get('TELEGRAM_BOT_TOKEN'),
        'chat_id': os.environ.get('TELEGRAM_CHAT_ID'),
        'events': [
            'errors',
            'trades',
            'large_loss',  # >2.5%
            'drawdown_warning',  # -10%, -15%, -20%
            'losing_streak',  # 15, 18, 20
        ]
    }
}
```

---

## 📋 Checklist Pre-Launch

### Antes de Paper Trading:
- [ ] Jesse instalado y actualizado
- [ ] Estrategia v9.3-RSI36 copiada
- [ ] Config.py con testnet=True
- [ ] Telegram bot configurado y testeado
- [ ] Script regime_monitor.py funcionando
- [ ] Backup de toda configuración

### Antes de Live Micro:
- [ ] Paper trading exitoso 1+ mes
- [ ] API keys creadas (trading permissions)
- [ ] IP whitelist configurada
- [ ] 2FA activado
- [ ] Capital inicial depositado ($500-1k)
- [ ] Circuit breakers entendidos
- [ ] Plan escrito de qué hacer si se activan

### Antes de Live Pequeño:
- [ ] Live micro exitoso 1-2 meses
- [ ] Capital adicional depositado ($5-10k)
- [ ] Monitoring diario establecido como rutina
- [ ] Regime monitor ejecutándose semanalmente

### Antes de Live Full:
- [ ] Live pequeño exitoso 3-6 meses
- [ ] Sharpe >0.8 y Calmar >1.0 mantenidos
- [ ] Sin señales de cambio de régimen
- [ ] Plan de escalado definido

---

## 🔧 Plan de Contingencia

### Si DD Alcanza -15%

1. ⏸️ **PAUSE trading** inmediatamente
2. 📊 **Analizar últimos 100 trades:**
   - ¿Win rate fuera de rango (20-30%)?
   - ¿Losing streak anormal (>15)?
   - ¿Muchos trades cerrados en BE?
3. 🔍 **Check régimen de mercado:**
   - Ejecutar regime_monitor.py
   - ¿ATR% <0.5%?
   - ¿BTC en tendencia parabólica?
4. ✅ **Decidir:**
   - Si régimen OK + varianza natural → Reanudar con caution
   - Si régimen cambió → STOP, esperar v10.0-ROBUST
   - Si no está claro → Pause 1 semana más, re-evaluar

### Si Losing Streak >18

1. ⏸️ **PAUSE trading**
2. 📈 **Analizar patrón:**
   - ¿Trades cerrados en BE consecutivos? (señal de tendencia larga)
   - ¿TP alcanzado pero luego reversal? (necesita TP más alto)
   - ¿Entradas en contra-tendencia?
3. 🔍 **Check régimen:**
   - Si régimen cambió → STOP
   - Si régimen OK → Puede ser racha de mala suerte, esperar
4. ⏱️ Pause mínimo 48h antes de reanudar

### Si ALERTA de Cambio de Régimen

1. ⏸️ **PAUSE trading** (no esperar a que empeore)
2. 📊 **Análisis profundo:**
   - BTC chart 3 meses: ¿Patrón parabólico?
   - Volatilidad trending down?
   - Performance bot última 4 semanas
3. 💬 **Consultar comunidad/expertos:**
   - ¿Otros traders notan cambio de régimen?
   - ¿Consenso en tendencia parabólica?
4. ✅ **Decisión:**
   - **Si régimen cambió definitivamente:**
     - STOP trading v9.3-RSI36
     - Esperar v10.0-ROBUST (re-optimizado para 2019-2025)
     - O manual override de parámetros (RSI=30, BE=2.5R, TP=5.0R)
   - **Si falsa alarma:**
     - Reanudar con monitoring MÁS estricto
     - Reducir leverage a 1x temporalmente

---

## 📈 Expectativas Realistas

### Performance Esperada (si régimen se mantiene)

**Basado en backtest 2023-2025:**

| Métrica | Backtest | Live Esperado | Tolerancia |
|---------|----------|---------------|------------|
| Annual Return | 30.8% | 22-35% | ±15-20% |
| Win Rate | 25.14% | 20-28% | ±20% |
| Sharpe | 1.09 | 0.9-1.3 | ±18% |
| Calmar | 1.55 | 1.2-1.8 | ±23% |
| Max DD | -19.93% | -15% a -28% | ±30% |

**Razones de divergencia esperadas:**
- Slippage (2-5 ticks en Binance)
- Fees reales vs backtest
- Latencia de ejecución
- Varianza natural del mercado

### Red Flags (Indicadores de Problema)

🔴 **Detener inmediatamente si:**
- Win rate <15% por 1 mes
- Annual return trending <10% por 3 meses
- Max DD >-25%
- Sharpe <0.5 por 2 meses
- **Régimen cambió (confirmado)**

---

## 🚀 Resumen Ejecutivo

### Deployment Plan

1. **Semanas 1-4:** Paper trading, validar ejecución
2. **Semanas 5-8 (o hasta 12):** Live micro $500-1k, leverage 1x
3. **Meses 3-6 (o hasta 9):** Live pequeño $5-10k, leverage 2x
4. **Mes 7+ (o 10+):** Live full $10k+, leverage 2x

**Timeline total:** 6-12 meses desde paper hasta full production

### Paralelo: Re-Optimización v10.0-ROBUST

Mientras haces deployment de v9.3, en paralelo:
- **Semanas 1-2:** Re-optimizar parámetros usando 2019-2025
- **Semanas 3-4:** Walk-forward testing largo
- **Semanas 5-6:** Validación de robustez v10.0
- **Mes 2+:** Si v10.0 pasa tests, migrar de v9.3 → v10.0

**Objetivo:** Tener v10.0-ROBUST listo ANTES de que régimen cambie.

---

## ⚠️ Disclaimers Finales

1. **Trading automatizado conlleva riesgo de pérdida total de capital**
2. **v9.3-RSI36 NO es universalmente robusto** - puede fallar si mercado cambia
3. **Monitoring DIARIO es OBLIGATORIO** - no es "set and forget"
4. **Circuit breakers son tu seguro** - respétalos SIEMPRE
5. **Si régimen cambia, PARA** - no intentes "aguantar" esperando reversión

**Solo deployea si aceptas TODOS estos riesgos y condiciones.**

---

**Documento creado:** 2025-12-27
**Versión:** v9.3-RSI36
**Tipo de deployment:** CONSERVADOR con circuit breakers estrictos
**Monitoring de régimen:** OBLIGATORIO
**Siguiente paso:** Paper trading Fase 1

**¡Buena suerte! 🚀**
