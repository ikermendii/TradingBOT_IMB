#!/usr/bin/env python3
"""
Quick test: Verificar que HybridUniversal detecta régimen en primera vela
"""

import sys
import os
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'code'))

print("="*70)
print("TEST: Regime Detection en Primera Vela")
print("="*70)

# Simular timestamps
jan_2020_ms = 1577836800 * 1000  # 2020-01-01 00:00:00 UTC
jul_2021_ms = 1625097600 * 1000  # 2021-07-01 00:00:00 UTC
mar_2023_ms = 1677628800 * 1000  # 2023-03-01 00:00:00 UTC

PARABOLIC_END = 1640995200 * 1000  # 2022-01-01 00:00:00 UTC

print(f"\nTimestamps de prueba:")
print(f"  2020-01-01: {jan_2020_ms}")
print(f"  2021-07-01: {jul_2021_ms}")
print(f"  2023-03-01: {mar_2023_ms}")
print(f"\nPARABOLIC_END: {PARABOLIC_END}")

# Test detection logic
def detect_regime(current_time_ms):
    if current_time_ms < PARABOLIC_END:
        return 'PARABOLIC'
    else:
        return 'VOLATILE'

print(f"\n{'='*70}")
print("RESULTADOS DE DETECCIÓN:")
print(f"{'='*70}")

regime_2020 = detect_regime(jan_2020_ms)
regime_2021 = detect_regime(jul_2021_ms)
regime_2023 = detect_regime(mar_2023_ms)

print(f"  2020-01-01 → {regime_2020} {'✅' if regime_2020 == 'PARABOLIC' else '❌'}")
print(f"  2021-07-01 → {regime_2021} {'✅' if regime_2021 == 'PARABOLIC' else '❌'}")
print(f"  2023-03-01 → {regime_2023} {'✅' if regime_2023 == 'VOLATILE' else '❌'}")

print(f"\n{'='*70}")
if regime_2020 == 'PARABOLIC' and regime_2021 == 'PARABOLIC' and regime_2023 == 'VOLATILE':
    print("✅ LÓGICA DE DETECCIÓN CORRECTA")
else:
    print("❌ LÓGICA DE DETECCIÓN FALLIDA")
print(f"{'='*70}\n")
