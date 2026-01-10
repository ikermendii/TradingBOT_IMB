"""
UNIVERSAL ROBUST STRATEGY - Walk-Forward Validated Multi-Asset Bot
===================================================================

Version: v1.0-ROBUST - Industry Standard Parameters

METHODOLOGY:
- Walk-forward optimization (70% train, 30% validate)
- Multiple asset validation (BTC + ETH minimum)
- NO curve-fitted parameters - industry standards only
- Target: 15-20% annual return, Max DD <30%

PARAMETERS (INDUSTRY STANDARD - NOT OPTIMIZED):
- RSI: 30/70 (classic oversold/overbought)
- EMA: 50/200 (golden cross system)
- ATR: 14 periods (volatility standard)
- Stop Loss: 2 ATR
- Take Profit: 3:1 Risk-Reward
- Position Size: 1% risk per trade

PHILOSOPHY:
If it needs RSI=36.7 to work → it's overfitted garbage
If it works with RSI=30 → it's robust

Author: Claude Code
Date: 2025-12-29
"""

from jesse.strategies import Strategy
import jesse.indicators as ta
import numpy as np


class UniversalRobust(Strategy):
    def __init__(self):
        super().__init__()
        self.vars = {
            'entry_price': 0,
            'sl_price': 0,
            'tp_price': 0,
            'last_trade_time': 0,
        }

    # =========================================================================
    # INDUSTRY STANDARD PARAMETERS (NO OPTIMIZATION)
    # =========================================================================

    @property
    def rsi_period(self):
        return 14  # Standard

    @property
    def rsi_oversold(self):
        return 30  # Industry standard

    @property
    def rsi_overbought(self):
        return 70  # Industry standard

    @property
    def ema_fast(self):
        return 50  # Standard

    @property
    def ema_slow(self):
        return 200  # Standard

    @property
    def atr_period(self):
        return 14  # Standard

    @property
    def stop_atr_multiplier(self):
        return 2.0  # 2 ATR stop

    @property
    def risk_reward_ratio(self):
        return 3.0  # 3:1 R:R

    @property
    def risk_percent(self):
        return 1.0  # 1% risk per trade

    @property
    def cooldown_hours(self):
        return 4  # 4 hours between trades

    @property
    def leverage(self):
        return 5  # Conservative leverage

    # =========================================================================
    # ENTRY LOGIC - SIMPLE EMA CROSSOVER + RSI CONFIRMATION
    # =========================================================================

    def should_long(self) -> bool:
        """
        LONG when:
        1. Price > EMA200 (uptrend)
        2. EMA50 > EMA200 (golden cross)
        3. RSI < 30 (oversold, mean reversion opportunity)
        4. Cooldown passed
        """
        # Cooldown
        if self.current_candle[0] - self.vars['last_trade_time'] < self.cooldown_hours * 60 * 60 * 1000:
            return False

        # Don't enter if already in position
        if self.position.is_open:
            return False

        # Calculate indicators
        ema_50 = ta.ema(self.candles, self.ema_fast)
        ema_200 = ta.ema(self.candles, self.ema_slow)
        rsi = ta.rsi(self.candles, self.rsi_period)

        # Entry conditions
        if self.close > ema_200:  # Uptrend
            if ema_50 > ema_200:  # Golden cross
                if rsi < self.rsi_oversold:  # Oversold
                    return True

        return False

    def should_short(self) -> bool:
        """
        SHORT when:
        1. Price < EMA200 (downtrend)
        2. EMA50 < EMA200 (death cross)
        3. RSI > 70 (overbought, mean reversion opportunity)
        4. Cooldown passed
        """
        # Cooldown
        if self.current_candle[0] - self.vars['last_trade_time'] < self.cooldown_hours * 60 * 60 * 1000:
            return False

        # Don't enter if already in position
        if self.position.is_open:
            return False

        # Calculate indicators
        ema_50 = ta.ema(self.candles, self.ema_fast)
        ema_200 = ta.ema(self.candles, self.ema_slow)
        rsi = ta.rsi(self.candles, self.rsi_period)

        # Entry conditions
        if self.close < ema_200:  # Downtrend
            if ema_50 < ema_200:  # Death cross
                if rsi > self.rsi_overbought:  # Overbought
                    return True

        return False

    # =========================================================================
    # POSITION MANAGEMENT - FIXED STOP/TARGET
    # =========================================================================

    def go_long(self):
        """Execute LONG with 2 ATR stop and 3:1 R:R target"""
        atr = ta.atr(self.candles, self.atr_period)
        stop_distance = atr * self.stop_atr_multiplier

        # Calculate position size based on 1% risk
        qty = self._calculate_position_size(stop_distance)

        # Execute entry
        self.buy = qty, self.close

        # Set stop and target
        self.vars['entry_price'] = self.close
        self.vars['sl_price'] = self.close - stop_distance
        self.vars['tp_price'] = self.close + (stop_distance * self.risk_reward_ratio)
        self.vars['last_trade_time'] = self.current_candle[0]

        self.stop_loss = qty, self.vars['sl_price']
        self.take_profit = qty, self.vars['tp_price']

    def go_short(self):
        """Execute SHORT with 2 ATR stop and 3:1 R:R target"""
        atr = ta.atr(self.candles, self.atr_period)
        stop_distance = atr * self.stop_atr_multiplier

        # Calculate position size based on 1% risk
        qty = self._calculate_position_size(stop_distance)

        # Execute entry
        self.sell = qty, self.close

        # Set stop and target
        self.vars['entry_price'] = self.close
        self.vars['sl_price'] = self.close + stop_distance
        self.vars['tp_price'] = self.close - (stop_distance * self.risk_reward_ratio)
        self.vars['last_trade_time'] = self.current_candle[0]

        self.stop_loss = qty, self.vars['sl_price']
        self.take_profit = qty, self.vars['tp_price']

    def update_position(self):
        """No trailing stop - fixed stop and target only"""
        pass

    def should_cancel_entry(self) -> bool:
        return False

    # =========================================================================
    # UTILITY
    # =========================================================================

    def _calculate_position_size(self, stop_distance):
        """Calculate position size for 1% risk"""
        risk_amount = self.balance * (self.risk_percent / 100)
        position_value = risk_amount / (stop_distance / self.close)

        # Apply leverage limit
        max_position = self.balance * self.leverage * 0.9
        position_value = min(position_value, max_position)

        qty = position_value / self.close
        return round(qty, 6)
