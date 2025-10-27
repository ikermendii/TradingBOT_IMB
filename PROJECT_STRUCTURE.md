# ESTRUCTURA COMPLETA DEL PROYECTO
**Generado:** 2025-10-25 20:50 UTC
**Ubicación:** `c:\Users\ikerm\Desktop\Pruebas BOTTrading\TradingBot_Project`

---

## ÁRBOL DE DIRECTORIOS

```
TradingBot_Project/
│
├── 📁 .claude/                          # Configuración de Claude Code
│   └── settings.local.json
│
├── 📁 .github/                          # Configuración GitHub (vacía)
│
├── 📁 backtests/                        # Resultados de backtests anteriores
│
├── 📁 code/                             # CÓDIGO PRINCIPAL
│   ├── 📁 storage/                      # Storage de Jesse
│   │   └── temp/
│   │
│   ├── 📁 strategies/                   # ESTRATEGIAS DE TRADING
│   │   ├── __init__.py                  # Package marker
│   │   │
│   │   ├── 📁 Multitimeframe/           # ⭐ ESTRATEGIA PRINCIPAL
│   │   │   ├── __init__.py              # Estrategia v4.0 Hybrid
│   │   │   └── __pycache__/
│   │   │
│   │   └── 📁 SimpleRSI/                # Estrategia de aprendizaje
│   │       ├── __init__.py
│   │       └── __pycache__/
│   │
│   ├── 📁 utils/                        # Utilidades
│   │
│   └── routes.py                        # Rutas de trading
│
├── 📁 docs/                             # DOCUMENTACIÓN TÉCNICA
│   ├── VERIFICATION_PROTOCOL.md         # ⭐ Protocolo de verificación
│   └── VERIFICATION_REPORT_2025-10-25.md # Reporte última verificación
│
├── 📁 notes/                            # Notas de desarrollo
│
├── 📁 storage/                          # Storage principal de Jesse
│   ├── 📁 logs/
│   │   ├── backtest-mode/
│   │   ├── collect-mode/
│   │   ├── live-mode/
│   │   └── optimize-mode/
│   └── 📁 temp/
│
├── 📄 00_Project_Overview.md            # Overview del proyecto
├── 📄 01_Installation_Guide.md          # Guía de instalación
├── 📄 02_Strategy_Documentation.md      # Documentación de estrategia
├── 📄 03_Code_Evolution_Log.md          # ⭐ Log de evolución del código
├── 📄 04_Backtest_results.md            # ⭐ Resultados de backtests
├── 📄 05_Troubleshooting.md             # Troubleshooting
├── 📄 06_Daily_Log.md                   # Log diario
├── 📄 STRATEGY_ROADMAP.md               # ⭐ Roadmap de estrategia (5 fases)
│
├── 📄 config.py                         # ⭐ Configuración de Jesse
├── 📄 routes.py                         # Symlink a code/routes.py
├── 📄 .env                              # Variables de entorno
│
├── 📄 import_candles.py                 # Script importación simple
├── 📄 import_all_candles.py             # Script importación masiva
│
├── 📄 run_jesse_wsl.bat                 # Script para ejecutar en Windows
└── 📄 nul                               # Archivo residual
```

---

## ARCHIVOS CRÍTICOS

### 🎯 Estrategia Principal

**`code/strategies/Multitimeframe/__init__.py`** (19.7 KB)
- **Versión:** v4.0 Hybrid
- **Estado:** ✅ Actualizado y funcional
- **Última modificación:** 2025-10-25
- **Cambios recientes:**
  - Bug `timestamp_to_datetime` corregido
  - Límite de pérdida diaria implementado (3%)
  - Import de `utils` eliminado
  - Método `_can_trade_today()` reescrito

**Características:**
```python
- RSI oversold: 42 (híbrido)
- RSI overbought: 58 (híbrido)
- Cooldown: 60 minutos
- Daily loss limit: 3%
- Stop loss: ATR × 1.8
- TP1: 1.5R (50%)
- TP2: 3R (30%)
- TP3: 6R (20%)
```

---

### ⚙️ Configuración

**`config.py`** (5.1 KB)
- Exchanges: Binance Spot + Binance Perpetual Futures
- Warm-up candles: 300
- Logging: Configurado para backtest
- Database: PostgreSQL configurado

**`code/routes.py`** (1.8 KB)
```python
routes = [
    ('Binance Perpetual Futures', 'BTC-USDT', '15m', 'Multitimeframe'),
]

extra_candles = [
    ('Binance Perpetual Futures', 'BTC-USDT', '1h'),
    ('Binance Perpetual Futures', 'BTC-USDT', '4h'),
]
```

---

### 📊 Documentación de Progreso

**`03_Code_Evolution_Log.md`** (6.6 KB)
- Registro de todas las versiones
- v1.0 → v4.0 documentadas
- Cambios y razones

**`04_Backtest_results.md`** (9.7 KB)
- Resultados de todos los backtests
- v1.0: 2 trades, -0.51%
- v2.0: 4 trades, -0.87%
- v3.0: Bug (1,017 días)
- v3.1 (Copilot): 575 trades, -41.16%
- v4.0: Pendiente

**`STRATEGY_ROADMAP.md`** (4.8 KB)
- PHASE 1 (v4.0): Filtros básicos ← **ACTUAL**
- PHASE 2 (v5.0): RSI divergences
- PHASE 3 (v6.0): Multi-timeframe 1H
- PHASE 4 (v7.0): Multi-timeframe 4H
- PHASE 5 (v8.0): Optimización final

---

### 📖 Documentación Técnica

**`docs/VERIFICATION_PROTOCOL.md`** (12 KB)
- Protocolo de 7 pasos para modificaciones
- Checklist completo
- Matriz de impacto de archivos
- Comandos de verificación
- Workflow estándar

**`docs/VERIFICATION_REPORT_2025-10-25.md`** (8.1 KB)
- Reporte de última verificación
- Estado de todos los archivos
- Bugs corregidos
- Tests ejecutados
- Próximos pasos

---

## ARCHIVOS DE SOPORTE

### Scripts de Importación

**`import_candles.py`** (1.7 KB)
- Importación simple de candles
- Uso: Para periodos específicos

**`import_all_candles.py`** (4.5 KB)
- Importación masiva de datos históricos
- Uso: Para setup inicial

### Estrategia de Aprendizaje

**`code/strategies/SimpleRSI/__init__.py`** (4.1 KB)
- Estrategia básica para aprendizaje
- Estado: Testeada pero no activa
- RSI básico + EMA 200

---

## ESTADO ACTUAL DEL PROYECTO

### ✅ Verificado y Funcional

- [x] Sintaxis de todas las estrategias
- [x] Imports funcionando correctamente
- [x] Config.py cargando sin errores
- [x] Routes.py apuntando a Multitimeframe
- [x] Servidor Jesse corriendo (puerto 9000)
- [x] Variables de estado inicializadas
- [x] Bug `timestamp_to_datetime` eliminado
- [x] Límite de pérdida diaria implementado

### 📋 Pendiente

- [ ] Ejecutar backtest v4.0 Hybrid
- [ ] Registrar resultados en 04_Backtest_results.md
- [ ] Actualizar 03_Code_Evolution_Log.md
- [ ] Evaluar métricas vs objetivos

---

## UBICACIONES CLAVE

### Código de Estrategias
```
c:\Users\ikerm\Desktop\Pruebas BOTTrading\TradingBot_Project\code\strategies\
```

### Documentación
```
c:\Users\ikerm\Desktop\Pruebas BOTTrading\TradingBot_Project\docs\
```

### Configuración
```
c:\Users\ikerm\Desktop\Pruebas BOTTrading\TradingBot_Project\config.py
c:\Users\ikerm\Desktop\Pruebas BOTTrading\TradingBot_Project\code\routes.py
```

### Resultados de Backtests
```
c:\Users\ikerm\Desktop\Pruebas BOTTrading\TradingBot_Project\04_Backtest_results.md
c:\Users\ikerm\Desktop\Pruebas BOTTrading\TradingBot_Project\storage\
```

---

## COMANDOS ÚTILES

### Ejecutar Backtest
```bash
cd /mnt/c/Users/ikerm/Desktop/Pruebas\ BOTTrading/TradingBot_Project
jesse backtest '2024-01-01' '2024-12-31'
```

### Verificar Sintaxis
```bash
cd /mnt/c/Users/ikerm/Desktop/Pruebas\ BOTTrading/TradingBot_Project
python3 -m py_compile code/strategies/Multitimeframe/__init__.py
```

### Test de Import
```bash
cd /mnt/c/Users/ikerm/Desktop/Pruebas\ BOTTrading/TradingBot_Project
python3 -c "from strategies.Multitimeframe import Multitimeframe; print('OK')"
```

### Limpiar Caché
```bash
cd /mnt/c/Users/ikerm/Desktop/Pruebas\ BOTTrading/TradingBot_Project
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
redis-cli FLUSHALL
```

### Ver Servidor Jesse
```bash
ps aux | grep jesse
```

---

## VERSIÓN ACTUAL

**Estrategia:** v4.0 Hybrid
**Jesse Framework:** 1.11.0
**Python:** 3.x
**Exchange:** Binance Perpetual Futures
**Símbolo:** BTC-USDT
**Timeframe principal:** 15m
**Timeframes adicionales:** 1h, 4h

---

## ARCHIVOS SINCRONIZADOS

✅ **CONFIRMADO:** Todos los archivos están sincronizados entre:
- WSL: `/mnt/c/Users/ikerm/Desktop/Pruebas BOTTrading/TradingBot_Project`
- Windows: `c:\Users\ikerm\Desktop\Pruebas BOTTrading\TradingBot_Project`
- IDE: Visual Studio Code

---

## NOTAS IMPORTANTES

⚠️ **Symlinks:**
- `routes.py` en raíz → symlink a `code/routes.py`
- `strategies/` en raíz → symlink a `code/strategies/`

⚠️ **Archivos __init__.py:**
- `code/strategies/__init__.py` - Package marker (NECESARIO)
- `code/strategies/Multitimeframe/__init__.py` - Estrategia completa (CRÍTICO)
- `code/strategies/SimpleRSI/__init__.py` - Estrategia de aprendizaje

⚠️ **Servidor Jesse:**
- Actualmente corriendo 2 procesos (379c2b, 9f2737)
- Puerto: 9000
- Modo: Development

---

**Última actualización:** 2025-10-25 20:50 UTC
**Estado:** ✅ SINCRONIZADO Y OPERATIVO
