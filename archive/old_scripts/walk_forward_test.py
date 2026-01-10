#!/usr/bin/env python3
"""
WALK-FORWARD VALIDATION TEST
=============================

Tests UniversalRobust strategy using proper methodology:

1. Training Period: 2018-01-01 to 2022-12-31 (5 years)
2. Validation Period: 2023-01-01 to 2024-12-31 (2 years out-of-sample)
3. Assets: BTC-USDT + ETH-USDT (multi-asset validation)

SUCCESS CRITERIA:
- Validation profit > 0
- Validation Sharpe > 0.5
- Validation Max DD < 40%
- Works on BOTH assets

If fails validation → DISCARD, it's overfitted
"""

import subprocess
import json
from datetime import datetime

TRAIN_START = "2018-01-01"
TRAIN_END = "2022-12-31"
VALIDATION_START = "2023-01-01"
VALIDATION_END = "2024-12-31"

ASSETS = [
    "BTC-USDT",
    # "ETH-USDT",  # Add when ready
]


def run_backtest(symbol, start_date, end_date):
    """Run Jesse backtest via command line"""
    print(f"\n{'='*70}")
    print(f"Testing {symbol} from {start_date} to {end_date}")
    print(f"{'='*70}\n")

    cmd = [
        "wsl", "bash", "-c",
        f'cd /mnt/c/Users/ikerm/Desktop/Pruebas\\ BOTTrading/TradingBot_Project && '
        f'/root/.local/bin/jesse backtest {start_date} {end_date}'
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)

    return result.returncode == 0


def main():
    print("\n" + "="*70)
    print("  WALK-FORWARD VALIDATION - UniversalRobust v1.0")
    print("  Testing with INDUSTRY STANDARD parameters")
    print("  NO curve-fitting, NO optimization to specific periods")
    print("="*70 + "\n")

    results = {}

    for symbol in ASSETS:
        print(f"\n\n==== ASSET: {symbol} ====\n")

        # Training period
        print("\n[1/2] TRAINING PERIOD (2018-2022)")
        print("-" * 70)
        train_success = run_backtest(symbol, TRAIN_START, TRAIN_END)

        if not train_success:
            print(f"❌ Training failed for {symbol}")
            continue

        input("\nPress ENTER to continue to validation period...")

        # Validation period (out-of-sample)
        print("\n[2/2] VALIDATION PERIOD (2023-2024) - OUT OF SAMPLE")
        print("-" * 70)
        val_success = run_backtest(symbol, VALIDATION_START, VALIDATION_END)

        if val_success:
            print(f"✅ Validation completed for {symbol}")
        else:
            print(f"❌ Validation failed for {symbol}")

        input("\nPress ENTER for next asset or Ctrl+C to stop...")

    print("\n\n" + "="*70)
    print("WALK-FORWARD VALIDATION COMPLETE")
    print("="*70)
    print("\nNow review the results:")
    print("- If validation profit > 0 on BOTH assets → ROBUST")
    print("- If validation fails on any asset → OVERFITTED, discard")
    print("="*70)


if __name__ == "__main__":
    main()
