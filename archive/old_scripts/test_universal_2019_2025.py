#!/usr/bin/env python3
"""
TEST UNIVERSAL ROBUST STRATEGY - 2019-2025 COMPLETO
====================================================

Test de robustez multi-regimen:
- 2019: Recovery post-crash 2018
- 2020-2021: Bull parabolico (+590%)
- 2022: Bear market (-64%)
- 2023-2025: Recovery volatil

Parametros: RSI 30/70, EMA 50/200, 2 ATR stop, 3:1 R:R
NO optimizados - industria estandar solamente
"""
import sys
import os

# Disable database requirements
os.environ['REDIS_HOST'] = ''
os.environ['POSTGRES_HOST'] = ''
os.environ['JESSE_MODE'] = 'research'

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("\n" + "="*70)
print("  TEST UNIVERSAL ROBUST - 2019-2025 COMPLETO")
print("  Parametros Estandar (NO optimizados)")
print("="*70 + "\n")

try:
    from jesse import research

    # Import routes - UniversalRobust ya esta configurado
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'code'))
    from routes import routes

    print("Estrategia configurada:", routes)
    print("\nPeriodo: 2019-01-01 a 2025-12-31 (6.9 años)")
    print("Regimenes incluidos:")
    print("  - 2019: Recovery")
    print("  - 2020-2021: Bull parabolico")
    print("  - 2022: Bear market")
    print("  - 2023-2025: Recovery volatil")
    print("\nDescargando velas y ejecutando backtest...")
    print("Esto puede tardar 5-10 minutos...\n")

    result = research.backtest(
        start_date='2019-01-01',
        finish_date='2025-12-31',
        candles={},
        routes=routes
    )

    print("\n" + "="*70)
    print("RESULTADOS UNIVERSAL ROBUST (2019-2025)")
    print("="*70)
    print(result)

    print("\n" + "="*70)
    print("ANALISIS")
    print("="*70)
    print("\nCRITERIOS DE EXITO:")
    print("  - Net Profit > 0% (sobrevive TODOS los regimenes)")
    print("  - Max Drawdown < 50% (aceptable para 6.9 años)")
    print("  - Win Rate > 18% (minimo para R:R 3:1)")
    print("  - Sharpe Ratio > 0.3 (positivo en largo plazo)")
    print("\nSi PASA todos los criterios -> Bot es ROBUSTO")
    print("Si FALLA cualquiera -> Necesita ajuste")
    print("="*70 + "\n")

except ImportError as e:
    print(f"\nError: {e}")
    print("\nJesse research module not available.")
    print("Please ensure Jesse is installed properly.")

except Exception as e:
    print(f"\nError durante backtest: {e}")
    import traceback
    traceback.print_exc()

    print("\n" + "="*70)
    print("TROUBLESHOOTING")
    print("="*70)
    print("\n1. Verificar que Jesse research esta instalado:")
    print("   python -c \"from jesse import research; print('OK')\"")
    print("\n2. Verificar que routes.py tiene UniversalRobust:")
    print("   python -c \"from code.routes import routes; print(routes)\"")
    print("\n3. Si falla por memoria, reducir periodo:")
    print("   - Test 1: 2020-2021 (bull parabolico)")
    print("   - Test 2: 2022 (bear market)")
    print("   - Test 3: 2023-2025 (recovery volatil)")
    print("="*70 + "\n")
