#!/usr/bin/env python3
"""
Script para importar datos recientes para paper trading
"""

import sys
import os
import uuid

# Cargar configuración
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jesse.config import config
import config as project_config

# Actualizar configuración
for key, value in project_config.config.items():
    if isinstance(value, dict) and key in config:
        config[key].update(value)
    else:
        config[key] = value

from jesse.modes import import_candles_mode

# Configuración para paper trading
exchange = 'Binance Perpetual Futures'
symbol = 'BTC-USDT'
start_date = '2025-11-01'

print("=" * 60)
print("IMPORTANDO DATOS RECIENTES PARA PAPER TRADING")
print("=" * 60)
print(f"Exchange:    {exchange}")
print(f"Symbol:      {symbol}")
print(f"Start Date:  {start_date}")
print(f"Description: Ultimos 2 meses de datos")
print("=" * 60)
print()

try:
    client_id = str(uuid.uuid4())

    import_candles_mode.run(
        client_id=client_id,
        exchange=exchange,
        symbol=symbol,
        start_date_str=start_date,
        mode='candles',
        running_via_dashboard=False,
        show_progressbar=True
    )

    print()
    print("=" * 60)
    print("IMPORTACION COMPLETADA EXITOSAMENTE!")
    print("=" * 60)
    print()
    print("Proximos pasos:")
    print("1. Ejecutar: jesse run")
    print("2. O iniciar dashboard para paper trading")
    print()

except KeyboardInterrupt:
    print("\nImportacion interrumpida por el usuario")
    sys.exit(1)
except Exception as e:
    print(f"\nError durante la importacion: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
