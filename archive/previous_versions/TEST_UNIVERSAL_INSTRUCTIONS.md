# TEST UNIVERSAL ROBUST - Instrucciones

**Estrategia:** UniversalRobust v1.0
**Parametros:** RSI 30/70, EMA 50/200, 2 ATR stop, 3:1 R:R (ESTANDAR - NO OPTIMIZADOS)

---

## Problema Identificado

Jesse research API no funciona correctamente en tu instalación. La única forma de ejecutar backtests es mediante la **interfaz web de Jesse**.

---

## INSTRUCCIONES PARA EJECUTAR EL BACKTEST

### 1. Asegúrate que los datos estén importados

Ya importaste los datos desde 2020-01-01. Verifica:

```bash
cd "C:\Users\ikerm\Desktop\Pruebas BOTTrading\TradingBot_Project"
```

### 2. Inicia el servidor Jesse

**Opcion A - Usando el bat:**
```bash
run_jesse_wsl.bat run
```

**Opcion B - Manual WSL:**
```bash
wsl bash -c "cd /mnt/c/Users/ikerm/Desktop/Pruebas\ BOTTrading/TradingBot_Project && /root/.local/bin/jesse run"
```

Espera a que aparezca:
```
Jesse is running on http://localhost:9000
```

### 3. Abre la interfaz web

Abre tu navegador en: **http://localhost:9000**

### 4. Configura el Backtest

En la interfaz web de Jesse:

1. **Tab "Backtest"** (arriba)
2. **Configuración:**
   - Exchange: `Binance Perpetual Futures`
   - Symbol: `BTC-USDT`
   - Timeframe: `15m`
   - Start Date: `2020-01-01`
   - End Date: `2025-12-27`
   - Strategy: `UniversalRobust`
   - Starting Balance: `10000`

3. **Click "Start Backtest"**

### 5. Espera Resultados

El backtest tardará 2-5 minutos. Jesse mostrará:

- Total Trades
- Net Profit %
- Win Rate %
- Max Drawdown %
- Sharpe Ratio
- Calmar Ratio

---

## CRITERIOS DE EXITO - BOT UNIVERSAL

Para que UniversalRobust sea considerado ROBUSTO (funciona en TODOS los regímenes):

| Criterio | Threshold | ¿Por qué? |
|----------|-----------|-----------|
| **Net Profit > 0%** | Positivo | Debe sobrevivir bull parabólico + bear market + recovery |
| **Max DD < -50%** | Mejor que -50% | Aceptable para 5.9 años multi-régimen |
| **Win Rate > 18%** | Mínimo 18% | Con R:R 3:1 es viable |
| **Sharpe > 0.3** | Positivo | Demuestra retorno ajustado por riesgo |

**Si PASA 4/4 criterios → UniversalRobust es ROBUSTO**
**Si PASA 2-3/4 → Tiene potencial, necesita ajustes**
**Si PASA 0-1/4 → Necesita rediseño completo**

---

## COMPARACIÓN vs v9.3-RSI36

Recuerda los resultados de v9.3 en 2020-2025:

```
v9.3-RSI36 (OVERFITTED a 2023-2025):
  Net Profit:   -66.9%  ❌
  Max DD:       -84.47% ❌
  Win Rate:     19.84%  ⚠️
  Sharpe:       -0.47   ❌
  Calmar:       -0.21   ❌

  Conclusión: COLAPSO total en periodo largo
```

**UniversalRobust debería ser MEJOR porque:**
1. Usa parámetros ESTANDAR (no optimizados)
2. No tiene overfitting temporal
3. Lógica simple: EMA crossover + RSI

---

## DESPUÉS DEL TEST

Una vez tengas los resultados, compara:

### SI UniversalRobust > v9.3 (Net Profit > -66.9%):
✅ **EXITO** - Estrategia universal es MEJOR que overfitted
→ Próximo paso: Deployment conservador con circuit breakers

### SI UniversalRobust ≈ v9.3 (Net Profit similar a -66.9%):
⚠️ **Problema profundo** - Ni optimizado ni universal funcionan
→ Próximo paso: Analizar por qué 2020-2021 destruye AMBAS estrategias

### SI UniversalRobust < v9.3 (Net Profit peor que -66.9%):
❌ **Simplificación excesiva** - Parámetros muy genéricos
→ Próximo paso: Añadir filtros adicionales (ADX, volume, etc.)

---

## NOTAS IMPORTANTES

1. **NO ejecutes backtests desde Python** - La API research no funciona en tu setup
2. **USA SIEMPRE la interfaz web** - Es la forma oficial y funciona
3. **Los datos YA están importados** - No necesitas reimportar (a menos que cambies de símbolo)
4. **UniversalRobust ya está en routes.py** - No necesitas modificar nada

---

## TROUBLESHOOTING

### Jesse no inicia (puerto 9000 ocupado)
```bash
wsl pkill -f "jesse run"
# Espera 5 segundos
run_jesse_wsl.bat run
```

### Backtest falla "No candles found"
Reimporta datos:
```bash
python3 import_candles.py
```

### "Strategy UniversalRobust not found"
Verifica routes.py:
```bash
cat code/routes.py | grep UniversalRobust
```
Debe mostrar:
```python
('Binance Perpetual Futures', 'BTC-USDT', '15m', 'UniversalRobust'),
```

---

## PRÓXIMOS PASOS DESPUÉS DE LOS RESULTADOS

1. **Si UniversalRobust pasa criterios:**
   - Deployment en paper trading
   - Monitoring con circuit breakers
   - Comparar con v9.3 en paper trading paralelo

2. **Si UniversalRobust falla:**
   - Analizar trades año por año (2020, 2021, 2022, 2023, 2024, 2025)
   - Identificar en qué régimen falla más
   - Diseñar filtros específicos para ese régimen

3. **Documentar resultados:**
   - Crear `UNIVERSAL_ROBUST_RESULTS.md`
   - Captura de pantalla de métricas
   - Análisis comparativo vs v9.3

---

**Buena suerte con el test!**
