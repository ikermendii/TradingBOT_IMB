# INICIAR PAPER TRADING - Instrucciones Finales

**Fecha:** 2025-12-27
**Todo configurado:** SI ✅
**Listo para iniciar:** SI ✅

---

## ✅ CONFIGURACION COMPLETADA

Todo esta listo para iniciar paper trading:

- ✅ Jesse v1.11.0 instalado
- ✅ Datos BTC-USDT importados (desde 2025-11-01)
- ✅ API keys de Binance Testnet configuradas en .env
- ✅ Routes configurado (Binance Perpetual Futures, BTC-USDT, 15m)
- ✅ Estrategia v9.3-RSI36 (BE=1.35R, RSI=36/64, TP=3.0R)
- ✅ PostgreSQL funcionando
- ✅ Documentacion completa creada

---

## 🚀 COMO INICIAR PAPER TRADING

### Metodo 1: Script Automatico (Mas Facil)

1. Busca el archivo: `start_paper_trading.bat`
2. Doble click en el
3. Espera 10-20 segundos a que Jesse inicie
4. Veras el mensaje: "Jesse is running on http://localhost:9000"
5. Continua al PASO SIGUIENTE abajo

### Metodo 2: Manual (CMD)

1. Abre Command Prompt (CMD)
2. Ejecuta:
   ```cmd
   cd "C:\Users\ikerm\Desktop\Pruebas BOTTrading\TradingBot_Project"
   jesse run
   ```
3. Espera a que Jesse inicie
4. Continua al PASO SIGUIENTE abajo

---

## 📊 PASO SIGUIENTE: Configurar Dashboard

Una vez que Jesse este corriendo:

### 1. Abrir Dashboard

- Abre tu navegador (Chrome/Firefox/Edge)
- Ve a: **http://localhost:9000**
- Deberia aparecer el Jesse Dashboard

### 2. Configurar Live Trading

En el dashboard:

1. **Click en la tab "Live"** (arriba en el menu)

2. **Configurar parametros:**
   - **Exchange:** Binance Perpetual Futures
   - **Paper Trading:** ✅ **ON** (ACTIVAR)
   - **Symbol:** BTC-USDT
   - **Timeframe:** 15m
   - **Strategy:** Multitimeframe

3. **Ingresar API Keys:**
   - **API Key:** `DA945RCR2GI6gaGbBvt0bnaOeLfBMEj7EReKQP9imbJBnZWzObTMEAL3fmMG2hHj`
   - **Secret:** `DK6QKnCnUDMUPwC4pVEkIgvmcxXKlh0cfo8nVPxryjoFzmaC40omVHreEHSkOH9H`

4. **Click "Start Trading"**

### 3. Verificar Conexion

En la consola de Jesse (la ventana CMD) deberia aparecer:

```
[INFO] Connected to Binance Perpetual Futures (Testnet)
[INFO] Paper Trading Mode: ENABLED
[INFO] Monitoring BTC-USDT on 15m timeframe
[INFO] Strategy: Multitimeframe v9.3-RSI36
[INFO] Waiting for trading signals...
```

**Si ves esto → TODO OK!** ✅

---

## ⏱️ Que Esperar Ahora

### Primeras Horas (0-24h)

- Jesse esta MONITOREANDO el mercado
- Esperando a que RSI alcance 36 (LONG) o 64 (SHORT)
- **Es NORMAL que NO haya trades inmediatamente**
- Puede tomar horas o incluso dias hasta el primer trade

### Primer Trade (cuando ocurra)

En la consola veras algo como:

```
[INFO] Signal detected: LONG at RSI 35.8
[INFO] Opening position: LONG BTC-USDT
[INFO] Entry: $98,450.00
[INFO] Stop Loss: $97,850.00
[INFO] Take Profit: $100,250.00
```

### Durante el Trading

- Jesse ejecutara trades automaticamente
- Veras las actualizaciones en la consola
- Puedes ver metricas en el dashboard (http://localhost:9000)
- Balance, posiciones abiertas, P&L, etc.

---

## 📋 MONITORING OBLIGATORIO

### DIARIO (cada dia a las 23:00 UTC):

1. Abre el dashboard: http://localhost:9000
2. Ve a "Live" → "Metrics"
3. Anota en Excel/Google Sheet:
   - Fecha
   - Total trades
   - Win rate
   - Net profit %
   - Max drawdown %
   - Balance actual

### SEMANAL (cada domingo):

```cmd
cd "C:\Users\ikerm\Desktop\Pruebas BOTTrading\TradingBot_Project"
python regime_monitor.py
```

**Si muestra CRITICAL → PAUSE trading inmediatamente**

---

## 🚨 CIRCUIT BREAKERS - ALERTAS CRITICAS

Revisa DIARIAMENTE estas metricas:

| Metrica | Threshold | Accion |
|---------|-----------|--------|
| **Max DD** | -15% | 🔍 Review urgente - analizar trades |
| **Max DD** | -20% | ⏸️ **PAUSE** trading inmediatamente |
| **Max DD** | -25% | 🛑 **STOP** definitivo |
| **Losing Streak** | 15 | 🔍 Review detallado |
| **Losing Streak** | 20 | ⏸️ **PAUSE** y analizar |
| **Win Rate <20%** | 1 semana | 🔍 Posible regime change |

**Como PAUSAR trading:**
1. En el dashboard: Click "Stop Trading"
2. O en CMD: Ctrl+C para detener Jesse

---

## ⚠️ IMPORTANTE: Mantener PC Encendido

### Durante Etapa 1.1 (1-2 semanas):

- **TU PC DEBE ESTAR ENCENDIDO 24/7**
- Jesse debe correr continuamente
- Si apagas el PC, Jesse se detiene
- Perderias señales de trading

### Despues de Etapa 1.1:

- Migrar a VPS (servidor cloud)
- Ya no necesitas tu PC encendido
- Ver: DEPLOYMENT_GUIDE_CONSERVATIVE.md seccion "Migracion a VPS"

---

## 🛠️ TROUBLESHOOTING

### Jesse no inicia

**Error:** "Port 9000 already in use"

**Solucion:**
1. Otro proceso esta usando el puerto 9000
2. Cierra cualquier otro Jesse que este corriendo
3. O cambia el puerto en .env: `APP_PORT=9001`

---

### Dashboard no abre (localhost:9000 no carga)

**Posibles causas:**
1. Jesse aun esta iniciando (espera 30 segundos)
2. Firewall bloqueando puerto 9000
3. Jesse inicio con error (revisa la consola CMD)

**Solucion:**
- Revisa la consola de Jesse, deberia decir "running on http://localhost:9000"
- Si ves errores, copia el mensaje y contactame

---

### "Authentication failed" al conectar Testnet

**Causa:** API keys incorrectas o sin permisos

**Solucion:**
1. Ve a Binance Testnet: https://testnet.binancefuture.com/
2. Click tu email → "API Management"
3. Verifica que "Enable Futures" esta activado
4. Si no funciona, regenera nueva API key
5. Actualiza .env con las nuevas keys
6. Reinicia Jesse

---

### Jesse conecta pero no ejecuta trades (3+ dias)

**Esto podria ser NORMAL**

v9.3-RSI36 espera condiciones especificas:
- RSI alcance 36 (LONG) o 64 (SHORT)
- Multi-timeframe conditions
- Puede tomar dias en mercado lateral

**Como verificar si funciona:**
1. En consola debe decir: "Waiting for trading signals..."
2. En Binance Testnet → Orders: NO deberia haber ordenes (porque no hay señal)
3. Si pasan 5 dias sin trades, contactame

---

### Max DD alcanza -20% rapidamente

**ACCION INMEDIATA:**

1. ⏸️ **PAUSE trading** (Stop en dashboard o Ctrl+C)
2. Ejecutar:
   ```cmd
   python regime_monitor.py
   ```
3. Si muestra **CRITICAL** → Mercado cambio de regimen
4. **NO reanudar trading** hasta nueva version (v10.0-ROBUST)
5. Contactame con resultados

---

## 📊 PROXIMOS HITOS

### Hito 1: Primer Trade (0-3 dias)

- Jesse ejecuta su primer trade
- Verifica que aparece en Binance Testnet
- Anota en spreadsheet

### Hito 2: 10 Trades (1-2 semanas)

- Criterios de exito Etapa 1.1:
  - [ ] Win rate >20%
  - [ ] Max DD <-25%
  - [ ] Jesse corre sin crashes

**Si TODO OK → Migrar a VPS (Etapa 1.2)**

### Hito 3: 30 Trades (1-2 meses)

- Completar Fase 1 completa
- Decidir si proceder a Fase 2 (Live Micro $500)
- O esperar v10.0-ROBUST

---

## 📁 ARCHIVOS DE REFERENCIA

Durante paper trading, consulta estos archivos:

- **[PAPER_TRADING_SETUP.md](PAPER_TRADING_SETUP.md)** - Guia paso a paso completa
- **[DEPLOYMENT_GUIDE_CONSERVATIVE.md](DEPLOYMENT_GUIDE_CONSERVATIVE.md)** - Plan 4 fases
- **[PROJECT_STATUS.md](PROJECT_STATUS.md)** - Estado actual del proyecto
- **[CRITICAL_FINDING_2020-2021.md](CRITICAL_FINDING_2020-2021.md)** - Hallazgo critico
- **[ROBUSTNESS_TEST_RESULTS.md](ROBUSTNESS_TEST_RESULTS.md)** - Tests de robustez

---

## 🎯 CHECKLIST FINAL PRE-START

Antes de ejecutar `start_paper_trading.bat`:

- [x] Cuenta Binance Testnet creada
- [x] API keys obtenidas
- [x] Archivo .env configurado con keys
- [x] Jesse v1.11.0 instalado
- [x] Datos BTC-USDT importados
- [x] Routes configurado (BTC-USDT 15m)
- [x] Estrategia v9.3-RSI36 lista
- [ ] **Excel/Google Sheet preparado** para tracking diario
- [ ] **Leido PAPER_TRADING_SETUP.md**
- [ ] **Ejecutado regime_monitor.py** (para verificar que funciona)

**Solo falta que TU:**
1. Prepares spreadsheet de tracking
2. Leas PAPER_TRADING_SETUP.md (opcional, ya tienes todo aqui)
3. Ejecutes regime_monitor.py una vez (para test)

---

## 🚀 CUANDO ESTES LISTO

### EJECUTA:

**Opcion 1:**
- Doble click en: `start_paper_trading.bat`

**Opcion 2:**
```cmd
cd "C:\Users\ikerm\Desktop\Pruebas BOTTrading\TradingBot_Project"
jesse run
```

### LUEGO:
1. Abre navegador: http://localhost:9000
2. Tab "Live"
3. Configurar (Exchange, Paper Trading ON, API keys)
4. "Start Trading"

---

## 📞 SOPORTE

Si tienes problemas:

1. Lee seccion TROUBLESHOOTING arriba
2. Revisa PAPER_TRADING_SETUP.md
3. Si sigue fallando, contactame con:
   - Screenshot del error
   - Ultimas 20 lineas de consola de Jesse
   - Que paso estabas ejecutando

---

**Todo listo!** 🎉

**Proximo paso:** Doble click en `start_paper_trading.bat`

**Good luck con el paper trading!** 🚀📈
