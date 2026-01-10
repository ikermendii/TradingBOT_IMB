#!/usr/bin/env python3
"""
Script para importar datos históricos de candles desde Binance
Uso: python3 import_candles.py
"""

import sys
import os
import uuid

# Cargar la configuración de Jesse desde config.py
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jesse.config import config
# Cargar config.py del proyecto
import config as project_config
# Actualizar la configuración de Jesse con la del proyecto
for key, value in project_config.config.items():
    if isinstance(value, dict) and key in config:
        config[key].update(value)
    else:
        config[key] = value

from jesse.modes import import_candles_mode

# Configuración para backtest completo
exchange = 'Binance Perpetual Futures'
symbol = 'BTC-USDT'
start_date = '2020-01-01'  # Datos completos para backtest multi-regimen

print(f"🚀 Iniciando importación de candles...")
print(f"   Exchange: {exchange}")
print(f"   Symbol: {symbol}")
print(f"   Start Date: {start_date}")
print()

try:
    # Generar un ID único para esta sesión
    client_id = str(uuid.uuid4())

    # Importar candles sin usar el dashboard (modo standalone)
    import_candles_mode.run(
        client_id=client_id,
        exchange=exchange,
        symbol=symbol,
        start_date_str=start_date,
        mode='candles',
        running_via_dashboard=False,  # Modo standalone sin Redis
        show_progressbar=True
    )

    print()
    print("✅ Importación completada exitosamente!")

except KeyboardInterrupt:
    print("\n⚠️  Importación interrumpida por el usuario")
    sys.exit(1)
except Exception as e:
    print(f"\n❌ Error durante la importación: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
