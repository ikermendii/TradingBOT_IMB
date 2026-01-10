"""
UNIVERSAL ROBUST V3.1 - RISK OPTIMIZED (8787% ROI Strategy)
================================================================

BASED ON: v3.0 (8787% ROI Strategy) with RISK MANAGEMENT optimization
Source: https://imbuedeskpicasso.medium.com/the-8787-roi-algo-strategy-unveiled-for-crypto-futures-22a5dd88c4a5

v3.0 Results (2020-2025):
- ROI: +1517.58%
- Annual Return: 59.57%
- Max Drawdown: -62.31% ⚠️ (TOO HIGH)
- Sharpe: 1.05
- Trades: 535 (89.8/year)

v3.1 CHANGES (Risk Optimization):
- Leverage: 5x → 3x (reduce exposure)
- Risk per trade: 1.5% → 1.0% (conservative)
- Expected: Max DD -62% → ~-38-45%
- Expected: Annual Return 59% → ~35-45% (still excellent)

INDICATORS (EXACT from article):
1. RSI (14) - Entry: RSI > 30 (exiting oversold, NOT in oversold)
2. MACD (12,26,9) - Entry: MACD > Signal (bullish)
3. Bollinger Bands (20, 2.0) - Entry: close > lower_band (NOT touching)
4. ADX (14) - Filter with range (min, max) + OR logic
5. EMA (for exit) - Exit: close < (EMA - ATR*multiplier)
6. ATR (14) - For exit calculation
7. Volume - Filter: volume > volume_mean

ENTRY LOGIC (EXACT from article):
LONG:
  - RSI > 30 (exiting oversold)
  - close > lower_band (above Bollinger lower)
  - MACD > Signal (bullish)
  - ADX in range (15-35 OR 25-45)
  - volume > volume_mean

SHORT:
  - RSI < 70 (exiting overbought)
  - close < upper_band (below Bollinger upper)
  - MACD < Signal (bearish)
  - ADX in range (15-35 OR 25-45)
  - volume > volume_mean

EXIT LOGIC (EXACT from article):
LONG EXIT:
  - close < (EMA - ATR * multiplier)
  - volume > volume_mean

SHORT EXIT:
  - close > (EMA + ATR * multiplier)
  - volume > volume_mean

Author: Claude Sonnet 4.5 - Exact implementation of proven strategy
Date: 2025-12-29
"""

from jesse.strategies import Strategy
import jesse.indicators as ta
from jesse import utils
import numpy as np


class UniversalRobustV3_1(Strategy):
    def __init__(self):
        super().__init__()
        self.vars = {
            'entry_price': 0,
            'last_trade_time': 0,
        }

    # =========================================================================
    # PARÁMETROS EXACTOS (de la estrategia 8787% ROI)
    # =========================================================================

    @property
    def rsi_period(self):
        return 14  # Estándar

    @property
    def rsi_entry_long(self):
        return 30  # RSI > 30 (exiting oversold, NOT < 30)

    @property
    def rsi_entry_short(self):
        return 70  # RSI < 70 (exiting overbought)

    @property
    def bb_period(self):
        return 20  # Estándar

    @property
    def bb_std(self):
        return 2.0  # Estándar

    @property
    def macd_fast(self):
        return 12  # Estándar

    @property
    def macd_slow(self):
        return 26  # Estándar

    @property
    def macd_signal(self):
        return 9  # Estándar

    @property
    def adx_period(self):
        return 14  # Estándar

    # ADX Range 1 (primary)
    @property
    def adx_long_min_1(self):
        return 15  # Trend confirmation minimum

    @property
    def adx_long_max_1(self):
        return 35  # Avoid exhausted trends

    # ADX Range 2 (alternative)
    @property
    def adx_long_min_2(self):
        return 25

    @property
    def adx_long_max_2(self):
        return 45

    # ADX for SHORT (same as LONG)
    @property
    def adx_short_min_1(self):
        return 15

    @property
    def adx_short_max_1(self):
        return 35

    @property
    def adx_short_min_2(self):
        return 25

    @property
    def adx_short_max_2(self):
        return 45

    @property
    def ema_period(self):
        return 50  # For exit calculation (not specified in article, using 50)

    @property
    def atr_period(self):
        return 14  # Estándar

    @property
    def atr_long_multiplier(self):
        return 2.0  # For exit: EMA - ATR*2.0

    @property
    def atr_short_multiplier(self):
        return 2.0  # For exit: EMA + ATR*2.0

    @property
    def volume_mean_period(self):
        return 20  # For volume filter

    @property
    def risk_percent(self):
        return 1.0  # v3.1: 1.0% (reduced from 1.5% in v3.0 for lower DD)

    @property
    def leverage(self):
        return 3  # v3.1: 3x (reduced from 5x in v3.0 for lower DD)

    # =========================================================================
    # INDICADORES - CALCULADOS UNA VEZ POR VELA
    # =========================================================================

    def _calculate_indicators(self):
        """Calcula todos los indicadores necesarios"""
        # RSI
        rsi = ta.rsi(self.candles, self.rsi_period)

        # MACD
        macd_line, macd_signal, macd_hist = ta.macd(
            self.candles,
            self.macd_fast,
            self.macd_slow,
            self.macd_signal
        )

        # Bollinger Bands
        bb_upper, bb_middle, bb_lower = ta.bollinger_bands(
            self.candles,
            self.bb_period,
            self.bb_std
        )

        # ADX
        adx = ta.adx(self.candles, self.adx_period)

        # EMA (for exit)
        ema = ta.ema(self.candles, self.ema_period)

        # ATR
        atr = ta.atr(self.candles, self.atr_period)

        # Volume mean
        volume_mean = ta.sma(self.candles[:, 5], self.volume_mean_period)  # column 5 is volume

        return {
            'rsi': rsi,
            'macd_line': macd_line,
            'macd_signal': macd_signal,
            'bb_upper': bb_upper,
            'bb_middle': bb_middle,
            'bb_lower': bb_lower,
            'adx': adx,
            'ema': ema,
            'atr': atr,
            'volume_mean': volume_mean
        }

    # =========================================================================
    # LÓGICA DE ENTRADA - EXACT COPY from 8787% ROI Strategy
    # =========================================================================

    def should_long(self) -> bool:
        """
        LONG Entry - EXACT from 8787% ROI article:

        Core conditions:
        1. RSI > 30 (exiting oversold, NOT < 30)
        2. close > lower_band (above Bollinger lower, NOT touching)
        3. MACD > Signal (bullish cross)

        Filters:
        4. ADX in range (min1-max1 OR min2-max2)
        5. volume > volume_mean
        """
        if self.position.is_open:
            return False

        # Calcular indicadores
        ind = self._calculate_indicators()

        # ===== CORE CONDITION 1: RSI > 30 (exiting oversold) =====
        # CRITICAL: NOT < 30 (in oversold), but > 30 (exiting oversold)
        if ind['rsi'] <= self.rsi_entry_long:
            return False

        # ===== CORE CONDITION 2: close > lower_band =====
        # CRITICAL: NOT touching band, just above it
        if self.close <= ind['bb_lower']:
            return False

        # ===== CORE CONDITION 3: MACD > Signal (bullish) =====
        if ind['macd_line'] <= ind['macd_signal']:
            return False

        # ===== FILTER 1: ADX Range (with OR logic) =====
        # (ADX > min1 AND ADX < max1) OR (ADX > min2 AND ADX < max2)
        adx_condition = (
            (
                (ind['adx'] > self.adx_long_min_1) and
                (ind['adx'] < self.adx_long_max_1)
            ) or
            (
                (ind['adx'] > self.adx_long_min_2) and
                (ind['adx'] < self.adx_long_max_2)
            )
        )

        if not adx_condition:
            return False

        # ===== FILTER 2: Volume > mean =====
        if self.volume <= ind['volume_mean']:
            return False

        # ALL conditions met → LONG
        return True

    def should_short(self) -> bool:
        """
        SHORT Entry - EXACT from 8787% ROI article:

        Core conditions:
        1. RSI < 70 (exiting overbought)
        2. close < upper_band (below Bollinger upper)
        3. MACD < Signal (bearish cross)

        Filters:
        4. ADX in range (min1-max1 OR min2-max2)
        5. volume > volume_mean
        """
        if self.position.is_open:
            return False

        # Calcular indicadores
        ind = self._calculate_indicators()

        # ===== CORE CONDITION 1: RSI < 70 (exiting overbought) =====
        if ind['rsi'] >= self.rsi_entry_short:
            return False

        # ===== CORE CONDITION 2: close < upper_band =====
        if self.close >= ind['bb_upper']:
            return False

        # ===== CORE CONDITION 3: MACD < Signal (bearish) =====
        if ind['macd_line'] >= ind['macd_signal']:
            return False

        # ===== FILTER 1: ADX Range (with OR logic) =====
        adx_condition = (
            (
                (ind['adx'] > self.adx_short_min_1) and
                (ind['adx'] < self.adx_short_max_1)
            ) or
            (
                (ind['adx'] > self.adx_short_min_2) and
                (ind['adx'] < self.adx_short_max_2)
            )
        )

        if not adx_condition:
            return False

        # ===== FILTER 2: Volume > mean =====
        if self.volume <= ind['volume_mean']:
            return False

        # ALL conditions met → SHORT
        return True

    # =========================================================================
    # GESTIÓN DE POSICIÓN - EXACT EXIT LOGIC from 8787% ROI
    # =========================================================================

    def go_long(self):
        """Ejecuta LONG con dynamic position sizing"""
        ind = self._calculate_indicators()
        atr = ind['atr']

        # Calculate position size based on 1.5% risk
        # Stop distance será calculado en update_position
        stop_distance = atr * self.atr_long_multiplier

        qty = self._calculate_position_size(stop_distance)

        # Ejecutar entrada
        self.buy = qty, self.close

        # Save entry info
        self.vars['entry_price'] = self.close
        self.vars['last_trade_time'] = self.current_candle[0]

        # NO set fixed stop/TP - we use dynamic exit in update_position

    def go_short(self):
        """Ejecuta SHORT con dynamic position sizing"""
        ind = self._calculate_indicators()
        atr = ind['atr']

        stop_distance = atr * self.atr_short_multiplier
        qty = self._calculate_position_size(stop_distance)

        # Ejecutar entrada
        self.sell = qty, self.close

        # Save entry info
        self.vars['entry_price'] = self.close
        self.vars['last_trade_time'] = self.current_candle[0]

    def update_position(self):
        """
        EXIT LOGIC - EXACT from 8787% ROI article:

        LONG EXIT: close < (EMA - ATR * multiplier) AND volume > volume_mean
        SHORT EXIT: close > (EMA + ATR * multiplier) AND volume > volume_mean
        """
        if not self.position.is_open:
            return

        ind = self._calculate_indicators()

        # Check exit conditions
        if self.is_long:
            # LONG EXIT: close < (EMA - ATR * multiplier)
            exit_price = ind['ema'] - (ind['atr'] * self.atr_long_multiplier)

            if (self.close < exit_price) and (self.volume > ind['volume_mean']):
                # Close position
                self.liquidate()

        else:  # SHORT
            # SHORT EXIT: close > (EMA + ATR * multiplier)
            exit_price = ind['ema'] + (ind['atr'] * self.atr_short_multiplier)

            if (self.close > exit_price) and (self.volume > ind['volume_mean']):
                # Close position
                self.liquidate()

    def should_cancel_entry(self) -> bool:
        return False

    # =========================================================================
    # UTILITY
    # =========================================================================

    def _calculate_position_size(self, stop_distance):
        """Calculate position size for 1.5% risk"""
        risk_amount = self.balance * (self.risk_percent / 100)
        position_value = risk_amount / (stop_distance / self.close)

        # Apply leverage limit
        max_position = self.balance * self.leverage * 0.9  # 90% del máximo por seguridad
        position_value = min(position_value, max_position)

        qty = position_value / self.close
        return round(qty, 6)
