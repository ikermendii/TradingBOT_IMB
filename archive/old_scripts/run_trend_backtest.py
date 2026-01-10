#!/usr/bin/env python
"""
Backtest de TrendFollowing Strategy - Periodo 2020-2022
Objetivo: Validar performance en mercado bull parabólico
"""

import sys
import os

# Add project root and code dir to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'code'))

import jesse.helpers as jh
from jesse.research import backtest, get_candles
from pprint import pprint
from datetime import datetime

# Import routes - read directly from file
import importlib.util
spec = importlib.util.spec_from_file_location("routes", os.path.join(project_root, "code", "routes.py"))
routes_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(routes_module)

configured_routes = routes_module.routes
extra_candles = routes_module.extra_candles

def run_backtest():
    """Ejecuta backtest de TrendFollowing en periodo 2020-2022"""

    print("\n" + "="*80)
    print("BACKTEST: TrendFollowing Strategy (v11.0-UNIVERSAL)")
    print("="*80)
    print(f"Periodo: 2020-01-01 → 2022-12-31 (3 años)")
    print(f"Exchange: Binance Perpetual Futures")
    print(f"Symbol: BTC-USDT")
    print(f"Timeframe: 15m")
    print(f"Strategy: TrendFollowing")
    print("="*80 + "\n")

    # Ejecutar backtest
    print("⏳ Descargando velas y ejecutando backtest...")
    print("   (Esto puede tomar varios minutos)\n")

    start_time = datetime.now()

    result = backtest(
        start_date='2020-01-01',
        finish_date='2022-12-31',
        starting_balance=10000,
        fee=0.0004,
        futures_leverage=3,
        futures_leverage_mode='cross',
        exchange='Binance Perpetual Futures',
        warm_up_candles=500
    )

    end_time = datetime.now()
    elapsed = (end_time - start_time).total_seconds()

    print(f"\n✅ Backtest completado en {elapsed:.1f} segundos\n")
    print("="*80)
    print("RESULTADOS")
    print("="*80 + "\n")

    # Extraer métricas principales
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

    print(f"📊 MÉTRICAS PRINCIPALES:")
    print(f"   Total Trades: {total_trades}")
    print(f"   Net Profit: {net_profit_pct:.2f}%")
    print(f"   Annual Return: {annual_return:.2f}%")
    print(f"   Win Rate: {win_rate:.2f}%")
    print(f"   Max Drawdown: {max_dd:.2f}%")
    print()

    print(f"📈 RATIOS:")
    print(f"   Sharpe Ratio: {sharpe:.2f}")
    print(f"   Calmar Ratio: {calmar:.2f}")
    print(f"   Sortino Ratio: {sortino:.2f}")
    print()

    print(f"💰 TRADES:")
    print(f"   Winning Trades: {winning_trades} ({win_rate:.2f}%)")
    print(f"   Losing Trades: {losing_trades} ({100-win_rate:.2f}%)")
    print(f"   Avg Win: ${avg_win:.2f}")
    print(f"   Avg Loss: ${avg_loss:.2f}")
    if avg_loss != 0:
        rr = abs(avg_win / avg_loss)
        print(f"   R:R Ratio: {rr:.2f}")
    print()

    # Criterios de éxito
    print("="*80)
    print("VALIDACIÓN CONTRA CRITERIOS DE ÉXITO")
    print("="*80 + "\n")

    criteria = {
        'Net Profit > +30%': net_profit_pct > 30,
        'Win Rate > 18%': win_rate > 18,
        'Max DD < -40%': max_dd > -40,
        'Calmar > 0.8': calmar > 0.8
    }

    passed = 0
    for criterion, result in criteria.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {criterion}")
        if result:
            passed += 1

    print(f"\n{'='*80}")
    print(f"RESULTADO FINAL: {passed}/4 criterios cumplidos")
    print(f"{'='*80}\n")

    if passed >= 3:
        print("🏆 TrendFollowing Strategy APROBADA para bull parabolic markets")
        print("   Proceder a Week 2: Integración con Regime Detector\n")
    elif passed >= 2:
        print("⚠️  TrendFollowing Strategy muestra potencial pero requiere optimización")
        print("   Revisar parámetros: minimum_score, tp_final_ratio, trailing_stop\n")
    else:
        print("❌ TrendFollowing Strategy NO cumple criterios mínimos")
        print("   Requiere rediseño de lógica de entrada/salida\n")

    return result

if __name__ == '__main__':
    try:
        result = run_backtest()
    except KeyboardInterrupt:
        print("\n\n⚠️  Backtest cancelado por usuario\n")
    except Exception as e:
        print(f"\n\n❌ ERROR: {e}\n")
        import traceback
        traceback.print_exc()
