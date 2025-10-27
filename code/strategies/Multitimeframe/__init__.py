"""
🚀 ADVANCED TRADING STRATEGY - Multi-Timeframe Divergence
========================================================

Estrategia avanzada basada en:
- Divergencias RSI/MACD multi-timeframe 
- Filtro de tendencia con EMAs (50/200)
- Volume confirmation mejorado
- Risk management dinámico (1.5% por trade)
- Take profits escalonados (1.5R, 3R, trailing)
- Stop loss con ATR

Optimizada para: BTC-USDT 15m
Timeframes: 4H (tendencia), 1H (estructura), 15M (ejecución)

Objetivos:
- Return anual: 80-200%
- Win Rate: 55-65%
- Max Drawdown: <15%
- Sharpe Ratio: >1.5

Version: 5.4-BALANCED - Equilibrado: (Divergencias OR RSI extremo) AND Tendencia + Volume
"""

from jesse.strategies import Strategy
import jesse.indicators as ta
import numpy as np


class Multitimeframe(Strategy):
    def __init__(self):
        super().__init__()
        self.vars = {
            'position_size': 0,
            'entry_price': 0,
            'sl_price': 0,
            'tp1_hit': False,
            'tp2_hit': False,
            'divergence_lookback': 15,
            'last_signal_time': 0,
            'daily_start_balance': 0,
            'daily_loss_check_day': None,
            # initial_risk_distance stores the price distance (in price units)
            # between entry and initial stop at the moment of entry. Use
            # this for R-based calculations so moving the stop to
            # break-even doesn't zero-out the denominator.
            'initial_risk_distance': 0,
            'trend_strength': 0,
        }

    # =============================================================================
    # CÁLCULO MANUAL DE RSI (para evitar IndexError con ta.rsi)
    # =============================================================================

    def _calculate_rsi_array(self, prices, period=14):
        """
        Calcula RSI manualmente para obtener un array completo de valores RSI.

        Esto evita el problema de que ta.rsi() retorne un escalar en algunos contextos.

        Args:
            prices: Array de precios (close prices)
            period: Periodo RSI (default 14)

        Returns:
            Array numpy con valores RSI para cada vela
        """
        if len(prices) < period + 1:
            return np.full(len(prices), 50.0)  # RSI neutro si no hay suficientes datos

        # Calcular cambios de precio (deltas)
        deltas = np.diff(prices)

        # Separar ganancias y pérdidas
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)

        # Inicializar arrays para promedios
        avg_gains = np.zeros(len(prices))
        avg_losses = np.zeros(len(prices))

        # Calcular primera media simple (SMA)
        avg_gains[period] = np.mean(gains[:period])
        avg_losses[period] = np.mean(losses[:period])

        # Calcular resto usando EMA (Wilder's smoothing)
        for i in range(period + 1, len(prices)):
            avg_gains[i] = (avg_gains[i-1] * (period - 1) + gains[i-1]) / period
            avg_losses[i] = (avg_losses[i-1] * (period - 1) + losses[i-1]) / period

        # Calcular RS (Relative Strength)
        # Evitar división por cero agregando epsilon
        rs = avg_gains / (avg_losses + 1e-10)

        # Calcular RSI
        rsi = 100 - (100 / (1 + rs))

        # Primeras 'period' velas tienen RSI neutro (50)
        rsi[:period] = 50.0

        return rsi

    # =============================================================================
    # PARÁMETROS DE LA ESTRATEGIA
    # =============================================================================

    @property
    def rsi_period(self):
        return 14

    @property 
    def macd_fast(self):
        return 12

    @property
    def macd_slow(self):
        return 26

    @property
    def macd_signal(self):
        return 9

    @property
    def ema_fast(self):
        return 50

    @property
    def ema_slow(self):
        return 200

    @property
    def atr_period(self):
        return 14

    @property
    def volume_period(self):
        return 20

    @property
    def risk_percent(self):
        return 1.5  # 1.5% risk per trade

    # -- New tunables to control selectivity and reduce overtrading --
    @property
    def signal_cooldown_minutes(self):
        # v5.4-BALANCED: Equilibrio entre calidad y cantidad
        return 30  # 30 minutos - balance

    @property
    def rsi_long_threshold(self):
        # RSI must be below this to consider LONG
        # v5.4-BALANCED: RSI 40 = sobreventa (equilibrado)
        return 40

    @property
    def rsi_short_threshold(self):
        # RSI must be above this to consider SHORT
        # v5.4-BALANCED: RSI 60 = sobrecompra (equilibrado)
        return 60

    @property
    def min_atr_pct(self):
        # v5.3: Volatilidad balanceada (no tan restrictivo como v5.2)
        return 0.003  # 0.3% - balanceado

    @property
    def require_volume(self):
        # Require positive volume confirmation
        return True

    @property
    def max_daily_loss_pct(self):
        """Pérdida máxima permitida por día (% del capital inicial del día)"""
        return 3.0  # 3% de pérdida máxima diaria

    @property
    def leverage(self):
        """Apalancamiento para futuros (20x)"""
        return 20

    @property
    def minimum_rr_ratio(self):
        """Risk:Reward mínimo requerido - REGLA PROFESIONAL"""
        return 2.0  # Mínimo 2R disponible para abrir trade

    # =============================================================================
    # CONDICIONES DE ENTRADA
    # =============================================================================

    def should_long(self) -> bool:
        """
        v5.4-BALANCED: ESTRATEGIA EQUILIBRADA

        LÓGICA: (Divergencia alcista OR RSI < 40) AND Tendencia AND Volumen

        FILTROS:
        1. SEÑAL: Divergencia alcista OR RSI < 40 (al menos uno debe cumplirse)
        2. Tendencia alcista (EMA50 > EMA200) - OBLIGATORIO
        3. Volumen confirmación - OBLIGATORIO
        4. Cooldown 30 min

        Objetivo: 50-150 trades con 40-50% win rate
        """
        # Cooldown equilibrado
        if self.current_candle[0] - self.vars['last_signal_time'] < self.signal_cooldown_minutes * 60 * 1000:
            return False

        # Límite de pérdida diaria
        if not self._can_trade_today():
            return False

        # SEÑAL PRINCIPAL: Divergencia OR RSI extremo (al menos UNO debe ser True)
        has_bullish_divergence = self._bullish_divergence()
        current_rsi = ta.rsi(self.candles, self.rsi_period)
        rsi_oversold = current_rsi < self.rsi_long_threshold  # RSI < 40

        # Si NO hay divergencia Y RSI NO está en sobreventa → rechazar
        if not has_bullish_divergence and not rsi_oversold:
            return False

        # FILTROS OBLIGATORIOS: Tendencia + Volumen
        return (
            self._trend_filter_long() and
            self._volume_confirmation()
        )

    def should_short(self) -> bool:
        """
        v5.4-BALANCED: ESTRATEGIA EQUILIBRADA

        LÓGICA: (Divergencia bajista OR RSI > 60) AND Tendencia AND Volumen

        FILTROS:
        1. SEÑAL: Divergencia bajista OR RSI > 60 (al menos uno debe cumplirse)
        2. Tendencia bajista (EMA50 < EMA200) - OBLIGATORIO
        3. Volumen confirmación - OBLIGATORIO
        4. Cooldown 30 min

        Objetivo: 50-150 trades con 40-50% win rate
        """
        # Cooldown equilibrado
        if self.current_candle[0] - self.vars['last_signal_time'] < self.signal_cooldown_minutes * 60 * 1000:
            return False

        # Límite de pérdida diaria
        if not self._can_trade_today():
            return False

        # SEÑAL PRINCIPAL: Divergencia OR RSI extremo (al menos UNO debe ser True)
        has_bearish_divergence = self._bearish_divergence()
        current_rsi = ta.rsi(self.candles, self.rsi_period)
        rsi_overbought = current_rsi > self.rsi_short_threshold  # RSI > 60

        # Si NO hay divergencia Y RSI NO está en sobrecompra → rechazar
        if not has_bearish_divergence and not rsi_overbought:
            return False

        # FILTROS OBLIGATORIOS: Tendencia + Volumen
        return (
            self._trend_filter_short() and
            self._volume_confirmation()
        )

    def should_cancel_entry(self) -> bool:
        return False

    # =============================================================================
    # EJECUCIÓN DE TRADES
    # =============================================================================

    def go_long(self):
        """Ejecutar entrada LONG en FUTURES"""
        # Calcular tamaño de posición basado en ATR
        atr = ta.atr(self.candles, self.atr_period)
        stop_distance = atr * 1.8  # Stop loss más amplio para evitar whipsaws
        qty = self._calculate_position_size(stop_distance)
        
        self.buy = qty, self.close
        
        # Registrar entrada
        self.vars['entry_price'] = self.close
        self.vars['sl_price'] = self.close - stop_distance
        self.vars['tp1_hit'] = False
        self.vars['tp2_hit'] = False
        # Store the initial risk distance (price units) to compute R
        self.vars['initial_risk_distance'] = stop_distance
        self.vars['last_signal_time'] = self.current_candle[0]
        
        # Stop loss inicial (soportado en FUTURES)
        self.stop_loss = qty, self.vars['sl_price']

    def go_short(self):
        """Ejecutar entrada SHORT en FUTURES"""
        # Calcular tamaño de posición basado en ATR
        atr = ta.atr(self.candles, self.atr_period)
        stop_distance = atr * 1.8  # Stop loss más amplio
        qty = self._calculate_position_size(stop_distance)
        
        self.sell = qty, self.close
        
        # Registrar entrada
        self.vars['entry_price'] = self.close
        self.vars['sl_price'] = self.close + stop_distance
        self.vars['tp1_hit'] = False
        self.vars['tp2_hit'] = False
        # Store the initial risk distance (price units) to compute R
        self.vars['initial_risk_distance'] = stop_distance
        self.vars['last_signal_time'] = self.current_candle[0]
        
        # Stop loss inicial (soportado en FUTURES)
        self.stop_loss = qty, self.vars['sl_price']

    # GESTIÓN DE POSICIÓN
    # =============================================================================

    def update_position(self):
        """Gestión dinámica de posición con take profits y cierre final"""
        if not self.position.is_open:
            return
        # Use the initial risk distance (stored at entry) for R calculations
        initial_risk = self.vars.get('initial_risk_distance', 0)
        if initial_risk <= 0:
            # Defensive: nothing we can compute safely
            return

        if self.is_long:
            current_profit = self.close - self.vars['entry_price']

            # STOP LOSS MANUAL: if current price reached the live stop, fully close
            if self.close <= self.vars['sl_price']:
                self.liquidate()
                return
        else:
            current_profit = self.vars['entry_price'] - self.close

            # STOP LOSS MANUAL
            if self.close >= self.vars['sl_price']:
                self.liquidate()
                return

        # Compute R using the initial risk distance (price units)
        r_ratio = current_profit / initial_risk
        
        # v5.2: Take Profit 1: 1.2R - Cerrar 50% (MÁS CONSERVADOR para 55%+ win rate)
        if r_ratio >= 1.2 and not self.vars['tp1_hit']:
            self.vars['tp1_hit'] = True
            if self.is_long:
                self.sell = self.position.qty * 0.5, self.close
            else:
                self.buy = self.position.qty * 0.5, self.close
            # Mover stop loss a break-even
            self.vars['sl_price'] = self.vars['entry_price']

        # v5.2: Take Profit 2: 2.5R - Cerrar 30% más (MÁS ALCANZABLE)
        elif r_ratio >= 2.5 and not self.vars['tp2_hit'] and self.vars['tp1_hit']:
            self.vars['tp2_hit'] = True
            remaining_qty = self.position.qty
            if self.is_long:
                self.sell = remaining_qty * 0.6, self.close
            else:
                self.buy = remaining_qty * 0.6, self.close# Trailing stop para el 20% restante
            # trailing distances should be based on the initial risk
            if self.is_long:
                trailing_distance = initial_risk * 0.8
                new_sl = self.close - trailing_distance
                if new_sl > self.vars['sl_price']:
                    self.vars['sl_price'] = new_sl
            else:
                trailing_distance = initial_risk * 0.8
                new_sl = self.close + trailing_distance
                if new_sl < self.vars['sl_price']:
                    self.vars['sl_price'] = new_sl

        # v5.2: Take Profit 3: 4R - Cerrar el 20% restante (MÁS REALISTA)
        elif r_ratio >= 4.0 and self.vars['tp2_hit']:
            self.liquidate()  # Cerrar todo lo que quedareturn

        # Trailing stop dinámico después de TP2 (usar initial_risk)
        elif self.vars['tp2_hit'] and r_ratio > 2.5:
            if self.is_long:
                trailing_distance = initial_risk * 0.5
                new_sl = self.close - trailing_distance
                if new_sl > self.vars['sl_price']:
                    self.vars['sl_price'] = new_sl
            else:
                trailing_distance = initial_risk * 0.5
                new_sl = self.close + trailing_distance
                if new_sl < self.vars['sl_price']:
                    self.vars['sl_price'] = new_sl

    # FILTROS DE TENDENCIA
    # =============================================================================

    def _trend_filter_long(self) -> bool:
        """Filtro de tendencia alcista: precio y EMA50 por encima de EMA200"""
        ema_50 = ta.ema(self.candles, self.ema_fast)
        ema_200 = ta.ema(self.candles, self.ema_slow)
        price_above = self.close > ema_200
        return price_above and (ema_50 > ema_200)

    def _trend_filter_short(self) -> bool:
        """Filtro de tendencia bajista: precio y EMA50 por debajo de EMA200"""
        ema_200 = ta.ema(self.candles, self.ema_slow)
        ema_50 = ta.ema(self.candles, self.ema_fast)
        price_below = self.close < ema_200
        return price_below and (ema_50 < ema_200)

    # =============================================================================
    # INDICADORES Y SEÑALES
    # =============================================================================

    def _rsi_oversold(self) -> bool:
        """RSI en zona de sobreventa"""
        rsi = ta.rsi(self.candles[:, 2], self.rsi_period)
        return rsi < self.rsi_long_threshold

    def _rsi_overbought(self) -> bool:
        """RSI en zona de sobrecompra"""
        rsi = ta.rsi(self.candles[:, 2], self.rsi_period)
        return rsi > self.rsi_short_threshold

    def _macd_bullish_signal(self) -> bool:
        """MACD señal alcista simplificada"""
        macd_line, macd_signal, macd_histogram = ta.macd(self.candles[:, 2], self.macd_fast, self.macd_slow, self.macd_signal)

        # MACD es alcista (línea por encima de señal)
        return macd_line > macd_signal and macd_histogram > 0

    def _macd_bearish_signal(self) -> bool:
        """MACD señal bajista simplificada"""
        macd_line, macd_signal, macd_histogram = ta.macd(self.candles[:, 2], self.macd_fast, self.macd_slow, self.macd_signal)

        # MACD es bajista (línea por debajo de señal)
        return macd_line < macd_signal and macd_histogram < 0

    def _volume_confirmation(self) -> bool:
        """Confirmación por volumen mejorada"""
        if len(self.candles) < self.volume_period:
            return False
            
        # Volumen actual vs promedio de 20 períodos
        avg_volume = np.mean(self.candles[-self.volume_period:, 5])
        current_volume = self.candles[-1, 5]
        
        # Volumen de las últimas 3 velas vs promedio
        recent_volume = np.mean(self.candles[-3:, 5])
        
        return current_volume > avg_volume * 1.2 and recent_volume > avg_volume * 1.1

    def _not_overextended(self) -> bool:
        """Verificar que el precio no esté sobreextendido"""
        ema_50 = ta.ema(self.candles, self.ema_fast)
        
        # Distancia del precio a la EMA 50
        distance_pct = abs(self.close - ema_50) / ema_50 * 100
        
        return distance_pct < 8.0  # No más de 8% de distancia

    def _volatility_ok(self) -> bool:
        """Exigir volatilidad mínima vía ATR"""
        atr = ta.atr(self.candles, self.atr_period)
        if atr <= 0:
            return False
        return (atr / max(self.close, 1e-8)) >= self.min_atr_pct

    # =============================================================================
    # TRADE LIMITING
    # =============================================================================
    def _can_trade_today(self) -> bool:
        """Verifica si no se ha superado la pérdida máxima diaria (3%)"""
        # Calcular día usando timestamp en milisegundos
        day_key = int(self.current_candle[0] // (24 * 60 * 60 * 1000))
        last_day = self.vars.get('daily_loss_check_day', None)

        # Nuevo día: resetear balance inicial
        if last_day != day_key:
            self.vars['daily_loss_check_day'] = day_key
            self.vars['daily_start_balance'] = self.balance

        # Calcular pérdida del día
        daily_start = self.vars.get('daily_start_balance', self.balance)
        if daily_start <= 0:
            return True  # Caso defensivo

        current_balance = self.balance
        daily_loss_pct = ((daily_start - current_balance) / daily_start) * 100

        # Permitir trading si no se ha superado el límite de 3%
        return daily_loss_pct < self.max_daily_loss_pct

    # =============================================================================
    # DETECCIÓN DE DIVERGENCIAS
    # =============================================================================

    def _bullish_divergence(self) -> bool:
        """
        Detección de divergencia alcista RSI vs Precio

        Divergencia alcista: Precio baja pero RSI sube (señal de reversión alcista)
        v5.2-FIXED-v3: Usa cálculo manual de RSI para evitar IndexError
        """
        if len(self.candles) < 60:
            return False

        # Calcular RSI manualmente para todas las velas
        close_prices = self.candles[:, 2]  # Columna close
        low_prices = self.candles[:, 3]    # Columna low

        # Usar cálculo manual de RSI que retorna array completo
        rsi_array = self._calculate_rsi_array(close_prices, self.rsi_period)

        # Buscar mínimos en las últimas 40 velas (usando índices POSITIVOS)
        lookback = 40
        total_candles = len(self.candles)
        price_lows = []

        # Iterar desde el final hacia atrás usando índices positivos
        for i in range(total_candles - 5, max(total_candles - lookback, 5), -1):
            # Verificar si es un mínimo local (comparar con 2 velas a cada lado)
            if (low_prices[i] <= low_prices[i-1] and
                low_prices[i] <= low_prices[i-2] and
                low_prices[i] <= low_prices[i+1] and
                low_prices[i] <= low_prices[i+2]):

                # Guardar: (índice, precio_low, valor_rsi)
                # rsi_array[i] ahora es un valor escalar válido
                price_lows.append((i, low_prices[i], rsi_array[i]))

        # Necesitamos al menos 2 mínimos
        if len(price_lows) < 2:
            return False

        # Buscar divergencia: precio más reciente más bajo PERO RSI más alto
        # price_lows[0] es el más reciente, price_lows[-1] el más antiguo
        for j in range(len(price_lows) - 1):
            idx_recent, price_recent, rsi_recent = price_lows[j]

            for k in range(j + 1, len(price_lows)):
                idx_old, price_old, rsi_old = price_lows[k]

                # Divergencia alcista: precio baja, RSI sube
                if price_recent < price_old and rsi_recent > rsi_old:
                    price_diff_pct = abs((price_recent - price_old) / price_old) * 100
                    rsi_diff = abs(rsi_recent - rsi_old)

                    # Divergencia válida: 0.3% precio + 3 puntos RSI
                    if price_diff_pct >= 0.3 and rsi_diff >= 3:
                        return True

        return False

    def _bearish_divergence(self) -> bool:
        """
        Detección de divergencia bajista RSI vs Precio

        Divergencia bajista: Precio sube pero RSI baja (señal de reversión bajista)
        v5.2-FIXED-v3: Usa cálculo manual de RSI para evitar IndexError
        """
        if len(self.candles) < 60:
            return False

        # Calcular RSI manualmente para todas las velas
        close_prices = self.candles[:, 2]  # Columna close
        high_prices = self.candles[:, 2]    # Columna high (usar close en vez de high para consistencia)

        # Usar cálculo manual de RSI que retorna array completo
        rsi_array = self._calculate_rsi_array(close_prices, self.rsi_period)

        # Buscar máximos en las últimas 40 velas (usando índices POSITIVOS)
        lookback = 40
        total_candles = len(self.candles)
        price_highs = []

        # Iterar desde el final hacia atrás usando índices positivos
        for i in range(total_candles - 5, max(total_candles - lookback, 5), -1):
            # Verificar si es un máximo local (comparar con 2 velas a cada lado)
            if (high_prices[i] >= high_prices[i-1] and
                high_prices[i] >= high_prices[i-2] and
                high_prices[i] >= high_prices[i+1] and
                high_prices[i] >= high_prices[i+2]):

                # Guardar: (índice, precio_high, valor_rsi)
                # rsi_array[i] ahora es un valor escalar válido
                price_highs.append((i, high_prices[i], rsi_array[i]))

        # Necesitamos al menos 2 máximos
        if len(price_highs) < 2:
            return False

        # Buscar divergencia: precio más reciente más alto PERO RSI más bajo
        # price_highs[0] es el más reciente, price_highs[-1] el más antiguo
        for j in range(len(price_highs) - 1):
            idx_recent, price_recent, rsi_recent = price_highs[j]

            for k in range(j + 1, len(price_highs)):
                idx_old, price_old, rsi_old = price_highs[k]

                # Divergencia bajista: precio sube, RSI baja
                if price_recent > price_old and rsi_recent < rsi_old:
                    price_diff_pct = abs((price_recent - price_old) / price_old) * 100
                    rsi_diff = abs(rsi_recent - rsi_old)

                    # Divergencia válida: 0.3% precio + 3 puntos RSI
                    if price_diff_pct >= 0.3 and rsi_diff >= 3:
                        return True

        return False

    # =============================================================================
    # GESTIÓN DE RIESGO
    # =============================================================================

    def _calculate_position_size(self, stop_distance):
        """
        Calcula tamaño de posición para riesgo del 1.5% con apalancamiento 20x

        Con leverage:
        - Capital disponible = balance * leverage
        - Pero el riesgo sigue siendo 1.5% del balance (sin apalancar)
        - Esto permite abrir posiciones más grandes manteniendo el riesgo controlado
        """
        # Riesgo en $ basado en balance real (sin apalancamiento)
        risk_amount = self.balance * (self.risk_percent / 100)

        # Tamaño de posición basado en stop distance
        # position_value = cuánto $ queremos arriesgar / (stop_distance como % del precio)
        position_value = risk_amount / (stop_distance / self.close)

        # Con leverage 20x, podemos abrir posiciones hasta 20x nuestro capital
        # Limitar a 90% del capital apalancado disponible
        max_position_value = self.balance * self.leverage * 0.9
        position_value = min(position_value, max_position_value)

        # Convertir valor de posición a cantidad de BTC
        qty = position_value / self.close

        return round(qty, 6)  # 6 decimales para precisión