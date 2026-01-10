# 📋 FASE 1: Instrucciones para Análisis de Baseline

**Objetivo:** Entender exactamente en qué años v9.3-RSI36 pierde dinero.

**Tiempo estimado:** 2-3 horas (4 backtests × 30-45min cada uno)

---

## 🚀 PASO 1: Iniciar Servidor Jesse

### Opción A: Desde terminal

```bash
wsl bash -c 'cd /mnt/c/Users/ikerm/Desktop/Pruebas\ BOTTrading/TradingBot_Project && /root/.local/bin/jesse run'
```

**Espera 10-15 segundos** hasta que veas:
```
 * Running on http://127.0.0.1:9000/ (Press CTRL+C to quit)
```

### Opción B: Verificar si ya está corriendo

```bash
# Ver procesos Jesse
wsl bash -c 'ps aux | grep jesse | grep -v grep'
```

Si ya está corriendo, pasa al PASO 2.

---

## 🧪 PASO 2: Ejecutar Backtests (Manual via Web UI)

### 2.1 Abrir Jesse Web UI

1. Abre navegador
2. Ve a: **http://localhost:9000**
3. Click en pestaña **"Backtest"**

---

### 2.2 Test #1: Baseline 2019-2025 (COMPLETO)

**Propósito:** Ver performance total en 6 años

**Configuración en Web UI:**
```
Exchange:     Binance Spot  ⚠️ IMPORTANTE: Usar SPOT no Futures
Symbol:       BTC-USDT
Strategy:     Multitimeframe
Start Date:   2019-01-01
End Date:     2025-10-17
Timeframe:    15m
```

**⚠️ IMPORTANTE:** Usar **Binance Spot** porque Binance Perpetual Futures no tiene datos antes de Nov 2021. SPOT tiene datos completos desde 2017.

**Click:** "Start Backtest"

**Espera:** 30-45 minutos (depende de CPU)

**Cuando termine, ANOTA:**
- Net Profit %: __________
- Max Drawdown %: __________
- Win Rate %: __________
- Total Trades: __________
- Sharpe Ratio: __________
- Calmar Ratio: __________

**Expectativa:**
- Net Profit: -50% a -70% ❌ (sabemos que falla)
- Max DD: -80% a -90% ❌

---

### 2.3 Test #2: Año 2019 Individual

**Propósito:** ¿Cómo funciona en pre-parabólico?

**Configuración:**
```
Exchange:     Binance Spot
Symbol:       BTC-USDT
Strategy:     Multitimeframe
Start Date:   2019-01-01
End Date:     2019-12-31
Timeframe:    15m
```

**Click:** "Start Backtest"

**Cuando termine, ANOTA:**
- Net Profit %: __________
- Max Drawdown %: __________
- Win Rate %: __________
- Total Trades: __________

**Expectativa:**
- Net Profit: -5% a +10% (neutral/ligeramente positivo)
- BTC subió +94% en 2019 (recuperación post-bear 2018)

---

### 2.4 Test #3: Año 2020 Individual 🔴 CRÍTICO

**Propósito:** ¿Este es el año que destruye el bot?

**Configuración:**
```
Exchange:     Binance Spot
Symbol:       BTC-USDT
Strategy:     Multitimeframe
Start Date:   2020-01-01
End Date:     2020-12-31
Timeframe:    15m
```

**Click:** "Start Backtest"

**Cuando termine, ANOTA:**
- Net Profit %: __________
- Max Drawdown %: __________
- Win Rate %: __________
- Total Trades: __________

**Expectativa:**
- Net Profit: -40% a -60% ❌❌ (PEOR AÑO)
- BTC subió +305% (de $7.2k a $29k - PARABÓLICO)
- Bot probablemente entra/sale en BE constantemente

---

### 2.5 Test #4: Año 2021 Individual 🔴 CRÍTICO

**Propósito:** ¿También falla en peak parabólico?

**Configuración:**
```
Exchange:     Binance Spot
Symbol:       BTC-USDT
Strategy:     Multitimeframe
Start Date:   2021-01-01
End Date:     2021-12-31
Timeframe:    15m
```

**Click:** "Start Backtest"

**Cuando termine, ANOTA:**
- Net Profit %: __________
- Max Drawdown %: __________
- Win Rate %: __________
- Total Trades: __________

**Expectativa:**
- Net Profit: -30% a -50% ❌ (SEGUNDO PEOR AÑO)
- BTC subió +60% (de $29k a $46k peak, luego bajó a $46k)
- Volatilidad más alta que 2020 pero sigue siendo tendencia larga

---

## 📊 PASO 3: Guardar Resultados

### Crear archivo de resultados manualmente

Crea un archivo: `phase1_baseline_results.txt`

```
==================================================
FASE 1: BASELINE ANALYSIS 2019-2025
Versión: v9.3-RSI36
Fecha: 2025-12-28
==================================================

TEST 1: Baseline 2019-2025
--------------------------
Periodo: 2019-01-01 → 2025-10-17
Net Profit %: [TU RESULTADO]
Max Drawdown %: [TU RESULTADO]
Win Rate %: [TU RESULTADO]
Total Trades: [TU RESULTADO]
Sharpe Ratio: [TU RESULTADO]
Calmar Ratio: [TU RESULTADO]

TEST 2: Año 2019 Individual
----------------------------
Periodo: 2019-01-01 → 2019-12-31
Net Profit %: [TU RESULTADO]
Max Drawdown %: [TU RESULTADO]
Win Rate %: [TU RESULTADO]
Total Trades: [TU RESULTADO]

TEST 3: Año 2020 Individual 🔴
-------------------------------
Periodo: 2020-01-01 → 2020-12-31
Net Profit %: [TU RESULTADO]
Max Drawdown %: [TU RESULTADO]
Win Rate %: [TU RESULTADO]
Total Trades: [TU RESULTADO]

TEST 4: Año 2021 Individual 🔴
-------------------------------
Periodo: 2021-01-01 → 2021-12-31
Net Profit %: [TU RESULTADO]
Max Drawdown %: [TU RESULTADO]
Win Rate %: [TU RESULTADO]
Total Trades: [TU RESULTADO]

==================================================
CONCLUSIONES:
==================================================

Peor año: [2020 o 2021?]
Net Profit peor año: [RESULTADO]%

Suma 2020 + 2021: [RESULTADO]%
% del daño total causado por 2020-2021: [CALCULAR]%

Confirmación: v9.3-RSI36 colapsa en bull parabólico (2020-2021)
```

---

## 🎯 PASO 4: Análisis de Resultados

Una vez tengas los 4 tests completados, comparte el archivo `phase1_baseline_results.txt` conmigo.

**Voy a analizar:**
1. ¿Qué año es el peor? (probablemente 2020)
2. ¿Cuánto del daño total es causado por 2020-2021?
3. ¿2019 es neutral o positivo? (para entender límite)
4. ¿Hay patrones en Total Trades? (overtrading en parabólico?)

**Luego diseñaré v10.0-ROBUST** con parámetros optimizados para ambos regímenes.

---

## ⏱️ Timeline

**Hoy (2025-12-28):**
- Ejecutar 4 backtests (~2-3 horas total)
- Compartir resultados

**Mañana (2025-12-29):**
- Diseñar parámetros v10.0-ROBUST
- Ejecutar backtests de v10.0
- Validar robustez

**Objetivo:** v10.0-ROBUST listo en 2-3 días

---

## 🔧 Troubleshooting

### Problema: "No data available for this period"

**Solución:** Importar datos históricos
```bash
wsl bash -c 'cd /mnt/c/Users/ikerm/Desktop/Pruebas\ BOTTrading/TradingBot_Project && /root/.local/bin/jesse import-candles "Binance Perpetual Futures" "BTC-USDT" "2019-01-01"'
```

Espera 10-20 minutos mientras descarga datos.

---

### Problema: Jesse Web UI no carga (http://localhost:9000)

**Solución:**
```bash
# Matar procesos viejos
wsl --shutdown

# Esperar 10 segundos
sleep 10

# Iniciar servidor limpio
wsl bash -c 'cd /mnt/c/Users/ikerm/Desktop/Pruebas\ BOTTrading/TradingBot_Project && /root/.local/bin/jesse run'
```

---

### Problema: Backtest falla con error

**Revisa:**
1. ¿Estrategia = "Multitimeframe"? (no "Multitimeframe_v93_Complete")
2. ¿Symbol = "BTC-USDT"? (con guión, no barra)
3. ¿Exchange = "Binance Perpetual Futures"? (exacto)

---

## ✅ Checklist

Antes de empezar:
- [ ] Servidor Jesse corriendo (http://localhost:9000 accesible)
- [ ] Datos históricos 2019-2025 importados
- [ ] Navegador abierto en pestaña Backtest
- [ ] Archivo de resultados preparado para anotar

Durante los tests:
- [ ] Test #1: Baseline 2019-2025 ejecutado
- [ ] Test #2: Año 2019 ejecutado
- [ ] Test #3: Año 2020 ejecutado 🔴
- [ ] Test #4: Año 2021 ejecutado 🔴

Después:
- [ ] Resultados anotados en phase1_baseline_results.txt
- [ ] Archivo compartido conmigo
- [ ] Listo para Fase 2 (diseño v10.0-ROBUST)

---

**¿Listo para empezar?**

Ejecuta los 4 backtests y comparte los resultados. Mientras tanto, el bot Freqtrade v9.3 sigue corriendo en paper trading 😊
