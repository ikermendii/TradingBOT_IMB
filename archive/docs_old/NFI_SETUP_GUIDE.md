# 🚀 NostalgiaForInfinity Setup Guide - Paso a Paso

**Fecha:** 2025-12-29
**Objetivo:** Implementar y validar NostalgiaForInfinity strategy
**Timeline:** 1-2 semanas
**Status:** Setup iniciado

---

## 📋 OVERVIEW DEL PLAN

### Fase 1: Setup (Días 1-2)
- ✅ Instalar Freqtrade
- ✅ Configurar environment
- ✅ Clonar NostalgiaForInfinity
- ✅ Importar candles históricos

### Fase 2: Backtest Baseline (Días 3-4)
- ⏳ Backtest completo 2020-2025
- ⏳ Analizar métricas vs v3.x
- ⏳ Optimizar config inicial

### Fase 3: Walk-Forward Validation (Días 5-6)
- ⏳ TRAIN period: 2020-2023
- ⏳ TEST period: 2024-2025
- ⏳ Calcular ratio, validar ≥0.6

### Fase 4: Decisión (Día 7)
- ⏳ Si PASS → Fase 2 (Semana 2)
- ⏳ Si FAIL → Analizar causa, plan B

---

## 🛠️ FASE 1: SETUP - Día 1-2

### Step 1: Verificar Python Environment

```bash
# Verificar Python version (necesitamos 3.9-3.12)
python --version

# Si tienes Python incorrecto, instalar Python 3.11
# Freqtrade funciona mejor con Python 3.11
```

**Requisitos:**
- Python 3.9, 3.10, 3.11, o 3.12
- Git instalado
- 4GB RAM mínimo (8GB recomendado)
- 10GB espacio en disco

---

### Step 2: Crear Directorio Limpio para Freqtrade

```bash
# Ir a tu directorio de trabajo
cd "c:\Users\ikerm\Desktop\Pruebas BOTTrading"

# Crear nuevo directorio para Freqtrade
mkdir FreqtradeBOT
cd FreqtradeBOT
```

**Por qué directorio nuevo:**
- Mantener Jesse y Freqtrade separados
- Evitar conflictos de dependencias
- Facilitar comparación entre frameworks

---

### Step 3: Instalar Freqtrade

**Opción A: Windows (Recomendado)**

```bash
# Clonar repositorio de Freqtrade
git clone https://github.com/freqtrade/freqtrade.git
cd freqtrade

# Crear virtual environment
python -m venv .venv

# Activar virtual environment
.venv\Scripts\activate

# Instalar Freqtrade
pip install -e .

# Verificar instalación
freqtrade --version
```

**Opción B: Via pip (Alternativo)**

```bash
# Crear y activar venv
python -m venv ft_venv
ft_venv\Scripts\activate

# Instalar Freqtrade
pip install freqtrade

# Verificar
freqtrade --version
```

**Output esperado:**
```
freqtrade 2025.8
```

---

### Step 4: Crear Configuración Inicial

```bash
# Crear configuración nueva (dentro de freqtrade directory)
freqtrade new-config --config user_data/config.json
```

**Respuestas a la configuración:**

```
? Exchange name: binance
? Stake currency: USDT
? Stake amount: unlimited
? Max open trades: 10
? Timeframe: 1h
? Dry-run: Yes
? Telegram: No (podemos agregar después)
```

**Config generado:** `user_data/config.json`

---

### Step 5: Configurar para Backtesting

Editar `user_data/config.json`:

```json
{
  "max_open_trades": 10,
  "stake_currency": "USDT",
  "stake_amount": "unlimited",
  "tradable_balance_ratio": 0.99,
  "fiat_display_currency": "USD",
  "dry_run": true,
  "cancel_open_orders_on_exit": false,

  "unfilledtimeout": {
    "entry": 10,
    "exit": 10,
    "exit_timeout_count": 0,
    "unit": "minutes"
  },

  "entry_pricing": {
    "price_side": "same",
    "use_order_book": true,
    "order_book_top": 1,
    "price_last_balance": 0.0,
    "check_depth_of_market": {
      "enabled": false,
      "bids_to_ask_delta": 1
    }
  },

  "exit_pricing": {
    "price_side": "same",
    "use_order_book": true,
    "order_book_top": 1
  },

  "exchange": {
    "name": "binance",
    "key": "",
    "secret": "",
    "ccxt_config": {},
    "ccxt_async_config": {},
    "pair_whitelist": [
      "BTC/USDT"
    ],
    "pair_blacklist": []
  },

  "pairlists": [
    {
      "method": "StaticPairList"
    }
  ],

  "edge": {
    "enabled": false
  },

  "telegram": {
    "enabled": false
  },

  "api_server": {
    "enabled": false,
    "listen_ip_address": "127.0.0.1",
    "listen_port": 8080,
    "verbosity": "error",
    "enable_openapi": false,
    "jwt_secret_key": "",
    "ws_token": "",
    "CORS_origins": [],
    "username": "",
    "password": ""
  },

  "bot_name": "freqtrade_nfi",
  "initial_state": "running",
  "force_entry_enable": false,
  "internals": {
    "process_throttle_secs": 5
  }
}
```

**Guardar como:** `user_data/config_backtest.json`

---

### Step 6: Clonar NostalgiaForInfinity Strategy

```bash
# Volver al directorio freqtrade root
cd c:\Users\ikerm\Desktop\Pruebas BOTTrading\FreqtradeBOT\freqtrade

# Clonar NFI en user_data/strategies
cd user_data/strategies
git clone https://github.com/iterativv/NostalgiaForInfinity.git

# Copiar estrategia principal al directorio strategies
# NFI tiene múltiples versiones, usar la más reciente
copy NostalgiaForInfinity\NostalgiaForInfinityNext.py .

# Volver a freqtrade root
cd ..\..
```

**Verificar estrategia:**

```bash
# Listar estrategias disponibles
freqtrade list-strategies --strategy-path user_data/strategies
```

**Output esperado:**
```
Strategy: NostalgiaForInfinityNext
```

---

### Step 7: Importar Candles Históricos

**Importar datos para BTC/USDT:**

```bash
# Importar datos desde 2020-01-01 hasta hoy
freqtrade download-data \
  --exchange binance \
  --pairs BTC/USDT \
  --timeframes 1h 5m 15m \
  --timerange 20200101- \
  --config user_data/config_backtest.json

# Esto tomará 5-10 minutos
```

**Por qué múltiples timeframes:**
- NFI usa 1h como base
- Pero también analiza 5m y 15m para confirmaciones
- Necesitamos importar todos los timeframes que usa la estrategia

**Verificar datos importados:**

```bash
# Listar datos descargados
dir user_data\data\binance
```

**Output esperado:**
```
BTC_USDT-1h.json
BTC_USDT-5m.json
BTC_USDT-15m.json
```

---

## 📊 FASE 2: BACKTEST BASELINE - Día 3-4

### Step 8: Primer Backtest Completo

```bash
# Activar venv si no está activo
.venv\Scripts\activate

# Ejecutar backtest 2020-2025
freqtrade backtesting \
  --config user_data/config_backtest.json \
  --strategy NostalgiaForInfinityNext \
  --timerange 20200114-20251227 \
  --timeframe 1h \
  --export trades \
  --export-filename user_data/backtest_results/nfi_baseline_2020_2025.json

# Esto tomará 10-20 minutos
```

**Qué analizar en resultados:**

```
Métricas clave:
  Total Trades:       ??? (comparar con v3.x: 536 trades)
  Win Rate:           ??? (v3.x: 33.58%)

  Profit:
    Total Profit:     ???% (v3.x: +1154.70%)
    Annual Return:    ???% (v3.x: 52.91%)

  Risk:
    Max Drawdown:     ???% (v3.x: -55.42%)

  Risk-Adjusted:
    Sharpe Ratio:     ??? (v3.x: 1.06, objetivo >1.0)
    Calmar Ratio:     ??? (v3.x: 0.95, objetivo >1.0)
    Sortino Ratio:    ??? (v3.x: 1.62)

  Per-Trade:
    Expectancy:       $??? (v3.x: $215.22)
    Avg Win:          $???
    Avg Loss:         $???
    Win/Loss Ratio:   ??? (v3.x: 2.68)
```

---

### Step 9: Analizar Resultados vs v3.x

**Crear documento de comparación:**

```markdown
# NFI vs v3.x Baseline Comparison

| Métrica | v3.x (8787% ROI) | NFI | Diferencia | Winner |
|---------|------------------|-----|------------|--------|
| Annual Return | 52.91% | ???% | ??? | ??? |
| Max DD | -55.42% | ???% | ??? | ??? |
| Sharpe | 1.06 | ??? | ??? | ??? |
| Calmar | 0.95 | ??? | ??? | ??? |
| Win Rate | 33.58% | ???% | ??? | ??? |
| Expectancy | $215.22 | $??? | ??? | ??? |
| Total Trades | 536 | ??? | ??? | ??? |

Target para continuar:
✅ Sharpe ≥1.0
✅ Calmar ≥0.9
✅ Annual Return ≥40%
```

**Guardar en:** `NFI_BASELINE_RESULTS.md`

---

### Step 10: Optimizar Config Inicial (Si es necesario)

**Si resultados baseline son pobres, ajustar:**

```python
# En NostalgiaForInfinityNext.py, buscar sección de config

# Parámetros ajustables:
minimal_roi = {
    "0": 0.10,    # 10% profit objetivo
    "30": 0.05,   # 5% después de 30 minutos
    "60": 0.03,   # 3% después de 1 hora
    "120": 0.01   # 1% después de 2 horas
}

stoploss = -0.10  # 10% stoploss (ajustar según risk tolerance)

trailing_stop = True
trailing_stop_positive = 0.01
trailing_stop_positive_offset = 0.02
trailing_only_offset_is_reached = True
```

**Re-ejecutar backtest después de ajustes.**

---

## 🔬 FASE 3: WALK-FORWARD VALIDATION - Día 5-6

### Step 11: TRAIN Period Backtest

```bash
# Backtest TRAIN: 2020-2023
freqtrade backtesting \
  --config user_data/config_backtest.json \
  --strategy NostalgiaForInfinityNext \
  --timerange 20200114-20231231 \
  --timeframe 1h \
  --export trades \
  --export-filename user_data/backtest_results/nfi_train_2020_2023.json
```

**Anotar Annual Return TRAIN:** ____%

---

### Step 12: TEST Period Backtest

```bash
# Backtest TEST: 2024-2025
freqtrade backtesting \
  --config user_data/config_backtest.json \
  --strategy NostalgiaForInfinityNext \
  --timerange 20240101-20251227 \
  --timeframe 1h \
  --export trades \
  --export-filename user_data/backtest_results/nfi_test_2024_2025.json
```

**Anotar Annual Return TEST:** ____%

---

### Step 13: Calcular Ratio y Validar

```python
# Cálculo Walk-Forward Ratio
Ratio = TEST Annual / TRAIN Annual

Ejemplo:
  TRAIN: 60% anual
  TEST:  40% anual
  Ratio: 40 / 60 = 0.67 ✅ PASS (≥0.6)

Criterio:
✅ PASS: Ratio ≥0.6 (60% de TRAIN)
⚠️ REVISAR: Ratio 0.4-0.6
❌ FAIL: Ratio <0.4
```

**Comparación con v3.x:**

| Versión | TRAIN Annual | TEST Annual | Ratio | Status |
|---------|--------------|-------------|-------|--------|
| v3.0 | 88.96% | 14.09% | 0.16 | ❌ FAIL |
| v3.1 | 64.1% | 12.96% | 0.20 | ❌ FAIL |
| v3.2 | 77.32% | 13.97% | 0.18 | ❌ FAIL |
| **NFI** | ???% | ???% | ??? | ??? |

---

### Step 14: Analizar Degradación por Métrica

**Template de análisis:**

```markdown
# NFI Walk-Forward Detailed Analysis

## TRAIN Period (2020-2023)
- Annual Return: ___%
- Max DD: -___%
- Sharpe: ___
- Calmar: ___
- Win Rate: ___%
- Expectancy: $___ per trade
- Total Trades: ___

## TEST Period (2024-2025)
- Annual Return: ___%
- Max DD: -___%
- Sharpe: ___
- Calmar: ___
- Win Rate: ___%
- Expectancy: $___ per trade
- Total Trades: ___

## Degradación Analysis

| Métrica | TRAIN | TEST | Ratio | Degradación % | Status |
|---------|-------|------|-------|---------------|--------|
| Annual Return | ___% | ___% | ___ | ___% | ✅/❌ |
| Sharpe | ___ | ___ | ___ | ___% | ✅/❌ |
| Calmar | ___ | ___ | ___ | ___% | ✅/❌ |
| Expectancy | $___ | $___ | ___ | ___% | ✅/❌ |
| Win Rate | ___% | ___% | ___ | ___% | ✅/❌ |

## Veredicto

Ratio: ___

✅ PASS (≥0.6): NFI validado, proceder a Semana 2
⚠️ REVISAR (0.4-0.6): Analizar causas, optimizar
❌ FAIL (<0.4): NFI overfitted, considerar Plan B
```

**Guardar en:** `NFI_WALK_FORWARD_RESULTS.md`

---

## 🎯 FASE 4: DECISIÓN - Día 7

### Si Walk-Forward PASS (Ratio ≥0.6) ✅

**Proceder a Semana 2:**

1. **Regime-Specific Validation:**
   ```bash
   # Bull market test (2021)
   freqtrade backtesting --timerange 20210101-20211231

   # Bear market test (2022)
   freqtrade backtesting --timerange 20220101-20221231

   # Sideways test (2024)
   freqtrade backtesting --timerange 20240101-20241231
   ```

2. **Optimización para BTC-USDT:**
   ```bash
   # Hyperopt para optimizar parámetros
   freqtrade hyperopt \
     --strategy NostalgiaForInfinityNext \
     --hyperopt-loss SharpeHyperOptLoss \
     --epochs 100 \
     --timerange 20200114-20231231
   ```

3. **Paper Trading Setup:**
   - Configurar API keys de Binance (testnet primero)
   - Setup dry-run mode
   - Monitorear 1 semana en dry-run

4. **Documentación:**
   - Crear deployment guide
   - Risk management plan
   - Monitoring checklist

---

### Si Walk-Forward FAIL (Ratio <0.4) ❌

**Analizar causas:**

1. **¿Mismo problema que v3.x?**
   - Si TEST period también falló en sideways → NFI no resolvió el problema
   - Necesitamos estrategia aún más adaptativa

2. **¿Problema de configuración?**
   - Probar con diferentes ROI targets
   - Ajustar stoploss
   - Cambiar trailing stop settings

3. **¿Problema específico de BTC?**
   - NFI diseñado para 40-80 pares
   - Puede no funcionar bien con single pair
   - Probar agregando ETH, BNB, SOL

**Plan B Options:**

**B1: Optimizar NFI con filtros adicionales**
```python
# Agregar volatility filter
if atr_mean < atr_threshold:
    return False  # No operar en baja volatilidad

# Agregar regime filter
if adx < 25:
    use_conservative_exit = True
```

**B2: Custom Regime-Adaptive Strategy**
- Diseñar desde cero
- Usar lecciones de v3.x + NFI
- Focus en adaptación a regímenes

**B3: Probar otra estrategia community**
- Buscar en Freqtrade Strategies Repo
- Filtrar por Sharpe >1.0
- Repetir proceso de validación

---

## 📊 MÉTRICAS DE ÉXITO

### Baseline Completo (2020-2025)

**Mínimos aceptables:**
- ✅ Annual Return: ≥40%
- ✅ Sharpe Ratio: ≥1.0
- ✅ Calmar Ratio: ≥0.9
- ✅ Max Drawdown: <40%
- ✅ Win Rate: ≥30%

**Targets aspiracionales:**
- 🏆 Annual Return: ≥60%
- 🏆 Sharpe Ratio: ≥1.2
- 🏆 Calmar Ratio: ≥1.3
- 🏆 Max Drawdown: <30%
- 🏆 Win Rate: ≥35%

---

### Walk-Forward Validation

**Criterio principal:**
- ✅ Ratio ≥0.6 (TEST ≥ 60% de TRAIN)

**Criterios secundarios:**
- ✅ TEST Sharpe ≥0.8
- ✅ TEST Calmar ≥0.6
- ✅ TEST Annual Return ≥25%
- ✅ Degradación Win Rate <20%
- ✅ Degradación Expectancy <50%

---

### Regime-Specific Performance

**Bull Market (2021):**
- ✅ Annual Return ≥60%
- ✅ Calmar ≥1.2

**Bear Market (2022):**
- ✅ Sobrevive (no colapsa)
- ✅ Annual Return ≥0% (positivo)
- ✅ Max DD <50%

**Sideways (2024):**
- ✅ Annual Return ≥20% (CLAVE - v3.x falló aquí)
- ✅ Win/Loss ratio se mantiene
- ✅ Expectancy no colapsa

---

## 🚨 TROUBLESHOOTING

### Problema: Freqtrade no instala

```bash
# Verificar pip version
pip --version

# Update pip
python -m pip install --upgrade pip

# Reinstalar con verbose
pip install -e . --verbose
```

---

### Problema: Download data falla

```bash
# Verificar conexión a Binance
ping api.binance.com

# Intentar con menos pares
freqtrade download-data --pairs BTC/USDT --timeframes 1h

# Si persiste, usar VPN (Binance puede estar bloqueado)
```

---

### Problema: Backtest muy lento

```bash
# Reducir timeframes
# Solo usar 1h si 5m/15m no son críticos

# Usar menos datos
--timerange 20220101-20251227  # Solo últimos 3 años

# Habilitar cache
--cache none  # Paradójicamente, sometimes faster
```

---

### Problema: Strategy no carga

```bash
# Verificar syntax errors
python user_data/strategies/NostalgiaForInfinityNext.py

# Listar estrategias disponibles
freqtrade list-strategies

# Verificar dependencies
pip install -r requirements.txt
```

---

## 📚 RECURSOS ÚTILES

### Documentación Oficial
- [Freqtrade Docs](https://www.freqtrade.io/en/stable/)
- [Backtesting Guide](https://www.freqtrade.io/en/stable/backtesting/)
- [Strategy Customization](https://www.freqtrade.io/en/stable/strategy-customization/)

### NFI Resources
- [NFI GitHub](https://github.com/iterativv/NostalgiaForInfinity)
- [NFI Setup Guide](https://alexbobes.com/crypto/automated-crypto-trading-with-freqtrade-and-nostalgiaforinfinity/)
- [Strategy Performance](https://strat.ninja/)

### Community
- [Freqtrade Discord](https://discord.gg/freqtrade)
- [Freqtrade GitHub Discussions](https://github.com/freqtrade/freqtrade/discussions)

---

## ✅ CHECKLIST COMPLETO

### Fase 1: Setup (Días 1-2)
- [ ] Python 3.9-3.12 instalado
- [ ] Git instalado
- [ ] Directorio FreqtradeBOT creado
- [ ] Freqtrade clonado e instalado
- [ ] Virtual environment activo
- [ ] Config backtest creado
- [ ] NFI strategy clonada
- [ ] Candles importados (1h, 5m, 15m)
- [ ] Verificar: `freqtrade list-strategies` muestra NFI

### Fase 2: Backtest (Días 3-4)
- [ ] Baseline backtest ejecutado (2020-2025)
- [ ] Métricas vs v3.x documentadas
- [ ] Decisión: continuar o ajustar config
- [ ] NFI_BASELINE_RESULTS.md creado

### Fase 3: Walk-Forward (Días 5-6)
- [ ] TRAIN backtest ejecutado (2020-2023)
- [ ] TEST backtest ejecutado (2024-2025)
- [ ] Ratio calculado
- [ ] Degradación analizada por métrica
- [ ] NFI_WALK_FORWARD_RESULTS.md creado

### Fase 4: Decisión (Día 7)
- [ ] Veredicto: PASS / REVISAR / FAIL
- [ ] Si PASS: Plan Semana 2 creado
- [ ] Si FAIL: Plan B decidido
- [ ] Documentación completa

---

## 🎯 SIGUIENTE PASO INMEDIATO

**Empezar con Step 1:**

```bash
# Verificar Python
python --version

# Si es 3.9-3.12, continuar
# Si no, instalar Python 3.11
```

**Luego reportar:**
- Python version instalada
- Sistema operativo (Windows/Linux/Mac)
- RAM disponible
- Espacio en disco

**Una vez confirmado, proceder a Step 2.**

---

**Fecha:** 2025-12-29
**Timeline:** 7 días para validación completa
**Objetivo:** Walk-forward ratio ≥0.6
**Creado por:** Setup Guide para NFI Implementation
