# Resultados de Backtests

## Formato de Registro:

Cada backtest debe documentarse así:

---

## [FECHA] - [ESTRATEGIA vX] - [PAR] - [PERIODO]

### Configuración:
- Capital Inicial: $10,000
- Comisiones: 0.04%
- Timeframe: 15m
- Periodo: YYYY-MM-DD a YYYY-MM-DD

### Métricas Principales:
| Métrica              | Valor        |
|---------------------|--------------|
| Total Trades        | XX           |
| Winning Trades      | XX (XX%)     |
| Losing Trades       | XX (XX%)     |
| Win Rate            | XX%          |
| Profit Factor       | X.XX         |
| Net Profit          | $X,XXX (XX%) |
| Max Drawdown        | -XX%         |
| Sharpe Ratio        | X.XX         |
| Average Win         | $XXX (X.X%)  |
| Average Loss        | $XXX (X.X%)  |
| Largest Win         | $XXX         |
| Largest Loss        | $XXX         |

### Análisis:
**Fortalezas**:
- Punto fuerte 1
- Punto fuerte 2

**Debilidades**:
- Punto débil 1
- Punto débil 2

**Próxima acción**:
- [ ] Optimizar parámetro X
- [ ] Añadir filtro Y
- [ ] Testear en otro par

### Screenshots:
[Guardar en backtests/screenshots/FECHA_PAR_vX.png]

---

## EJEMPLO DE ENTRADA:

## 2024-01-15 - Estrategia v1 - BTC-USDT - 2023

### Configuración:
- Capital Inicial: $10,000
- Comisiones: 0.04%
- Timeframe: 15m
- Periodo: 2023-01-01 a 2023-12-31

### Métricas Principales:
| Métrica              | Valor          |
|---------------------|----------------|
| Total Trades        | 145            |
| Winning Trades      | 74 (51%)       |
| Losing Trades       | 71 (49%)       |
| Win Rate            | 51%            |
| Profit Factor       | 1.23           |
| Net Profit          | $1,234 (12.3%) |
| Max Drawdown        | -18.5%         |
| Sharpe Ratio        | 0.87           |
| Average Win         | $125 (1.25%)   |
| Average Loss        | $98 (0.98%)    |
| Largest Win         | $543           |
| Largest Loss        | $287           |

### Análisis:
**Fortalezas**:
- Win rate ligeramente positivo (51%)
- Average win > Average loss
- Profit factor >1 (rentable)

**Debilidades**:
- Drawdown muy alto (-18.5%)
- Sharpe ratio bajo (<1)
- Demasiados trades (probablemente ruido)

**Próxima acción**:
- [x] Añadir filtro de divergencias para reducir trades
- [ ] Optimizar gestión de riesgo para reducir drawdown
- [ ] Testear en ETH-USDT para validar

### Screenshots:
[Ver: backtests/screenshots/2024-01-15_BTC_v1.png]

---

## [AÑADIR NUEVOS BACKTESTS AQUÍ]
## 2025-10-25 - Multitimeframe v1.0 - BTC-USDT - SPOT - 2023-2025

### Configuración:
- Capital Inicial: 0,000
- Comisiones: 0.04%
- Exchange: Binance Spot
- Timeframe: 15m
- Periodo: 2023-01-01 a 2025-10-19
- Stop Loss: Manual con self.liquidate()
- Take Profits: TP1(1.5R), TP2(3R), Trailing Stop

### Métricas Principales:
| Métrica              | Valor          |
|---------------------|----------------|
| Total Trades        | 2              |
| Winning Trades      | 0 (0%)         |
| Losing Trades       | 2 (100%)       |
| Win Rate            | 0%             |
| Net Profit          | -1.22 (-0.51%) |
| Max Drawdown        | -1.47%         |
| Annual Return       | -0.18%         |
| Sharpe Ratio        | -0.19          |
| Average Win         | /bin/bash             |
| Average Loss        | 5.61         |
| Largest Win         | /bin/bash             |
| Largest Loss        | -6.02        |
| Avg Holding Time    | 6h 52m         |

### Análisis:
**Debilidades CRÍTICAS**:
- Solo 2 trades en 3 años (condiciones demasiado restrictivas)
- 0% win rate (ambos trades perdedores)
- Estrategia NO funciona en Spot Trading (sin SHORT)

**Problema Fundamental**:
- SPOT no permite operaciones SHORT
- RSI < 35 es extremadamente conservador
- Requiere precio > EMA 200 + EMA 50 > EMA 200 simultáneamente
- 4 horas entre señales reduce oportunidades

**Próxima acción**:
- [x] Cambiar a Binance Futures para permitir SHORT
- [x] Relajar RSI: < 35 → < 45 (LONG), > 65 → > 55 (SHORT)
- [x] Reducir tiempo entre señales: 4h → 30 min
- [x] Simplificar filtro de tendencia

---

## 2025-10-25 - Multitimeframe v2.0 - BTC-USDT - FUTURES - 2023-2025

### Configuración:
- Capital Inicial: 0,000
- Comisiones: 0.02%
- Exchange: Binance Perpetual Futures
- Timeframe: 15m
- Periodo: 2023-01-01 a 2025-10-19
- Stop Loss: Manual con self.liquidate()
- Take Profits: TP1(1.5R), TP2(3R), Trailing Stop

### Métricas Principales:
| Métrica              | Valor          |
|---------------------|----------------|
| Total Trades        | 4              |
| Winning Trades      | 0 (0%)         |
| Losing Trades       | 4 (100%)       |
| Win Rate            | 0%             |
| Longs \| Shorts      | 50% \| 50%     |
| Net Profit          | -7.20 (-0.87%) |
| Max Drawdown        | -1.86%         |
| Annual Return       | -0.31%         |
| Sharpe Ratio        | -0.33          |
| Average Win         | /bin/bash             |
| Average Loss        | 1.80         |
| Largest Win         | /bin/bash             |
| Largest Loss        | -6.57        |
| Avg Holding Time    | 3h 46m         |

### Análisis:
**Mejoras respecto a v1.0**:
- Permite SHORT (50% LONG / 50% SHORT)
- 4 trades vs 2 trades (100% más oportunidades)
- Tiempo de holding más corto (3h vs 7h)

**Debilidades PERSISTENTES**:
- Solo 4 trades en 3 años (sigue siendo muy restrictivo)
- 0% win rate (todos perdedores)
- Condiciones aún demasiado estrictas

**Problemas identificados**:
- RSI < 35 / > 65 sigue siendo muy extremo
- Requiere EMA 50 > EMA 200 + precio > EMA 200
- 4 horas entre señales muy restrictivo

**Próxima acción**:
- [x] Relajar umbrales de RSI
- [x] Simplificar filtros de tendencia
- [x] Reducir tiempo entre señales

---

## 2025-10-25 - Multitimeframe v3.0 - BTC-USDT - FUTURES - 2023-2025 (BUG: Trade Eterno)

### Configuración:
- Capital Inicial: 0,000
- Comisiones: 0.02%
- Exchange: Binance Perpetual Futures
- Timeframe: 15m
- Periodo: 2023-01-01 a 2025-10-19
- Condiciones: RSI < 45 (LONG), RSI > 55 (SHORT)
- Tiempo entre señales: 30 minutos
- Filtro tendencia: Solo EMA 50 vs EMA 200

### Métricas Principales:
| Métrica              | Valor           |
|---------------------|-----------------|
| Total Trades        | 2               |
| Winning Trades      | 1 (50%)         |
| Losing Trades       | 1 (50%)         |
| Win Rate            | 50%             |
| Longs \| Shorts      | 50% \| 50%      |
| Net Profit          | 9,353 (493%)  |
| Max Drawdown        | -27.52%         |
| Annual Return       | 89.14%          |
| Sharpe Ratio        | 1.63            |
| Average Win         | 9,371         |
| Average Loss        | 8.30          |
| Largest Win         | 9,371         |
| Largest Loss        | -8.30         |
| Avg Holding Time    | 12,207h (508 DÍAS!) |
| Winning Trade Time  | 24,413h (1,017 DÍAS!) |
| Open Trades         | 1 (nunca cerró) |

### Análisis:
**BUG CRÍTICO DETECTADO**:
- Un trade se mantuvo abierto 1,017 DÍAS (2.8 años)
- Capturó toda la subida de BTC pero es completamente irrealista
- Estrategia = "Buy and Hold" no intencional

**Causa raíz**:
- TP1 (1.5R): Cierra 50% ✅
- TP2 (3.0R): Cierra 30% ✅  
- **20% RESTANTE NUNCA SE CIERRA** ❌
- Trailing stop solo mueve el SL, no cierra activamente

**Solución implementada**:
- [x] Añadir TP3 en 6R que cierra el 20% final
- [x] Usar self.liquidate() para cerrar todo al alcanzar 6R

**Estado**:
- ⚠️ RESULTADOS NO VÁLIDOS (bug de cierre)
- Esperando backtest de v3.1 con corrección

---

## [PRÓXIMO BACKTEST: v3.1 CON TP3 IMPLEMENTADO]

---

## 2025-10-25 - Multitimeframe v3.1 - BTC-USDT - FUTURES - 2023-2025

### Configuración:
- Capital Inicial: $10,000
- Comisiones: 0.02%
- Exchange: Binance Perpetual Futures
- Timeframe: 15m
- Periodo: 2023-01-01 a 2025-10-19
- Stop Loss: ATR(14) x 1.8 (con self.stop_loss)
- Take Profits: TP1(1.5R 50%), TP2(3R 30%), TP3(6R 20% + trailing)
- Cambios clave v3.1: Cálculo de R con riesgo inicial, TP3 que liquida 20% final

### Métricas Principales:
| Métrica              | Valor             |
|---------------------|-------------------|
| Total Trades        | 575               |
| Winning Trades      | 115 (20.0%)       |
| Losing Trades       | 460 (80.0%)       |
| Win Rate            | 20%               |
| Longs \| Shorts      | 64.17% \| 35.83%   |
| Net Profit          | -$4,116.17 (-41.16%) |
| Max Drawdown        | -46.11%           |
| Annual Return       | -17.41%           |
| Sharpe Ratio        | -1.24             |
| Sortino Ratio       | -1.93             |
| Calmar Ratio        | -0.38             |
| Average Win         | $126.39           |
| Average Loss        | $40.55            |
| Largest Win         | $431.59           |
| Largest Loss        | -$152.96          |
| Avg Holding Time    | 7h 50m            |

### Análisis:
**Observaciones**:
- Volumen de trades muy alto (575) → comisiones elevadas ($3,199.55) y sobreoperación.
- Win rate bajo (20%), aunque R medio de ganadoras > perdedoras (3.12x).
- Drawdown y retorno anual negativos: estrategia no rentable así configurada.

**Causas probables**:
- Condiciones de entrada demasiado permisivas (RSI 45/55, cooldown 30m, sin filtro de volatilidad/volumen estricto).
- Falta de filtro de tendencia con precio relativo a EMA200.

**Acciones tomadas (v3.2-preview)**:
- Aumentado cooldown entre señales a 90 min.
- Umbrales RSI: LONG < 40, SHORT > 60.
- Filtro de tendencia más estricto: precio y EMA50 respecto a EMA200.
- Requerido volumen positivo y volatilidad mínima (ATR/close ≥ 0.3%).
- Límite de entradas por día (8) para reducir churn/fees.

**Siguiente paso**:
- Ejecutar backtest v3.2 con estos filtros para validar reducción de trades y mejora de métricas.

---

## 2025-10-25 - Multitimeframe v4.0 Hybrid - BTC-USDT - FUTURES - 2023-2025

### Configuración:
- Capital Inicial: $10,000
- Comisiones: 0.04%
- Exchange: Binance Perpetual Futures
- Timeframe: 15m
- Periodo: 2023-01-08 a 2025-10-17
- Stop Loss: ATR(14) x 1.8
- Take Profits: TP1(1.5R 50%), TP2(3R 30%), TP3(6R 20%)
- **Límite diario**: 3% pérdida máxima (NO límite numérico de trades)
- **Parámetros Hybrid**:
  - RSI oversold: 42 (híbrido entre permisivo 45 y restrictivo 40)
  - RSI overbought: 58 (híbrido entre permisivo 55 y restrictivo 60)
  - Cooldown: 60 minutos
  - Filtros: Tendencia estricta + volumen + volatilidad (ATR/close ≥ 0.3%)
  - **SIN divergencias** (reservadas para PHASE 2)

### Métricas Principales:
| Métrica              | Valor             |
|---------------------|-------------------|
| Total Trades        | 6                 |
| Winning Trades      | 1 (16.67%)        |
| Losing Trades       | 5 (83.33%)        |
| Win Rate            | 16.67%            |
| Longs \| Shorts      | 0% \| 100%         |
| Net Profit          | -$101.45 (-1.01%) |
| Max Drawdown        | -1.57%            |
| Annual Return       | -0.37%            |
| Sharpe Ratio        | -0.25             |
| Sortino Ratio       | -0.42             |
| Calmar Ratio        | -0.23             |
| Omega Ratio         | 0.66              |
| Average Win         | $191.74           |
| Average Loss        | $58.64            |
| Ratio Avg Win/Loss  | 3.27x             |
| Largest Win         | $191.74           |
| Largest Loss        | -$79.82           |
| Total Fees          | $43.03            |
| Avg Holding Time    | 5h 23m            |
| Win Trades Time     | 3h 30m            |
| Losing Trades Time  | 5h 45m            |
| Winning Streak      | 1                 |
| Losing Streak       | 3                 |

### Análisis:

**Mejoras respecto a v3.1**:
- ✅ Reducción DRÁSTICA de trades: 575 → 6 (98.96% menos)
- ✅ Reducción de pérdidas: -41.16% → -1.01% (97.5% mejor)
- ✅ Reducción de drawdown: -46.11% → -1.57% (96.6% mejor)
- ✅ Sharpe ratio mejorado: -1.24 → -0.25 (80% mejor)
- ✅ Ratio Win/Loss excelente: 3.27x (ganadoras 3x más grandes que perdedoras)

**Problemas CRÍTICOS**:
- ❌ Solo 6 trades en 3 años (2 trades/año) → INSUFICIENTE para ser rentable
- ❌ Win rate 16.67% (1 de 6) → EXTREMADAMENTE BAJO
- ❌ 100% shorts, 0% longs → Estrategia desbalanceada
- ❌ Fees $43.03 representan 42% de la pérdida neta
- ❌ Losing streak de 3 trades consecutivos

**Análisis Técnico**:

**¿Por qué solo 6 trades?**
Los filtros híbridos son DEMASIADO estrictos en combinación:
1. RSI 42/58 (más restrictivo que v3.1 con 45/55)
2. Cooldown 60 min (2x más que v3.1 con 30 min)
3. Tendencia estricta (precio + EMA50 vs EMA200)
4. Volumen positivo requerido
5. Volatilidad mínima (ATR/close ≥ 0.3%)

**¿Por qué 100% shorts?**
- RSI < 42 para LONG es MUY extremo (solo en sobreventa severa)
- En mercado alcista de 2023-2025, BTC rara vez cae a RSI < 42
- La estrategia solo encontró oportunidades en caídas (shorts)

**¿Por qué win rate 16.67%?**
- 1 ganadora de $191.74 → TP2 o TP3 alcanzado (excelente)
- 5 perdedoras promedio -$58.64 → Stop loss activándose
- Los pocos trades generados no tienen calidad suficiente

**Paradoja identificada**:
- v3.1: Muchos trades (575), mala calidad → -41.16%
- v4.0: Pocos trades (6), sigue mala calidad → -1.01%
- **Necesitamos**: Trades medianos (50-100), BUENA calidad → +20-50%

**Causas raíz del fracaso**:
1. **Filtros en conflicto**: RSI extremo + tendencia estricta + volatilidad alta = casi nunca coinciden
2. **Sin divergencias**: La señal PRINCIPAL de la estrategia está desactivada
3. **Estrategia incompleta**: v4.0 es PHASE 1 (básica), necesita PHASE 2 (divergencias)

**Próximas acciones**:

**Opción A - Ajustar v4.1 (manteniendo PHASE 1)**:
- [ ] Relajar RSI: 42 → 45 (LONG), 58 → 55 (SHORT)
- [ ] Reducir cooldown: 60min → 45min
- [ ] Simplificar filtro de tendencia: Solo EMA50 vs EMA200 (no precio)
- [ ] Relajar volatilidad: ATR/close ≥ 0.2% (en vez de 0.3%)
- **Objetivo**: 30-50 trades con 30-40% win rate

**Opción B - Activar PHASE 2 (divergencias RSI)** ⭐ RECOMENDADO:
- [ ] Activar detección de divergencias RSI
- [ ] Mantener filtros híbridos pero usar divergencia como señal principal
- [ ] RSI como filtro de contexto, no como trigger
- **Objetivo**: 20-40 trades de ALTA calidad con 50-60% win rate

**Opción C - Probar mini-período de validación**:
- [ ] Backtest solo Q1 2024 (3 meses) con diferentes configuraciones
- [ ] Encontrar parámetros óptimos antes de testear periodo completo
- **Objetivo**: Iteración rápida sin esperar backtests largos

### Recomendación:

**ACTIVAR PHASE 2 (Divergencias RSI)**

La estrategia fue diseñada desde el inicio para usar divergencias como señal principal. Los filtros básicos (RSI, tendencia, volumen) nunca fueron pensados para funcionar solos.

**Razones**:
1. Las divergencias son la ESENCIA de la estrategia Multitimeframe
2. v4.0 es solo "esqueleto" sin el "cerebro" (divergencias)
3. Históricamente, las divergencias RSI tienen 55-65% win rate
4. Reducirán trades pero aumentarán calidad significativamente

**Estado actual**:
- ⚠️ v4.0 NO ES UNA ESTRATEGIA COMPLETA
- ⚠️ Es solo PHASE 1 del roadmap (sin divergencias)
- ✅ Sirve como baseline para comparar con v5.0

### Próximo backtest sugerido:
**v5.0 - PHASE 2: RSI Divergences activadas**

---

## 2025-10-25 - Multitimeframe v5.0 - BTC-USDT - FUTURES - 2023-2025

### Configuración:
- Capital Inicial: $10,000
- Comisiones: 0.04%
- Exchange: Binance Perpetual Futures
- Leverage: 20x
- Timeframe: 15m
- Periodo: 2023-01-08 a 2025-10-17
- Stop Loss: ATR(14) x 1.8
- Take Profits: TP1(1.5R 50%), TP2(3R 30%), TP3(6R 20%)
- **PHASE 2 ACTIVADA**: Divergencias RSI como señal principal
- **Parámetros v5.0**:
  - Señal: SOLO divergencias RSI (alcista/bajista)
  - RSI threshold: LONG < 45, SHORT > 55
  - Cooldown: 60 minutos
  - Volatilidad: ATR/close ≥ 0.3%
  - Filtros: Tendencia + Volumen + MACD (ALL con AND)

### Métricas Principales:
| Métrica              | Valor             |
|---------------------|-------------------|
| Total Trades        | 0                 |
| Winning Trades      | 0                 |
| Losing Trades       | 0                 |
| Win Rate            | N/A               |
| Net Profit          | $0 (0%)           |

### Análisis:
**Problema CRÍTICO**:
- ❌ **CERO trades ejecutados** en 3 años (2023-2025)
- Condiciones demasiado restrictivas: divergencias + RSI + tendencia + volumen + MACD + volatilidad (ALL con AND)

**Causa raíz**:
1. **Lógica AND demasiado estricta**: Requiere divergencia + MACD + RSI extremo + tendencia + volumen SIMULTÁNEAMENTE
2. **Divergencias demasiado restrictivas**: Solo 15 velas de lookback, requiere 1% price diff + 2% RSI diff
3. **Conflicto de señales**: MACD puede no estar alineado cuando hay divergencia RSI válida

**Solución implementada (v5.1)**:
- Cambiar de AND a OR para señales
- Hacer divergencias más permisivas (40 velas lookback, 0.3% price + 3 RSI points)
- Permitir que cualquier señal fuerte (divergencia O RSI O MACD) pueda abrir trade

**Estado**:
- ⚠️ v5.0 FALLIDO - Demasiado restrictivo
- ✅ Lección aprendida: AND logic con 6+ filtros = impossible to satisfy

---

## 2025-10-25 - Multitimeframe v5.1 - BTC-USDT - FUTURES - 2023-2025

### Configuración:
- Capital Inicial: $10,000
- Comisiones: 0.04%
- Exchange: Binance Perpetual Futures
- Leverage: 20x
- Timeframe: 15m
- Periodo: 2023-01-08 a 2025-10-17
- Stop Loss: ATR(14) x 1.8
- Take Profits: TP1(1.5R 50%), TP2(3R 30%), TP3(6R 20%)
- **Parámetros v5.1**:
  - **Cambio CRÍTICO**: Lógica OR para señales (divergencia O RSI O MACD)
  - Divergencias PERMISIVAS: 40 velas lookback, 0.3% price + 3 RSI points
  - RSI: LONG < 45, SHORT > 55
  - Cooldown: 60 minutos
  - Volatilidad: ATR/close ≥ 0.3%

### Métricas Principales:
| Métrica              | Valor             |
|---------------------|-------------------|
| Total Trades        | 333               |
| Winning Trades      | 75 (22.52%)       |
| Losing Trades       | 258 (77.48%)      |
| Win Rate            | 22.52%            |
| Net Profit          | -$3,956 (-39.56%) |
| Max Drawdown        | ~-45%             |

### Análisis:
**Problema inverso a v5.0**:
- ✅ Generó muchos trades (333 en 3 años)
- ❌ **Win rate TERRIBLE: 22.52%** (objetivo era 55%+)
- ❌ **Pérdida catastrófica: -39.56%**

**Causa raíz**:
1. **Lógica OR demasiado permisiva**: Permite trades de baja calidad (RSI solo, MACD solo)
2. **Divergencias permisivas**: 0.3% + 3 puntos detecta muchas divergencias falsas
3. **Sin filtro de calidad**: No verifica que haya espacio para mínimo 2R antes de abrir

**Feedback del usuario**:
> "un trader de verdad no abre ningun trade si no lleva un minimo de 2R"

**Solución implementada (v5.2)**:
- Volver a AND logic pero SOLO con divergencias obligatorias
- Agregar verificación de 2R mínimo antes de abrir trade
- RSI debe estar en zona EXTREMA (<40 para LONG, >60 para SHORT)
- Aumentar volatilidad requerida a 0.4%
- TPs más conservadores: 1.2R, 2.5R, 4R (más fáciles de alcanzar)

**Estado**:
- ⚠️ v5.1 FALLIDO - Demasiado permisivo, baja calidad
- ✅ Lección aprendada: OR logic sin filtro de calidad = muchos trades perdedores

**Comparación v5.0 vs v5.1**:
| Métrica | v5.0 | v5.1 |
|---------|------|------|
| Trades | 0 | 333 |
| Win Rate | N/A | 22.52% |
| Net Profit | 0% | -39.56% |
| Problema | Too restrictive | Too permissive |

---

## 2025-10-25 - Multitimeframe v5.2 - PROFESSIONAL TRADER - PENDIENTE

### Configuración:
- Capital Inicial: $10,000
- Comisiones: 0.04%
- Exchange: Binance Perpetual Futures
- Leverage: 20x
- Timeframe: 15m
- Periodo: 2023-01-08 a 2025-10-17
- Stop Loss: ATR(14) x 1.8
- Take Profits: TP1(1.2R 50%), TP2(2.5R 30%), TP3(4R 20%)
- **Parámetros v5.2 - PROFESSIONAL RULES**:
  - **REGLA FUNDAMENTAL**: Solo abrir trade si hay mínimo 2R disponible
  - Señal: SOLO divergencias RSI (obligatorio - no RSI/MACD solos)
  - RSI EXTREMO: LONG < 40, SHORT > 60 (más restrictivo que v5.1)
  - Cooldown: 60 minutos
  - Volatilidad: ATR/close ≥ 0.4% (más restrictivo para garantizar 2R)
  - Divergencias: Mantener permisivas (40 velas, 0.3% + 3 RSI)
  - Todos los filtros deben alinearse (AND logic)

### Objetivo:
- **Win rate**: 55%+ (objetivo principal)
- **Trade frequency**: Balanceado (30-100 trades en 3 años)
- **Quality over quantity**: Solo trades profesionales con 2R mínimo

### Resultados:
⏳ **PENDIENTE DE EJECUCIÓN**

Esperando que el usuario ejecute backtest desde web interface (http://localhost:9000)

