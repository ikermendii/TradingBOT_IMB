# Paper Trading Setup - Paso a Paso

**Version:** v9.3-RSI36
**Fecha:** 2025-12-27
**Fase:** 1 - Paper Trading Local

---

## PASO 1: Configurar Binance Testnet

### 1.1 Crear Cuenta en Testnet

1. Ve a: https://testnet.binancefuture.com/
2. Haz clic en "Register" (esquina superior derecha)
3. Registrate con tu email
4. Verifica tu email
5. Inicia sesion

### 1.2 Obtener API Keys

1. Una vez dentro, ve a la esquina superior derecha
2. Haz clic en tu email → "API Management"
3. Haz clic en "Create API"
4. Dale un nombre: "Jesse Paper Trading"
5. Completa la verificacion 2FA (si aplica)
6. **IMPORTANTE**: Copia y guarda:
   - API Key
   - Secret Key

   **NUNCA podras ver el Secret Key de nuevo**

### 1.3 Verificar Fondos Testnet

- Binance Testnet te da **fondos virtuales automaticamente** (10,000 USDT)
- Para agregar mas fondos virtuales:
  1. Ve a "Wallet" → "Futures Wallet"
  2. Deberia haber un boton "Get Test Funds" o similar
  3. Si no, los fondos ya estan disponibles

---

## PASO 2: Configurar Jesse para Paper Trading

### 2.1 Crear Archivo .env

```bash
# En tu proyecto:
cd "C:\Users\ikerm\Desktop\Pruebas BOTTrading\TradingBot_Project"

# Copia el archivo ejemplo
copy .env.example .env
```

### 2.2 Editar .env con tus Credenciales

Abre `.env` con notepad y reemplaza:

```env
BINANCE_TESTNET_API_KEY=tu_api_key_de_testnet_aqui
BINANCE_TESTNET_API_SECRET=tu_secret_key_de_testnet_aqui
```

### 2.3 Verificar routes.py

Tu archivo `code/routes.py` ya esta configurado correctamente:

```python
routes = [
    ('Binance Perpetual Futures', 'BTC-USDT', '15m', 'Multitimeframe'),
]

extra_candles = [
    ('Binance Perpetual Futures', 'BTC-USDT', '1h'),
    ('Binance Perpetual Futures', 'BTC-USDT', '4h'),
]
```

**Status:** OK - No cambiar nada

---

## PASO 3: Iniciar Paper Trading

### IMPORTANTE: Dos Modos Disponibles

Jesse tiene 2 formas de ejecutar paper trading:

#### Opcion A: Jesse Dashboard (Recomendado para principiantes)

```bash
cd "C:\Users\ikerm\Desktop\Pruebas BOTTrading\TradingBot_Project"
jesse run
```

Luego:
1. Abre tu navegador en: http://localhost:9000
2. Ve a la tab "Live"
3. Configura:
   - Exchange: Binance Perpetual Futures
   - Paper Trading: ON
   - API Keys: Ingresa tus testnet keys
4. Click "Start"

#### Opcion B: Jesse CLI (Modo avanzado)

```bash
cd "C:\Users\ikerm\Desktop\Pruebas BOTTrading\TradingBot_Project"
jesse live --paper-trading
```

**IMPORTANTE:** Este comando requiere que `.env` este configurado correctamente.

---

## PASO 4: Monitoring Durante Paper Trading

### 4.1 Que Observar

Mientras Jesse esta corriendo, monitorea:

1. **Console Output:**
   - "Connected to Binance Testnet" (OK)
   - "Position opened: LONG BTC-USDT" (trade abierto)
   - "Position closed: profit +X%" (trade cerrado)

2. **Jesse Dashboard (si usaste Opcion A):**
   - Balance actual
   - Posiciones abiertas
   - Trades ejecutados
   - P&L en tiempo real

3. **Binance Testnet Website:**
   - Ve a: https://testnet.binancefuture.com/
   - Inicia sesion
   - Ve a "Orders" → "Order History"
   - Verifica que las ordenes de Jesse aparecen ahi

### 4.2 Circuit Breakers - MONITOREO OBLIGATORIO

Revisa DIARIAMENTE:

| Metrica | Threshold | Accion |
|---------|-----------|--------|
| **Max DD** | -15% | Review urgente - analizar trades |
| **Max DD** | -20% | PAUSE trading inmediatamente |
| **Max DD** | -25% | STOP - esperar v10.0-ROBUST |
| **Losing Streak** | 15 | Review detallado |
| **Losing Streak** | 20 | PAUSE y analizar |
| **Win Rate** | <20% por 1 semana | Review - posible regime change |
| **2 semanas negativas** | Profit <0% | PAUSE y ejecutar regime_monitor.py |

### 4.3 Monitoring de Regimen (SEMANAL)

**OBLIGATORIO cada domingo:**

```bash
cd "C:\Users\ikerm\Desktop\Pruebas BOTTrading\TradingBot_Project"
python regime_monitor.py
```

Si el monitor reporta:
- **FAVORABLE:** Continuar trading normalmente
- **WARNING:** Ejecutar DIARIAMENTE (no semanal)
- **CRITICAL:** PAUSE trading, analizar situacion

---

## PASO 5: Registro de Performance

### 5.1 Crear Spreadsheet de Tracking

Crea un Google Sheet o Excel con estas columnas:

| Fecha | Trades | Win Rate | Net Profit | Max DD | Balance | Notas |
|-------|--------|----------|------------|--------|---------|-------|
| 2025-12-27 | 0 | - | 0% | 0% | $10,000 | Inicio paper trading |
| 2025-12-28 | 2 | 50% | +0.5% | -0.2% | $10,050 | 1W, 1L |
| ... | ... | ... | ... | ... | ... | ... |

### 5.2 Registro Diario (5 minutos)

Cada dia a las 23:00 UTC:

1. Abre Jesse dashboard
2. Anota en spreadsheet:
   - Total trades ejecutados hoy
   - Win rate actual
   - Net profit total
   - Max DD
   - Balance actual
3. Si hubo trades, anota observaciones:
   - "Entrada correcta en RSI 36, cerro en TP 3.0R - OK"
   - "Cerro en BE, precio continuo sin el bot - normal"
   - "Losing streak 5 - dentro de esperado"

---

## PASO 6: Duracion del Paper Trading

### Fase 1: Local PC (1-2 semanas)

**Objetivo:** Validar que Jesse funciona correctamente con Binance Testnet

**Criterios de exito:**
- [ ] Jesse se conecta sin errores
- [ ] Ejecuta al menos 10 trades
- [ ] Win rate >20%
- [ ] Max DD <-25%
- [ ] No hay crashes/errores criticos

**Si TODOS los criterios se cumplen:**
→ Continuar a Fase 1.5 (VPS)

**Si algun criterio FALLA:**
→ STOP, analizar problema antes de continuar

### Fase 1.5: VPS Migration (1-2 meses)

**Solo si Fase 1 fue exitosa**

Migrar Jesse a VPS para operar 24/7 sin tu PC encendido.

Referencia: [DEPLOYMENT_GUIDE_CONSERVATIVE.md](DEPLOYMENT_GUIDE_CONSERVATIVE.md) seccion "Migracion a VPS"

---

## PASO 7: Troubleshooting

### Problema 1: Jesse no se conecta a Binance Testnet

**Error:** "Authentication failed" o similar

**Solucion:**
1. Verifica que API keys en `.env` son correctas
2. Verifica que API key tiene permisos de "Futures Trading" activados
3. En Binance Testnet → API Management → Edit → Enable "Enable Futures"
4. Regenera API keys si es necesario

### Problema 2: No ejecuta trades

**Sintoma:** Jesse corre pero no abre posiciones

**Posibles causas:**
1. **RSI no alcanza 36/64:** Normal - esperar a que condiciones se cumplan
2. **Balance insuficiente:** Verifica en Testnet que tienes fondos
3. **Paper trading no activado:** Verifica que `--paper-trading` flag esta activo

**Como verificar:**
```bash
# En la consola de Jesse, deberia mostrar:
[INFO] Paper Trading Mode: ENABLED
[INFO] Exchange: Binance Perpetual Futures (Testnet)
```

### Problema 3: Jesse se desconecta frecuentemente

**Sintoma:** "Connection lost", "Reconnecting..."

**Solucion:**
1. Verifica tu conexion a internet
2. Binance Testnet puede tener downtime ocasional (normal)
3. Jesse reintenta automaticamente
4. Si es frecuente (>5 veces/dia), considera:
   - Cambiar de ISP
   - Usar VPS con mejor uptime
   - Contactar soporte de Binance Testnet

### Problema 4: Drawdown mayor a esperado

**Sintoma:** Max DD alcanza -20% rapidamente

**Accion INMEDIATA:**
1. PAUSE trading (detener Jesse)
2. Ejecutar regime monitor:
   ```bash
   python regime_monitor.py
   ```
3. Si regime = CRITICAL → NO reanudar hasta nueva version
4. Analizar ultimos 20 trades:
   - Muchos BE exits? (regime cambio)
   - Losing streak >15? (mala racha o regime)
   - Win rate <15%? (definitivamente regime cambio)

---

## PASO 8: Siguiente Fase (Cuando Paper Trading Exitoso)

Una vez que Fase 1 y 1.5 sean exitosos (1-2 meses total):

1. Revisar resultados en [DEPLOYMENT_GUIDE_CONSERVATIVE.md](DEPLOYMENT_GUIDE_CONSERVATIVE.md)
2. Decidir si proceder a Fase 2: Live Micro ($500-1k)
3. O esperar a v10.0-ROBUST (re-optimizacion 2019-2025)

**Mi recomendacion:**
- Si regime monitor = FAVORABLE durante todo paper trading → Fase 2
- Si regime monitor = WARNING/CRITICAL en algun momento → Esperar v10.0

---

## Checklist Pre-Trading

Antes de ejecutar `jesse live` por PRIMERA vez:

- [ ] Binance Testnet account creada
- [ ] API keys de testnet obtenidas
- [ ] `.env` configurado con keys correctas
- [ ] Datos importados (ejecutaste `import_recent_data.py`)
- [ ] `routes.py` verificado (Binance Perpetual Futures, BTC-USDT, 15m)
- [ ] Spreadsheet de tracking creado
- [ ] Leido [DEPLOYMENT_GUIDE_CONSERVATIVE.md](DEPLOYMENT_GUIDE_CONSERVATIVE.md)
- [ ] `regime_monitor.py` testeado (ejecutado una vez para verificar que funciona)

**Solo cuando TODOS los items esten marcados → Iniciar paper trading**

---

## Comandos Rapidos

```bash
# Importar datos recientes
python import_recent_data.py

# Monitoring de regimen (semanal)
python regime_monitor.py

# Iniciar Jesse dashboard
jesse run
# Luego abrir: http://localhost:9000

# Iniciar paper trading CLI (alternativa)
jesse live --paper-trading

# Detener Jesse
# Ctrl+C en la consola
```

---

**Status:** READY para iniciar Paper Trading Fase 1
**Proximos pasos:** Configurar Binance Testnet API keys
**Documentacion:** [DEPLOYMENT_GUIDE_CONSERVATIVE.md](DEPLOYMENT_GUIDE_CONSERVATIVE.md)
