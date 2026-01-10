@echo off
echo Reestructurando proyecto...

REM Crear directorio archive
if not exist "archive\previous_versions" mkdir "archive\previous_versions"

REM Mover archivos antiguos
move V10_*.md archive\previous_versions\ 2>nul
move V11*.md archive\previous_versions\ 2>nul
move BACKTEST_*.md archive\previous_versions\ 2>nul
move CRITICAL_*.md archive\previous_versions\ 2>nul
move DAY1*.md archive\previous_versions\ 2>nul
move DEPLOYMENT*.md archive\previous_versions\ 2>nul
move FUTURES*.md archive\previous_versions\ 2>nul
move HYBRID*.md archive\previous_versions\ 2>nul
move OPTIMIZATION*.md archive\previous_versions\ 2>nul
move PAPER_*.md archive\previous_versions\ 2>nul
move PHASE1*.md archive\previous_versions\ 2>nul
move PROJECT_STATUS.md archive\previous_versions\ 2>nul
move ROBUSTNESS*.md archive\previous_versions\ 2>nul
move SEMANA*.md archive\previous_versions\ 2>nul
move SENSITIVITY*.md archive\previous_versions\ 2>nul
move SPOT*.md archive\previous_versions\ 2>nul
move START_HERE.md archive\previous_versions\ 2>nul
move TREND*.md archive\previous_versions\ 2>nul
move UNIVERSAL_ROBUST_RESULTS.md archive\previous_versions\ 2>nul

REM Mover estrategias antiguas
if not exist "archive\old_strategies" mkdir "archive\old_strategies"
move code\strategies\MultitimeframeTrailing archive\old_strategies\ 2>nul
move code\strategies\TrendFollowing archive\old_strategies\ 2>nul
move code\strategies\HybridUniversal archive\old_strategies\ 2>nul
move code\strategies\UniversalRobust archive\old_strategies\ 2>nul

REM Mover scripts de test antiguos
if not exist "archive\old_scripts" mkdir "archive\old_scripts"
move debug_*.py archive\old_scripts\ 2>nul
move modify_params.py archive\old_scripts\ 2>nul
move quick_sensitivity.py archive\old_scripts\ 2>nul
move regime_monitor.py archive\old_scripts\ 2>nul
move run_backtest_*.sh archive\old_scripts\ 2>nul
move run_phase1_*.py archive\old_scripts\ 2>nul
move run_trend_*.py archive\old_scripts\ 2>nul
move sensitivity_*.py archive\old_scripts\ 2>nul
move simple_backtest.py archive\old_scripts\ 2>nul
move test_*.py archive\old_scripts\ 2>nul
move verify_*.py archive\old_scripts\ 2>nul
move walk_forward_*.py archive\old_scripts\ 2>nul

echo.
echo Proyecto reestructurado!
echo - Versiones anteriores: archive\previous_versions\
echo - Estrategias antiguas: archive\old_strategies\
echo - Scripts antiguos: archive\old_scripts\
echo.
pause
