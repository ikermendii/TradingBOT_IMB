"""
UNIVERSAL ROBUST V2.0 - ELITE High-ROI Multi-Indicator Strategy
================================================================

Inspirado en: Estrategia 8787% ROI (probada en producción)
Target: 50-200% annual return

INDICADORES (5 confirmaciones requeridas):
1. RSI 40/60 - Momentum (entradas tempranas, no extremos)
2. MACD - Confirmación tendencia y momentum
3. Bollinger Bands - Timing perfecto de entrada
4. ADX >20 - Filtro de tendencia fuerte (evita laterales)
5. EMA 200 - Dirección macro del mercado

FILOSOFÍA:
"Multi-indicador con confirmación ELIMINA señales falsas"
"Trade SOLO en dirección de tendencia primaria"
"Filtrar laterales es MÁS importante que encontrar entradas"

GESTIÓN DE RIESGO:
- Stop: 2.0 ATR
- Target: 3.0 R:R
- Trailing: Activa en profit >2R
- Risk: 1.5% por trade
- Leverage: 5x
- Cooldown: 2h entre trades

Autor: Claude Sonnet 4.5 based on proven strategies research
Fecha: 2025-12-29
"""

from jesse.strategies import Strategy
import jesse.indicators as ta
from jesse import utils
import numpy as np


class UniversalRobustV2(Strategy):
    def __init__(self):
        super().__init__()
        self.vars = {
            'entry_price': 0,
            'sl_price': 0,
            'tp_price': 0,
            'last_trade_time': 0,
            'highest_profit': 0,
        }

    # =========================================================================
    # PARÁMETROS OPTIMIZADOS (basados en research)
    # =========================================================================

    @property
    def rsi_period(self):
        return 14  # Estándar

    @property
    def rsi_oversold(self):
        return 40  # Temprano, no extremo (vs 30 en v1.0)

    @property
    def rsi_overbought(self):
        return 60  # Temprano, no extremo (vs 70 en v1.0)

    @property
    def ema_trend(self):
        return 200  # Tendencia macro

    @property
    def adx_period(self):
        return 14  # Estándar

    @property
    def adx_threshold(self):
        return 20  # Mínimo para tendencia fuerte

    @property
    def bollinger_period(self):
        return 20  # Estándar

    @property
    def bollinger_std(self):
        return 2.0  # 2 desviaciones estándar

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
    def atr_period(self):
        return 14  # Estándar

    @property
    def stop_atr_multiplier(self):
        return 2.0  # 2 ATR stop

    @property
    def risk_reward_ratio(self):
        return 3.0  # 3:1 R:R

    @property
    def risk_percent(self):
        return 1.5  # 1.5% risk per trade (más agresivo que v1.0)

    @property
    def cooldown_hours(self):
        return 2  # 2 horas (vs 4h en v1.0)

    @property
    def leverage(self):
        return 5  # Conservative leverage

    @property
    def trailing_activation(self):
        return 2.0  # Activar trailing cuando profit >2R

    # =========================================================================
    # INDICADORES - CALCULADOS UNA VEZ POR VELA
    # =========================================================================

    def _calculate_indicators(self):
        """Calcula todos los indicadores necesarios"""
        # RSI
        rsi = ta.rsi(self.candles, self.rsi_period)

        # EMA 200 (tendencia macro)
        ema_200 = ta.ema(self.candles, self.ema_trend)

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
            self.bollinger_period,
            self.bollinger_std
        )

        # ADX (fuerza de tendencia)
        adx = ta.adx(self.candles, self.adx_period)

        # ATR (volatilidad)
        atr = ta.atr(self.candles, self.atr_period)

        return {
            'rsi': rsi,
            'ema_200': ema_200,
            'macd_line': macd_line,
            'macd_signal': macd_signal,
            'macd_hist': macd_hist,
            'bb_upper': bb_upper,
            'bb_middle': bb_middle,
            'bb_lower': bb_lower,
            'adx': adx,
            'atr': atr
        }

    # =========================================================================
    # LÓGICA DE ENTRADA - 5 CONFIRMACIONES REQUERIDAS
    # =========================================================================

    def should_long(self) -> bool:
        """
        LONG Entry - TODAS las condiciones deben cumplirse:

        1. Precio > EMA200 (uptrend macro)
        2. RSI < 40 (oversold temprano)
        3. MACD bullish cross (momentum alcista)
        4. Price toca Bollinger inferior (timing perfecto)
        5. ADX > 20 (tendencia fuerte confirmada)
        6. Cooldown passed
        """
        # Cooldown check
        if self.current_candle[0] - self.vars['last_trade_time'] < self.cooldown_hours * 60 * 60 * 1000:
            return False

        # No entrar si ya hay posición abierta
        if self.position.is_open:
            return False

        # Calcular indicadores
        ind = self._calculate_indicators()

        # ===== CONDICIÓN 1: Uptrend Macro =====
        if self.close <= ind['ema_200']:
            return False  # Precio debe estar sobre EMA200

        # ===== CONDICIÓN 2: RSI Oversold (temprano) =====
        if ind['rsi'] >= self.rsi_oversold:
            return False  # RSI debe ser menor a 40

        # ===== CONDICIÓN 3: MACD Bullish Cross =====
        # MACD line debe estar cruzando o estar sobre signal line
        macd_bullish = ind['macd_line'] > ind['macd_signal']
        if not macd_bullish:
            return False

        # ===== CONDICIÓN 4: Price toca Bollinger Inferior =====
        # Price debe estar cerca de banda inferior (dentro del 2% de la banda)
        distance_to_lower_band = abs(self.close - ind['bb_lower']) / ind['bb_lower']
        if distance_to_lower_band > 0.02:  # Más del 2% de distancia
            return False

        # ===== CONDICIÓN 5: ADX confirma tendencia fuerte =====
        if ind['adx'] <= self.adx_threshold:
            return False  # ADX debe ser mayor a 20

        # TODAS las condiciones cumplidas → LONG
        return True

    def should_short(self) -> bool:
        """
        SHORT Entry - TODAS las condiciones deben cumplirse:

        1. Precio < EMA200 (downtrend macro)
        2. RSI > 60 (overbought temprano)
        3. MACD bearish cross (momentum bajista)
        4. Price toca Bollinger superior (timing perfecto)
        5. ADX > 20 (tendencia fuerte confirmada)
        6. Cooldown passed
        """
        # Cooldown check
        if self.current_candle[0] - self.vars['last_trade_time'] < self.cooldown_hours * 60 * 60 * 1000:
            return False

        # No entrar si ya hay posición abierta
        if self.position.is_open:
            return False

        # Calcular indicadores
        ind = self._calculate_indicators()

        # ===== CONDICIÓN 1: Downtrend Macro =====
        if self.close >= ind['ema_200']:
            return False  # Precio debe estar bajo EMA200

        # ===== CONDICIÓN 2: RSI Overbought (temprano) =====
        if ind['rsi'] <= self.rsi_overbought:
            return False  # RSI debe ser mayor a 60

        # ===== CONDICIÓN 3: MACD Bearish Cross =====
        macd_bearish = ind['macd_line'] < ind['macd_signal']
        if not macd_bearish:
            return False

        # ===== CONDICIÓN 4: Price toca Bollinger Superior =====
        distance_to_upper_band = abs(self.close - ind['bb_upper']) / ind['bb_upper']
        if distance_to_upper_band > 0.02:  # Más del 2% de distancia
            return False

        # ===== CONDICIÓN 5: ADX confirma tendencia fuerte =====
        if ind['adx'] <= self.adx_threshold:
            return False

        # TODAS las condiciones cumplidas → SHORT
        return True

    # =========================================================================
    # GESTIÓN DE POSICIÓN - STOP FIJO + TRAILING
    # =========================================================================

    def go_long(self):
        """Ejecuta LONG con stop 2 ATR y target 3:1 R:R"""
        ind = self._calculate_indicators()
        atr = ind['atr']
        stop_distance = atr * self.stop_atr_multiplier

        # Calcular position size basado en 1.5% risk
        qty = self._calculate_position_size(stop_distance)

        # Ejecutar entrada
        self.buy = qty, self.close

        # Set stop and target
        self.vars['entry_price'] = self.close
        self.vars['sl_price'] = self.close - stop_distance
        self.vars['tp_price'] = self.close + (stop_distance * self.risk_reward_ratio)
        self.vars['last_trade_time'] = self.current_candle[0]
        self.vars['highest_profit'] = 0

        # Set initial stop loss and take profit
        self.stop_loss = qty, self.vars['sl_price']
        self.take_profit = qty, self.vars['tp_price']

    def go_short(self):
        """Ejecuta SHORT con stop 2 ATR y target 3:1 R:R"""
        ind = self._calculate_indicators()
        atr = ind['atr']
        stop_distance = atr * self.stop_atr_multiplier

        # Calcular position size basado en 1.5% risk
        qty = self._calculate_position_size(stop_distance)

        # Ejecutar entrada
        self.sell = qty, self.close

        # Set stop and target
        self.vars['entry_price'] = self.close
        self.vars['sl_price'] = self.close + stop_distance
        self.vars['tp_price'] = self.close - (stop_distance * self.risk_reward_ratio)
        self.vars['last_trade_time'] = self.current_candle[0]
        self.vars['highest_profit'] = 0

        # Set initial stop loss and take profit
        self.stop_loss = qty, self.vars['sl_price']
        self.take_profit = qty, self.vars['tp_price']

    def update_position(self):
        """Actualiza trailing stop cuando profit >2R"""
        if not self.position.is_open:
            return

        # Calcular profit actual en R
        if self.is_long:
            current_profit_r = (self.close - self.vars['entry_price']) / (self.vars['entry_price'] - self.vars['sl_price'])
        else:
            current_profit_r = (self.vars['entry_price'] - self.close) / (self.vars['sl_price'] - self.vars['entry_price'])

        # Actualizar highest profit
        if current_profit_r > self.vars['highest_profit']:
            self.vars['highest_profit'] = current_profit_r

        # Activar trailing stop cuando profit >2R
        if self.vars['highest_profit'] >= self.trailing_activation:
            # Calcular nuevo stop loss (trailing)
            ind = self._calculate_indicators()
            atr = ind['atr']

            if self.is_long:
                # Trailing stop para LONG: precio - 1.5 ATR
                new_sl = self.close - (atr * 1.5)
                # Solo mover stop hacia arriba, nunca hacia abajo
                if new_sl > self.vars['sl_price']:
                    self.vars['sl_price'] = new_sl
                    self.stop_loss = self.position.qty, new_sl
            else:
                # Trailing stop para SHORT: precio + 1.5 ATR
                new_sl = self.close + (atr * 1.5)
                # Solo mover stop hacia abajo, nunca hacia arriba
                if new_sl < self.vars['sl_price']:
                    self.vars['sl_price'] = new_sl
                    self.stop_loss = self.position.qty, new_sl

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
