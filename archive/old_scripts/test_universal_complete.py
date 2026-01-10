#!/usr/bin/env python
"""
UNIVERSAL ROBUST STRATEGY - Test Completo 2019-2025
====================================================

Objetivo: Validar que PARAMETROS ESTANDAR funcionan en TODOS los regimenes
- 2019: Recovery post-crash
- 2020-2021: Bull parabolico (+590%)
- 2022: Bear market (-64%)
- 2023-2025: Recovery volatil

Parametros (INDUSTRIA ESTANDAR - NO OPTIMIZADOS):
- RSI: 30/70
- EMA: 50/200
- Stop: 2 ATR
- Target: 3:1 R:R
"""

import sys
import os

# Add project root and code dir to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'code'))

import jesse.helpers as jh
from jesse.research import backtest
from datetime import datetime

# Import routes
import importlib.util
spec = importlib.util.spec_from_file_location("routes", os.path.join(project_root, "code", "routes.py"))
routes_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(routes_module)

configured_routes = routes_module.routes

def run_backtest():
    """Ejecuta backtest de UniversalRobust en periodo COMPLETO 2019-2025"""

    print("\n" + "="*80)
    print("UNIVERSAL ROBUST STRATEGY - TEST MULTI-REGIMEN 2019-2025")
    print("="*80)
    print(f"Periodo: 2019-01-01 → 2025-12-31 (6.9 años)")
    print(f"Exchange: Binance Perpetual Futures")
    print(f"Symbol: BTC-USDT")
    print(f"Timeframe: 15m")
    print(f"Strategy: UniversalRobust v1.0")
    print()
    print("PARAMETROS (ESTANDAR - NO OPTIMIZADOS):")
    print("  - RSI: 30/70 (classic)")
    print("  - EMA: 50/200 (golden cross)")
    print("  - Stop: 2 ATR")
    print("  - Target: 3:1 Risk-Reward")
    print()
    print("REGIMENES INCLUIDOS:")
    print("  2019: Recovery")
    print("  2020-2021: Bull parabolico")
    print("  2022: Bear market")
    print("  2023-2025: Recovery volatil")
    print("="*80 + "\n")

    # Ejecutar backtest
    print("Descargando velas y ejecutando backtest...")
    print("(Esto puede tomar 5-10 minutos)\n")

    start_time = datetime.now()

    result = backtest(
        start_date='2019-01-01',
        finish_date='2025-12-31',
        starting_balance=10000,
        fee=0.0004,  # 0.04% taker fee
        futures_leverage=5,  # Conservative leverage
        futures_leverage_mode='cross',
        exchange='Binance Perpetual Futures',
        warm_up_candles=500
    )

    end_time = datetime.now()
    elapsed = (end_time - start_time).total_seconds()

    print(f"\nBacktest completado en {elapsed:.1f} segundos\n")
    print("="*80)
    print("RESULTADOS UNIVERSAL ROBUST (2019-2025)")
    print("="*80 + "\n")

    # Extraer metricas
    metrics = result['metrics']

    total_trades = metrics['total']
    net_profit_pct = metrics['net_profit_percentage']
    win_rate = metrics['win_rate']
    max_dd = metrics['max_drawdown']
    sharpe = metrics.get('sharpe_ratio', 0)
    calmar = metrics.get('calmar_ratio', 0)
    sortino = metrics.get('sortino_ratio', 0)

    winning_trades = metrics['total_winning_trades']
    losing_trades = metrics['total_losing_trades']
    avg_win = metrics.get('average_win', 0)
    avg_loss = metrics.get('average_loss', 0)
    annual_return = metrics.get('annual_return', 0)

    print(f"METRICAS PRINCIPALES:")
    print(f"  Total Trades: {total_trades}")
    print(f"  Net Profit: {net_profit_pct:.2f}%")
    print(f"  Annual Return: {annual_return:.2f}%")
    print(f"  Win Rate: {win_rate:.2f}%")
    print(f"  Max Drawdown: {max_dd:.2f}%")
    print()

    print(f"RATIOS:")
    print(f"  Sharpe Ratio: {sharpe:.2f}")
    print(f"  Calmar Ratio: {calmar:.2f}")
    print(f"  Sortino Ratio: {sortino:.2f}")
    print()

    print(f"TRADES:")
    print(f"  Winning Trades: {winning_trades} ({win_rate:.2f}%)")
    print(f"  Losing Trades: {losing_trades} ({100-win_rate:.2f}%)")
    print(f"  Avg Win: ${avg_win:.2f}")
    print(f"  Avg Loss: ${avg_loss:.2f}")
    if avg_loss != 0:
        rr = abs(avg_win / avg_loss)
        print(f"  R:R Ratio: {rr:.2f}")
    print()

    # Criterios de exito para bot UNIVERSAL
    print("="*80)
    print("CRITERIOS DE EXITO - BOT UNIVERSAL")
    print("="*80 + "\n")

    criteria = {
        'Net Profit > 0%': net_profit_pct > 0,
        'Max DD < -50%': max_dd > -50,
        'Win Rate > 18%': win_rate > 18,
        'Sharpe > 0.3': sharpe > 0.3
    }

    passed = 0
    for criterion, result_check in criteria.items():
        status = "PASS" if result_check else "FAIL"
        print(f"  {status} - {criterion}")
        if result_check:
            passed += 1

    print(f"\n{'='*80}")
    print(f"RESULTADO FINAL: {passed}/4 criterios cumplidos")
    print(f"{'='*80}\n")

    if passed == 4:
        print("UNIVERSAL ROBUST es ROBUSTO")
        print("  Funciona en TODOS los regimenes (bull parabolico, bear, volatil)")
        print("  Proceder a deployment conservador con circuit breakers\n")
    elif passed >= 2:
        print("UNIVERSAL ROBUST muestra potencial pero requiere ajuste")
        print("  Revisar parametros o agregar filtros adicionales\n")
    else:
        print("UNIVERSAL ROBUST NO es robusto")
        print("  Requiere rediseño completo de logica\n")

    # Comparacion vs v9.3-RSI36
    print("="*80)
    print("COMPARACION vs v9.3-RSI36 (OVERFITTED)")
    print("="*80 + "\n")
    print("v9.3-RSI36 en 2020-2025:")
    print("  Net Profit: -66.9%")
    print("  Max DD: -84.47%")
    print("  Win Rate: 19.84%")
    print("  Calmar: -0.21")
    print()
    print(f"UniversalRobust v1.0 en 2019-2025:")
    print(f"  Net Profit: {net_profit_pct:.2f}%")
    print(f"  Max DD: {max_dd:.2f}%")
    print(f"  Win Rate: {win_rate:.2f}%")
    print(f"  Calmar: {calmar:.2f}")
    print()

    if net_profit_pct > -66.9:
        delta = net_profit_pct - (-66.9)
        print(f"  UniversalRobust es {delta:.2f}% MEJOR que v9.3 en largo plazo")
    else:
        print(f"  UniversalRobust es PEOR que v9.3 (necesita trabajo)")

    print("\n" + "="*80 + "\n")

    return result

if __name__ == '__main__':
    try:
        result = run_backtest()
    except KeyboardInterrupt:
        print("\n\nBacktest cancelado por usuario\n")
    except Exception as e:
        print(f"\n\nERROR: {e}\n")
        import traceback
        traceback.print_exc()
