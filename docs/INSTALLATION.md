# Guía de Instalación - Trading Bot

## Requisitos del Sistema
- OS: Windows 10/11, macOS 10.14+, o Linux
- RAM: Mínimo 4GB
- Espacio: 5GB libres
- Internet: Estable para descargar datos

## Paso 1: Instalar Python 3.11

### Windows:
1. Ir a https://www.python.org/downloads/
2. Descargar Python 3.11.x
3. IMPORTANTE: Marcar "Add Python to PATH"
4. Instalar
5. Verificar en CMD:
```
   python --version
```

### macOS:
```bash
brew install python@3.11
python3.11 --version
```

### Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip
python3.11 --version
```

## Paso 2: Instalar Jesse
```bash
# Instalar Jesse
pip install jesse

# Verificar instalación
jesse --version
```

## Paso 3: Crear Proyecto
```bash
# Crear proyecto
jesse make-project trading_bot

# Entrar al directorio
cd trading_bot

# Estructura creada:
# trading_bot/
# ├── strategies/
# ├── storage/
# ├── config.py
# └── routes.py
```

## Paso 4: Primera Prueba
```bash
# Importar datos de prueba (puede tardar)
jesse import-candles 'Binance' 'BTC-USDT' '2023-01-01'

# Ejecutar backtest de prueba
jesse backtest '2023-01-01' '2023-12-31'
```

## Troubleshooting Común

### Error: "jesse: command not found"
**Solución**:
```bash
# Añadir Python Scripts al PATH
# Windows: Buscar "Variables de entorno" en el menú inicio
# Añadir: C:\Users\TU_USUARIO\AppData\Local\Programs\Python\Python311\Scripts
```

### Error: "TA-Lib installation failed"
**Solución Windows**:
1. Descargar wheel pre-compilado:
   https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib
2. Instalar:
```
   pip install TA_Lib-0.4.XX-cpXX-cpXX-win_amd64.whl
```

### Error: "No module named 'jesse'"
**Solución**:
```bash
python -m pip install --upgrade jesse
```

## Estado de la Instalación
- [x] Python 3.11.9 instalado
- [x] Jesse instalado
- [x] Proyecto configurado (TradingBot_Project)
- [x] Archivos config.py y routes.py creados
- [x] Estructura de directorios lista (code/strategies, storage)
- [ ] Primera prueba exitosa (pendiente: importar datos)

## Estructura del Proyecto Actual
```
TradingBot_Project/
├── code/
│   ├── strategies/       # Estrategias de trading
│   └── utils/           # Utilidades
├── storage/             # Datos de Jesse (candles, logs)
├── backtests/           # Resultados de backtests
├── notes/               # Notas del proyecto
├── config.py            # Configuración de Jesse
└── routes.py            # Rutas de trading
```

## Comandos Útiles
```bash
# Usar Python 3.11 específicamente
py -3.11 --version

# Ejecutar Jesse con Python 3.11
py -3.11 -m jesse <comando>

# O usar el ejecutable directo
"C:\Users\ikerm\AppData\Local\Programs\Python\Python311\Scripts\jesse.exe" <comando>
```