# ⚡ Walk-Forward Validation v3.2 - Pasos Rápidos

**Objetivo:** Validar que v3.2 NO está overfitted y funciona en datos nuevos

---

## 📋 2 Backtests a Ejecutar

### 1️⃣ TRAIN Period (Primero)

```
http://localhost:9000 → Backtest

Exchange:     Binance Perpetual Futures
Symbol:       BTC-USDT
Timeframe:    1h
Start Date:   2020-01-14  ← TRAIN
End Date:     2023-12-31  ← TRAIN (3.96 años)
Strategy:     UniversalRobustV3_2
Balance:      10000

→ Start Backtest
```

**Anotar:** Annual Return TRAIN = ???%

---

### 2️⃣ TEST Period (Después)

```
http://localhost:9000 → Backtest

Exchange:     Binance Perpetual Futures
Symbol:       BTC-USDT
Timeframe:    1h
Start Date:   2024-01-01  ← TEST
End Date:     2025-12-27  ← TEST (1.99 años)
Strategy:     UniversalRobustV3_2
Balance:      10000

→ Start Backtest
```

**Anotar:** Annual Return TEST = ???%

---

## ✅ Criterio de ÉXITO

```
Ratio = TEST Annual / TRAIN Annual

Ejemplo:
  TRAIN: 50% anual
  TEST:  30% anual
  Ratio: 30 / 50 = 0.6 → ✅ PASS (>0.5)

✅ PASS si Ratio ≥ 0.5 (TEST ≥ 50% de TRAIN)
⚠️ REVISAR si Ratio 0.3-0.5
❌ FAIL si Ratio < 0.3
```

---

## 📊 Baseline Reference

**v3.2 Completo (2020-2025):**
- Annual Return: 52.91%
- Max DD: -55.42%
- Sharpe: 1.06
- Calmar: 0.95

---

## 🎯 Qué Pasa Después

### Si PASS (Ratio ≥0.5):
✅ v3.2 VALIDADO
→ Paper Trading 4-8 semanas
→ Deployment

### Si FAIL (Ratio <0.3):
❌ Overfitting detectado
→ Revisar v3.0 o v3.1
→ Analizar causa

---

**Tiempo total:** 5 minutos (ambos backtests)

**Ir a:** http://localhost:9000

**Empezar con:** TRAIN period (2020-2023) ← PRIMERO
