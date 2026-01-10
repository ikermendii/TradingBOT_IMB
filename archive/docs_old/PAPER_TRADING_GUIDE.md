# 📋 GUÍA DE PAPER TRADING - NFI

## 🎯 CONFIGURACIONES DISPONIBLES

Tienes **2 configuraciones** de paper trading preparadas:

### **1. NFI 7 Pares (RECOMENDADO)**
- **Archivo:** `start_paper_7pairs.bat`
- **Config:** `config_paper_7pairs.json`
- **Pares:** BTC, ETH, SOL, BNB, XRP, ADA, DOGE
- **Max Trades:** 7
- **API Port:** 8080
- **Status:** ✅ Validado en backtest (Ratio 0.474)

### **2. NFI 37 Pares (EXPERIMENTAL)**
- **Archivo:** `start_paper_37pairs.bat`
- **Config:** `config_paper_37pairs.json`
- **Pares:** Todos los 37 pares originales NFI
- **Max Trades:** 10
- **API Port:** 8081
- **Status:** ⚠️ No testeado por RAM, pero en paper puede funcionar

---

## 🚀 CÓMO INICIAR

### **Opción 1: 7 Pares (Recomendado para empezar)**

1. Navega a la carpeta:
   ```
   cd c:\Users\ikerm\Desktop\Pruebas BOTTrading\FreqtradeBOT\freqtrade
   ```

2. Ejecuta el script:
   ```
   start_paper_7pairs.bat
   ```

3. Verás el bot iniciar con:
   - Balance virtual: 1000 USDT
   - Modo dry_run (simulación)
   - API en http://127.0.0.1:8080

### **Opción 2: 37 Pares (Mayor diversificación)**

1. Navega a la carpeta:
   ```
   cd c:\Users\ikerm\Desktop\Pruebas BOTTrading\FreqtradeBOT\freqtrade
   ```

2. Ejecuta el script:
   ```
   start_paper_37pairs.bat
   ```

3. Verás el bot iniciar con:
   - Balance virtual: 1000 USDT
   - Modo dry_run (simulación)
   - API en http://127.0.0.1:8081

---

## 📊 MONITOREO DEL BOT

### **Via FreqUI (Web Interface)**

**Para 7 pares:**
```
http://127.0.0.1:8080
Usuario: freqtrader
Password: changeme_password
```

**Para 37 pares:**
```
http://127.0.0.1:8081
Usuario: freqtrader
Password: changeme_password
```

### **Via Comandos (Terminal)**

En otra terminal, con el entorno activado:

**Ver status:**
```bash
freqtrade status --config user_data/config_paper_7pairs.json
```

**Ver profit:**
```bash
freqtrade profit --config user_data/config_paper_7pairs.json
```

**Ver balance:**
```bash
freqtrade show_balance --config user_data/config_paper_7pairs.json
```

**Ver trades:**
```bash
freqtrade show_trades --config user_data/config_paper_7pairs.json
```

---

## 📈 QUÉ ESPERAR

### **Primeras Horas:**
- El bot descargará datos actuales
- Calculará indicadores
- Puede no abrir trades inmediatamente (NFI es selectivo)

### **Primeros Días:**
- Espera ver 1-3 trades por día (promedio)
- Algunos días sin trades es NORMAL
- Win rate esperado: 90-99%

### **Primera Semana:**
- Deberías ver ~5-15 trades totales
- Profit esperado: 2-8% (conservador)
- Max drawdown esperado: <5%

### **Primer Mes:**
- Trades: 20-60
- CAGR mensual: 15-30% (si sigue backtest)
- Comparar con resultados backtest

---

## ⚠️ DIFERENCIAS PAPER vs BACKTEST

### **Paper Trading usa datos REALES:**
- ✅ Precios en tiempo real de Binance
- ✅ Orden book real
- ✅ Latencia de red real
- ⚠️ Pero NO ejecuta órdenes reales (dry_run)

### **Lo que puede diferir del backtest:**
1. **Timing de entradas** - Mercado actual vs histórico
2. **Volatilidad** - Puede ser mayor/menor que 2020-2025
3. **Oportunidades** - Menos/más según condiciones
4. **Slippage** - En paper es simulado

---

## 🔍 MÉTRICAS A MONITOREAR

### **Diarias:**
| Métrica | Target | Acción si fuera de rango |
|---------|--------|-------------------------|
| Trades abiertos | 0-7 | Normal |
| Drawdown actual | <10% | Monitor si >10% |
| Trades cerrados/día | 0-3 | Normal si 0, bueno si 1-3 |

### **Semanales:**
| Métrica | Target | Acción si fuera de rango |
|---------|--------|-------------------------|
| Win rate | >90% | Investigar si <85% |
| Profit semanal | 1-6% | OK si positivo |
| Trades totales | 3-15 | Normal |

### **Mensuales:**
| Métrica | Target Backtest | Target Paper (Conservador) |
|---------|----------------|---------------------------|
| CAGR | 25.85% | 15-20% |
| Win rate | 99.3% | 90-95% |
| Max DD | 3.56% | 5-10% |
| Sharpe | 2.31 | 1.5-2.0 |

---

## 🛑 CUÁNDO DETENER

### **Señales de Alerta:**

⛔ **DETENER INMEDIATAMENTE si:**
- Drawdown > 30%
- Win rate < 70% después de 50+ trades
- Pérdidas consecutivas > 5
- Errores técnicos repetidos

⚠️ **REVISAR CONFIGURACIÓN si:**
- No abre trades en 7+ días
- Abre >10 trades/día consistentemente
- Win rate <85% después de 30+ trades
- Drawdown >15%

✅ **CONTINUAR si:**
- Win rate 90-99%
- Drawdown <10%
- CAGR mensual 10-30%
- Comportamiento similar al backtest

---

## 📝 REGISTRO Y DOCUMENTACIÓN

### **Crear log diario:**

Crea archivo: `paper_trading_log.txt`

```
DÍA 1 - 2026-01-02
- Trades abiertos: 2
- Trades cerrados: 1 (ganador)
- P&L día: +1.2%
- Balance: 1012 USDT
- Observaciones: Primera entrada en SOL, cumplió TP

DÍA 2 - 2026-01-03
...
```

### **Revisión semanal:**

```
SEMANA 1 (2026-01-02 a 2026-01-08)
Total trades: 8
Ganadores: 7
Perdedores: 1
Win rate: 87.5%
P&L: +4.3%
Balance: 1043 USDT
Max DD: -2.1%
Desvíos vs backtest: Win rate ligeramente bajo (esperado 99%), pero dentro de rango normal
```

---

## 🔄 TRANSICIÓN A LIVE TRADING

**NO hacer hasta:**
1. ✅ Mínimo 1 mes paper trading exitoso
2. ✅ Win rate >90%
3. ✅ Drawdown <10%
4. ✅ Comportamiento consistente con backtest
5. ✅ Sin errores técnicos

**Cuando estés listo:**

1. **Cambiar configuración:**
   - `"dry_run": false` (CUIDADO!)
   - Agregar API keys reales
   - Reducir balance inicial (ej: $500)

2. **Configurar Telegram (IMPORTANTE):**
   ```json
   "telegram": {
     "enabled": true,
     "token": "tu_token_real",
     "chat_id": "tu_chat_id"
   }
   ```

3. **Empezar conservador:**
   - Capital inicial: $500-1000 máximo
   - Monitorear CADA día
   - Aumentar solo si funciona bien

---

## 🆘 TROUBLESHOOTING

### **Error: "Unable to allocate memory"**
- **Para 37 pares:** Reduce a 7 pares
- **Para 7 pares:** Cierra otras aplicaciones

### **No abre trades después de días**
- Normal si NFI es muy selectivo
- Verificar que datos se descargan bien
- Revisar logs por errores

### **Muchos errores de conexión**
- Verificar internet
- Binance puede tener rate limits
- Esperar y reintentar

### **Trades muy diferentes al backtest**
- Normal en primeros días
- Evaluar después de 30+ trades
- Mercado actual puede ser diferente

---

## 📞 COMANDOS ÚTILES

### **Detener el bot:**
```
Ctrl + C en la terminal
```

### **Ver logs en tiempo real:**
```bash
tail -f user_data/logs/freqtrade.log
```

### **Actualizar datos:**
```bash
freqtrade download-data --config user_data/config_paper_7pairs.json --days 3
```

### **Reiniciar limpio:**
```bash
# Detener bot
# Borrar database (opcional)
rm user_data/tradesv3.sqlite
# Reiniciar
start_paper_7pairs.bat
```

---

## 🎯 CHECKLIST SEMANAL

**Cada Domingo:**
- [ ] Revisar trades de la semana
- [ ] Calcular win rate semanal
- [ ] Calcular profit semanal
- [ ] Verificar max drawdown
- [ ] Comparar vs expectativas backtest
- [ ] Documentar en log semanal
- [ ] Decidir: continuar / ajustar / detener

---

## 📊 COMPARACIÓN 7 vs 37 PARES

Después de 1 mes paper trading con ambos, compara:

| Métrica | 7 Pares | 37 Pares | Ganador |
|---------|---------|----------|---------|
| CAGR | ? | ? | ? |
| Win rate | ? | ? | ? |
| Max DD | ? | ? | ? |
| Sharpe | ? | ? | ? |
| Trades/mes | ? | ? | ? |
| Estabilidad RAM | ? | ? | ? |

**Decisión final:** Usar configuración con mejor ratio riesgo/retorno

---

## ✅ PRÓXIMOS PASOS

1. **HOY:** Iniciar ambos paper tradings
2. **Día 7:** Primera revisión semanal
3. **Día 30:** Evaluación mensual completa
4. **Día 60:** Decisión live trading o continuar paper

**IMPORTANTE:** No te apresures. Paper trading es GRATIS y te da experiencia valiosa sin riesgo.

---

**Archivos Creados:**
- ✅ `NFI_FINAL_REPORT.md` - Reporte completo del proyecto
- ✅ `config_paper_7pairs.json` - Config 7 pares
- ✅ `config_paper_37pairs.json` - Config 37 pares
- ✅ `start_paper_7pairs.bat` - Script launch 7 pares
- ✅ `start_paper_37pairs.bat` - Script launch 37 pares
- ✅ `PAPER_TRADING_GUIDE.md` - Esta guía

**Ubicación:** `c:\Users\ikerm\Desktop\Pruebas BOTTrading\FreqtradeBOT\freqtrade\`

¡Buena suerte con el paper trading! 🚀
