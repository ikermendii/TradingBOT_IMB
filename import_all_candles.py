#!/usr/bin/env python3
"""
🚀 IMPORT ALL CANDLES - Multi-Timeframe
=======================================

Script para importar datos históricos de TODOS los timeframes necesarios

Timeframes a importar:
- 15m: Timeframe principal para ejecución
- 1h:  Timeframe intermedio para confirmación
- 4h:  Timeframe largo para tendencia

Exchange: Binance Spot
Symbol: BTC-USDT
Period: 2023-01-01 hasta hoy
"""

import sys
import os
import uuid
from datetime import datetime

# Configurar el directorio de trabajo
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Cargar la configuración de Jesse
from jesse.config import config
import config as project_config

# Actualizar la configuración de Jesse con la del proyecto
for key, value in project_config.config.items():
    if isinstance(value, dict) and key in config:
        config[key].update(value)
    else:
        config[key] = value

from jesse.modes import import_candles_mode

# =================================================
# CONFIGURACIÓN
# =================================================

exchange = 'Binance Spot'
symbol = 'BTC-USDT'
start_date = '2023-01-01'

# Timeframes a importar (en orden de más corto a más largo)
timeframes = [
    '15m',  # Ejecución principal
    '1h',   # Confirmación intermedia
    '4h',   # Tendencia largo plazo
]

# =================================================
# FUNCIÓN DE IMPORTACIÓN
# =================================================

def import_timeframe(timeframe):
    """Importa candles para un timeframe específico"""
    print()
    print("=" * 70)
    print(f"📊 IMPORTANDO: {symbol} @ {timeframe}")
    print("=" * 70)
    print(f"   Exchange:    {exchange}")
    print(f"   Symbol:      {symbol}")
    print(f"   Timeframe:   {timeframe}")
    print(f"   Start Date:  {start_date}")
    print(f"   End Date:    {datetime.now().strftime('%Y-%m-%d')}")
    print()

    try:
        # Generar un ID único para esta sesión
        client_id = str(uuid.uuid4())

        # Importar candles
        import_candles_mode.run(
            client_id=client_id,
            exchange=exchange,
            symbol=symbol,
            start_date_str=start_date,
            mode='candles',
            running_via_dashboard=False,  # Modo standalone
            show_progressbar=True
        )

        print()
        print(f"✅ {timeframe} importado exitosamente!")
        return True

    except KeyboardInterrupt:
        print(f"\n⚠️  Importación de {timeframe} interrumpida por el usuario")
        return False
    except Exception as e:
        print(f"\n❌ Error importando {timeframe}: {e}")
        import traceback
        traceback.print_exc()
        return False

# =================================================
# MAIN
# =================================================

if __name__ == '__main__':
    print()
    print("=" * 70)
    print("🚀 IMPORTACIÓN MULTI-TIMEFRAME")
    print("=" * 70)
    print()
    print(f"Exchange:  {exchange}")
    print(f"Symbol:    {symbol}")
    print(f"Period:    {start_date} → {datetime.now().strftime('%Y-%m-%d')}")
    print(f"Timeframes: {', '.join(timeframes)}")
    print()
    print("⏳ Este proceso puede tardar 15-30 minutos...")
    print("   No interrumpas el proceso una vez iniciado.")
    print()

    # Importar cada timeframe
    results = {}
    for tf in timeframes:
        success = import_timeframe(tf)
        results[tf] = success

        if not success:
            print()
            print("⚠️  Hubo un error, continuando con siguientes timeframes...")
            print()

    # Resumen final
    print()
    print("=" * 70)
    print("📊 RESUMEN DE IMPORTACIÓN")
    print("=" * 70)
    print()

    for tf, success in results.items():
        status = "✅ Exitoso" if success else "❌ Fallido"
        print(f"   {tf:6s} : {status}")

    successful = sum(1 for v in results.values() if v)
    total = len(results)

    print()
    print(f"Total: {successful}/{total} timeframes importados exitosamente")
    print()

    if successful == total:
        print("🎉 ¡Importación completa! Ahora puedes ejecutar backtests.")
    elif successful > 0:
        print("⚠️  Importación parcial. Algunos timeframes fallaron.")
    else:
        print("❌ La importación falló completamente.")

    print()
