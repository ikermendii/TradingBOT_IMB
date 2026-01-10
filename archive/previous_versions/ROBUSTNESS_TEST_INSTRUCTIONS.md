# 🧪 Instrucciones Rápidas - Tests de Robustez

**Versión a testear:** v9.3-RSI36
**Prioridad:** ALTA (tests críticos antes de deployment)

---

## 📋 Test 1: Diferentes Periodos de Tiempo

### Objetivo
Validar que v9.3-RSI36 funciona en diferentes condiciones de mercado (bull, bear, transición).

### Tests a Ejecutar

#### Test 1.1: Bull Market 2023 ⏳

**Periodo:** 2023-01-01 a 2023-12-31 (1 año)
**Contexto:** BTC +150% en el año, mercado alcista fuerte

**Comando Jesse:**
```bash
python run_backtest.py
# En Jesse web interface:
# Start Date: 2023-01-01
# Finish Date: 2023-12-31
```

**Métricas a capturar:**
- [ ] Screenshot de resultados completos
- [ ] Net Profit
- [ ] Win Rate
- [ ] Max DD
- [ ] Sharpe Ratio
- [ ] Total Trades

**Expectativa:**
- ✅ Net Profit positivo (objetivo: >+30%)
- ✅ Sharpe > 0.8
- ✅ Max DD < -30%

---

#### Test 1.2: Bear to Bull 2024 ⏳

**Periodo:** 2024-01-01 a 2024-12-31 (1 año)
**Contexto:** BTC +120% en el año, rally post-halving

**Comando Jesse:**
```bash
python run_backtest.py
# Start Date: 2024-01-01
# Finish Date: 2024-12-31
```

**Métricas a capturar:**
- [ ] Screenshot de resultados completos
- [ ] Net Profit
- [ ] Win Rate
- [ ] Max DD
- [ ] Sharpe Ratio
- [ ] Total Trades

**Expectativa:**
- ✅ Net Profit positivo (objetivo: >+25%)
- ✅ Sharpe > 0.8
- ✅ Max DD < -25%

---

#### Test 1.3: Reciente 2025 ⏳

**Periodo:** 2025-01-01 a 2025-10-17 (10 meses)
**Contexto:** Datos más frescos, out-of-sample

**Comando Jesse:**
```bash
python run_backtest.py
# Start Date: 2025-01-01
# Finish Date: 2025-10-17
```

**Métricas a capturar:**
- [ ] Screenshot de resultados completos
- [ ] Net Profit
- [ ] Win Rate
- [ ] Max DD
- [ ] Sharpe Ratio
- [ ] Total Trades

**Expectativa:**
- ✅ Net Profit positivo (objetivo: >+15%)
- ✅ Sharpe > 0.7
- ✅ Max DD < -25%

---

#### Test 1.4: Bear Market 2022 ⏳ (CRÍTICO)

**Periodo:** 2022-01-01 a 2022-12-31 (1 año)
**Contexto:** BTC -64% en el año, bear market brutal

**Comando Jesse:**
```bash
python run_backtest.py
# Start Date: 2022-01-01
# Finish Date: 2022-12-31
```

**Métricas a capturar:**
- [ ] Screenshot de resultados completos
- [ ] Net Profit (puede ser negativo, solo que no colapso)
- [ ] Win Rate
- [ ] Max DD (CRÍTICO)
- [ ] Sharpe Ratio
- [ ] Total Trades

**Expectativa (RELAJADA para bear market):**
- ⚠️ Net Profit puede ser negativo (objetivo: >-20%)
- ⚠️ Sharpe puede ser bajo (objetivo: >-0.5)
- ✅ Max DD < -50% (CRÍTICO: sobrevivir)
- ✅ Win Rate > 15%

**NOTA:** Si sobrevive 2022 sin colapsar (DD <-50%), es EXCELENTE señal de robustez.

---

## 📋 Test 2: Altcoins (ETH-USDT)

### Objetivo
Validar si v9.3-RSI36 es generalizable a otros pares crypto.

#### Test 2.1: ETH-USDT (2023-2025) ⏳

**Periodo:** 2023-01-01 a 2025-10-17 (2.78 años)
**Par:** ETH-USDT (Binance Perpetual Futures)

**Pasos:**
1. Abrir `run_backtest.py`
2. Cambiar línea del símbolo:
   ```python
   # ANTES:
   'symbol': 'BTC-USDT',

   # DESPUÉS:
   'symbol': 'ETH-USDT',
   ```
3. Ejecutar backtest

**Comando Jesse:**
```bash
python run_backtest.py
```

**Métricas a capturar:**
- [ ] Screenshot de resultados completos
- [ ] Net Profit
- [ ] Win Rate
- [ ] Max DD
- [ ] Sharpe Ratio
- [ ] Total Trades
- [ ] R:R Ratio

**Expectativa (más relajada que BTC):**
- ✅ Net Profit positivo (objetivo: >+40%)
- ⚠️ Sharpe > 0.5 (ETH más volátil)
- ⚠️ Max DD < -35% (ETH más volátil)
- ✅ Win Rate > 18%

**NOTA:** Si ETH también da profit positivo con Sharpe >0.5, confirma que la estrategia NO está overfitted a BTC específicamente.

---

## 📋 Test 4: Stress Testing (Crashes Históricos)

### Objetivo
Validar que v9.3-RSI36 sobrevive a eventos extremos de mercado.

#### Test 4.1: FTX Collapse (Nov 2022) ⏳

**Periodo:** 2022-11-01 a 2022-11-30 (1 mes)
**Contexto:** BTC -20% en ~1 semana, pánico extremo

**Comando Jesse:**
```bash
python run_backtest.py
# Start Date: 2022-11-01
# Finish Date: 2022-11-30
```

**Métricas a capturar:**
- [ ] Screenshot de resultados completos
- [ ] Net Profit
- [ ] Max DD (CRÍTICO)
- [ ] Largest Loss
- [ ] ¿Sobrevivió sin liquidación?

**Expectativa:**
- ⚠️ Net Profit puede ser muy negativo
- ✅ Max DD < -40% (objetivo: sobrevivir)
- ✅ No liquidación
- ✅ Recovery posible después del evento

---

#### Test 4.2: Luna Crash (Mayo 2022) ⏳

**Periodo:** 2022-05-01 a 2022-05-31 (1 mes)
**Contexto:** BTC -25% en 1 semana, colapso de Terra/Luna

**Comando Jesse:**
```bash
python run_backtest.py
# Start Date: 2022-05-01
# Finish Date: 2022-05-31
```

**Métricas a capturar:**
- [ ] Screenshot de resultados completos
- [ ] Net Profit
- [ ] Max DD (CRÍTICO)
- [ ] Largest Loss
- [ ] ¿Sobrevivió sin liquidación?

**Expectativa:**
- ⚠️ Net Profit puede ser muy negativo
- ✅ Max DD < -40%
- ✅ No liquidación

---

#### Test 4.3: Banking Crisis (Marzo 2023) ⏳

**Periodo:** 2023-03-01 a 2023-03-31 (1 mes)
**Contexto:** SVB collapse, volatilidad extrema

**Comando Jesse:**
```bash
python run_backtest.py
# Start Date: 2023-03-01
# Finish Date: 2023-03-31
```

**Métricas a capturar:**
- [ ] Screenshot de resultados completos
- [ ] Net Profit
- [ ] Max DD
- [ ] Volatilidad de equity curve

**Expectativa:**
- ⚠️ Alta volatilidad esperada
- ✅ Max DD < -35%
- ✅ Profit puede ser positivo o ligeramente negativo

---

## 📊 Cómo Ejecutar los Tests

### Método 1: Jesse Web Interface (Recomendado)

1. Abrir navegador en `http://localhost:9000` (si Jesse está corriendo)
2. O ejecutar:
   ```bash
   python run_backtest.py
   ```
3. Cambiar fechas en interfaz web
4. Click en "Start Backtest"
5. Capturar screenshot de resultados
6. Guardar screenshots en carpeta `robustness_tests/`

### Método 2: Modificar run_backtest.py

Editar `run_backtest.py` y cambiar:
```python
backtest(
    config={
        # ...
        'start_date': '2022-01-01',  # ← CAMBIAR AQUÍ
        'finish_date': '2022-12-31', # ← CAMBIAR AQUÍ
        'symbol': 'BTC-USDT',        # ← O CAMBIAR SÍMBOLO
        # ...
    }
)
```

Luego ejecutar:
```bash
python run_backtest.py
```

---

## 📋 Template de Resultados

Para cada test, documentar:

```markdown
### Test X.Y: [Nombre del Test]

**Periodo:** YYYY-MM-DD a YYYY-MM-DD
**Símbolo:** BTC-USDT / ETH-USDT
**Contexto:** [Descripción del mercado]

**Resultados:**
```
Total Trades:    XXX
Win Rate:        XX.XX%
Net Profit:      +XX.XX%
Max Drawdown:    -XX.XX%
Sharpe Ratio:    X.XX
Calmar Ratio:    X.XX
Annual Return:   XX.XX%
R:R Ratio:       X.XX
Expectancy:      $XX.XX

Avg Win:         $XXX.XX
Avg Loss:        $XXX.XX
Largest Win:     $XXX.XX
Largest Loss:    -$XXX.XX
```

**Screenshot:** [Adjuntar captura de pantalla]

**Análisis:**
- ✅/❌ Cumple criterio de Net Profit
- ✅/❌ Cumple criterio de Sharpe
- ✅/❌ Cumple criterio de Max DD
- ✅/❌ Cumple criterio de Win Rate

**Conclusión:** [✅ PASS / ⚠️ MARGINAL / ❌ FAIL]
```

---

## ✅ Criterios de Éxito

### Test 1: Diferentes Periodos
**PASS si:**
- Al menos 3/4 periodos tienen Net Profit positivo
- Bear market 2022 tiene DD < -50%
- Promedio de Sharpe en periodos positivos > 0.8

### Test 2: Altcoins (ETH)
**PASS si:**
- ETH-USDT tiene Net Profit positivo
- Sharpe > 0.5
- Max DD < -40%

### Test 4: Stress Testing
**PASS si:**
- Sobrevive 3/3 eventos sin liquidación
- Max DD en cada evento < -50%
- Recovery visible después de cada evento

---

## 🎯 Orden Recomendado de Ejecución

1. **Test 1.1:** Bull Market 2023 (debería ir muy bien)
2. **Test 1.4:** Bear Market 2022 (CRÍTICO - test duro)
3. **Test 2.1:** ETH-USDT 2023-2025 (validar generalización)
4. **Test 1.2:** 2024 (debería ir bien)
5. **Test 4.1:** FTX Collapse (stress test)
6. **Test 1.3:** 2025 (out-of-sample)
7. **Test 4.2:** Luna Crash (stress test)
8. **Test 4.3:** Banking Crisis (stress test)

**Tiempo estimado:** 2-3 horas para ejecutar todos los tests

---

## 📝 Documentación

Cuando completes los tests, actualizar:
- `ROBUSTNESS_TESTING_PLAN.md` con resultados
- Crear carpeta `robustness_tests/screenshots/`
- Guardar todos los screenshots con nombres descriptivos

**Ejemplo de nombres:**
- `test1.1_bull2023_btc.png`
- `test1.4_bear2022_btc.png`
- `test2.1_eth_2023-2025.png`
- `test4.1_ftx_collapse.png`

---

**Documento creado:** 2025-12-27
**Listo para ejecutar:** SÍ
**Siguiente paso:** Ejecutar Test 1.1 (Bull Market 2023)
