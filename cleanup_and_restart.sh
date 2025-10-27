#!/bin/bash
# Script de limpieza TOTAL para Jesse Trading Bot
# Este script mata TODOS los procesos, limpia caché y levanta servidor limpio

echo "========================================="
echo "LIMPIEZA TOTAL JESSE TRADING BOT"
echo "========================================="

# 1. MATAR TODOS LOS PROCESOS JESSE/PYTHON
echo "1. Matando TODOS los procesos Python/Jesse..."
pkill -9 -f "jesse run" 2>/dev/null
pkill -9 -f "jesse" 2>/dev/null
pkill -9 python3 2>/dev/null
pkill -9 python 2>/dev/null
pkill -9 uvicorn 2>/dev/null
sleep 2
echo "   ✓ Procesos matados"

# 2. LIMPIAR CACHE PYTHON
echo "2. Limpiando caché Python..."
cd /mnt/c/Users/ikerm/Desktop/Pruebas\ BOTTrading/TradingBot_Project
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -name "*.pyc" -delete 2>/dev/null
find . -name "*.pyo" -delete 2>/dev/null
echo "   ✓ Caché Python limpiado"

# 3. LIMPIAR REDIS
echo "3. Limpiando Redis..."
redis-cli FLUSHALL 2>/dev/null && echo "   ✓ Redis limpiado" || echo "   ⚠ Redis no disponible"

# 4. LIMPIAR STORAGE JESSE
echo "4. Limpiando storage Jesse..."
rm -rf storage/temp/* 2>/dev/null
rm -rf .jesse/* 2>/dev/null
echo "   ✓ Storage limpiado"

# 5. VERIFICAR QUE NO HAY PROCESOS
echo "5. Verificando procesos..."
PROCESSES=$(ps aux | grep -E "jesse|python" | grep -v grep | wc -l)
if [ "$PROCESSES" -gt 0 ]; then
    echo "   ⚠ Aún hay $PROCESSES procesos corriendo"
    ps aux | grep -E "jesse|python" | grep -v grep
else
    echo "   ✓ No hay procesos corriendo"
fi

echo ""
echo "========================================="
echo "LIMPIEZA COMPLETADA"
echo "========================================="
echo ""
echo "Ahora puedes levantar Jesse con:"
echo "  /root/.local/bin/jesse run"
echo ""
