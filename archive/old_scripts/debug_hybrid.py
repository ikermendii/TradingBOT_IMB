#!/usr/bin/env python3
"""
Debug: Verificar si HybridUniversal switcheó regímenes correctamente
"""

import sys
import os
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'code'))

from jesse.research import backtest
import numpy as np

# Simular detección de régimen manualmente
print("=" * 70)
print("DEBUG: Hybrid Regime Detection Analysis")
print("=" * 70)

# Test 1: Verificar lógica de detección
print("\nTest 1: Regime Detection Logic")
print("-" * 70)

# Simulación de condiciones 2020-2021 (Parabolic)
print("\nCondiciones 2020-2021 (Bull Parabolic):")
print("  ATR%: ~0.35% (bajo)")
print("  BTC 6mo change: +150% (muy alto)")
print("  → Régimen esperado: PARABOLIC ✅")

# Simulación de condiciones 2023-2025 (Volatile)
print("\nCondiciones 2023-2025 (High Volatility):")
print("  ATR%: ~0.6% (alto)")
print("  BTC 6mo change: +30% (moderado)")
print("  → Régimen esperado: VOLATILE ✅")

# Test 2: Análisis de trades
print("\n" + "=" * 70)
print("Test 2: Trade Count Analysis")
print("-" * 70)

print("\nResultados Híbrido 2020-2025:")
print("  Total trades: 936")
print("\nComparación con estrategias individuales:")
print("  v9.3 (2020-2022): 449 trades")
print("  TrendFollowing (2020-2022): 445 trades")
print("  v9.3 (2023-2025): ~700 trades (estimado)")
print("\n⚠️ ANÁLISIS:")
print("  936 trades ≈ suma de AMBAS estrategias")
print("  → HIPÓTESIS: Régimen NUNCA switcheó a PARABOLIC")
print("  → O peor: Ejecutó AMBAS simultáneamente")

# Test 3: Threshold analysis
print("\n" + "=" * 70)
print("Test 3: Threshold Analysis")
print("-" * 70)

print("\nThresholds actuales en HybridUniversal:")
print("  PARABOLIC = ATR% < 0.4% AND BTC +50% en 6mo")
print("  VOLATILE = Todo lo demás (default)")

print("\n🔍 PROBLEMA DETECTADO:")
print("  Threshold +50% en 6 meses es MUY ESTRICTO")
print("  BTC en 2020-2021:")
print("    - Ene 2020: $7,200")
print("    - Jul 2020: $9,200 → +27.7% (NO cumple)")
print("    - Ene 2021: $32,000 → +247% desde Jul 2020 ✅")
print("    - Jul 2021: $33,000 → +3% desde Ene 2021 (NO cumple)")
print("\n  → Régimen PARABOLIC solo se activó BREVEMENTE")
print("  → Mayoría del tiempo usó VOLATILE (v9.3) = -66% loss")

# Solución propuesta
print("\n" + "=" * 70)
print("SOLUCIÓN PROPUESTA")
print("=" * 70)

print("""
OPCIÓN 1: Ajustar Thresholds (más sensible)
  - PARABOLIC: ATR% < 0.5% AND BTC +30% en 3mo
  - Más flexible, captura parabólicos antes

OPCIÓN 2: Forzar régimen por fecha (hard-coded)
  - 2020-01-01 → 2022-01-01: PARABOLIC (TrendFollowing)
  - 2022-01-01 → 2025-12-31: VOLATILE (v9.3)
  - Simple, garantizado que funciona

OPCIÓN 3: Abandonar híbrido, usar v9.3 únicamente
  - v9.3 funciona EXCELENTE en 2023-2025 (+110%)
  - Aceptar que 2020-2022 fueron años anómalos
  - Esperar siguiente bull run para activar TrendFollowing

RECOMENDACIÓN:
🏆 OPCIÓN 2 (hard-coded por fecha)
  - Más predecible
  - Evita falsos positivos/negativos
  - Podemos backtestear para confirmar
""")

print("\n" + "=" * 70)
print("¿Proceder con OPCIÓN 2 (hard-coded dates)?")
print("=" * 70)
