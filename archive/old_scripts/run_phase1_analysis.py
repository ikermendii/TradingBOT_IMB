"""
🔬 RE-OPTIMIZATION PHASE 1: Baseline Analysis 2019-2025

Este script ejecuta los backtests de Fase 1 para entender dónde v9.3-RSI36 falla.

Ejecuta:
1. Baseline completo 2019-2025
2. Breakdown por año (2019, 2020, 2021)

Uso:
    python run_phase1_analysis.py
"""

import subprocess
import json
from datetime import datetime
import os

# ============================================
# CONFIGURACIÓN
# ============================================

# Periodos a testear
TESTS = [
    {
        'name': 'Baseline 2019-2025',
        'start': '2019-01-01',
        'end': '2025-10-17',
        'description': 'Test completo para baseline de referencia'
    },
    {
        'name': '2019 Individual',
        'start': '2019-01-01',
        'end': '2019-12-31',
        'description': 'Pre-parabólico, BTC +94%'
    },
    {
        'name': '2020 Individual',
        'start': '2020-01-01',
        'end': '2020-12-31',
        'description': 'Bull parabólico inicio, BTC +305% 🔴'
    },
    {
        'name': '2021 Individual',
        'start': '2021-01-01',
        'end': '2021-12-31',
        'description': 'Bull parabólico peak, BTC +60% 🔴'
    }
]

# Estrategia y símbolo
STRATEGY = 'Multitimeframe'
SYMBOL = 'BTC-USDT'
EXCHANGE = 'Binance Perpetual Futures'

# ============================================
# FUNCIONES
# ============================================

def run_backtest_wsl(start_date, end_date):
    """
    Ejecuta backtest usando Jesse en WSL

    Nota: Jesse en WSL no soporta backtests desde CLI directamente.
    Necesitamos usar la interfaz web o API.

    Este script proporciona las instrucciones para ejecutar manualmente.
    """
    print(f"\n⚠️ EJECUTAR MANUALMENTE EN NAVEGADOR:")
    print(f"   1. Abre http://localhost:9000")
    print(f"   2. En 'Backtest', selecciona:")
    print(f"      - Start Date: {start_date}")
    print(f"      - End Date: {end_date}")
    print(f"      - Strategy: {STRATEGY}")
    print(f"      - Symbol: {SYMBOL}")
    print(f"      - Exchange: {EXCHANGE}")
    print(f"   3. Click 'Start Backtest'")
    print(f"   4. Espera resultados y ANOTA:")
    print(f"      - Net Profit %")
    print(f"      - Max Drawdown %")
    print(f"      - Win Rate %")
    print(f"      - Total Trades")
    print(f"      - Sharpe Ratio")
    print(f"      - Calmar Ratio")

    input(f"\nPresiona ENTER cuando hayas completado el backtest...")

    # Pedir al usuario que ingrese resultados
    print(f"\n📊 Ingresa los resultados del backtest:")
    net_profit = input(f"   Net Profit % (ej: -66.9): ")
    max_dd = input(f"   Max Drawdown % (ej: -84.47): ")
    win_rate = input(f"   Win Rate % (ej: 19.84): ")
    total_trades = input(f"   Total Trades (ej: 892): ")
    sharpe = input(f"   Sharpe Ratio (ej: -0.47): ")
    calmar = input(f"   Calmar Ratio (ej: -0.21): ")

    return {
        'net_profit_pct': float(net_profit),
        'max_drawdown_pct': float(max_dd),
        'win_rate_pct': float(win_rate),
        'total_trades': int(total_trades),
        'sharpe_ratio': float(sharpe),
        'calmar_ratio': float(calmar),
        'start_date': start_date,
        'end_date': end_date
    }

def save_results(results, filename='phase1_results.json'):
    """Guarda resultados en JSON"""
    filepath = os.path.join(os.path.dirname(__file__), filename)

    with open(filepath, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n✅ Resultados guardados en: {filename}")

def print_summary(all_results):
    """Imprime resumen de todos los tests"""
    print("\n" + "="*70)
    print("📊 RESUMEN FASE 1: BASELINE ANALYSIS")
    print("="*70)

    for result in all_results:
        print(f"\n{result['name']}:")
        print(f"  Periodo: {result['data']['start_date']} → {result['data']['end_date']}")
        print(f"  Net Profit: {result['data']['net_profit_pct']:.2f}%")
        print(f"  Max DD: {result['data']['max_drawdown_pct']:.2f}%")
        print(f"  Win Rate: {result['data']['win_rate_pct']:.2f}%")
        print(f"  Trades: {result['data']['total_trades']}")
        print(f"  Sharpe: {result['data']['sharpe_ratio']:.2f}")
        print(f"  Calmar: {result['data']['calmar_ratio']:.2f}")

    print("\n" + "="*70)
    print("📋 ANÁLISIS:")
    print("="*70)

    # Identificar peores años
    yearly_results = [r for r in all_results if 'Individual' in r['name']]
    if yearly_results:
        worst_year = min(yearly_results, key=lambda x: x['data']['net_profit_pct'])
        print(f"\n🔴 PEOR AÑO: {worst_year['name']}")
        print(f"   Net Profit: {worst_year['data']['net_profit_pct']:.2f}%")
        print(f"   Max DD: {worst_year['data']['max_drawdown_pct']:.2f}%")

        best_year = max(yearly_results, key=lambda x: x['data']['net_profit_pct'])
        print(f"\n✅ MEJOR AÑO: {best_year['name']}")
        print(f"   Net Profit: {best_year['data']['net_profit_pct']:.2f}%")

    # Comparar baseline con suma de años
    baseline = next((r for r in all_results if 'Baseline' in r['name']), None)
    if baseline:
        print(f"\n📊 BASELINE 2019-2025:")
        print(f"   Net Profit: {baseline['data']['net_profit_pct']:.2f}%")
        print(f"   Max DD: {baseline['data']['max_drawdown_pct']:.2f}%")

        if baseline['data']['net_profit_pct'] < 0:
            print(f"\n⚠️ CONFIRMADO: v9.3-RSI36 NO es robusto en periodos largos")
        else:
            print(f"\n✅ v9.3-RSI36 funciona en periodo largo")

# ============================================
# MAIN
# ============================================

def main():
    print("="*70)
    print("🔬 FASE 1: BASELINE ANALYSIS 2019-2025")
    print("="*70)
    print(f"\nVersión: v9.3-RSI36")
    print(f"Strategy: {STRATEGY}")
    print(f"Symbol: {SYMBOL}")
    print(f"Exchange: {EXCHANGE}")
    print(f"\nTests a ejecutar: {len(TESTS)}")

    # Verificar que servidor Jesse esté corriendo
    print("\n⚠️ IMPORTANTE:")
    print("   1. Asegúrate de que el servidor Jesse esté corriendo:")
    print("      wsl bash -c 'cd /mnt/c/Users/ikerm/Desktop/Pruebas\\ BOTTrading/TradingBot_Project && /root/.local/bin/jesse run' &")
    print("   2. Abre http://localhost:9000 en tu navegador")
    print("   3. Presiona ENTER para continuar...")

    input()

    all_results = []

    # Ejecutar cada test
    for i, test in enumerate(TESTS, 1):
        print("\n" + "="*70)
        print(f"TEST {i}/{len(TESTS)}: {test['name']}")
        print("="*70)
        print(f"Descripción: {test['description']}")
        print(f"Periodo: {test['start']} → {test['end']}")

        # Ejecutar backtest (manual via web UI)
        result_data = run_backtest_wsl(test['start'], test['end'])

        all_results.append({
            'name': test['name'],
            'description': test['description'],
            'data': result_data,
            'timestamp': datetime.now().isoformat()
        })

        print(f"\n✅ Test {i} completado")

    # Guardar resultados
    save_results(all_results, 'phase1_baseline_results.json')

    # Imprimir resumen
    print_summary(all_results)

    print("\n" + "="*70)
    print("✅ FASE 1 COMPLETADA")
    print("="*70)
    print(f"\nPróximo paso:")
    print(f"   1. Revisa los resultados en phase1_baseline_results.json")
    print(f"   2. Identifica años críticos (probablemente 2020-2021)")
    print(f"   3. Ejecuta run_phase2_hypothesis.py para testear nuevos parámetros")

if __name__ == '__main__':
    main()
