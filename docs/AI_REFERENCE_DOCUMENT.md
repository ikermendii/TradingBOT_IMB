# AI Reference Document - Trading Bot Project
> **Última actualización:** 2026-02-21
> **Propósito:** Documento de referencia para IAs que continúen el desarrollo/mantenimiento de este proyecto

---

## 1. RESUMEN EJECUTIVO

Este proyecto consiste en **3 bots de trading automatizado** ejecutándose en paper trading (testnet):

| Bot | Framework | Estrategia | Servidor | Estado |
|-----|-----------|------------|----------|--------|
| v9.3-RSI36 | Freqtrade | Multitimeframe_v93_Complete | Oracle Cloud 92.5.17.169:8080 | ✅ ACTIVO |
| NFI 7 | Freqtrade | NostalgiaForInfinityX7 | Oracle Cloud 141.147.2.82:8082 | ✅ ACTIVO |
| NFI 10 | Freqtrade | NostalgiaForInfinityX7 | Google Cloud 35.189.234.240:8084 | ✅ ACTIVO |

---

## 2. ARQUITECTURA DEL PROYECTO

### 2.1 Estructura de Directorios Local
```
C:\Users\ikerm\Desktop\Pruebas BOTTrading\
├── TradingBot_Project/           # Proyecto principal Jesse -> Freqtrade migration
│   ├── code/
│   │   └── strategies/
│   │       └── Multitimeframe/   # v9.3-RSI36 (ESTRATEGIA ACTIVA)
│   ├── docs/                     # Documentación
│   └── v93-TradingBot/
│       └── freqtrade/
│           └── user_data/
│               └── strategies/
│                   └── Multitimeframe_v93_Complete.py
│
└── FreqtradeBOT/                 # Proyecto NFI (NostalgiaForInfinityX7)
    └── freqtrade/
        └── user_data/
            ├── strategies/
            │   └── NFI_X7.py
            └── config_paper_*.json
```

### 2.2 Servidores Remotos

#### Oracle Cloud - v9.3 Bot (92.5.17.169)
```
Usuario: ubuntu
SSH Key: C:/Users/ikerm/.ssh/oracle_freqtrade.key
Puerto API: 8080
Directorio: /home/ubuntu/freqtrade/
Config: /home/ubuntu/freqtrade/user_data/config.json
Strategy: Multitimeframe_v93_Complete
Database: /home/ubuntu/freqtrade/tradesv3.dryrun.sqlite
Logs: /home/ubuntu/freqtrade/user_data/logs/v93_bot.log
```

#### Oracle Cloud - NFI 7 Bot (141.147.2.82)
```
Usuario: ubuntu
SSH Key: C:/Users/ikerm/.ssh/oracle_freqtrade.key (misma key)
Puerto API: 8082
Directorio: /home/ubuntu/freqtrade/
Config: /home/ubuntu/freqtrade/user_data/config.json
Strategy: NostalgiaForInfinityX7
RAM: ~960MB + 1GB Swap
Pares: 4 (BTC, ETH, SOL, BNB)
```

#### Google Cloud - NFI 10 Bot (35.189.234.240)
```
Usuario: ikermendii
SSH: gcloud compute ssh trading-bot-nfi --zone=europe-southwest1-a
Puerto API: 8084
Directorio: /home/ikermendii/freqtrade/
Config: /home/ikermendii/freqtrade/user_data/config_gcp_4pairs.json
Strategy: NostalgiaForInfinityX7
RAM: ~960MB + 1GB Swap
Pares: 4 (BTC, ETH, SOL, BNB)
```

---

## 3. ESTRATEGIAS

### 3.1 Multitimeframe v9.3-RSI36 (Bot Principal)

**Origen:** Migrada desde Jesse Framework a Freqtrade

**Archivo:** `Multitimeframe_v93_Complete.py`

**Parámetros Clave:**
```python
timeframe = "15m"
rsi_long_threshold = 36      # Entry LONG cuando RSI < 36
rsi_short_threshold = 64     # Entry SHORT cuando RSI > 64
break_even_ratio = 1.35      # Mover SL a entry cuando profit = 1.35R
tp_final_ratio = 3.0         # Take Profit a 3.0R
stoploss = -0.99             # Stoploss amplio (real manejado en custom_exit)
use_custom_stoploss = False  # SL manejado en custom_exit(), no en custom_stoploss()
```

**Lógica de Salida (custom_exit):**
1. Calcular R-ratio = (current_price - entry_price) / ATR
2. Si R >= 1.35 y BE no activado → Mover SL a entry (break-even)
3. Si precio toca SL → Cerrar con "stop_loss_hit"
4. Si R >= 3.0 → Cerrar con "tp_3.0R_hit"

**Resultados Jesse Backtest (2018-2025):**
- Win Rate: 25.14%
- Annual Return: 30.8%
- Max Drawdown: -19.93%
- Net Profit: +110.68%

**Resultados Actuales Paper Trading (13 días, 45 trades):**
- Win Rate: 22.2%
- Total Profit: -231.25 USDT (-2.34%)
- Exit distribution:
  - stop_loss_hit: 34 trades (-982.74 USDT)
  - tp_3.0R_hit: 10 trades (+764.65 USDT)
  - trailing_stop: 1 trade (-13.16 USDT)

**Nota:** El win rate actual (22%) está dentro de la varianza esperada. La muestra de 45 trades es pequeña para conclusiones estadísticas.

### 3.2 NostalgiaForInfinityX7 (NFI)

**Archivo:** `NFI_X7.py` (versión 17.3.36)

**Características:**
- Timeframe: 5m
- Multi-timeframe analysis: 5m, 15m, 1h, 4h, 1d
- startup_candle_count: 800
- Ultra-conservadora (~1 trade cada 8 días con 7 pares)

**Requisitos de Memoria:**
- ~100MB por par de trading
- ~200MB base del bot
- ~150MB sistema operativo
- Total recomendado: 4 pares + 1GB swap en VMs de 1GB RAM

---

## 4. HISTORIAL DE DESARROLLO

### Fase 1: Desarrollo Jesse (Completada)
- Estrategia v9.3-RSI36 desarrollada en Jesse Framework
- Backtesting extensivo 2018-2025
- Robustness testing completado
- Resultados: Win Rate 25%, Annual Return 30.8%

### Fase 2: Migración a Freqtrade (Completada)
- Razón: Jesse no soporta paper trading nativo
- Migración de lógica a `Multitimeframe_v93_Complete.py`
- Adaptación de custom_exit() para replicar update_position() de Jesse
- Deploy en Oracle Cloud

### Fase 3: NFI Bots Setup (Completada)
- Deploy de NFI 7 en Oracle Cloud
- Deploy de NFI 10 en Google Cloud
- Configuración de 4 pares por bot
- Adición de 1GB swap para estabilidad

### Fase 4: Troubleshooting NFI (Completada - 2026-01-31)
**Problema:** NFI bots mostraban "Outdated history" y analysis times de 500+ segundos
**Causa:** RAM insuficiente (960MB) para análisis multi-timeframe
**Solución:**
1. Añadido 1GB swap a ambos VMs
2. Reducido pares a 4 (BTC, ETH, SOL, BNB)
3. Configuración permanente de swap via /etc/fstab

**Cálculo de Memoria:**
```
Memoria requerida = (Pares × 100MB) + 200MB (bot) + 150MB (sistema)
4 pares = 400 + 200 + 150 = 750MB
Con swap 1GB = 1.96GB disponibles total
Headroom suficiente para peaks de análisis
```

### Fase 5: Verificación v9.3 (Completada - 2026-01-31)
- Verificación de parámetros vs Jesse backtest: ✅ Coinciden
- Break-even funcionando correctamente: ✅
- Take Profit funcionando correctamente: ✅
- Win rate actual (22%) cercano a esperado (25%): ✅

---

## 5. PROBLEMAS CONOCIDOS Y SOLUCIONES

### 5.1 NFI "Analysis took X seconds"
**Síntoma:** Warnings de análisis lento (>25% del timeframe)
**Causa:** Memoria insuficiente
**Solución:** Añadir swap + reducir pares

### 5.2 SSH Connection Issues
**Problema:** `Permission denied (publickey)`
**Solución:** Usar la key correcta:
- Oracle: `C:/Users/ikerm/.ssh/oracle_freqtrade.key`
- GCP: `gcloud compute ssh` (usa google_compute_engine automáticamente)

### 5.3 API Authentication
**Problema:** Token JWT expira o no funciona
**Solución:** Consultar directamente la base de datos SQLite:
```bash
ssh -i KEY ubuntu@IP "python3 -c \"
import sqlite3
conn = sqlite3.connect('/home/ubuntu/freqtrade/tradesv3.dryrun.sqlite')
c = conn.cursor()
c.execute('SELECT COUNT(*), SUM(close_profit_abs) FROM trades WHERE is_open = 0')
print(c.fetchone())
\""
```

### 5.4 v9.3 Pérdidas en Break-Even
**Observación:** Muchos trades pierden <0.25% después de activar break-even
**Explicación:** Comportamiento correcto - el precio vuelve al entry después de activar BE
**No es bug:** Es protección de ganancias funcionando como diseñado

---

## 6. COMANDOS ÚTILES

### Conectar a Oracle v9.3
```bash
ssh -i "C:/Users/ikerm/.ssh/oracle_freqtrade.key" ubuntu@92.5.17.169
```

### Conectar a Oracle NFI 7
```bash
ssh -i "C:/Users/ikerm/.ssh/oracle_freqtrade.key" ubuntu@141.147.2.82
```

### Conectar a GCP NFI 10
```bash
# Opción 1: SSH directo (más fiable)
ssh -i "C:/Users/ikerm/.ssh/google_compute_engine" ikermendii@35.189.234.240
# Opción 2: gcloud (nombre correcto de VM)
gcloud compute ssh freqtrade-nfi-37 --zone=europe-west1-b --project=project-c8c8bdb2-a95e-47c7-887
```

### Ver logs en tiempo real
```bash
tail -f ~/freqtrade/user_data/logs/v93_bot.log
```

### Consultar estadísticas de trades
```bash
python3 -c "
import sqlite3
conn = sqlite3.connect('tradesv3.dryrun.sqlite')
c = conn.cursor()
c.execute('SELECT COUNT(*), SUM(CASE WHEN close_profit > 0 THEN 1 ELSE 0 END), SUM(close_profit_abs) FROM trades WHERE is_open = 0')
r = c.fetchone()
print(f'Total: {r[0]}, Wins: {r[1]}, Profit: {r[2]:.2f} USDT')
"
```

### Verificar swap
```bash
free -h
swapon --show
```

### Reiniciar bot
```bash
pkill -f 'freqtrade trade'
cd ~/freqtrade && .venv/bin/freqtrade trade --config user_data/config.json --strategy STRATEGY_NAME --logfile user_data/logs/bot.log &
```

---

## 7. ARCHIVOS CRÍTICOS

### Estrategias
| Archivo | Ubicación | Descripción |
|---------|-----------|-------------|
| Multitimeframe_v93_Complete.py | Oracle v9.3: ~/freqtrade/user_data/strategies/ | Estrategia principal migrada de Jesse |
| NFI_X7.py | Oracle/GCP NFI: ~/freqtrade/user_data/strategies/ | NostalgiaForInfinityX7 |

### Configuraciones
| Archivo | Ubicación | Descripción |
|---------|-----------|-------------|
| config.json | Oracle v9.3: ~/freqtrade/user_data/ | Config del bot v9.3 (BTC/USDT) |
| config.json | Oracle NFI: ~/freqtrade/user_data/ | Config NFI 7 (4 pares) |
| config_gcp_4pairs.json | GCP NFI: ~/freqtrade/user_data/ | Config NFI 10 (4 pares) |

### Bases de Datos
| Archivo | Ubicación | Descripción |
|---------|-----------|-------------|
| tradesv3.dryrun.sqlite | ~/freqtrade/ | Historial de trades (paper trading) |

### Documentación Local
| Archivo | Descripción |
|---------|-------------|
| docs/AI_REFERENCE_DOCUMENT.md | Este documento |
| docs/INSTALLATION.md | Guía de instalación |
| CHANGELOG.md | Historial de cambios |

---

## 8. CREDENCIALES Y SEGURIDAD

**IMPORTANTE:** Las credenciales reales están en archivos .env que NO se suben a Git.

### API Keys (Testnet)
- Binance Testnet API: Configuradas en config.json de cada bot
- Telegram Bot Token: Configurado para notificaciones

### SSH Keys
- Oracle: `C:/Users/ikerm/.ssh/oracle_freqtrade.key`
- GCP: Gestionadas por gcloud CLI

### API Freqtrade
- Usuario: `freqtrader`
- Password: `freqtrade123` (paper trading, no crítico)

---

## 9. MÉTRICAS DE REFERENCIA

### v9.3 Expected Performance (Jesse Backtest)
```
Win Rate: 25.14%
Profit Factor: ~1.5
Annual Return: 30.8%
Max Drawdown: -19.93%
Avg Trade Duration: Variable (depende de si llega a TP o SL)
```

### NFI Expected Performance
```
Win Rate: ~100% en backtest (ultra-conservadora)
Trade Frequency: ~1 trade cada 8 días (7 pares)
Profit por Trade: +23.94% total en backtest 2024-2025
```

---

## 10. PRÓXIMOS PASOS SUGERIDOS

1. **Monitoreo Continuo:** Verificar performance cada semana
2. **Aumentar Muestra:** Esperar 100+ trades para análisis estadístico válido
3. **Optimización NFI:** Si performance es buena, considerar aumentar a 7 pares con más RAM
4. **Real Trading:** Solo después de 3+ meses de paper trading rentable
5. **Documentación:** Mantener este documento actualizado

---

## 11. NOTAS PARA FUTURAS IAs

### Contexto Rápido
- El usuario (Iker) está desarrollando bots de trading para BTC/USDT
- El objetivo es validar estrategias en paper trading antes de ir a real
- La estrategia principal (v9.3) fue desarrollada y backtested en Jesse, luego migrada a Freqtrade
- Los bots NFI son una estrategia alternativa ultra-conservadora

### Preferencias del Usuario
- Prefiere explicaciones técnicas detalladas
- Valora la verificación matemática de resultados
- Quiere entender el "por qué" de los problemas, no solo soluciones
- Idioma: Español

### Cómo Actualizar Este Documento
1. Leer el estado actual
2. Realizar las tareas solicitadas
3. Documentar cambios significativos
4. Actualizar la fecha de "Última actualización"

### Archivos a Revisar para Contexto Completo
```
1. Este documento (AI_REFERENCE_DOCUMENT.md)
2. La estrategia activa: Multitimeframe_v93_Complete.py
3. Los configs de cada bot
4. Los logs recientes para ver actividad
5. La base de datos para estadísticas actuales
```

---

## 12. CHANGELOG DE ESTE DOCUMENTO

| Fecha | Cambios |
|-------|---------|
| 2026-01-31 | Creación inicial del documento |
| | Documentado: 3 bots activos, arquitectura, estrategias |
| | Documentado: Troubleshooting NFI (swap + 4 pares) |
| | Documentado: Verificación v9.3 vs Jesse backtest |
| 2026-02-05 | Verificación completa de bots NFI |
| | NFI genera 0 trades (estrategia ultra-conservadora por diseño) |
| | Backtest 30 días = 0 trades (comportamiento esperado de NFI) |
| | Consumo recursos: NFI7 622MB, NFI10 510MB (con swap) |
| | Tiempos análisis: 75s-545s (exceden límite 75s ocasionalmente) |
| | Decisión: Mantener 4 pares, no aumentar (límite de recursos) |
| 2026-02-21 | Verificación completa de los 3 bots |
| | **v9.3:** 155 trades, -1021 USDT. WR 21.9% < breakeven 27%. Ratio W/L 2.71 (esperado 3.0) |
| | **v9.3 problema:** Fees/slippage reducen ratio de 3R a 2.71R, haciendo breakeven inalcanzable |
| | **NFI:** Backtest 4 meses BTC+ETH = 0 trades (spot y futures) |
| | **NFI causa raíz:** Necesita 50-100+ pares, 4 pares es insuficiente |
| | **NFI:** VMs saturadas por backtests, GCP reiniciado, Oracle NFI requiere reinicio manual |
| | Conexiones GCP corregidas: VM=freqtrade-nfi-37, zona=europe-west1-b |
| | AVISO: NUNCA ejecutar backtests NFI en las VMs de 1GB, causan OOM |

---

*Este documento fue creado por Claude AI para servir como referencia en futuras conversaciones sobre el proyecto de Trading Bots.*
