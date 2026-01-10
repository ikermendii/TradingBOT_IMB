#!/usr/bin/env python3
"""
WALK-FORWARD VALIDATION - UniversalRobust v1.0
==============================================

Training: 2018-01-01 to 2022-12-31 (5 years)
Validation: 2023-01-01 to 2024-12-31 (2 years out-of-sample)

Industry standard parameters only - NO optimization
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
print("  WALK-FORWARD VALIDATION - UniversalRobust v1.0")
print("  Industry Standard Parameters (NO optimization)")
print("="*70 + "\n")

try:
    from jesse import research
    from routes import routes

    # ===== TRAINING PERIOD =====
    print("\n[1/2] TRAINING PERIOD: 2018-01-01 to 2022-12-31")
    print("-" * 70)
    print("Downloading candles and running backtest...")
    print("This may take several minutes...\n")

    train_result = research.backtest(
        start_date='2018-01-01',
        finish_date='2022-12-31',
        candles={},
        routes=routes
    )

    print("\n" + "="*70)
    print("TRAINING RESULTS (2018-2022)")
    print("="*70)
    print(train_result)

    input("\n\nPress ENTER to continue to validation period...")

    # ===== VALIDATION PERIOD (OUT-OF-SAMPLE) =====
    print("\n\n[2/2] VALIDATION PERIOD: 2023-01-01 to 2024-12-31")
    print("-" * 70)
    print("OUT-OF-SAMPLE TEST - Strategy has NOT seen this data")
    print("Downloading candles and running backtest...")
    print("This may take several minutes...\n")

    val_result = research.backtest(
        start_date='2023-01-01',
        finish_date='2024-12-31',
        candles={},
        routes=routes
    )

    print("\n" + "="*70)
    print("VALIDATION RESULTS (2023-2024) - OUT-OF-SAMPLE")
    print("="*70)
    print(val_result)

    print("\n\n" + "="*70)
    print("WALK-FORWARD VALIDATION COMPLETE")
    print("="*70)
    print("\nSUCCESS CRITERIA:")
    print("- Validation Net Profit > 0%")
    print("- Validation Sharpe Ratio > 0.5")
    print("- Validation Max Drawdown < 40%")
    print("\nIf validation FAILS any criteria -> Strategy is OVERFITTED")
    print("="*70 + "\n")

except ImportError as e:
    print(f"\nError: {e}")
    print("\nJesse research module not available.")
    print("Please install: pip install jesse")

except Exception as e:
    print(f"\nError during backtest: {e}")
    import traceback
    traceback.print_exc()
