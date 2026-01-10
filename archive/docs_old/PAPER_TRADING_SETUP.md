# 🤖 PAPER TRADING - 3 BOTS EN PARALELO

## 📊 CONFIGURACIÓN ACTUAL

Tienes **3 bots de paper trading** configurados para correr simultáneamente:

### **Bot 1: v9.3-RSI36 (Jesse Strategy)**
- **Puerto:** 8080 ✅ (YA EN EJECUCIÓN)
- **Framework:** Jesse
- **Estrategia:** v9.3-RSI36 (BE=1.35R optimizado)
- **Pares:** 1 (BTC/USDT)
- **Status:** ✅ Activo
- **URL:** http://127.0.0.1:8080

---

### **Bot 2: NFI 7 Pares (Freqtrade)**
- **Puerto:** 8082 🆕
- **Framework:** Freqtrade
- **Estrategia:** NostalgiaForInfinityX7
- **Pares:** 7 (BTC, ETH, SOL, BNB, XRP, ADA, DOGE)
- **Max Trades:** 7
- **CAGR Validado:** 25.85% (TEST)
- **Ratio Walk-Forward:** 0.474
- **URL:** http://127.0.0.1:8082
- **Lanzar:** `start_paper_7pairs.bat`

---

### **Bot 3: NFI 37 Pares (Freqtrade)**
- **Puerto:** 8083 🆕
- **Framework:** Freqtrade
- **Estrategia:** NostalgiaForInfinityX7
- **Pares:** 37 (todos los originales NFI)
- **Max Trades:** 10
- **Status:** Experimental (no testeado en backtest)
- **URL:** http://127.0.0.1:8083
- **Lanzar:** `start_paper_37pairs.bat`

---

## 🚀 CÓMO LANZAR LOS NUEVOS BOTS

### **Opción 1: Lanzar NFI 7 Pares**

```bash
cd c:\Users\ikerm\Desktop\Pruebas BOTTrading\FreqtradeBOT\freqtrade
start_paper_7pairs.bat
```

**Acceso Web:**
- URL: http://127.0.0.1:8082
- Usuario: `freqtrader`
- Password: `changeme_password`

---

### **Opción 2: Lanzar NFI 37 Pares**

```bash
cd c:\Users\ikerm\Desktop\Pruebas BOTTrading\FreqtradeBOT\freqtrade
start_paper_37pairs.bat
```

**Acceso Web:**
- URL: http://127.0.0.1:8083
- Usuario: `freqtrader`
- Password: `changeme_password`

---

### **Opción 3: Lanzar AMBOS NFI (Recomendado)**

Abre **2 terminales** y ejecuta uno en cada:

**Terminal 1:**
```bash
cd c:\Users\ikerm\Desktop\Pruebas BOTTrading\FreqtradeBOT\freqtrade
start_paper_7pairs.bat
```

**Terminal 2:**
```bash
cd c:\Users\ikerm\Desktop\Pruebas BOTTrading\FreqtradeBOT\freqtrade
start_paper_37pairs.bat
```

---

## 📊 COMPARACIÓN DE LOS 3 BOTS

| Característica | v9.3-RSI36 (Jesse) | NFI 7 Pares | NFI 37 Pares |
|----------------|-------------------|-------------|--------------|
| **Framework** | Jesse | Freqtrade | Freqtrade |
| **Pares** | 1 (BTC) | 7 | 37 |
| **Timeframe** | 1h | 5m | 5m |
| **Puerto** | 8080 | 8082 | 8083 |
| **CAGR Backtest** | ~52% | 25.85% | ? |
| **Walk-Forward Ratio** | 0.16-0.20 | 0.474 | ? |
| **Validación** | ❌ Overfitting | ✅ Validado | ⏳ Por validar |
| **Diversificación** | Baja (1 par) | Media (7 pares) | Alta (37 pares) |
| **Uso RAM** | Bajo | Medio | Alto |

---

## 🎯 ESTRATEGIA DE COMPARACIÓN

### **Objetivos del Experimento:**

1. **Comparar performance** entre single-pair vs multi-pair
2. **Validar** si 37 pares funciona mejor que 7 en paper
3. **Detectar** si v9.3-RSI36 sigue teniendo overfitting en forward
4. **Identificar** mejor configuración para live trading

### **Período de Prueba:**

**Mínimo:** 1 mes (30 días)
**Ideal:** 2 meses (60 días)

### **Métricas a Comparar:**

| Métrica | v9.3-RSI36 | NFI 7p | NFI 37p | Mejor |
|---------|------------|--------|---------|-------|
| CAGR Mensual | ? | ? | ? | ? |
| Win Rate | ? | ? | ? | ? |
| Max Drawdown | ? | ? | ? | ? |
| Sharpe Ratio | ? | ? | ? | ? |
| Trades/Mes | ? | ? | ? | ? |
| Estabilidad | ? | ? | ? | ? |

---

## 📈 EXPECTATIVAS POR BOT

### **Bot 1: v9.3-RSI36**

**Expectativa Optimista (si no hay overfitting):**
- CAGR: 40-50% anual
- Win rate: 60-70%
- Trades: 20-40/mes

**Expectativa Realista (basado en walk-forward previo):**
- CAGR: 8-15% anual (degradación)
- Win rate: 50-60%
- Posible underperformance vs backtest

---

### **Bot 2: NFI 7 Pares**

**Expectativa (basado en backtest TEST):**
- CAGR: 15-25% mensual
- Win rate: 90-95%
- Max DD: 5-10%
- Trades: 30-60/mes
- Diversificación moderada

---

### **Bot 3: NFI 37 Pares**

**Expectativa (hipótesis):**
- CAGR: 20-35% mensual (potencialmente mejor)
- Win rate: 90-95%
- Max DD: 5-15%
- Trades: 80-150/mes
- Alta diversificación
- **Ventaja:** En paper, RAM no es problema (solo procesa nuevas velas)

---

## 🔍 MONITOREO RECOMENDADO

### **Revisión Diaria (5 minutos):**

Para cada bot:
1. Check si está corriendo sin errores
2. Ver P&L del día
3. Ver trades abiertos/cerrados
4. Verificar drawdown actual

### **Revisión Semanal (30 minutos):**

Completar tabla comparativa:

```
SEMANA 1 (DD/MM/YYYY - DD/MM/YYYY)

Bot v9.3-RSI36:
- Trades: X
- Win rate: X%
- P&L semanal: X%
- Balance: X USDT
- Max DD: X%

Bot NFI 7p:
- Trades: X
- Win rate: X%
- P&L semanal: X%
- Balance: X USDT
- Max DD: X%

Bot NFI 37p:
- Trades: X
- Win rate: X%
- P&L semanal: X%
- Balance: X USDT
- Max DD: X%

Observaciones:
- ...
```

### **Revisión Mensual (2 horas):**

1. Calcular todas las métricas
2. Comparar vs expectativas backtest
3. Graficar curvas equity
4. Decidir próximos pasos

---

## 🎲 ESCENARIOS POSIBLES

### **Escenario A: NFI 37 pares GANA** 🏆
- Mayor diversificación = mejor performance
- Más trades = mayor consistencia
- **Decisión:** Usar NFI 37p para live

### **Escenario B: NFI 7 pares GANA** ✅
- Balance óptimo diversificación/complejidad
- Consistente con backtest validado
- **Decisión:** Usar NFI 7p para live

### **Escenario C: v9.3-RSI36 GANA** 🤔
- Single-pair supera multi-pair
- Walk-forward previo era muy conservador
- **Decisión:** Re-evaluar v9.3, considerar para live

### **Escenario D: Todos SIMILARES** 🤷
- No hay ganador claro
- **Decisión:** Correr los 3 en live con capital dividido

### **Escenario E: Todos FALLAN** ❌
- Performance negativa o muy baja
- **Decisión:** Volver a optimización/nueva estrategia

---

## 💡 RECOMENDACIONES

### **Primeros 7 Días:**

1. **Observa sin intervenir**
   - Deja correr los bots
   - No hagas ajustes
   - Solo monitorea

2. **Documenta todo**
   - Captura screenshots
   - Anota trades relevantes
   - Registra errores

3. **Compara diariamente**
   - ¿Cuál tiene mejor P&L?
   - ¿Cuál tiene más trades?
   - ¿Cuál tiene mejor win rate?

### **Día 30:**

**Toma decisión:**
- Si hay un ganador claro → preparar para live
- Si no está claro → continuar 30 días más
- Si todos fallan → re-estrategizar

---

## 🛠️ TROUBLESHOOTING

### **Si un bot falla al iniciar:**

**Error: Port already in use**
```bash
# Verificar qué usa el puerto
netstat -ano | findstr :8082
# Matar proceso si es necesario
```

**Error: Strategy not found**
```bash
# Verificar estrategia
freqtrade list-strategies --config user_data/config_paper_7pairs.json
```

**Error: Out of memory**
```bash
# Solo correr 2 bots a la vez
# O reducir pares en NFI 37p
```

---

## 📊 DASHBOARD MULTI-BOT

Puedes abrir **3 pestañas** en tu navegador:

1. http://127.0.0.1:8080 - v9.3-RSI36
2. http://127.0.0.1:8082 - NFI 7 pares
3. http://127.0.0.1:8083 - NFI 37 pares

**Tip:** Usa FreqUI para ver todos lado a lado y comparar en tiempo real.

---

## ✅ CHECKLIST DE INICIO

Antes de lanzar los nuevos bots:

- [x] ✅ v9.3-RSI36 corriendo en 8080
- [ ] ⏳ Leer esta guía completa
- [ ] ⏳ Decidir: ¿lanzar 7p, 37p, o ambos?
- [ ] ⏳ Abrir terminales necesarias
- [ ] ⏳ Ejecutar scripts `.bat`
- [ ] ⏳ Verificar acceso web (8082, 8083)
- [ ] ⏳ Configurar monitoreo diario
- [ ] ⏳ Preparar template log semanal

---

## 🎯 OBJETIVO FINAL

**Determinar la mejor configuración** para maximizar:
- ROI (Return on Investment)
- Sharpe Ratio (risk-adjusted return)
- Consistencia
- Robustez

Y **minimizar:**
- Drawdown
- Volatilidad
- Complejidad

---

**Archivos Relacionados:**
- `NFI_FINAL_REPORT.md` - Análisis completo NFI
- `PAPER_TRADING_GUIDE.md` - Guía operativa detallada
- `README_FINAL.md` - Resumen del proyecto

**Scripts de Lanzamiento:**
- `start_paper_7pairs.bat` - NFI 7 pares
- `start_paper_37pairs.bat` - NFI 37 pares

**Configs:**
- `config_paper_7pairs.json` - NFI 7 pares
- `config_paper_37pairs.json` - NFI 37 pares

---

*Actualizado: 2026-01-02*
*Puertos Configurados: 8080 (v9.3), 8082 (NFI7), 8083 (NFI37)*
*Status: ✅ Listo para lanzar*
