# 🚀 Deployment Guide - v9.3-RSI36

**Versión:** v9.3-RSI36
**Estado:** ELITE (Calmar 1.55, +110.68% profit)
**Ready for production:** SÍ 🏆

---

## ⚠️ IMPORTANTE - LEE ANTES DE DEPLOYAR

**NUNCA deployees directamente a live trading sin:**
1. ✅ Completar tests de robustez (ROBUSTNESS_TESTING_PLAN.md)
2. ✅ Ejecutar en paper trading al menos 1 mes
3. ✅ Entender completamente los riesgos
4. ✅ Tener plan de gestión de capital definido
5. ✅ Configurar alertas y monitoreo

**El trading automatizado conlleva riesgos significativos de pérdida de capital.**

---

## 📋 Pre-requisitos

### 1. Infraestructura

- [ ] Servidor/VPS con uptime >99.9%
- [ ] Conexión a internet estable
- [ ] Python 3.9+ instalado
- [ ] Jesse framework actualizado
- [ ] Backup automático de base de datos
- [ ] Sistema de alertas (Telegram/Discord/Email)

### 2. Exchange Setup

- [ ] Cuenta en Binance Futures (recomendado)
- [ ] API Keys creadas (con permisos de trading)
- [ ] API Keys con whitelist de IP (seguridad)
- [ ] 2FA activado en cuenta
- [ ] Funding suficiente en cuenta
- [ ] VIP level apropiado para fees bajos

### 3. Testing Previo

- [ ] Tests de robustez completados (Prioridad ALTA)
- [ ] Paper trading ejecutado 1+ mes
- [ ] Sin errores de ejecución en paper trading
- [ ] Métricas de paper trading alineadas con backtest

---

## 🔧 Configuración de Jesse para Live Trading

### 1. Instalación de Jesse (si no está)

```bash
# Instalar Jesse
pip install jesse

# O actualizar a última versión
pip install -U jesse

# Verificar instalación
jesse -v
```

### 2. Crear Proyecto Live Trading

```bash
# Crear proyecto separado para live trading
mkdir jesse-live
cd jesse-live

# Inicializar Jesse
jesse make-project

# Copiar estrategia v9.3-RSI36
cp path/to/Multitimeframe/__init__.py strategies/Multitimeframe/
```

### 3. Configurar Credenciales de Exchange

Editar `config.py`:

```python
# config.py
config = {
    # ...

    'exchanges': {
        'Binance Futures': {
            'fee': 0.04,  # 0.04% taker fee (VIP 0)

            # LIVE TRADING
            'type': 'futures',
            'futures_leverage_mode': 'cross',  # o 'isolated'
            'futures_leverage': 2,  # ⚠️ AJUSTAR SEGÚN TOLERANCIA

            # API CREDENTIALS (NUNCA COMMITEAR A GIT)
            'api_key': os.environ.get('BINANCE_API_KEY'),
            'api_secret': os.environ.get('BINANCE_API_SECRET'),

            # TESTNET (para paper trading inicial)
            # 'testnet': True,
        }
    },

    # CONFIGURACIÓN DE LIVE TRADING
    'env': {
        'metrics': {
            'enabled': True,
            'port': 8000,
        },
        'notifications': {
            'enabled': True,
            'events': ['errors', 'trades'],

            # TELEGRAM (recomendado)
            'telegram': {
                'enabled': True,
                'token': os.environ.get('TELEGRAM_BOT_TOKEN'),
                'chat_id': os.environ.get('TELEGRAM_CHAT_ID'),
            }
        }
    }
}
```

### 4. Variables de Entorno (Seguridad)

Crear archivo `.env`:

```bash
# .env (NUNCA COMMITEAR A GIT)
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id
```

Añadir a `.gitignore`:
```
.env
config.py  # Si contiene secrets
```

---

## 🎯 Estrategia de Deployment (Fases)

### Fase 1: Paper Trading (OBLIGATORIO) ⏳

**Duración:** 1-2 meses
**Capital:** Virtual ($10,000)
**Objetivo:** Validar ejecución sin riesgo

**Configuración:**
```python
# En config.py
'exchanges': {
    'Binance Futures': {
        'testnet': True,  # ← PAPER TRADING
        'futures_leverage': 2,
    }
}
```

**Comando:**
```bash
jesse run 2025-01-01 2025-02-01
```

**Checklist de validación:**
- [ ] Bot ejecuta trades sin errores
- [ ] Órdenes se llenan correctamente
- [ ] Stop loss funciona
- [ ] Take profit funciona
- [ ] Break-even se activa correctamente
- [ ] Métricas similares a backtest (±10%)
- [ ] No hay crashes ni desconexiones

**Criterio de paso:** Si paper trading 1 mes tiene métricas dentro del ±20% del backtest → Proceder a Fase 2

---

### Fase 2: Live Micro (Bajo Riesgo) ⏳

**Duración:** 1 mes
**Capital:** $500-1,000 (capital que puedes permitirte perder)
**Leverage:** 1x (conservador)
**Objetivo:** Validar en live con capital real mínimo

**Configuración:**
```python
# En config.py
'exchanges': {
    'Binance Futures': {
        'testnet': False,  # ← LIVE TRADING
        'futures_leverage': 1,  # Conservador
    }
}
```

**Gestión de riesgo:**
- Tamaño de posición: 1% del capital por trade
- Max drawdown aceptable: -20%
- Stop trading si DD > -15%

**Comando:**
```bash
jesse live
```

**Checklist de validación:**
- [ ] Trades ejecutan sin slippage excesivo
- [ ] Fees coinciden con configuración
- [ ] Latencia aceptable (<500ms)
- [ ] Profit tracking funciona
- [ ] Alertas funcionan correctamente
- [ ] Monitoreo diario sin problemas

**Criterio de paso:** Si después de 1 mes tienes profit >0% y DD <-20% → Proceder a Fase 3

---

### Fase 3: Live Pequeño (Producción Inicial) ⏳

**Duración:** 3-6 meses
**Capital:** $5,000-10,000
**Leverage:** 2x (según backtest)
**Objetivo:** Escalado gradual con capital significativo

**Configuración:**
```python
'exchanges': {
    'Binance Futures': {
        'testnet': False,
        'futures_leverage': 2,  # Según backtest v9.3
    }
}
```

**Gestión de riesgo:**
- Tamaño de posición: 2% del capital por trade
- Max drawdown aceptable: -25%
- Stop trading si DD > -20%
- Review semanal de performance

**Monitoreo:**
- [ ] Dashboard de métricas (Jesse web)
- [ ] Alertas diarias de trades
- [ ] Weekly P&L report
- [ ] Monthly full analysis vs backtest

**Criterio de paso:** Si después de 3-6 meses mantienes Sharpe >0.8 y Calmar >1.0 → Considerar Fase 4

---

### Fase 4: Live Full (Producción Completa) ⏳

**Duración:** Indefinido
**Capital:** $10,000-50,000+ (según tu capital disponible)
**Leverage:** 2x (máximo recomendado)
**Objetivo:** Operación a escala completa

**Configuración:**
```python
'exchanges': {
    'Binance Futures': {
        'testnet': False,
        'futures_leverage': 2,  # NO exceder
    }
}
```

**Gestión de riesgo:**
- Tamaño de posición: 2% del capital por trade
- Max drawdown aceptable: -30% (hard stop)
- Retiro de profits mensual (compounding controlado)
- Diversificación: No más del 50% de capital total en bot

**Reglas de operación:**
- [ ] Review diario de trades
- [ ] Análisis semanal de métricas
- [ ] Monthly comparison vs backtest
- [ ] Quarterly strategy review
- [ ] Immediate stop si Sharpe <0.5 por 2 meses consecutivos

---

## 🔍 Monitoreo y Alertas

### Dashboard (Jesse Web Interface)

```bash
# Iniciar dashboard
jesse metrics

# Acceder a http://localhost:8000
```

**Métricas a monitorear:**
- Equity curve (real-time)
- Open positions
- Recent trades
- Win rate (rolling 30 días)
- Sharpe ratio (rolling 90 días)
- Current drawdown

### Alertas de Telegram

**Eventos a notificar:**
- Trade ejecutado (entry/exit)
- Error de ejecución
- Pérdida > 2% en un trade
- Drawdown alcanza -10%, -15%, -20%
- Winning streak de 5+
- Losing streak de 10+

**Configuración:**
```python
'notifications': {
    'telegram': {
        'enabled': True,
        'events': [
            'errors',
            'trades',
            'large_loss',  # >2%
            'drawdown_warning',  # DD levels
        ]
    }
}
```

---

## ⚠️ Gestión de Riesgos

### Reglas de Stop Trading (Circuit Breakers)

**Stop INMEDIATO si:**
1. ❌ Drawdown alcanza -25% (Fase 2)
2. ❌ Drawdown alcanza -30% (Fase 3+)
3. ❌ 3+ errores de ejecución consecutivos
4. ❌ Sharpe ratio cae <0.3 por 1 mes
5. ❌ Winning streak negativa de 15+ trades

**Review y posible stop si:**
1. ⚠️ Sharpe ratio <0.5 por 2 meses
2. ⚠️ Win rate cae <18% por 1 mes
3. ⚠️ Drawdown >-20% por más de 2 semanas
4. ⚠️ Profit mensual negativo 2 meses consecutivos

### Position Sizing (Recomendado)

**Conservador (Recomendado):**
- Risk per trade: 1-2% del capital
- Max open positions: 1 (como en backtest)
- Leverage: 1-2x
- Stop loss: Según estrategia (BE=1.35R)

**Moderado:**
- Risk per trade: 2-3% del capital
- Max open positions: 1
- Leverage: 2x
- Stop loss: Según estrategia

**Agresivo (NO RECOMENDADO):**
- Risk per trade: >3% del capital
- Leverage: >2x
- ALTO RIESGO DE LIQUIDACIÓN

---

## 🔧 Mantenimiento

### Diario
- [ ] Check de trades ejecutados
- [ ] Review de alertas
- [ ] Verificar conexión activa

### Semanal
- [ ] Análisis de P&L semanal
- [ ] Comparación vs backtest metrics
- [ ] Review de trades perdedores
- [ ] Check de fees acumulados

### Mensual
- [ ] Full performance report
- [ ] Sharpe/Calmar calculation
- [ ] Equity curve analysis
- [ ] Decision: continuar/pausar/ajustar

### Trimestral
- [ ] Strategy review completo
- [ ] Considerar re-optimización
- [ ] Análisis de cambios de mercado
- [ ] Decision: mantener/actualizar estrategia

---

## 🚨 Plan de Contingencia

### Si Drawdown > -20%
1. Pausar trading inmediatamente
2. Analizar últimos 50 trades
3. Verificar si hay cambio de régimen de mercado
4. Decidir: continuar/pausar/re-optimizar

### Si Errores de Ejecución
1. Pausar trading
2. Check de logs detallado
3. Verificar conexión a exchange
4. Test en paper trading
5. Resolver issue antes de reanudar

### Si Performance Degrada
1. Comparar métricas rolling vs backtest
2. Analizar si es varianza natural o cambio estructural
3. Considerar re-calibración de parámetros
4. Opción: volver a paper trading para validar

---

## 📊 Benchmarks Esperados (Live Trading)

**Basado en backtest v9.3-RSI36:**

| Métrica | Backtest | Live Esperado | Tolerancia |
|---------|----------|---------------|------------|
| Annual Return | 30.8% | 25-35% | ±15% |
| Win Rate | 25.14% | 22-28% | ±12% |
| Sharpe Ratio | 1.09 | 0.9-1.3 | ±18% |
| Calmar Ratio | 1.55 | 1.2-1.8 | ±23% |
| Max DD | -19.93% | -15% a -25% | ±25% |

**Razones de divergencia esperadas:**
- Slippage (no modelado en backtest)
- Fees reales vs backtest
- Latencia de ejecución
- Varianza de mercado natural
- Diferencias en liquidez

---

## ✅ Checklist Pre-Launch

### Antes de iniciar paper trading:
- [ ] Jesse instalado y actualizado
- [ ] Estrategia v9.3-RSI36 copiada correctamente
- [ ] Config.py configurado (testnet=True)
- [ ] Variables de entorno creadas
- [ ] Telegram bot configurado
- [ ] Dashboard accesible
- [ ] Backup de configuración realizado

### Antes de iniciar live trading:
- [ ] Paper trading exitoso (1+ mes)
- [ ] Tests de robustez completados
- [ ] API keys creadas con permisos correctos
- [ ] Whitelist de IP configurada
- [ ] Capital inicial depositado
- [ ] Plan de gestión de riesgo definido
- [ ] Alertas funcionando
- [ ] Conocimiento completo de cómo pausar/detener bot

---

## 📚 Recursos Adicionales

### Documentación Jesse
- [Jesse Docs](https://docs.jesse.trade)
- [Live Trading Guide](https://docs.jesse.trade/docs/getting-started/live-trading.html)
- [Notifications](https://docs.jesse.trade/docs/notifications.html)

### Comunidad
- [Jesse Discord](https://discord.gg/jesse)
- [Jesse Forum](https://forum.jesse.trade)

### Seguridad
- [Binance API Security](https://www.binance.com/en/support/faq/360002502072)
- [2FA Setup](https://www.binance.com/en/support/faq/115000584451)

---

## 🎯 Resumen Ejecutivo

**v9.3-RSI36 está listo para deployment siguiendo esta ruta:**

1. **Paper Trading** (1-2 meses) → Validar ejecución sin riesgo
2. **Live Micro** ($500-1k, 1 mes) → Validar con capital mínimo
3. **Live Pequeño** ($5-10k, 3-6 meses) → Escalar gradualmente
4. **Live Full** ($10k+, indefinido) → Operación completa

**NO SALTAR FASES. La paciencia es clave para el éxito en trading automatizado.**

---

**Documento creado:** 2025-12-27
**Versión:** v9.3-RSI36
**Estado:** GUÍA COMPLETA - LISTO PARA USAR
**Siguiente paso:** Completar tests de robustez antes de deployar
