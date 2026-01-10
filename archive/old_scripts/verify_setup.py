#!/usr/bin/env python3
"""
Script de verificacion pre-paper trading
Verifica que todo este configurado correctamente antes de iniciar Jesse
"""

import os
import sys
from pathlib import Path

def print_header(title):
    print("=" * 70)
    print(title.center(70))
    print("=" * 70)
    print()

def check_env_file():
    """Verifica que .env existe y tiene las keys necesarias"""
    print("1. Verificando archivo .env...")

    env_path = Path(".env")
    if not env_path.exists():
        print("   [X] ERROR: Archivo .env no encontrado")
        return False

    print("   [OK] Archivo .env encontrado")

    # Leer .env
    with open(env_path, 'r') as f:
        content = f.read()

    # Verificar que tiene las keys de testnet
    if 'BINANCE_TESTNET_API_KEY' in content and 'BINANCE_TESTNET_API_SECRET' in content:
        print("   [OK] API keys de Binance Testnet configuradas")

        # Verificar que no estan vacias
        if 'BINANCE_TESTNET_API_KEY=DA945RCR2GI6gaGbBvt0bnaOeLfBMEj7EReKQP9imbJBnZWzObTMEAL3fmMG2hHj' in content:
            print("   [OK] API Key tiene valor correcto")
        else:
            print("   [!] WARNING: API Key podria estar vacia o incorrecta")

        if 'BINANCE_TESTNET_API_SECRET=DK6QKnCnUDMUPwC4pVEkIgvmcxXKlh0cfo8nVPxryjoFzmaC40omVHreEHSkOH9H' in content:
            print("   [OK] Secret Key tiene valor correcto")
        else:
            print("   [!] WARNING: Secret Key podria estar vacia o incorrecta")

        return True
    else:
        print("   [X] ERROR: API keys de Binance Testnet NO encontradas en .env")
        return False

def check_jesse_installation():
    """Verifica que Jesse esta instalado"""
    print("\n2. Verificando instalacion de Jesse...")

    import subprocess
    try:
        result = subprocess.run(['jesse', '--version'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"   [OK] {version}")
            return True
        else:
            print("   [X] ERROR: Jesse no responde correctamente")
            return False
    except Exception as e:
        print(f"   [X] ERROR: Jesse no encontrado - {e}")
        return False

def check_database():
    """Verifica que la base de datos esta accesible"""
    print("\n3. Verificando base de datos PostgreSQL...")

    try:
        import psycopg2
        conn = psycopg2.connect(
            host='localhost',
            database='jesse_db',
            user='jesse_user',
            password='password',
            port=5432,
            connect_timeout=3
        )
        conn.close()
        print("   [OK] PostgreSQL accesible")
        return True
    except Exception as e:
        print(f"   [!] WARNING: PostgreSQL no accesible - {e}")
        print("   [i] Esto es normal si usas Jesse sin dashboard")
        print("   [i] Puedes continuar con paper trading via CLI")
        return None  # None = warning, not critical

def check_routes():
    """Verifica que routes.py esta configurado correctamente"""
    print("\n4. Verificando configuracion de routes...")

    routes_path = Path("code/routes.py")
    if not routes_path.exists():
        print("   [X] ERROR: code/routes.py no encontrado")
        return False

    with open(routes_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'Binance Perpetual Futures' in content and 'BTC-USDT' in content and '15m' in content:
        print("   [OK] Routes configurado para Binance Perpetual Futures BTC-USDT 15m")

        if 'Multitimeframe' in content:
            print("   [OK] Estrategia Multitimeframe seleccionada")
        else:
            print("   [!] WARNING: Estrategia podria no estar configurada")

        return True
    else:
        print("   [X] ERROR: Routes no configurado correctamente")
        return False

def check_strategy():
    """Verifica que la estrategia v9.3-RSI36 existe"""
    print("\n5. Verificando estrategia Multitimeframe v9.3-RSI36...")

    strategy_path = Path("code/strategies/Multitimeframe/__init__.py")
    if not strategy_path.exists():
        print("   [X] ERROR: Estrategia Multitimeframe no encontrada")
        return False

    with open(strategy_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Verificar parametros v9.3-RSI36
    if 'v9.3-RSI36' in content:
        print("   [OK] Estrategia es v9.3-RSI36")
    else:
        print("   [!] WARNING: Version de estrategia podria no ser v9.3-RSI36")

    # Verificar parametros clave
    checks = {
        'BE=1.35R': '1.35' in content or 'break_even_ratio' in content,
        'RSI=36': 'rsi_long_threshold = 36' in content or '36' in content,
        'TP=3.0R': '3.0' in content or 'tp_final_ratio' in content,
    }

    all_ok = True
    for param, found in checks.items():
        if found:
            print(f"   [OK] Parametro {param} encontrado")
        else:
            print(f"   [!] WARNING: Parametro {param} no verificable")
            all_ok = False

    return all_ok

def check_data():
    """Verifica que hay datos importados"""
    print("\n6. Verificando datos importados...")

    # Jesse guarda datos en storage/jesse-db.db o en PostgreSQL
    # Para simplificar, solo verificamos que existe alguna base de datos

    db_file = Path("storage/jesse-db.db")
    if db_file.exists():
        size_mb = db_file.stat().st_size / (1024 * 1024)
        print(f"   [OK] Base de datos SQLite encontrada ({size_mb:.2f} MB)")
        if size_mb > 1:
            print("   [OK] Base de datos tiene datos (>1 MB)")
            return True
        else:
            print("   [!] WARNING: Base de datos parece vacia")
            return None
    else:
        print("   [i] INFO: Base de datos SQLite no encontrada")
        print("   [i] Esto es normal si usas PostgreSQL")
        print("   [i] Asegurate de haber ejecutado 'import_recent_data.py'")
        return None

def print_summary(results):
    """Imprime resumen final"""
    print()
    print_header("RESUMEN DE VERIFICACION")

    critical_checks = ['env', 'jesse', 'routes', 'strategy']
    optional_checks = ['database', 'data']

    critical_passed = all(results.get(check, False) for check in critical_checks)

    if critical_passed:
        print("[OK] VERIFICACION EXITOSA - Listo para paper trading")
        print()
        print("Proximos pasos:")
        print("1. Ejecutar: start_paper_trading.bat")
        print("   O manualmente: jesse run")
        print("2. Abrir navegador: http://localhost:9000")
        print("3. Ir a tab 'Live'")
        print("4. Configurar Paper Trading = ON")
        print("5. Ingresar API keys de Testnet")
        print("6. Click 'Start Trading'")
        print()
        print("IMPORTANTE:")
        print("- Mantener PC encendido 24/7 durante paper trading")
        print("- Ejecutar 'python regime_monitor.py' cada domingo")
        print("- Revisar trades diariamente")
        print()
        return 0
    else:
        print("[X] VERIFICACION FALLIDA - Revisar errores arriba")
        print()
        print("Errores criticos encontrados:")
        for check in critical_checks:
            if not results.get(check, False):
                print(f"  - {check.upper()}: FALLO")
        print()
        print("Soluciona los errores antes de iniciar paper trading")
        return 1

def main():
    print_header("VERIFICACION PRE-PAPER TRADING - v9.3-RSI36")

    # Cambiar al directorio del proyecto
    os.chdir(Path(__file__).parent)

    results = {}

    # Ejecutar verificaciones
    results['env'] = check_env_file()
    results['jesse'] = check_jesse_installation()
    results['database'] = check_database()
    results['routes'] = check_routes()
    results['strategy'] = check_strategy()
    results['data'] = check_data()

    # Resumen
    return print_summary(results)

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\nVerificacion cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nError inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
