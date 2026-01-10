#!/usr/bin/env python
"""
Simple backtest using jesse-research (no Redis needed)
"""
import sys
import os
os.environ['REDIS_HOST'] = ''  # Disable Redis
os.environ['POSTGRES_HOST'] = ''  # Disable Postgres

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("\n" + "="*80)
print("BACKTEST: TrendFollowing Strategy (2020-2022)")
print("="*80 + "\n")

try:
    from backtesting import research
    from routes import routes

    print("📊 Configuración:")
    print(f"   Routes: {routes}")
    print(f"   Periodo: 2020-01-01 → 2022-12-31")
    print()

    print("⏳ Descargando velas...")

    # Use jesse's research module
    result = research.backtest(
        start_date='2020-01-01',
        finish_date='2022-12-31'
    )

    print("\n✅ Backtest completado!\n")
    print(result)

except ImportError as e:
    print(f"❌ Error de import: {e}")
    print("\nIntentando método alternativo...")

    # Método alternativo: usar subprocess
    import subprocess

    print("\n🔄 Iniciando backtest via subprocess...")
    result = subprocess.run(
        ['python', '-c', '''
import os
os.chdir(r"c:\\Users\\ikerm\\Desktop\\Pruebas BOTTrading\\TradingBot_Project")

# Simular que estamos en modo research
os.environ["JESSIE_MODE"] = "research"

from jesse import research
from routes import routes

result = research.backtest(
    start_date="2020-01-01",
    finish_date="2022-12-31",
    candles={},
    routes=routes
)

print("\\n" + "="*80)
print("RESULTADOS")
print("="*80)
print(result)
'''],
        capture_output=True,
        text=True,
        cwd=r"c:\Users\ikerm\Desktop\Pruebas BOTTrading\TradingBot_Project"
    )

    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)

except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()

    print("\n" + "="*80)
    print("SOLUCIÓN ALTERNATIVA")
    print("="*80)
    print()
    print("Por favor, ejecuta el backtest manualmente desde la web UI:")
    print()
    print("1. Asegúrate que Redis esté corriendo:")
    print("   wsl sudo service redis-server start")
    print()
    print("2. Inicia Jesse web server (en otra terminal):")
    print("   cd c:\\Users\\ikerm\\Desktop\\Pruebas BOTTrading\\TradingBot_Project")
    print("   jesse run-server")
    print()
    print("3. Abre navegador en: http://localhost:9000")
    print()
    print("4. Configura backtest:")
    print("   - Start: 2020-01-01")
    print("   - End: 2022-12-31")
    print("   - Click 'Start Backtest'")
    print()
