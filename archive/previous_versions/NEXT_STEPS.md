# Proximos Pasos - Paper Trading v9.3-RSI36

**Fecha:** 2025-12-27
**Status:** Setup completado - Listo para configuracion de API keys

---

## ✅ Lo que YA esta hecho:

1. ✅ Jesse v1.11.0 verificado e instalado correctamente
2. ✅ Datos recientes importados (BTC-USDT desde 2025-11-01)
3. ✅ Archivos de configuracion creados:
   - `.env.example` (template para API keys)
   - `PAPER_TRADING_SETUP.md` (guia completa paso a paso)
   - `start_paper_trading.bat` (script de inicio rapido)
   - `import_recent_data.py` (importacion de datos)
   - `regime_monitor.py` (monitoring semanal de regimen)
4. ✅ Routes configurado para Binance Perpetual Futures BTC-USDT 15m
5. ✅ Estrategia v9.3-RSI36 lista (BE=1.35R, RSI=36/64, TP=3.0R)

---

## 📋 PROXIMOS PASOS (TU - USUARIO)

### PASO 1: Crear Cuenta en Binance Testnet (10 minutos)

1. Abre tu navegador
2. Ve a: https://testnet.binancefuture.com/
3. Click "Register" (esquina superior derecha)
4. Registrate con tu email
5. Verifica tu email
6. Inicia sesion

**Fondos testnet:** Binance te da automaticamente ~10,000 USDT virtuales

---

### PASO 2: Obtener API Keys de Testnet (5 minutos)

1. Una vez dentro de Binance Testnet
2. Click en tu email (esquina superior derecha)
3. Click "API Management"
4. Click "Create API"
5. Nombre: "Jesse Paper Trading v9.3"
6. Completa verificacion 2FA (si te lo pide)
7. **MUY IMPORTANTE:**
   - Copia el **API Key**
   - Copia el **Secret Key**
   - Guardalo en un lugar seguro (notepad temporal)
   - NO podras ver el Secret Key de nuevo

---

### PASO 3: Configurar .env con tus API Keys (2 minutos)

1. En tu proyecto, busca el archivo `.env.example`
2. Copia `.env.example` y renombralo a `.env`:
   ```
   Archivo: C:\Users\ikerm\Desktop\Pruebas BOTTrading\TradingBot_Project\.env.example
   Copiar como: C:\Users\ikerm\Desktop\Pruebas BOTTrading\TradingBot_Project\.env
   ```

3. Abre `.env` con Notepad
4. Reemplaza estas lineas:
   ```env
   BINANCE_TESTNET_API_KEY=pega_tu_api_key_aqui
   BINANCE_TESTNET_API_SECRET=pega_tu_secret_key_aqui
   ```

5. Guarda el archivo

**IMPORTANTE:** `.env` contiene tus keys, NUNCA lo compartas ni lo subas a git

---

### PASO 4: Iniciar Jesse Dashboard (PRIMERA VEZ)

Opcion A - Script automatico (Recomendado):

1. Doble click en: `start_paper_trading.bat`
2. Espera a que Jesse inicie (puede tardar 10-20 segundos)
3. Deberia aparecer: "Jesse is running on http://localhost:9000"

Opcion B - Manual:

1. Abre CMD (Command Prompt)
2. Ejecuta:
   ```cmd
   cd "C:\Users\ikerm\Desktop\Pruebas BOTTrading\TradingBot_Project"
   jesse run
   ```

---

### PASO 5: Configurar Paper Trading en Dashboard

1. Abre tu navegador
2. Ve a: http://localhost:9000
3. Deberia aparecer el Jesse Dashboard
4. Click en la tab "Live" (arriba)
5. Configura:
   - **Exchange:** Binance Perpetual Futures
   - **Paper Trading:** ON (activado)
   - **API Key:** Pega tu testnet API key
   - **API Secret:** Pega tu testnet secret key
   - **Symbol:** BTC-USDT
   - **Timeframe:** 15m
   - **Strategy:** Multitimeframe
6. Click "Start Trading"

---

### PASO 6: Verificar que Funciona

Dentro de 5-10 minutos deberia aparecer en la consola de Jesse:

```
[INFO] Connected to Binance Perpetual Futures (Testnet)
[INFO] Paper Trading Mode: ENABLED
[INFO] Monitoring BTC-USDT on 15m
[INFO] Strategy: Multitimeframe v9.3-RSI36
[INFO] Waiting for trading signals...
```

**Si aparece esto → TODO OK!**

---

### PASO 7: Monitoring Diario (Durante Paper Trading)

**CADA DIA a las 23:00 UTC:**

1. Abre Jesse dashboard: http://localhost:9000
2. Ve a la tab "Live" → "Metrics"
3. Anota en un Excel/Google Sheet:
   - Fecha
   - Total trades
   - Win rate
   - Net profit %
   - Max drawdown %
   - Balance actual
4. Revisa circuit breakers (ver tabla abajo)

**Circuit Breakers:**

| Metrica | Threshold | Accion |
|---------|-----------|--------|
| Max DD | -15% | Review urgente |
| Max DD | -20% | PAUSE trading |
| Max DD | -25% | STOP definitivo |
| Losing Streak | 15 | Review |
| Losing Streak | 20 | PAUSE |

---

### PASO 8: Monitoring Semanal de Regimen

**CADA DOMINGO (o cada 7 dias):**

1. Abre CMD
2. Ejecuta:
   ```cmd
   cd "C:\Users\ikerm\Desktop\Pruebas BOTTrading\TradingBot_Project"
   python regime_monitor.py
   ```

3. Lee el resultado:
   - **✅ FAVORABLE:** Continuar trading normalmente
   - **⚠️ WARNING:** Ejecutar DIARIAMENTE (no semanal), monitorear de cerca
   - **🔴 CRITICAL:** PAUSE trading, mercado cambio de regimen

---

## 🚨 Que Hacer Si Algo Sale Mal

### Problema: Jesse no inicia

```cmd
# Verifica que Jesse esta instalado:
jesse --version

# Deberia mostrar: jesse, version 1.11.0
```

Si no funciona, contactame.

---

### Problema: Jesse dice "Authentication failed"

**Posibles causas:**
1. API key incorrecta en `.env`
2. API key no tiene permisos de Futures activados

**Solucion:**
1. Ve a Binance Testnet → API Management
2. Click en tu API key → "Edit"
3. Asegurate que "Enable Futures" esta ON
4. Si sigue fallando, regenera nueva API key

---

### Problema: Jesse conecta pero no ejecuta trades

**Esto es NORMAL al inicio.**

v9.3-RSI36 espera a que:
- RSI alcance 36 (LONG) o 64 (SHORT)
- Condiciones de multi-timeframe se cumplan
- Puede tomar horas o dias hasta el primer trade

**Como verificar que funciona:**
- En Jesse console deberia decir: "Waiting for trading signals..."
- En Binance Testnet → Orders, NO deberia haber ordenes (porque no hay señal aun)

**Si pasan 3 dias sin ningun trade:**
- Es posible que el mercado este lateral (sin señales claras)
- Contactame para verificar

---

### Problema: Max DD alcanza -20% rapidamente

**ACCION INMEDIATA:**

1. Detener Jesse (Ctrl+C en la consola)
2. Ejecutar:
   ```cmd
   python regime_monitor.py
   ```
3. Si muestra CRITICAL → Mercado cambio de regimen
4. NO reanudar trading hasta nueva version (v10.0-ROBUST)
5. Contactame con los resultados

---

## 📊 Duracion del Paper Trading

### Fase 1: Local PC (1-2 semanas)

**Objetivo:** Validar que Jesse funciona sin errores

**Criterios de exito:**
- [ ] Jesse corre sin crashes
- [ ] Al menos 10 trades ejecutados
- [ ] Win rate >20%
- [ ] Max DD <-25%

**Si TODO OK → Migrar a VPS para Fase 1.5 (1-2 meses completos)**

---

## 📁 Archivos Importantes

```
TradingBot_Project/
│
├── .env                          ← TUS API KEYS (crear este)
├── .env.example                  ← Template de ejemplo
├── PAPER_TRADING_SETUP.md        ← Guia completa paso a paso
├── NEXT_STEPS.md                 ← Este archivo
├── start_paper_trading.bat       ← Script inicio rapido
├── import_recent_data.py         ← Importar datos
├── regime_monitor.py             ← Monitor semanal
├── DEPLOYMENT_GUIDE_CONSERVATIVE.md  ← Guia completa deployment
│
├── code/
│   └── routes.py                 ← Configuracion de trading
│   └── strategies/
│       └── Multitimeframe/
│           └── __init__.py       ← Estrategia v9.3-RSI36
```

---

## ✅ Checklist Pre-Trading

Antes de ejecutar `jesse run` por PRIMERA vez:

- [ ] Cuenta en Binance Testnet creada
- [ ] API keys de testnet obtenidas
- [ ] Archivo `.env` creado con keys correctas
- [ ] Leido `PAPER_TRADING_SETUP.md` completamente
- [ ] Excel/Google Sheet preparado para tracking diario
- [ ] `regime_monitor.py` ejecutado una vez (para verificar que funciona)

**Solo cuando TODO este marcado → Doble click en `start_paper_trading.bat`**

---

## 🎯 Resumen Ultra-Rapido

1. Crea cuenta Binance Testnet: https://testnet.binancefuture.com/
2. Obtén API keys (API Management)
3. Copia `.env.example` → `.env`
4. Edita `.env` con tus keys
5. Doble click `start_paper_trading.bat`
6. Abre navegador: http://localhost:9000
7. Click "Live" tab → Configurar → "Start Trading"
8. Monitorear diariamente

---

## 📞 Soporte

Si tienes problemas:

1. Lee `PAPER_TRADING_SETUP.md` seccion "Troubleshooting"
2. Verifica que `.env` tiene keys correctas
3. Ejecuta `jesse --version` para verificar instalacion
4. Si sigue sin funcionar, contactame con:
   - Screenshot del error
   - Contenido de la consola de Jesse (ultimas 20 lineas)
   - Que paso estabas ejecutando

---

**Estado:** LISTO para que TU configures Binance Testnet
**Siguiente:** Ejecutar Paso 1 (crear cuenta testnet)
**Tiempo estimado:** 20-30 minutos total (pasos 1-5)

**Good luck! 🚀**
