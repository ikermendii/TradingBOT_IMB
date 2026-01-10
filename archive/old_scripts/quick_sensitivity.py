#!/usr/bin/env python3
"""
Quick Sensitivity Analysis - Enfoque por Fases
==============================================

Estrategia eficiente: En vez de probar todas las combinaciones (80 tests),
probamos parámetros en FASES, optimizando uno a la vez.

FASE 1: Break-even R ratio (mantener RSI=38, TP=3.0)
  → [1.2, 1.25, 1.3, 1.35] = 4 tests

FASE 2: RSI threshold (usar mejor break-even, mantener TP=3.0)
  → [36, 37, 38, 39, 40] = 5 tests

FASE 3: TP final (usar mejor break-even + RSI)
  → [2.5, 3.0, 3.5, 4.0] = 4 tests

Total: 13 backtests (vs 80 del enfoque full grid)
Tiempo estimado: ~45 minutos (vs 4-5 horas)
"""

import subprocess
import json
import os
import re
from datetime import datetime
from pathlib import Path

# Configuración
BASE_STRATEGY = "code/strategies/Multitimeframe/__init__.py"
BACKUP = "code/strategies/Multitimeframe/__init__.py.sensitivity_backup"
RESULTS_FILE = "sensitivity_quick_results.json"

# Periodo walk-forward
START = "2024-07-01"
END = "2025-10-17"

# Valores base (v9.1-TP1 actual)
BASE_BREAKEVEN = 1.25
BASE_RSI = 38
BASE_TP = 3.0


def backup():
    """Backup de estrategia"""
    with open(BASE_STRATEGY, 'r', encoding='utf-8') as f:
        content = f.read()
    with open(BACKUP, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Backup: {BACKUP}")


def restore():
    """Restaurar desde backup"""
    if os.path.exists(BACKUP):
        with open(BACKUP, 'r', encoding='utf-8') as f:
            content = f.read()
        with open(BASE_STRATEGY, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Restaurado desde backup")
    else:
        print(f"⚠️  No se encontró backup")


def modify(breakeven=None, rsi=None, tp=None):
    """
    Modifica parámetros en la estrategia

    Args:
        breakeven: R ratio para break-even (None = no cambiar)
        rsi: RSI threshold (None = no cambiar)
        tp: TP final R ratio (None = no cambiar)
    """
    with open(BASE_STRATEGY, 'r', encoding='utf-8') as f:
        content = f.read()

    if rsi is not None:
        # RSI long threshold
        content = re.sub(
            r'(def rsi_long_threshold\(self\):.*?return\s+)\d+',
            rf'\g<1>{rsi}',
            content,
            flags=re.DOTALL
        )

        # RSI short threshold (simétrico)
        rsi_short = 100 - rsi
        content = re.sub(
            r'(def rsi_short_threshold\(self\):.*?return\s+)\d+',
            rf'\g<1>{rsi_short}',
            content,
            flags=re.DOTALL
        )

    if breakeven is not None:
        # Break-even R ratio
        content = re.sub(
            r'if r_ratio >= [\d.]+(?= and not self\.vars\[\'tp1_hit\'\])',
            f'if r_ratio >= {breakeven}',
            content
        )

    if tp is not None:
        # TP final (buscar el segundo if r_ratio >=, que es el TP final)
        # Pattern: REGLA 2: TP completo en 3R
        content = re.sub(
            r'(# REGLA 2: TP completo.*?\n\s+if r_ratio >= )[\d.]+',
            rf'\g<1>{tp}',
            content,
            flags=re.DOTALL
        )

    with open(BASE_STRATEGY, 'w', encoding='utf-8') as f:
        f.write(content)


def run_test(be, rsi, tp, phase_desc):
    """Ejecuta un backtest"""
    print(f"\n{'='*70}")
    print(f"🔄 {phase_desc}")
    print(f"   BE={be}R | RSI={rsi} | TP={tp}R")
    print(f"{'='*70}")

    # Modificar estrategia
    modify(breakeven=be, rsi=rsi, tp=tp)

    # Comando Jesse (ejecutar directamente en WSL sin wrapper)
    cmd = [
        "jesse", "backtest", START, END, "--json"
    ]

    # Configurar environment
    env = os.environ.copy()
    env['PATH'] = f"{os.path.expanduser('~/.local/bin')}:{env.get('PATH', '')}"

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300, env=env)

        if result.returncode != 0:
            print(f"❌ Error: {result.stderr[:200]}")
            return None

        # Parse JSON
        for line in reversed(result.stdout.strip().split('\n')):
            if line.strip().startswith('{'):
                try:
                    data = json.loads(line)

                    metrics = {
                        'phase': phase_desc,
                        'breakeven': be,
                        'rsi': rsi,
                        'tp': tp,
                        'trades': data.get('total', 0),
                        'win_rate': data.get('win_rate', 0),
                        'profit_pct': data.get('net_profit_percentage', 0),
                        'dd_pct': data.get('max_drawdown', 0),
                        'sharpe': data.get('sharpe_ratio', 0),
                        'rr_ratio': data.get('ratio_avg_win_loss', 0),
                        'expectancy': data.get('expectancy', 0),
                    }

                    print(f"✅ {metrics['trades']} trades | WR {metrics['win_rate']:.1f}% | "
                          f"Profit {metrics['profit_pct']:.2f}% | DD {metrics['dd_pct']:.1f}%")

                    return metrics

                except json.JSONDecodeError:
                    print(f"❌ JSON parse error")
                    return None

        print(f"❌ No JSON found in output")
        return None

    except subprocess.TimeoutExpired:
        print(f"❌ Timeout (>5min)")
        return None
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None


def main():
    print(f"""
{'='*70}
🔬 QUICK SENSITIVITY ANALYSIS
{'='*70}

Periodo: {START} a {END}
Baseline: BE={BASE_BREAKEVEN}R, RSI={BASE_RSI}, TP={BASE_TP}R

Plan:
  Fase 1: Variar Break-even [1.2, 1.25, 1.3, 1.35] → 4 tests
  Fase 2: Variar RSI [36, 37, 38, 39, 40] → 5 tests
  Fase 3: Variar TP [2.5, 3.0, 3.5, 4.0] → 4 tests

Total: 13 backtests (~45 minutos)
{'='*70}
""")

    # Backup
    backup()

    all_results = []

    try:
        # ==================================================================
        # FASE 1: Break-even optimization
        # ==================================================================
        separator = '#' * 70
        print(f"\n{separator}")
        print("# FASE 1: OPTIMIZACIÓN DE BREAK-EVEN")
        print(f"{separator}\n")

        phase1_results = []
        for be_value in [1.2, 1.25, 1.3, 1.35]:
            result = run_test(
                be=be_value,
                rsi=BASE_RSI,
                tp=BASE_TP,
                phase_desc=f"FASE 1 - Break-even {be_value}R"
            )
            if result:
                phase1_results.append(result)
                all_results.append(result)

        # Encontrar mejor break-even
        best_be = max(phase1_results, key=lambda x: x['profit_pct'])
        print(f"\n🏆 MEJOR BREAK-EVEN: {best_be['breakeven']}R "
              f"(Profit: {best_be['profit_pct']:.2f}%)")

        # ==================================================================
        # FASE 2: RSI optimization
        # ==================================================================
        print(f"\n{separator}")
        print("# FASE 2: OPTIMIZACIÓN DE RSI")
        print(f"{separator}\n")

        phase2_results = []
        for rsi_value in [36, 37, 38, 39, 40]:
            result = run_test(
                be=best_be['breakeven'],
                rsi=rsi_value,
                tp=BASE_TP,
                phase_desc=f"FASE 2 - RSI {rsi_value}"
            )
            if result:
                phase2_results.append(result)
                all_results.append(result)

        # Encontrar mejor RSI
        best_rsi = max(phase2_results, key=lambda x: x['profit_pct'])
        print(f"\n🏆 MEJOR RSI: {best_rsi['rsi']} "
              f"(Profit: {best_rsi['profit_pct']:.2f}%)")

        # ==================================================================
        # FASE 3: TP optimization
        # ==================================================================
        print(f"\n{separator}")
        print("# FASE 3: OPTIMIZACIÓN DE TP FINAL")
        print(f"{separator}\n")

        phase3_results = []
        for tp_value in [2.5, 3.0, 3.5, 4.0]:
            result = run_test(
                be=best_be['breakeven'],
                rsi=best_rsi['rsi'],
                tp=tp_value,
                phase_desc=f"FASE 3 - TP {tp_value}R"
            )
            if result:
                phase3_results.append(result)
                all_results.append(result)

        # Encontrar mejor TP
        best_tp = max(phase3_results, key=lambda x: x['profit_pct'])
        print(f"\n🏆 MEJOR TP: {best_tp['tp']}R "
              f"(Profit: {best_tp['profit_pct']:.2f}%)")

        # ==================================================================
        # RESUMEN FINAL
        # ==================================================================
        print(f"\n{'='*70}")
        print("📊 CONFIGURACIÓN ÓPTIMA ENCONTRADA")
        print(f"{'='*70}\n")

        print(f"Break-even: {best_be['breakeven']}R (baseline: {BASE_BREAKEVEN}R)")
        print(f"RSI threshold: {best_rsi['rsi']} (baseline: {BASE_RSI})")
        print(f"TP final: {best_tp['tp']}R (baseline: {BASE_TP}R)")
        print()
        print(f"Mejor resultado combinado:")
        print(f"  Trades: {best_tp['trades']}")
        print(f"  Win Rate: {best_tp['win_rate']:.2f}%")
        print(f"  Net Profit: {best_tp['profit_pct']:.2f}%")
        print(f"  Max DD: {best_tp['dd_pct']:.2f}%")
        print(f"  R:R Ratio: {best_tp['rr_ratio']:.2f}")
        print(f"  Expectancy: ${best_tp['expectancy']:.2f}")
        print()

        # Comparación con baseline
        print(f"{'='*70}")
        print("📈 MEJORA vs BASELINE (v9.1-TP1)")
        print(f"{'='*70}\n")

        baseline = next((r for r in phase1_results if r['breakeven'] == BASE_BREAKEVEN), None)
        if baseline and best_tp:
            profit_delta = best_tp['profit_pct'] - baseline['profit_pct']
            wr_delta = best_tp['win_rate'] - baseline['win_rate']
            dd_delta = best_tp['dd_pct'] - baseline['dd_pct']

            print(f"Net Profit: {baseline['profit_pct']:.2f}% → {best_tp['profit_pct']:.2f}% "
                  f"({profit_delta:+.2f}%)")
            print(f"Win Rate: {baseline['win_rate']:.2f}% → {best_tp['win_rate']:.2f}% "
                  f"({wr_delta:+.2f}%)")
            print(f"Max DD: {baseline['dd_pct']:.2f}% → {best_tp['dd_pct']:.2f}% "
                  f"({dd_delta:+.2f}%)")

        # Guardar resultados
        with open(RESULTS_FILE, 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'period': f"{START} to {END}",
                'baseline': {'breakeven': BASE_BREAKEVEN, 'rsi': BASE_RSI, 'tp': BASE_TP},
                'optimal': {
                    'breakeven': best_be['breakeven'],
                    'rsi': best_rsi['rsi'],
                    'tp': best_tp['tp']
                },
                'all_results': all_results
            }, f, indent=2)

        print(f"\n✅ Resultados guardados: {RESULTS_FILE}")

    finally:
        # Restaurar
        restore()


if __name__ == "__main__":
    main()
