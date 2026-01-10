"""
🚀 HYBRID UNIVERSAL STRATEGY - Adaptive Multi-Regime Trading System
====================================================================

Version: v11.0-UNIVERSAL-v6 - DYNAMIC Technical Regime Detection

ARQUITECTURA:
- RegimeDetector: REAL-TIME analysis using technical indicators
- Bull Parabolic (detected dynamically) → TrendFollowing v11.2
- High Volatility (default safe mode) → Multitimeframe v9.3-RSI36

REGIME DETECTION SYSTEM (v6 - TECHNICAL INDICATORS):

PARABOLIC detected when ALL conditions met:
1. Price > EMA200 4H (strong uptrend confirmation)
2. ROC 180 days > +50% (parabolic 6-month rally)
3. MACD 1D bullish (daily momentum positive)
4. Volume increasing 20%+ (institutional confirmation)

VOLATILE detected when ANY condition fails (safe default)

KEY IMPROVEMENT vs v5:
- NO hardcoded dates - works for FUTURE bull runs
- Detects regime changes in real-time
- Adapts to actual market conditions
- Can predict and catch next parabolic bull run

STRATEGY ROUTING:
- PARABOLIC regime → TrendFollowing v11.2 (breakout system)
- VOLATILE regime → Multitimeframe v9.3-RSI36 (mean-reversion)

TARGET USE CASE:
- Automatically detect next BTC bull run (2025? 2028?)
- Maximize gains during parabolic phases
- Protect capital during volatile/bear markets

Author: Claude Code
Date: 2025-12-28
"""

from jesse.strategies import Strategy
import jesse.indicators as ta
import numpy as np
from datetime import datetime

# Import sub-strategies
import sys
import os
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)


class HybridUniversal(Strategy):
    """
    Master hybrid strategy that switches between:
    - Multitimeframe v9.3 (mean-reversion for volatility)
    - TrendFollowing v11.2 (breakout for parabolic)
    """

    def __init__(self):
        super().__init__()
        self.vars = {
            # Regime tracking
            'current_regime': 'VOLATILE',  # PARABOLIC or VOLATILE
            'last_regime_check': 0,  # Timestamp of last check
            'regime_check_interval': 4 * 60 * 60 * 1000,  # 4 hours in ms

            # Position tracking (common to both strategies)
            'position_size': 0,
            'entry_price': 0,
            'sl_price': 0,
            'tp1_hit': False,
            'tp2_hit': False,
            'initial_risk_distance': 0,
            'last_signal_time': 0,
            'daily_start_balance': 0,
            'daily_loss_check_day': None,

            # TrendFollowing specific
            'score': 0,
            'breakout_price': 0,

            # Multitimeframe specific
            'divergence_lookback': 15,
            'trend_strength': 0,
            'trailing_activated': False,
            'highest_price': 0,
            'lowest_price': 0,
        }

    # =================================================================
    # REGIME DETECTION
    # =================================================================

    def _detect_regime(self) -> str:
        """
        Detect current market regime using TECHNICAL INDICATORS (DYNAMIC)

        v11.0-UNIVERSAL-v6: REAL regime detection for future prediction

        PARABOLIC BULL RUN detected when ALL conditions met:
        1. Price > EMA200 4H (strong uptrend)
        2. ROC 180 days > +50% (6-month rally >50%)
        3. MACD 1D bullish (daily momentum positive)
        4. Volume trending up (institutional confirmation)

        VOLATILE detected when ANY condition fails (default safe state)

        This allows the bot to:
        - Detect FUTURE bull runs automatically
        - Not rely on hardcoded historical dates
        - Adapt to real market conditions in real-time

        Returns:
            'PARABOLIC': Bull parabolic market (use TrendFollowing)
            'VOLATILE': High volatility market (use Multitimeframe v9.3)
        """
        try:
            # INDICATOR 1: Price > EMA200 4H (strong trend)
            candles_4h = self.get_candles(self.exchange, self.symbol, '4h')
            if len(candles_4h) < 200:
                return 'VOLATILE'  # Not enough data

            ema_200_4h = ta.ema(candles_4h, 200)
            price_4h = candles_4h[-1, 2]  # Close price

            if price_4h <= ema_200_4h:
                return 'VOLATILE'  # Not in strong uptrend

            # INDICATOR 2: ROC 180 days > 50% (parabolic move)
            # ROC = (price_now - price_180d_ago) / price_180d_ago * 100
            candles_1d = self.get_candles(self.exchange, self.symbol, '1D')
            if len(candles_1d) < 180:
                return 'VOLATILE'  # Not enough data

            price_now = candles_1d[-1, 2]  # Current close
            price_180d = candles_1d[-180, 2]  # 180 days ago close
            roc_180d = ((price_now - price_180d) / price_180d) * 100

            if roc_180d < 50.0:
                return 'VOLATILE'  # Not parabolic move

            # INDICATOR 3: MACD 1D bullish (momentum)
            if len(candles_1d) < 100:
                return 'VOLATILE'

            macd, signal, _ = ta.macd(candles_1d, 12, 26, 9)
            if macd <= signal or macd <= 0:
                return 'VOLATILE'  # Momentum not bullish

            # INDICATOR 4: Volume trending up (last 30d > previous 30d)
            if len(candles_1d) < 60:
                return 'VOLATILE'

            volume_recent = np.mean(candles_1d[-30:, 5])  # Last 30 days
            volume_previous = np.mean(candles_1d[-60:-30, 5])  # Previous 30 days

            if volume_recent <= volume_previous * 1.2:
                return 'VOLATILE'  # Volume not increasing

            # ALL CONDITIONS MET → PARABOLIC BULL RUN DETECTED
            return 'PARABOLIC'

        except Exception as e:
            # If any error, default to safe VOLATILE mode
            return 'VOLATILE'

    def _should_check_regime(self) -> bool:
        """Check if it's time to re-evaluate regime (every 4H)"""
        current_time = self.current_candle[0]
        time_since_check = current_time - self.vars['last_regime_check']
        return time_since_check >= self.vars['regime_check_interval']

    def _update_regime(self):
        """Update regime if needed and log changes"""
        if not self._should_check_regime():
            return

        new_regime = self._detect_regime()
        old_regime = self.vars['current_regime']

        # Update check timestamp
        self.vars['last_regime_check'] = self.current_candle[0]

        # If regime changed, log it
        if new_regime != old_regime:
            timestamp = datetime.fromtimestamp(self.current_candle[0] / 1000)
            print(f"\n{'='*70}")
            print(f"🔄 REGIME CHANGE DETECTED - {timestamp}")
            print(f"   Old: {old_regime} → New: {new_regime}")
            print(f"{'='*70}\n")

            self.vars['current_regime'] = new_regime

    # =================================================================
    # ENTRY LOGIC (DELEGATES TO SUB-STRATEGIES)
    # =================================================================

    def should_long(self) -> bool:
        """Route to appropriate strategy based on current regime"""
        # CRITICAL FIX: Detect regime on FIRST candle
        if self.vars['last_regime_check'] == 0:
            new_regime = self._detect_regime()
            self.vars['current_regime'] = new_regime
            self.vars['last_regime_check'] = self.current_candle[0]
            print(f"\n{'='*70}")
            print(f"🔄 INITIAL REGIME DETECTION")
            print(f"   Timestamp: {self.current_candle[0]}")
            print(f"   Detected: {new_regime}")
            print(f"{'='*70}\n")

        # Update regime before checking entries
        self._update_regime()

        # Don't enter if we have open position
        if self.position.is_open:
            return False

        # Route to correct strategy
        if self.vars['current_regime'] == 'PARABOLIC':
            result = self._trendfollowing_should_long()
            if result:
                print(f"[DEBUG] PARABOLIC LONG ENTRY @ {self.close}")
            return result
        else:  # VOLATILE
            result = self._multitimeframe_should_long()
            if result:
                print(f"[DEBUG] VOLATILE LONG ENTRY @ {self.close}")
            return result

    def should_short(self) -> bool:
        """Route to appropriate strategy based on current regime"""
        # CRITICAL FIX: Detect regime on FIRST candle
        if self.vars['last_regime_check'] == 0:
            new_regime = self._detect_regime()
            self.vars['current_regime'] = new_regime
            self.vars['last_regime_check'] = self.current_candle[0]
            print(f"\n{'='*70}")
            print(f"🔄 INITIAL REGIME DETECTION")
            print(f"   Timestamp: {self.current_candle[0]}")
            print(f"   Detected: {new_regime}")
            print(f"{'='*70}\n")

        # Update regime before checking entries
        self._update_regime()

        # Don't enter if we have open position
        if self.position.is_open:
            return False

        # Route to correct strategy
        if self.vars['current_regime'] == 'PARABOLIC':
            result = self._trendfollowing_should_short()
            if result:
                print(f"[DEBUG] PARABOLIC SHORT ENTRY @ {self.close}")
            return result
        else:  # VOLATILE
            result = self._multitimeframe_should_short()
            if result:
                print(f"[DEBUG] VOLATILE SHORT ENTRY @ {self.close}")
            return result

    # =================================================================
    # TRENDFOLLOWING v11.2 LOGIC (for PARABOLIC regime)
    # =================================================================

    @property
    def tf_minimum_score(self):
        return 2  # v11.2-RISK

    @property
    def tf_tp_ratio(self):
        return 4.0  # v11.2

    @property
    def tf_be_ratio(self):
        return 2.0  # v11.2

    @property
    def tf_breakout_lookback(self):
        return 20

    @property
    def tf_breakout_threshold(self):
        return 0.01  # 1%

    @property
    def tf_adx_threshold(self):
        return 25

    @property
    def tf_volume_multiplier(self):
        return 1.3

    @property
    def tf_macd_fast(self):
        return 15

    @property
    def tf_macd_slow(self):
        return 30

    @property
    def tf_macd_signal(self):
        return 9

    @property
    def tf_ema_fast(self):
        return 50

    @property
    def tf_min_atr_pct(self):
        return 0.004  # 0.4%

    def _trendfollowing_should_long(self) -> bool:
        """
        TrendFollowing v11.2 COMPLETE entry logic for PARABOLIC markets

        Score system (minimum 2):
        - Breakout (2 points PREMIUM)
        - MACD 1H bullish (2 points PREMIUM)
        - Momentum (1 point)
        - Volume (1 point)
        - ADX trending (1 point)
        """
        # BASIC FILTERS
        # Cooldown
        if self.current_candle[0] - self.vars['last_signal_time'] < 60 * 60 * 1000:
            return False

        # Daily loss limit
        if not self._can_trade_today():
            return False

        # Volatility check
        atr = ta.atr(self.candles, 14)
        if (atr / self.close) < self.tf_min_atr_pct:
            return False

        # Directional filter (prevent conflicts)
        if self.close < self.open:
            return False

        # SCORE SYSTEM
        score = 0

        # 1. BREAKOUT detection (2 points PREMIUM)
        if len(self.candles) >= self.tf_breakout_lookback:
            high_20 = np.max(self.candles[-self.tf_breakout_lookback:, 2])  # High column
            breakout_level = high_20 * (1 + self.tf_breakout_threshold)
            if self.close > breakout_level:
                score += 2

        # 2. MACD 1H bullish (2 points PREMIUM)
        try:
            candles_1h = self.get_candles(self.exchange, self.symbol, '1h')
            if len(candles_1h) >= 100:
                macd, signal, _ = ta.macd(candles_1h, self.tf_macd_fast, self.tf_macd_slow, self.tf_macd_signal)
                if macd > signal and macd > 0:
                    score += 2
        except:
            pass

        # 3. Momentum bullish (1 point)
        ema_50 = ta.ema(self.candles, self.tf_ema_fast)
        if self.close > ema_50:
            score += 1

        # 4. Volume confirmation (1 point)
        if len(self.candles) >= 20:
            avg_volume = np.mean(self.candles[-20:, 5])
            current_volume = self.candles[-1, 5]
            if current_volume > avg_volume * self.tf_volume_multiplier:
                score += 1

        # 5. ADX trending (1 point)
        try:
            adx = ta.adx(self.candles, period=14)
            if adx > self.tf_adx_threshold:
                score += 1
        except:
            pass

        # Check minimum score
        return score >= self.tf_minimum_score

    def _trendfollowing_should_short(self) -> bool:
        """
        TrendFollowing v11.2 COMPLETE entry logic for PARABOLIC markets

        Score system (minimum 2):
        - Breakdown (2 points PREMIUM)
        - MACD 1H bearish (2 points PREMIUM)
        - Momentum (1 point)
        - Volume (1 point)
        - ADX trending (1 point)
        """
        # BASIC FILTERS
        # Cooldown
        if self.current_candle[0] - self.vars['last_signal_time'] < 60 * 60 * 1000:
            return False

        # Daily loss limit
        if not self._can_trade_today():
            return False

        # Volatility check
        atr = ta.atr(self.candles, 14)
        if (atr / self.close) < self.tf_min_atr_pct:
            return False

        # Directional filter (prevent conflicts)
        if self.close > self.open:
            return False

        # SCORE SYSTEM
        score = 0

        # 1. BREAKDOWN detection (2 points PREMIUM)
        if len(self.candles) >= self.tf_breakout_lookback:
            low_20 = np.min(self.candles[-self.tf_breakout_lookback:, 3])  # Low column
            breakdown_level = low_20 * (1 - self.tf_breakout_threshold)
            if self.close < breakdown_level:
                score += 2

        # 2. MACD 1H bearish (2 points PREMIUM)
        try:
            candles_1h = self.get_candles(self.exchange, self.symbol, '1h')
            if len(candles_1h) >= 100:
                macd, signal, _ = ta.macd(candles_1h, self.tf_macd_fast, self.tf_macd_slow, self.tf_macd_signal)
                if macd < signal and macd < 0:
                    score += 2
        except:
            pass

        # 3. Momentum bearish (1 point)
        ema_50 = ta.ema(self.candles, self.tf_ema_fast)
        if self.close < ema_50:
            score += 1

        # 4. Volume confirmation (1 point)
        if len(self.candles) >= 20:
            avg_volume = np.mean(self.candles[-20:, 5])
            current_volume = self.candles[-1, 5]
            if current_volume > avg_volume * self.tf_volume_multiplier:
                score += 1

        # 5. ADX trending (1 point)
        try:
            adx = ta.adx(self.candles, period=14)
            if adx > self.tf_adx_threshold:
                score += 1
        except:
            pass

        # Check minimum score
        return score >= self.tf_minimum_score

    # =================================================================
    # MULTITIMEFRAME v9.3 LOGIC (for VOLATILE regime)
    # =================================================================

    @property
    def mf_rsi_long(self):
        return 36  # v9.3-RSI36

    @property
    def mf_rsi_short(self):
        return 64  # v9.3-RSI36

    @property
    def mf_minimum_score(self):
        return 3  # v9.3

    @property
    def mf_be_ratio(self):
        return 1.35  # v9.3

    @property
    def mf_tp_ratio(self):
        return 3.0  # v9.3

    def _multitimeframe_should_long(self) -> bool:
        """Multitimeframe v9.3 entry logic for VOLATILE markets"""
        # Cooldown
        if self.current_candle[0] - self.vars['last_signal_time'] < 60 * 60 * 1000:
            return False

        # Daily loss limit
        if not self._can_trade_today():
            return False

        # Volatility check
        atr = ta.atr(self.candles, 14)
        atr_pct = atr / self.close
        if atr_pct < 0.004:
            return False

        # SCORE SYSTEM
        score = 0

        # RSI 15M oversold (1 point)
        rsi = ta.rsi(self.candles, 14)
        if rsi < self.mf_rsi_long:
            score += 1

        # MACD 15M bullish (1 point)
        macd, signal, _ = ta.macd(self.candles, 15, 30, 9)
        if macd > signal:
            score += 1

        # MACD 1H bullish (1 point)
        try:
            candles_1h = self.get_candles(self.exchange, self.symbol, '1h')
            if len(candles_1h) >= 50:
                macd_1h, signal_1h, _ = ta.macd(candles_1h, 15, 30, 9)
                if macd_1h > signal_1h:
                    score += 1
        except:
            pass

        # FVG bullish (2 points) - simplified
        if len(self.candles) >= 20:
            for i in range(len(self.candles) - 3, max(len(self.candles) - 20, 2), -1):
                high_old = self.candles[i-2, 3]
                low_new = self.candles[i, 4]
                if high_old < low_new:
                    gap_mid = (low_new + high_old) / 2
                    if abs(self.close - gap_mid) / gap_mid < 0.005:
                        score += 2
                        break

        # Check minimum score
        if score < self.mf_minimum_score:
            return False

        # No enter if RSI in SHORT zone
        if rsi > self.mf_rsi_short:
            return False

        return True

    def _multitimeframe_should_short(self) -> bool:
        """Multitimeframe v9.3 entry logic for VOLATILE markets"""
        # Cooldown
        if self.current_candle[0] - self.vars['last_signal_time'] < 60 * 60 * 1000:
            return False

        # Daily loss limit
        if not self._can_trade_today():
            return False

        # Volatility check
        atr = ta.atr(self.candles, 14)
        atr_pct = atr / self.close
        if atr_pct < 0.004:
            return False

        # SCORE SYSTEM
        score = 0

        # RSI 15M overbought (1 point)
        rsi = ta.rsi(self.candles, 14)
        if rsi > self.mf_rsi_short:
            score += 1

        # MACD 15M bearish (1 point)
        macd, signal, _ = ta.macd(self.candles, 15, 30, 9)
        if macd < signal:
            score += 1

        # MACD 1H bearish (1 point)
        try:
            candles_1h = self.get_candles(self.exchange, self.symbol, '1h')
            if len(candles_1h) >= 50:
                macd_1h, signal_1h, _ = ta.macd(candles_1h, 15, 30, 9)
                if macd_1h < signal_1h:
                    score += 1
        except:
            pass

        # FVG bearish (2 points) - simplified
        if len(self.candles) >= 20:
            for i in range(len(self.candles) - 3, max(len(self.candles) - 20, 2), -1):
                low_old = self.candles[i-2, 4]
                high_new = self.candles[i, 3]
                if low_old > high_new:
                    gap_mid = (low_old + high_new) / 2
                    if abs(self.close - gap_mid) / gap_mid < 0.005:
                        score += 2
                        break

        # Check minimum score
        if score < self.mf_minimum_score:
            return False

        # No enter if RSI in LONG zone
        if rsi < self.mf_rsi_long:
            return False

        return True

    # =================================================================
    # POSITION MANAGEMENT
    # =================================================================

    @property
    def risk_percent(self):
        return 1.0 if self.vars['current_regime'] == 'PARABOLIC' else 1.5

    @property
    def leverage(self):
        return 10 if self.vars['current_regime'] == 'PARABOLIC' else 20

    def go_long(self):
        """Execute LONG entry"""
        atr = ta.atr(self.candles, 14)
        stop_distance = atr * 3.5
        qty = self._calculate_position_size(stop_distance)

        self.buy = qty, self.close

        self.vars['entry_price'] = self.close
        self.vars['sl_price'] = self.close - stop_distance
        self.vars['tp1_hit'] = False
        self.vars['tp2_hit'] = False
        self.vars['initial_risk_distance'] = stop_distance
        self.vars['last_signal_time'] = self.current_candle[0]
        self.vars['highest_price'] = self.close

        self.stop_loss = qty, self.vars['sl_price']

    def go_short(self):
        """Execute SHORT entry"""
        atr = ta.atr(self.candles, 14)
        stop_distance = atr * 3.5
        qty = self._calculate_position_size(stop_distance)

        self.sell = qty, self.close

        self.vars['entry_price'] = self.close
        self.vars['sl_price'] = self.close + stop_distance
        self.vars['tp1_hit'] = False
        self.vars['tp2_hit'] = False
        self.vars['initial_risk_distance'] = stop_distance
        self.vars['last_signal_time'] = self.current_candle[0]
        self.vars['lowest_price'] = self.close

        self.stop_loss = qty, self.vars['sl_price']

    def update_position(self):
        """Manage open position based on current regime"""
        if not self.position.is_open:
            return

        initial_risk = self.vars.get('initial_risk_distance', 0)
        if initial_risk <= 0:
            return

        # Calculate current profit
        if self.is_long:
            current_profit = self.close - self.vars['entry_price']
            if self.close > self.vars['highest_price']:
                self.vars['highest_price'] = self.close
            if self.close <= self.vars['sl_price']:
                self.liquidate()
                return
        else:
            current_profit = self.vars['entry_price'] - self.close
            if self.close < self.vars['lowest_price']:
                self.vars['lowest_price'] = self.close
            if self.close >= self.vars['sl_price']:
                self.liquidate()
                return

        r_ratio = current_profit / initial_risk

        # Use regime-specific parameters
        if self.vars['current_regime'] == 'PARABOLIC':
            # TrendFollowing v11.2 management
            be_ratio = self.tf_be_ratio
            tp_ratio = self.tf_tp_ratio
        else:
            # Multitimeframe v9.3 management
            be_ratio = self.mf_be_ratio
            tp_ratio = self.mf_tp_ratio

        # Break-even
        if r_ratio >= be_ratio and not self.vars['tp1_hit']:
            self.vars['tp1_hit'] = True
            self.vars['sl_price'] = self.vars['entry_price']

        # Take profit
        if r_ratio >= tp_ratio:
            self.liquidate()

    def _calculate_position_size(self, stop_distance):
        """Calculate position size based on risk%"""
        risk_amount = self.balance * (self.risk_percent / 100)
        position_value = risk_amount / (stop_distance / self.close)
        max_position_value = self.balance * self.leverage * 0.9
        position_value = min(position_value, max_position_value)
        qty = position_value / self.close
        return round(qty, 6)

    # =================================================================
    # UTILITY FUNCTIONS
    # =================================================================

    def should_cancel_entry(self) -> bool:
        return False

    @property
    def max_daily_loss_pct(self):
        return 3.0

    def _can_trade_today(self) -> bool:
        """Check if daily loss limit not exceeded"""
        day_key = int(self.current_candle[0] // (24 * 60 * 60 * 1000))
        last_day = self.vars.get('daily_loss_check_day', None)

        if last_day != day_key:
            self.vars['daily_loss_check_day'] = day_key
            self.vars['daily_start_balance'] = self.balance

        daily_start = self.vars.get('daily_start_balance', self.balance)
        if daily_start <= 0:
            return True

        current_balance = self.balance
        daily_loss_pct = ((daily_start - current_balance) / daily_start) * 100

        return daily_loss_pct < self.max_daily_loss_pct
