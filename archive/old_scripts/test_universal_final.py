#!/usr/bin/env python
"""
UNIVERSAL ROBUST STRATEGY - Test 2019-2025
==========================================

Test con parametros ESTANDAR (NO optimizados)
"""

import sys
import os
import numpy as np
from datetime import datetime

# Add paths
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'code'))

# Import Jesse modules
from jesse.research import backtest, get_candles
import importlib.util

# Load routes
spec = importlib.util.spec_from_file_location("routes", os.path.join(project_root, "code", "routes.py"))
routes_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(routes_module)

def run_universal_test():
    print("\n" + "="*80)
    print("UNIVERSAL ROBUST - TEST 2020-2025")
    print("="*80)
    print("Estrategia: UniversalRobust v1.0")
    print("Parametros: RSI 30/70, EMA 50/200, 2 ATR stop, 3:1 R:R")
    print("Periodo: 2020-01-01 a 2025-12-27 (5.9 años)")
    print("Regimenes: Bull parabolico (2020-2021) + Bear (-64% en 2022) + Recovery (2023-2025)\n")

    # Configuration
    config = {
        'starting_balance': 10_000,
        'fee': 0.0004,
        'type': 'futures',
        'futures_leverage': 5,
        'futures_leverage_mode': 'cross',
        'exchange': 'Binance Perpetual Futures',
        'warm_up_candles': 500
    }

    # Routes
    routes = [
        {'exchange': 'Binance Perpetual Futures', 'strategy': 'UniversalRobust', 'symbol': 'BTC-USDT', 'timeframe': '15m'}
    ]

    # Extra routes (for multi-timeframe)
    extra_routes = []

    print("Descargando velas BTC-USDT...")
    print("(Esto puede tardar varios minutos)\n")

    # Download candles - convert dates to timestamps
    import jesse.helpers as jh
    start_ts = jh.date_to_timestamp('2020-01-01')
    end_ts = jh.date_to_timestamp('2025-12-27')

    candles = get_candles(
        'Binance Perpetual Futures',
        'BTC-USDT',
        '15m',
        start_ts,
        end_ts
    )

    print(f"Velas descargadas: {len(candles)} candles")
    print("Ejecutando backtest...\n")

    # Prepare candles dict
    candles_dict = {
        'Binance Perpetual Futures-BTC-USDT': {
            'exchange': 'Binance Perpetual Futures',
            'symbol': 'BTC-USDT',
            'candles': candles,
        },
    }

    start_time = datetime.now()

    # Run backtest
    result = backtest(
        config=config,
        routes=routes,
        data_routes=extra_routes,
        candles=candles_dict
    )

    elapsed = (datetime.now() - start_time).total_seconds()

    print(f"\nBacktest completado en {elapsed:.1f} segundos\n")
    print("="*80)
    print("RESULTADOS")
    print("="*80 + "\n")

    # Extract metrics
    metrics = result['metrics']

    net_profit = metrics['net_profit_percentage']
    annual_return = metrics.get('annual_return', 0)
    total_trades = metrics['total']
    win_rate = metrics['win_rate']
    max_dd = metrics['max_drawdown']
    sharpe = metrics.get('sharpe_ratio', 0)
    calmar = metrics.get('calmar_ratio', 0)

    print(f"Total Trades:    {total_trades}")
    print(f"Net Profit:      {net_profit:.2f}%")
    print(f"Annual Return:   {annual_return:.2f}%")
    print(f"Win Rate:        {win_rate:.2f}%")
    print(f"Max Drawdown:    {max_dd:.2f}%")
    print(f"Sharpe Ratio:    {sharpe:.2f}")
    print(f"Calmar Ratio:    {calmar:.2f}")
    print()

    # Success criteria
    print("="*80)
    print("CRITERIOS DE EXITO")
    print("="*80 + "\n")

    passed = 0
    total = 4

    criteria = [
        ('Net Profit > 0%', net_profit > 0),
        ('Max DD < -50%', max_dd > -50),
        ('Win Rate > 18%', win_rate > 18),
        ('Sharpe > 0.3', sharpe > 0.3)
    ]

    for name, check in criteria:
        status = "PASS" if check else "FAIL"
        print(f"  {status} - {name}")
        if check:
            passed += 1

    print(f"\nRESULTADO: {passed}/{total} criterios cumplidos\n")

    if passed == 4:
        print("UniversalRobust es ROBUSTO - Funciona en TODOS los regimenes")
    elif passed >= 2:
        print("UniversalRobust tiene potencial - Necesita ajustes")
    else:
        print("UniversalRobust FALLA - Requiere rediseño")

    print("\n" + "="*80)
    print("vs v9.3-RSI36 (overfitted a 2023-2025)")
    print("="*80)
    print(f"\nv9.3 en 2020-2025: -66.9% profit, -84.47% DD")
    print(f"UniversalRobust:   {net_profit:.2f}% profit, {max_dd:.2f}% DD")

    if net_profit > -66.9:
        print(f"\nUniversalRobust es MEJOR (+{net_profit+66.9:.2f}% diferencia)")
    else:
        print(f"\nUniversalRobust es PEOR")

    print("\n" + "="*80 + "\n")

    return result

if __name__ == '__main__':
    try:
        run_universal_test()
    except KeyboardInterrupt:
        print("\n\nCancelado\n")
    except Exception as e:
        print(f"\n\nERROR: {e}\n")
        import traceback
        traceback.print_exc()
