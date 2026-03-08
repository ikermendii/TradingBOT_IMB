# AI Quick Start Guide
> **Lee primero:** `AI_REFERENCE_DOCUMENT.md` para contexto completo

## Estado Actual (2026-01-31)

### Bots Activos
| Bot | IP:Puerto | Status | Comando SSH |
|-----|-----------|--------|-------------|
| v9.3 | 92.5.17.169:8080 | ✅ | `ssh -i "C:/Users/ikerm/.ssh/oracle_freqtrade.key" ubuntu@92.5.17.169` |
| NFI 7 | 141.147.2.82:8082 | ✅ | `ssh -i "C:/Users/ikerm/.ssh/oracle_freqtrade.key" ubuntu@141.147.2.82` |
| NFI 10 | 35.189.234.240:8084 | ✅ | `gcloud compute ssh trading-bot-nfi --zone=europe-southwest1-a` |

## Verificación Rápida de Salud

### 1. Comprobar que el bot está corriendo
```bash
ps aux | grep freqtrade | grep -v grep
```

### 2. Ver estadísticas de trades
```bash
python3 -c "
import sqlite3
conn = sqlite3.connect('$HOME/freqtrade/tradesv3.dryrun.sqlite')
c = conn.cursor()
c.execute('SELECT COUNT(*), SUM(CASE WHEN close_profit > 0 THEN 1 ELSE 0 END), ROUND(SUM(close_profit_abs),2) FROM trades WHERE is_open = 0')
r = c.fetchone()
print(f'Trades: {r[0]} | Wins: {r[1]} | Profit: {r[2]} USDT')
"
```

### 3. Ver logs recientes
```bash
tail -20 ~/freqtrade/user_data/logs/*.log
```

### 4. Verificar memoria y swap
```bash
free -h
```

## Problemas Comunes

| Síntoma | Causa Probable | Solución |
|---------|---------------|----------|
| "Analysis took X seconds" | RAM baja | Verificar swap, reducir pares |
| Bot no responde | Proceso muerto | Reiniciar con script |
| API 401 Unauthorized | Token expirado | Usar SQLite directamente |
| SSH Permission denied | Key incorrecta | Usar oracle_freqtrade.key |

## Archivos Clave por Bot

### v9.3 (Oracle 92.5.17.169)
```
Strategy: ~/freqtrade/user_data/strategies/Multitimeframe_v93_Complete.py
Config:   ~/freqtrade/user_data/config.json
DB:       ~/freqtrade/tradesv3.dryrun.sqlite
Logs:     ~/freqtrade/user_data/logs/v93_bot.log
```

### NFI (Oracle 141.147.2.82 / GCP 35.189.234.240)
```
Strategy: ~/freqtrade/user_data/strategies/NFI_X7.py
Config:   ~/freqtrade/user_data/config.json (Oracle)
          ~/freqtrade/user_data/config_gcp_4pairs.json (GCP)
DB:       ~/freqtrade/tradesv3.dryrun.sqlite
```

## Parámetros Críticos v9.3

```python
rsi_long_threshold = 36    # Entry LONG
rsi_short_threshold = 64   # Entry SHORT
break_even_ratio = 1.35    # Mover SL a entry
tp_final_ratio = 3.0       # Take Profit
```

**Expected:** Win Rate ~25%, Annual Return ~30%

## Reiniciar un Bot

```bash
# Matar proceso existente
pkill -f 'freqtrade trade'

# Iniciar de nuevo (v9.3)
cd ~/freqtrade
nohup .venv/bin/freqtrade trade \
  --config user_data/config.json \
  --strategy Multitimeframe_v93_Complete \
  --logfile user_data/logs/v93_bot.log &

# Verificar
ps aux | grep freqtrade
```

## Para Más Información

Ver documento completo: `docs/AI_REFERENCE_DOCUMENT.md`
