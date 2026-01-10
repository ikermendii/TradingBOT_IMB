"""
🚀 TREND-FOLLOWING STRATEGY - Multi-Timeframe Breakout System
==============================================================

Version: v11.2-RISK - Risk Management Optimized
Part of: v11.0-UNIVERSAL Hybrid System

CAMBIOS v11.2 vs v11.1:
- risk_percent: 1.5% → 1.0% (reducir pérdidas promedio)
- leverage: 20 → 10 (menos apalancamiento, menos riesgo)

CAMBIOS v11.1 vs v11.0:
- minimum_score: 4 → 2 (menos restrictivo, más trades)
- tp_final_ratio: 6R → 4R (TP más realista para crypto)
- break_even_ratio: 3R → 2R (proteger profits antes)

PROBLEMA v11.1:
- Win rate excelente (30.16%) pero Avg Loss demasiado alto ($182)
- Expectancy casi cero (-$0.19)
- Net Profit -1.14% (break-even después de fees)

OBJETIVO v11.2:
Reducir Avg Loss manteniendo Win Rate

PERFORMANCE TARGET (2020-2022):
- Net Profit: +15-30%
- Win Rate: >28%
- Max DD: <-35%
- Calmar: >0.5

Autor: Claude Sonnet 4.5
Fecha: 2025-12-28
"""

from jesse.strategies import Strategy
import jesse.indicators as ta
import numpy as np


class TrendFollowing(Strategy):
    def __init__(self):
        super().__init__()
        self.vars = {
            'position_size': 0,
            'entry_price': 0,
            'sl_price': 0,
            'be_activated': False,
            'last_signal_time': 0,
            'daily_start_balance': 0,
            'daily_loss_check_day': None,
            'initial_risk_distance': 0,
            'highest_price': 0,  # Para trailing stop
            'lowest_price': 0,   # Para trailing stop SHORT
        }

    # =========================================================================
    # PARÁMETROS DE LA ESTRATEGIA
    # =========================================================================

    @property
    def rsi_period(self):
        return 14

    @property
    def macd_fast(self):
        return 15

    @property
    def macd_slow(self):
        return 30

    @property
    def macd_signal(self):
        return 9

    @property
    def ema_fast(self):
        return 50

    @property
    def atr_period(self):
        return 14

    @property
    def volume_period(self):
        return 20

    @property
    def risk_percent(self):
        return 1.0  # v11.2: Reducido de 1.5% → 1.0%

    # --- Trend-Following Specific Parameters ---

    @property
    def breakout_lookback(self):
        """Velas para detectar high/low de breakout"""
        return 20

    @property
    def breakout_threshold(self):
        """Threshold mínimo de breakout (1%)"""
        return 0.01

    @property
    def minimum_score(self):
        """Score mínimo - SIMPLIFICADO para más trades"""
        return 2  # v11.1: Reducido de 4 → 2

    @property
    def break_even_ratio(self):
        """Break-even OPTIMIZADO - proteger profits rápido"""
        return 2.0  # v11.1: Reducido de 3.0 → 2.0

    @property
    def tp_final_ratio(self):
        """Take profit REALISTA para crypto volatility"""
        return 4.0  # v11.1: Reducido de 6.0 → 4.0

    @property
    def trailing_stop_ratio(self):
        """Trailing stop desde el high/low"""
        return 2.0  # 2R de espacio

    @property
    def signal_cooldown_minutes(self):
        return 60

    @property
    def min_atr_pct(self):
        return 0.004  # 0.4%

    @property
    def adx_threshold(self):
        """ADX para confirmar trending market"""
        return 25  # Más estricto que Mean-Reversion (15)

    @property
    def volume_multiplier(self):
        """Volumen debe ser X veces mayor que promedio"""
        return 1.3  # 30% más volumen

    @property
    def max_daily_loss_pct(self):
        return 3.0

    @property
    def leverage(self):
        return 10  # v11.2: Reducido de 20 → 10

    # =========================================================================
    # CONDICIONES DE ENTRADA
    # =========================================================================

    def should_long(self) -> bool:
        """
        Trend-Following LONG: Entrar en BREAKOUTS alcistas

        Score system (mínimo 2 puntos - v11.1):
        - Breakout de resistencia (2 puntos) - PREMIUM
        - MACD alcista 1H (2 puntos) - PREMIUM
        - Momentum alcista (1 punto)
        - Volumen alto (1 punto)
        - ADX trending (1 punto)
        """
        # CAPA 1: FILTROS BÁSICOS
        if not self._basic_filters():
            return False

        # PREVENIR CONFLICTO: No LONG si precio está cayendo
        if self.close < self.open:
            return False

        # CAPA 2: SCORE SYSTEM
        score = 0

        # 1. BREAKOUT de resistencia (2 puntos - SEÑAL PREMIUM)
        if self._detect_breakout_long():
            score += 2

        # 2. MACD alcista 1H (2 puntos - SEÑAL PREMIUM)
        if self._macd_bullish_1h():
            score += 2

        # 3. Momentum alcista 15M (1 punto)
        if self._momentum_bullish():
            score += 1

        # 4. Volumen confirmación (1 punto)
        if self._volume_confirmation():
            score += 1

        # 5. ADX trending (1 punto)
        if self._adx_trending():
            score += 1

        # Score mínimo: 2 puntos (v11.1)
        return score >= self.minimum_score

    def should_short(self) -> bool:
        """
        Trend-Following SHORT: Entrar en BREAKDOWNS bajistas

        Score system (mínimo 2 puntos - v11.1):
        - Breakdown de soporte (2 puntos) - PREMIUM
        - MACD bajista 1H (2 puntos) - PREMIUM
        - Momentum bajista (1 punto)
        - Volumen alto (1 punto)
        - ADX trending (1 punto)
        """
        # CAPA 1: FILTROS BÁSICOS
        if not self._basic_filters():
            return False

        # PREVENIR CONFLICTO: No SHORT si precio está subiendo
        if self.close > self.open:
            return False

        # CAPA 2: SCORE SYSTEM
        score = 0

        # 1. BREAKDOWN de soporte (2 puntos - SEÑAL PREMIUM)
        if self._detect_breakdown_short():
            score += 2

        # 2. MACD bajista 1H (2 puntos - SEÑAL PREMIUM)
        if self._macd_bearish_1h():
            score += 2

        # 3. Momentum bajista 15M (1 punto)
        if self._momentum_bearish():
            score += 1

        # 4. Volumen confirmación (1 punto)
        if self._volume_confirmation():
            score += 1

        # 5. ADX trending (1 punto)
        if self._adx_trending():
            score += 1

        # Score mínimo: 4 puntos
        return score >= self.minimum_score

    def should_cancel_entry(self) -> bool:
        return False

    # =========================================================================
    # EJECUCIÓN DE TRADES
    # =========================================================================

    def go_long(self):
        """Ejecutar entrada LONG"""
        atr = ta.atr(self.candles, self.atr_period)
        stop_distance = atr * 3.5
        qty = self._calculate_position_size(stop_distance)

        self.buy = qty, self.close

        # Registrar entrada
        self.vars['entry_price'] = self.close
        self.vars['sl_price'] = self.close - stop_distance
        self.vars['be_activated'] = False
        self.vars['initial_risk_distance'] = stop_distance
        self.vars['highest_price'] = self.close
        self.vars['last_signal_time'] = self.current_candle[0]

        # Stop loss inicial
        self.stop_loss = qty, self.vars['sl_price']

    def go_short(self):
        """Ejecutar entrada SHORT"""
        atr = ta.atr(self.candles, self.atr_period)
        stop_distance = atr * 3.5
        qty = self._calculate_position_size(stop_distance)

        self.sell = qty, self.close

        # Registrar entrada
        self.vars['entry_price'] = self.close
        self.vars['sl_price'] = self.close + stop_distance
        self.vars['be_activated'] = False
        self.vars['initial_risk_distance'] = stop_distance
        self.vars['lowest_price'] = self.close
        self.vars['last_signal_time'] = self.current_candle[0]

        # Stop loss inicial
        self.stop_loss = qty, self.vars['sl_price']

    # =========================================================================
    # GESTIÓN DE POSICIÓN - TRAILING STOP
    # =========================================================================

    def update_position(self):
        """
        Trend-Following: Dejar correr ganancias con trailing stop

        REGLAS:
        1. Break-even a 3.0R (más relajado que Mean-Reversion)
        2. Trailing stop 2R desde high/low después de 3.0R
        3. TP final en 6.0R (captura mega trends)
        """
        if not self.position.is_open:
            return

        initial_risk = self.vars.get('initial_risk_distance', 0)
        if initial_risk <= 0:
            return

        if self.is_long:
            current_profit = self.close - self.vars['entry_price']

            # Stop loss manual
            if self.close <= self.vars['sl_price']:
                self.liquidate()
                return
        else:
            current_profit = self.vars['entry_price'] - self.close

            if self.close >= self.vars['sl_price']:
                self.liquidate()
                return

        # Calcular R ratio
        r_ratio = current_profit / initial_risk

        # REGLA 1: Break-even a 3.0R
        if r_ratio >= self.break_even_ratio and not self.vars['be_activated']:
            self.vars['be_activated'] = True
            self.vars['sl_price'] = self.vars['entry_price']

        # REGLA 2: Trailing stop DESPUÉS de 3.0R
        if r_ratio >= self.break_even_ratio:
            if self.is_long:
                # Track highest price
                self.vars['highest_price'] = max(self.vars['highest_price'], self.close)

                # Trailing stop: 2R desde el high
                trailing_sl = self.vars['highest_price'] - (initial_risk * self.trailing_stop_ratio)

                # Solo mover SL hacia arriba
                if trailing_sl > self.vars['sl_price']:
                    self.vars['sl_price'] = trailing_sl

            else:  # SHORT
                # Track lowest price
                self.vars['lowest_price'] = min(self.vars['lowest_price'], self.close)

                # Trailing stop: 2R desde el low
                trailing_sl = self.vars['lowest_price'] + (initial_risk * self.trailing_stop_ratio)

                # Solo mover SL hacia abajo
                if trailing_sl < self.vars['sl_price']:
                    self.vars['sl_price'] = trailing_sl

        # REGLA 3: TP final en 6.0R
        if r_ratio >= self.tp_final_ratio:
            self.liquidate()
            return

    # =========================================================================
    # FILTROS Y DETECCIÓN DE SEÑALES
    # =========================================================================

    def _basic_filters(self) -> bool:
        """Filtros básicos que deben pasar SIEMPRE"""
        # Cooldown
        if self.current_candle[0] - self.vars['last_signal_time'] < self.signal_cooldown_minutes * 60 * 1000:
            return False

        # Daily loss limit
        if not self._can_trade_today():
            return False

        # Volatilidad mínima
        atr = ta.atr(self.candles, self.atr_period)
        atr_pct = atr / self.close
        if atr_pct < self.min_atr_pct:
            return False

        return True

    def _detect_breakout_long(self) -> bool:
        """Detecta breakout alcista de resistencia"""
        if len(self.candles) < self.breakout_lookback:
            return False

        # High de las últimas 20 velas
        high_20 = np.max(self.candles[-self.breakout_lookback:, 2])  # High column

        # Breakout si precio actual > high_20 × (1 + threshold)
        breakout_level = high_20 * (1 + self.breakout_threshold)

        return self.close > breakout_level

    def _detect_breakdown_short(self) -> bool:
        """Detecta breakdown bajista de soporte"""
        if len(self.candles) < self.breakout_lookback:
            return False

        # Low de las últimas 20 velas
        low_20 = np.min(self.candles[-self.breakout_lookback:, 3])  # Low column

        # Breakdown si precio actual < low_20 × (1 - threshold)
        breakdown_level = low_20 * (1 - self.breakout_threshold)

        return self.close < breakdown_level

    def _macd_bullish_1h(self) -> bool:
        """MACD alcista en 1H"""
        try:
            candles_1h = self.get_candles(self.exchange, self.symbol, '1h')
            if len(candles_1h) < 100:
                return False

            macd_line, signal_line, _ = ta.macd(candles_1h, self.macd_fast, self.macd_slow, self.macd_signal)

            # MACD alcista: línea > señal AND línea > 0
            return macd_line > signal_line and macd_line > 0

        except Exception:
            return False

    def _macd_bearish_1h(self) -> bool:
        """MACD bajista en 1H"""
        try:
            candles_1h = self.get_candles(self.exchange, self.symbol, '1h')
            if len(candles_1h) < 100:
                return False

            macd_line, signal_line, _ = ta.macd(candles_1h, self.macd_fast, self.macd_slow, self.macd_signal)

            # MACD bajista: línea < señal AND línea < 0
            return macd_line < signal_line and macd_line < 0

        except Exception:
            return False

    def _momentum_bullish(self) -> bool:
        """Momentum alcista: precio > EMA50"""
        ema_50 = ta.ema(self.candles, self.ema_fast)
        return self.close > ema_50

    def _momentum_bearish(self) -> bool:
        """Momentum bajista: precio < EMA50"""
        ema_50 = ta.ema(self.candles, self.ema_fast)
        return self.close < ema_50

    def _volume_confirmation(self) -> bool:
        """Volumen confirmación: volume > avg × multiplier"""
        if len(self.candles) < self.volume_period:
            return False

        avg_volume = np.mean(self.candles[-self.volume_period:, 5])
        current_volume = self.candles[-1, 5]

        return current_volume > avg_volume * self.volume_multiplier

    def _adx_trending(self) -> bool:
        """ADX confirma trending market"""
        adx = ta.adx(self.candles, period=14)
        return adx > self.adx_threshold

    def _can_trade_today(self) -> bool:
        """Verifica daily loss limit"""
        day_key = int(self.current_candle[0] // (24 * 60 * 60 * 1000))
        last_day = self.vars.get('daily_loss_check_day', None)

        # Nuevo día: resetear
        if last_day != day_key:
            self.vars['daily_loss_check_day'] = day_key
            self.vars['daily_start_balance'] = self.balance

        # Calcular pérdida del día
        daily_start = self.vars.get('daily_start_balance', self.balance)
        if daily_start <= 0:
            return True

        current_balance = self.balance
        daily_loss_pct = ((daily_start - current_balance) / daily_start) * 100

        return daily_loss_pct < self.max_daily_loss_pct

    def _calculate_position_size(self, stop_distance):
        """Calcula tamaño de posición para 1.5% risk"""
        risk_amount = self.balance * (self.risk_percent / 100)
        position_value = risk_amount / (stop_distance / self.close)
        max_position_value = self.balance * self.leverage * 0.9
        position_value = min(position_value, max_position_value)
        qty = position_value / self.close

        return round(qty, 6)
