# PROTOCOLO DE VERIFICACIÓN COMPLETA
## Sistema de Verificación para Modificaciones de Código

**Creado:** 2025-10-25
**Versión:** 1.0
**Propósito:** Asegurar que TODAS las modificaciones de código se validen completamente antes de considerarse finalizadas.

---

## REGLA FUNDAMENTAL

**NUNCA modificar código sin ejecutar el protocolo de verificación completo.**

Cada cambio debe validar:
1. Sintaxis del archivo modificado
2. Dependencias con otros archivos
3. Configuración relacionada (config.py, routes.py, etc.)
4. Importaciones cruzadas
5. Compatibilidad con versiones de librerías

---

## CHECKLIST DE VERIFICACIÓN OBLIGATORIA

### 1️⃣ ANTES DE MODIFICAR

- [ ] Leer el archivo completo a modificar
- [ ] Identificar todas las importaciones del archivo
- [ ] Buscar referencias a este archivo en el proyecto (grep/search)
- [ ] Revisar config.py para configuración relacionada
- [ ] Verificar routes.py para rutas/estrategias activas

### 2️⃣ DURANTE LA MODIFICACIÓN

- [ ] Mantener coherencia con el estilo del código existente
- [ ] Documentar cambios significativos con comentarios
- [ ] No eliminar código sin verificar si es usado externamente
- [ ] No añadir dependencias sin verificar compatibilidad

### 3️⃣ DESPUÉS DE MODIFICAR

#### A. Validación de Sintaxis
```bash
python3 -m py_compile <archivo_modificado>
```

#### B. Verificación de Importaciones
```bash
# Buscar si el archivo es importado por otros
grep -r "from.*<nombre_archivo>" .
grep -r "import.*<nombre_archivo>" .
```

#### C. Verificación de Dependencias
- Revisar todos los archivos que importan el modificado
- Verificar que las funciones/clases usadas siguen existiendo
- Comprobar que las firmas de métodos no cambiaron

#### D. Archivos Relacionados Clave
**SIEMPRE revisar estos archivos después de cambios en estrategias:**
- `config.py` - Configuración de exchanges, símbolos, timeframes
- `routes.py` - Rutas activas de trading
- `storage/jesse-store.db` - Base de datos (verificar integridad)
- `requirements.txt` - Dependencias de librerías

#### E. Validación de Jesse Framework
```bash
# Verificar que Jesse puede importar la estrategia
cd /mnt/c/Users/ikerm/Desktop/Pruebas\ BOTTrading/TradingBot_Project
python3 -c "from code.strategies.Multitimeframe import Multitimeframe; print('✓ Import OK')"
```

#### F. Test de Servidor Jesse
```bash
# Verificar que el servidor puede arrancar (si no está corriendo)
jesse run &
sleep 5
curl http://localhost:9000/system/general-info
```

---

## MATRIZ DE IMPACTO

| Archivo Modificado | Archivos a Verificar Obligatoriamente |
|-------------------|--------------------------------------|
| `code/strategies/Multitimeframe/__init__.py` | config.py, routes.py, storage/jesse-store.db |
| `config.py` | routes.py, todas las estrategias en code/strategies/ |
| `routes.py` | config.py, estrategia referenciada |
| `requirements.txt` | Todos los archivos .py (verificar imports) |

---

## COMANDOS DE VERIFICACIÓN RÁPIDA

### Verificación Completa de Proyecto
```bash
# 1. Sintaxis de todas las estrategias
find code/strategies -name "*.py" -exec python3 -m py_compile {} \;

# 2. Verificar imports de Jesse
python3 -c "from jesse.strategies import Strategy; print('✓ Jesse OK')"

# 3. Listar todas las estrategias activas
grep -E "^\s+'Multitimeframe'" routes.py

# 4. Verificar configuración
python3 -c "import config; print(f'Exchange: {config.config[\"env\"][\"exchanges\"]}'); print('✓ Config OK')"

# 5. Estado del servidor Jesse
ps aux | grep "jesse run" | grep -v grep
```

### Verificación Post-Modificación de Estrategia
```bash
# Ejecutar EN ORDEN:
cd /mnt/c/Users/ikerm/Desktop/Pruebas\ BOTTrading/TradingBot_Project

# 1. Sintaxis
python3 -m py_compile code/strategies/Multitimeframe/__init__.py

# 2. Import test
python3 -c "from code.strategies.Multitimeframe import Multitimeframe; print('✓ Import OK')"

# 3. Verificar routes.py
cat routes.py | grep -A 3 "Multitimeframe"

# 4. Limpiar caché
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete 2>/dev/null

# 5. Reiniciar servidor si es necesario
killall -9 python3 2>/dev/null
redis-cli FLUSHALL 2>/dev/null
wsl --shutdown
```

---

## ERRORES COMUNES Y PREVENCIÓN

### Error 1: `AttributeError` por método inexistente
**Causa:** Usar API que no existe en la versión de Jesse instalada
**Prevención:**
- Consultar docs de Jesse 1.11.0 antes de usar nuevos métodos
- Verificar con `dir(utils)` los métodos disponibles

### Error 2: Import circular
**Causa:** Archivo A importa B, B importa A
**Prevención:**
- Revisar todas las importaciones antes de añadir nuevas
- Usar imports locales si es necesario

### Error 3: Configuración desincronizada
**Causa:** Modificar estrategia sin actualizar config.py/routes.py
**Prevención:**
- Siempre revisar config.py después de cambios en estrategia
- Verificar que routes.py apunta a la estrategia correcta

### Error 4: Caché desactualizada
**Causa:** Python/Redis usan versión antigua del código
**Prevención:**
- Limpiar `__pycache__` después de cada cambio
- Ejecutar `redis-cli FLUSHALL` después de cambios significativos
- Hacer `wsl --shutdown` para cambios críticos

---

## WORKFLOW DE MODIFICACIÓN ESTÁNDAR

```
┌─────────────────────────────────────────────┐
│ 1. PLANIFICAR CAMBIO                        │
│    - Identificar archivos afectados         │
│    - Listar verificaciones necesarias       │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│ 2. LEER ARCHIVOS RELACIONADOS               │
│    - Archivo a modificar (completo)         │
│    - config.py                              │
│    - routes.py                              │
│    - Archivos que importan el modificado    │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│ 3. REALIZAR MODIFICACIÓN                    │
│    - Editar código                          │
│    - Mantener estilo consistente            │
│    - Documentar cambios                     │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│ 4. VERIFICACIÓN SINTAXIS                    │
│    - py_compile del archivo modificado      │
│    - Verificar imports funcionan            │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│ 5. VERIFICACIÓN DEPENDENCIAS                │
│    - Buscar referencias al archivo          │
│    - Validar archivos dependientes          │
│    - Verificar config.py/routes.py          │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│ 6. LIMPIEZA DE CACHÉ                        │
│    - Eliminar __pycache__                   │
│    - Limpiar Redis si necesario             │
│    - Reiniciar WSL si es cambio crítico     │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│ 7. VALIDACIÓN FINAL                         │
│    - Test de import completo                │
│    - Verificar servidor Jesse funciona      │
│    - Ejecutar backtest de prueba            │
└─────────────────────────────────────────────┘
```

---

## EJEMPLO PRÁCTICO

### Modificación: Cambiar RSI threshold de 42 a 40

**PASO 1: Planificación**
- Archivo afectado: `code/strategies/Multitimeframe/__init__.py`
- Archivos a verificar: `config.py`, `routes.py`
- Tipo de cambio: Parámetro de estrategia (no afecta estructura)

**PASO 2: Lectura**
```bash
# Leer archivo completo
cat code/strategies/Multitimeframe/__init__.py

# Verificar config
cat config.py | grep -A 10 "config ="

# Verificar routes
cat routes.py
```

**PASO 3: Modificación**
```python
# ANTES
@property
def rsi_oversold(self):
    return 42

# DESPUÉS
@property
def rsi_oversold(self):
    return 40  # Más permisivo para captar más entradas
```

**PASO 4: Verificación Sintaxis**
```bash
python3 -m py_compile code/strategies/Multitimeframe/__init__.py
# Salida esperada: Sin errores
```

**PASO 5: Verificación Dependencias**
```bash
# Buscar referencias a rsi_oversold
grep -r "rsi_oversold" code/

# Verificar que no hay hardcoded values
grep -r "42" code/strategies/Multitimeframe/__init__.py | grep -i rsi
```

**PASO 6: Limpieza**
```bash
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete 2>/dev/null
```

**PASO 7: Validación Final**
```bash
# Import test
python3 -c "from code.strategies.Multitimeframe import Multitimeframe; s = Multitimeframe(); print(f'RSI Oversold: {s.rsi_oversold}')"
# Salida esperada: RSI Oversold: 40
```

---

## DOCUMENTACIÓN DE CAMBIOS

Después de cada modificación verificada, actualizar:

1. **03_Code_Evolution_Log.md**
   - Versión nueva
   - Descripción del cambio
   - Archivos modificados
   - Razón del cambio

2. **STRATEGY_ROADMAP.md** (si aplica)
   - Actualizar fase actual
   - Marcar hitos completados

3. **04_Backtest_results.md** (después de backtest)
   - Registrar resultados de nueva versión
   - Comparar con versión anterior

---

## COMPROMISO

**Este protocolo se ejecutará SIEMPRE, sin excepciones, en cada modificación de código.**

El objetivo es prevenir:
- Errores de sintaxis no detectados
- Incompatibilidades entre archivos
- Configuración desincronizada
- Caché desactualizada causando comportamiento erróneo
- Pérdida de tiempo en debugging de errores prevenibles

---

**Última actualización:** 2025-10-25
**Autor:** Claude (Asistente de desarrollo)
**Estado:** Activo y obligatorio
