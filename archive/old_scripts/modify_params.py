#!/usr/bin/env python3
"""
Script para modificar parámetros de la estrategia v9.1-TP1

Uso:
    python3 modify_params.py --breakeven 1.3 --rsi 37 --tp 3.5
    python3 modify_params.py --breakeven 1.2  # Solo modifica break-even
    python3 modify_params.py --reset  # Restaura a v9.1-TP1 original
"""

import argparse
import re
import shutil
from pathlib import Path

STRATEGY_FILE = "code/strategies/Multitimeframe/__init__.py"
BACKUP_FILE = "code/strategies/Multitimeframe/__init__.py.v9.1_original"

# Valores originales v9.1-TP1
ORIGINAL_BREAKEVEN = 1.25
ORIGINAL_RSI_LONG = 38
ORIGINAL_RSI_SHORT = 62
ORIGINAL_TP = 3.0


def create_backup():
    """Crear backup si no existe"""
    if not Path(BACKUP_FILE).exists():
        shutil.copy(STRATEGY_FILE, BACKUP_FILE)
        print(f"✅ Backup creado: {BACKUP_FILE}")
    else:
        print(f"ℹ️  Backup ya existe: {BACKUP_FILE}")


def restore_original():
    """Restaurar desde backup"""
    if Path(BACKUP_FILE).exists():
        shutil.copy(BACKUP_FILE, STRATEGY_FILE)
        print(f"✅ Estrategia restaurada a v9.1-TP1 original")
        print(f"   Break-even: {ORIGINAL_BREAKEVEN}R")
        print(f"   RSI: {ORIGINAL_RSI_LONG} / {ORIGINAL_RSI_SHORT}")
        print(f"   TP: {ORIGINAL_TP}R")
    else:
        print(f"❌ No se encontró backup en {BACKUP_FILE}")


def modify_strategy(breakeven=None, rsi_long=None, tp=None):
    """
    Modifica parámetros en la estrategia

    Args:
        breakeven: R ratio para break-even
        rsi_long: RSI threshold para LONG
        tp: TP final R ratio
    """
    with open(STRATEGY_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    changes = []

    if rsi_long is not None:
        # RSI long threshold
        old_rsi = re.search(r'(def rsi_long_threshold\(self\):.*?return\s+)(\d+)', content, re.DOTALL)
        if old_rsi:
            old_value = old_rsi.group(2)
            content = re.sub(
                r'(def rsi_long_threshold\(self\):.*?return\s+)\d+',
                rf'\g<1>{rsi_long}',
                content,
                flags=re.DOTALL
            )
            changes.append(f"RSI LONG: {old_value} → {rsi_long}")

        # RSI short threshold (simétrico)
        rsi_short = 100 - rsi_long
        old_rsi_short = re.search(r'(def rsi_short_threshold\(self\):.*?return\s+)(\d+)', content, re.DOTALL)
        if old_rsi_short:
            old_value = old_rsi_short.group(2)
            content = re.sub(
                r'(def rsi_short_threshold\(self\):.*?return\s+)\d+',
                rf'\g<1>{rsi_short}',
                content,
                flags=re.DOTALL
            )
            changes.append(f"RSI SHORT: {old_value} → {rsi_short}")

    if breakeven is not None:
        # Break-even R ratio
        old_be = re.search(r'if r_ratio >= ([\d.]+)(?= and not self\.vars\[\'tp1_hit\'\])', content)
        if old_be:
            old_value = old_be.group(1)
            content = re.sub(
                r'if r_ratio >= [\d.]+(?= and not self\.vars\[\'tp1_hit\'\])',
                f'if r_ratio >= {breakeven}',
                content
            )
            changes.append(f"Break-even: {old_value}R → {breakeven}R")

    if tp is not None:
        # TP final
        # Buscar el comentario "REGLA 2: TP completo" para asegurar que modificamos el correcto
        pattern = r'(# REGLA 2: TP completo.*?\n\s+if r_ratio >= )([\d.]+)'
        old_tp = re.search(pattern, content, re.DOTALL)
        if old_tp:
            old_value = old_tp.group(2)
            content = re.sub(pattern, rf'\g<1>{tp}', content, flags=re.DOTALL)
            changes.append(f"TP final: {old_value}R → {tp}R")

    # Guardar cambios
    with open(STRATEGY_FILE, 'w', encoding='utf-8') as f:
        f.write(content)

    print("✅ Estrategia modificada:")
    for change in changes:
        print(f"   {change}")


def main():
    parser = argparse.ArgumentParser(description='Modificar parámetros de v9.1-TP1')
    parser.add_argument('--breakeven', '-b', type=float, help='Break-even R ratio (ej: 1.3)')
    parser.add_argument('--rsi', '-r', type=int, help='RSI threshold LONG (ej: 37)')
    parser.add_argument('--tp', '-t', type=float, help='TP final R ratio (ej: 3.5)')
    parser.add_argument('--reset', action='store_true', help='Restaurar a original v9.1-TP1')

    args = parser.parse_args()

    # Crear backup si es la primera vez
    create_backup()

    if args.reset:
        restore_original()
        return

    if not any([args.breakeven, args.rsi, args.tp]):
        print("❌ Debes especificar al menos un parámetro a modificar")
        print("   Uso: python3 modify_params.py --breakeven 1.3 --rsi 37 --tp 3.5")
        print("   O:   python3 modify_params.py --reset")
        return

    modify_strategy(
        breakeven=args.breakeven,
        rsi_long=args.rsi,
        tp=args.tp
    )

    print("\n📝 Recuerda:")
    print("   1. Limpia caché antes del backtest:")
    print("      wsl bash -c 'cd /mnt/c/Users/ikerm/Desktop/Pruebas\\ BOTTrading/TradingBot_Project && ./clean_cache.sh'")
    print("   2. Ejecuta backtest desde http://localhost:9000")
    print("   3. Periodo walk-forward: 2024-07-01 a 2025-10-17")


if __name__ == "__main__":
    main()
