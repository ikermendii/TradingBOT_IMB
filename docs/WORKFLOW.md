# WORKFLOW OBLIGATORIO - Modificación de Código y Backtesting

**Creado**: 2025-10-26
**Objetivo**: Evitar interferencias de procesos zombie y caché corrupto

---

## 🔴 PROBLEMA IDENTIFICADO

Durante el desarrollo de v5.0-v5.5, tuvimos **13 procesos Jesse zombie** corriendo simultáneamente, causando:
- ❌ Backtest ejecutando código viejo (caché corrupto)
- ❌ IndexError repetidos incluso después de correcciones
- ❌ Imposibilidad de matar procesos desde herramientas normales
- ❌ Necesidad de reinicio completo de computadora

---

## ✅ SOLUCIÓN: WORKFLOW AUTOMÁTICO OBLIGATORIO

**Claude DEBE seguir este workflow SIEMPRE antes de cualquier cambio de código:**

### PASO 1: LIMPIEZA PRE-MODIFICACIÓN (SIEMPRE)

Antes de modificar CUALQUIER archivo de código, ejecutar:

```bash
# 1. Shutdown completo WSL (mata todos los procesos)
wsl --shutdown

# 2. Esperar 10 segundos
sleep 10

# 3. Limpiar caché Python
wsl bash -c 'cd /mnt/c/Users/ikerm/Desktop/Pruebas\ BOTTrading/TradingBot_Project && find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null; find . -name "*.pyc" -delete 2>/dev/null; find . -name "*.pyo" -delete 2>/dev/null'

# 4. Limpiar Redis
wsl bash -c 'redis-cli FLUSHALL 2>/dev/null'

# 5. Limpiar storage Jesse
wsl bash -c 'cd /mnt/c/Users/ikerm/Desktop/Pruebas\ BOTTrading/TradingBot_Project && rm -rf storage/temp/* .jesse/* 2>/dev/null'

# 6. Shutdown final
wsl --shutdown

# 7. Esperar 5 segundos
sleep 5
```

**TOTAL: ~20 segundos de limpieza obligatoria**

---

### PASO 2: MODIFICACIÓN DE CÓDIGO

Solo DESPUÉS de la limpieza del PASO 1:

1. ✅ Modificar archivos `.py` necesarios
2. ✅ Verificar sintaxis: `python3 -m py_compile archivo.py`
3. ✅ Actualizar versión en header del archivo
4. ✅ Documentar cambios

---

### PASO 3: LIMPIEZA POST-MODIFICACIÓN (SIEMPRE)

Después de modificar código, ANTES de levantar servidor:

```bash
# Repetir limpieza completa (PASO 1)
wsl --shutdown
sleep 10
# ... (todos los comandos del PASO 1)
```

---

### PASO 4: LEVANTAR SERVIDOR LIMPIO (UN SOLO PROCESO)

```bash
# Levantar UN ÚNICO servidor Jesse
wsl bash -c 'cd /mnt/c/Users/ikerm/Desktop/Pruebas\ BOTTrading/TradingBot_Project && /root/.local/bin/jesse run' &

# Esperar 10 segundos para que arranque
sleep 10

# Verificar que solo hay 1 proceso corriendo
wsl bash -c 'ps aux | grep jesse | grep -v grep | wc -l'
# Debe retornar: 1
```

**IMPORTANTE**: Si retorna más de 1, ejecutar `wsl --shutdown` y repetir desde PASO 1.

---

### PASO 5: VERIFICACIÓN PRE-BACKTEST

Antes de que el usuario ejecute backtest:

```bash
# Verificar versión cargada
wsl bash -c 'cd /mnt/c/Users/ikerm/Desktop/Pruebas\ BOTTrading/TradingBot_Project && head -25 code/strategies/Multitimeframe/__init__.py | grep "Version:"'

# Verificar que servidor está respondiendo
curl -s http://localhost:9000 > /dev/null && echo "✓ Servidor OK" || echo "❌ Servidor no responde"

# Verificar procesos
wsl bash -c 'ps aux | grep jesse | grep -v grep'
# Debe mostrar SOLO 1 proceso
```

---

## 📋 CHECKLIST OBLIGATORIO

Claude DEBE confirmar ANTES de cada modificación:

- [ ] ¿Ejecuté limpieza PRE-modificación (PASO 1)?
- [ ] ¿Modifiqué el código?
- [ ] ¿Verifiqué sintaxis?
- [ ] ¿Ejecuté limpieza POST-modificación (PASO 3)?
- [ ] ¿Levanté UN SOLO servidor limpio (PASO 4)?
- [ ] ¿Verifiqué versión correcta cargada (PASO 5)?
- [ ] ¿Confirmé que solo hay 1 proceso Jesse corriendo?

**SOLO después de completar TODOS los pasos**, informar al usuario que puede ejecutar backtest.

---

## 🚨 QUÉ HACER SI HAY PROCESOS ZOMBIE

Si después del `wsl --shutdown` siguen habiendo múltiples procesos:

1. **Informar al usuario inmediatamente**
2. **Solicitar reinicio de computadora**
3. **NO continuar con modificaciones** hasta que sistema esté limpio
4. **Después del reinicio**, seguir workflow desde PASO 1

---

## ⏱️ TIEMPO TOTAL POR MODIFICACIÓN

- Limpieza PRE: ~20 segundos
- Modificación: Variable
- Limpieza POST: ~20 segundos
- Levantar servidor: ~10 segundos
- Verificación: ~5 segundos

**TOTAL: ~55 segundos + tiempo de modificación**

**Vale la pena**: Evita horas de debugging de problemas de caché.

---

## 📝 REGISTRO DE USO

Claude debe registrar cada vez que sigue este workflow:

```
[FECHA] [HORA] - Workflow ejecutado para versión vX.X
- Limpieza PRE: ✅
- Modificación: [descripción]
- Limpieza POST: ✅
- Servidor levantado: ✅
- Verificación: ✅
- Procesos corriendo: 1
- Estado: LISTO PARA BACKTEST
```

---

## 🎯 OBJETIVO FINAL

**CERO procesos zombie + CERO caché corrupto = Backtests confiables**

**Si no puedo matar procesos → Informar al usuario → Solicitar reinicio**

NO intentar "workarounds" - El reinicio es la solución correcta.

---

**Este workflow es OBLIGATORIO. No hay excepciones.**
