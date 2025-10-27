# Documentación de la Estrategia

## Versión Actual: [v1, v2, v3, etc.]

### Changelog:
- **v1.0** (Fecha): Estrategia simple RSI básica
- **v2.0** (Fecha): Añadidas divergencias
- **v3.0** (Fecha): Multi-timeframe implementado
- **v4.0** (Fecha): Volume profile + FVG

### Lógica Actual:

#### Entry Long:
```
SI (Precio > EMA200 en 4H) Y
   (Divergencia Alcista detectada) Y
   (RSI < 40) Y
   (MACD cruza al alza) Y
   (Volumen > 1.2x promedio)
ENTONCES Comprar
```

#### Entry Short:
```
SI (Precio < EMA200 en 4H) Y
   (Divergencia Bajista detectada) Y
   (RSI > 60) Y
   (MACD cruza a la baja) Y
   (Volumen > 1.2x promedio)
ENTONCES Vender
```

#### Exit:
- Stop Loss: Entry ± (ATR × 1.5)
- TP1: 1.5R (cerrar 50%)
- TP2: 3R (cerrar 30%)
- TP3: 5R (cerrar 20%)
- Trailing: Activar después TP1

### Parámetros Ajustables:
```python
RSI_PERIOD = 14
RSI_OVERSOLD = 40
RSI_OVERBOUGHT = 60
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9
EMA_FAST = 50
EMA_SLOW = 200
ATR_PERIOD = 14
ATR_MULTIPLIER = 1.5
VOLUME_SURGE = 1.2
RISK_PERCENT = 1.5
```

### Resultados Históricos:
[Actualizar después de cada backtest importante]

| Versión | Periodo | Trades | Win% | PF | Net Profit | Max DD |
|---------|---------|--------|------|----|-----------:|--------|
| v1.0    | 2023    | 45     | 51%  | 1.2| +8.5%      | -12%   |
| v2.0    | 2023    | 68     | 58%  | 1.6| +15.3%     | -10%   |
| v3.0    | 2023    | [TBD]  |      |    |            |        |