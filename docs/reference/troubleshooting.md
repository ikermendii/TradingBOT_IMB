# Solución de Problemas Comunes

## Error: "ImportError: No module named 'jesse'"
**Causa**: Jesse no está instalado o Python usa versión incorrecta
**Solución**:
```bash
python -m pip install --upgrade jesse
# O especificar versión Python
python3.11 -m pip install jesse
```

## Error: "numpy.dtype size changed"
**Causa**: Incompatibilidad versiones numpy
**Solución**:
```bash
pip uninstall numpy
pip install numpy==1.23.5
```

## Error: Backtest no retorna resultados
**Causa**: Datos no descargados o periodo incorrecto
**Solución**:
1. Verificar datos:
```bash
   jesse list-candles
```
2. Reimportar si es necesario:
```bash
   jesse import-candles 'Binance' 'BTC-USDT' '2023-01-01'
```

## Bot no ejecuta trades en paper trading
**Causa**: Condiciones muy restrictivas o configuración incorrecta
**Solución**:
1. Añadir prints de debug:
```python
   print(f"RSI: {rsi}, Divergence: {div}, Trend: {trend}")
```
2. Relajar condiciones temporalmente para test
3. Verificar config.py está correctamente configurado

## Métricas de backtest son irreales (>100% ganancia)
**Causa**: Look-ahead bias o error en la lógica
**Solución**:
1. Revisar que no uses datos futuros:
```python
   # INCORRECTO:
   rsi = indicators['rsi'][0]  # Mira al futuro
   
   # CORRECTO:
   rsi = indicators['rsi']     # Usa valor actual
```
2. Verificar stop loss y take profit están bien definidos

## [AÑADIR MÁS A MEDIDA QUE ENCUENTRES ERRORES]