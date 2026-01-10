#!/usr/bin/env python3
"""
Sensitivity Analysis Script - v9.1-TP1
======================================

Ejecuta backtests con variaciones de parámetros críticos para identificar
la configuración óptima en el periodo walk-forward (2024-07-01 a 2025-10-17).

Parámetros a variar:
1. Break-even R ratio: [1.2, 1.25, 1.3, 1.35]
2. RSI thresholds: [36, 37, 38, 39, 40]
3. TP final R ratio: [2.5, 3.0, 3.5, 4.0]

Total combinaciones: 4 × 5 × 4 = 80 backtests
"""

import subprocess
import json
import os
from datetime import datetime
from pathlib import Path

# Configuración base
BASE_STRATEGY_PATH = "code/strategies/Multitimeframe/__init__.py"
BACKUP_PATH = "code/strategies/Multitimeframe/__init__.py.backup"
RESULTS_DIR = "sensitivity_results"

# Rango de parámetros a testear
BREAKEVEN_VALUES = [1.2, 1.25, 1.3, 1.35]
RSI_VALUES = [36, 37, 38, 39, 40]
TP_FINAL_VALUES = [2.5, 3.0, 3.5, 4.0]

# Periodo walk-forward
START_DATE = "2024-07-01"
END_DATE = "2025-10-17"


def backup_strategy():
    """Crear backup de la estrategia original"""
    with open(BASE_STRATEGY_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    with open(BACKUP_PATH, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Backup creado: {BACKUP_PATH}")


def restore_strategy():
    """Restaurar estrategia original desde backup"""
    with open(BACKUP_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    with open(BASE_STRATEGY_PATH, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Estrategia restaurada desde backup")


def modify_strategy(breakeven_r, rsi_threshold, tp_final_r):
    """
    Modifica la estrategia con los parámetros especificados

    Args:
        breakeven_r: R ratio para break-even (ej: 1.25)
        rsi_threshold: RSI threshold base (ej: 38)
        tp_final_r: R ratio para TP final (ej: 3.0)
    """
    with open(BASE_STRATEGY_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # Modificar RSI thresholds (LONG y SHORT simétricos)
    # Pattern: def rsi_long_threshold(self):\n        # v9.0-MICRO: RSI 38
    content = content.replace(
        f"def rsi_long_threshold(self):\n        # v9.0-MICRO: RSI 38 (permite entradas ligeramente más tempranas)\n        return 38",
        f"def rsi_long_threshold(self):\n        # SENSITIVITY: RSI {rsi_threshold}\n        return {rsi_threshold}"
    )

    # RSI short threshold (simétrico: 100 - rsi_long)
    rsi_short = 100 - rsi_threshold
    content = content.replace(
        f"def rsi_short_threshold(self):\n        # v9.0-MICRO: RSI 62 (simetría con LONG, permite entradas más tempranas)\n        return 62",
        f"def rsi_short_threshold(self):\n        # SENSITIVITY: RSI {rsi_short}\n        return {rsi_short}"
    )

    # Modificar break-even R ratio
    # Pattern: if r_ratio >= 1.25 and not self.vars['tp1_hit']:
    content = content.replace(
        f"if r_ratio >= 1.25 and not self.vars['tp1_hit']:",
        f"if r_ratio >= {breakeven_r} and not self.vars['tp1_hit']:"
    )

    # Modificar TP final R ratio
    # Pattern: if r_ratio >= 3.0:
    content = content.replace(
        f"if r_ratio >= 3.0:",
        f"if r_ratio >= {tp_final_r}:"
    )

    with open(BASE_STRATEGY_PATH, 'w', encoding='utf-8') as f:
        f.write(content)


def run_backtest(breakeven_r, rsi_threshold, tp_final_r):
    """
    Ejecuta un backtest con los parámetros especificados

    Returns:
        dict: Resultados del backtest
    """
    print(f"\n{'='*80}")
    print(f"🔄 Testing: BE={breakeven_r}R | RSI={rsi_threshold} | TP={tp_final_r}R")
    print(f"{'='*80}")

    # Modificar estrategia
    modify_strategy(breakeven_r, rsi_threshold, tp_final_r)

    # Construir comando Jesse
    cmd = [
        "wsl", "bash", "-c",
        f"export PATH=\"$HOME/.local/bin:$PATH\" && "
        f"cd /mnt/c/Users/ikerm/Desktop/Pruebas\\ BOTTrading/TradingBot_Project && "
        f"jesse backtest {START_DATE} {END_DATE} --json"
    ]

    try:
        # Ejecutar backtest
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5 minutos timeout
        )

        if result.returncode == 0:
            # Parse JSON output
            output_lines = result.stdout.strip().split('\n')
            json_line = None
            for line in reversed(output_lines):
                if line.strip().startswith('{'):
                    json_line = line
                    break

            if json_line:
                data = json.loads(json_line)

                # Extraer métricas clave
                metrics = {
                    'breakeven_r': breakeven_r,
                    'rsi_threshold': rsi_threshold,
                    'tp_final_r': tp_final_r,
                    'total_trades': data.get('total', 0),
                    'win_rate': data.get('win_rate', 0),
                    'net_profit_pct': data.get('net_profit_percentage', 0),
                    'max_dd_pct': data.get('max_drawdown', 0),
                    'sharpe': data.get('sharpe_ratio', 0),
                    'expectancy': data.get('expectancy', 0),
                    'avg_win_loss_ratio': data.get('ratio_avg_win_loss', 0),
                }

                print(f"✅ Trades: {metrics['total_trades']} | WR: {metrics['win_rate']:.2f}% | Profit: {metrics['net_profit_pct']:.2f}%")

                return metrics
            else:
                print(f"❌ Error: No se encontró JSON en output")
                return None
        else:
            print(f"❌ Error ejecutando backtest: {result.stderr}")
            return None

    except subprocess.TimeoutExpired:
        print(f"❌ Timeout: El backtest tardó más de 5 minutos")
        return None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None


def main():
    """Ejecuta el análisis de sensibilidad completo"""

    print(f"""
{'='*80}
🔬 SENSITIVITY ANALYSIS - v9.1-TP1
{'='*80}

Periodo: {START_DATE} a {END_DATE}
Parámetros a variar:
  - Break-even: {BREAKEVEN_VALUES}
  - RSI threshold: {RSI_VALUES}
  - TP final: {TP_FINAL_VALUES}

Total combinaciones: {len(BREAKEVEN_VALUES)} × {len(RSI_VALUES)} × {len(TP_FINAL_VALUES)} = {len(BREAKEVEN_VALUES) * len(RSI_VALUES) * len(TP_FINAL_VALUES)}

ADVERTENCIA: Esto tomará varias horas. ¿Continuar? (y/n)
""")

    response = input("> ").strip().lower()
    if response != 'y':
        print("❌ Cancelado por el usuario")
        return

    # Crear directorio de resultados
    Path(RESULTS_DIR).mkdir(exist_ok=True)

    # Backup de estrategia original
    backup_strategy()

    # Almacenar todos los resultados
    all_results = []

    try:
        # Iterar sobre todas las combinaciones
        total = len(BREAKEVEN_VALUES) * len(RSI_VALUES) * len(TP_FINAL_VALUES)
        current = 0

        for be in BREAKEVEN_VALUES:
            for rsi in RSI_VALUES:
                for tp in TP_FINAL_VALUES:
                    current += 1
                    print(f"\n[{current}/{total}] Progreso: {current/total*100:.1f}%")

                    # Ejecutar backtest
                    result = run_backtest(be, rsi, tp)

                    if result:
                        all_results.append(result)

                    # Pequeña pausa entre backtests
                    import time
                    time.sleep(2)

        # Guardar resultados
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = f"{RESULTS_DIR}/sensitivity_{timestamp}.json"

        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(all_results, f, indent=2)

        print(f"\n✅ Resultados guardados en: {results_file}")

        # Análisis de mejores configuraciones
        print(f"\n{'='*80}")
        print("📊 TOP 10 MEJORES CONFIGURACIONES POR NET PROFIT")
        print(f"{'='*80}\n")

        sorted_by_profit = sorted(all_results, key=lambda x: x['net_profit_pct'], reverse=True)

        for i, r in enumerate(sorted_by_profit[:10], 1):
            print(f"{i}. BE={r['breakeven_r']}R | RSI={r['rsi_threshold']} | TP={r['tp_final_r']}R")
            print(f"   Trades: {r['total_trades']} | WR: {r['win_rate']:.2f}% | Profit: {r['net_profit_pct']:.2f}% | DD: {r['max_dd_pct']:.2f}%")
            print(f"   R:R: {r['avg_win_loss_ratio']:.2f} | Expectancy: ${r['expectancy']:.2f}")
            print()

    finally:
        # Restaurar estrategia original
        restore_strategy()
        print("\n✅ Estrategia restaurada a configuración original")


if __name__ == "__main__":
    main()
