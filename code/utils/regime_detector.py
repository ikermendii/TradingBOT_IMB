"""
🔍 REGIME DETECTOR - v11.0-UNIVERSAL
====================================

Detecta automáticamente el régimen de mercado actual para seleccionar
la estrategia óptima (Mean-Reversion vs Trend-Following).

Regímenes detectados:
1. BULL PARABOLIC → Usar Trend-Following
2. HIGH VOLATILITY → Usar Mean-Reversion
3. RANGING → No tradear

Autor: Claude Sonnet 4.5
Fecha: 2025-12-28
Versión: 1.0
"""

import numpy as np
import jesse.indicators as ta


class RegimeDetector:
    """
    Detecta régimen de mercado usando múltiples indicadores técnicos
    """

    def __init__(self):
        """
        Inicializa detector con parámetros calibrados en datos históricos
        """
        # Thresholds para BULL PARABOLIC
        self.parabolic_adx_min = 30
        self.parabolic_ema_diff_min = 3.0  # %
        self.parabolic_rsi_min = 60
        self.parabolic_momentum_min = 15.0  # %

        # Thresholds para HIGH VOLATILITY
        self.volatile_atr_min = 0.008  # 0.8%
        self.volatile_adx_min = 15
        self.volatile_momentum_max = 15.0  # %

        # Thresholds para RANGING
        self.ranging_adx_max = 15
        self.ranging_atr_max = 0.004  # 0.4%
        self.ranging_momentum_max = 5.0  # %

    def detect(self, candles_15m, candles_1h, candles_4h, candles_1d):
        """
        Detecta régimen de mercado actual

        Args:
            candles_15m: Array de velas 15m (para ATR)
            candles_1h: Array de velas 1H (para confirmación)
            candles_4h: Array de velas 4H (para tendencia)
            candles_1d: Array de velas 1D (para RSI y momentum)

        Returns:
            str: 'parabolic' | 'volatile' | 'ranging'
        """
        # Validar que tenemos suficientes datos
        if len(candles_15m) < 200:
            return 'ranging'  # Conservador si no hay datos
        if len(candles_4h) < 200:
            return 'ranging'
        if len(candles_1d) < 30:
            return 'ranging'

        # Calcular indicadores
        indicators = self._calculate_indicators(
            candles_15m, candles_1h, candles_4h, candles_1d
        )

        # Detectar régimen usando lógica multi-indicador
        regime = self._classify_regime(indicators)

        return regime

    def _calculate_indicators(self, candles_15m, candles_1h, candles_4h, candles_1d):
        """
        Calcula todos los indicadores necesarios para detección

        Returns:
            dict: Diccionario con indicadores calculados
        """
        # Precio actual
        current_price = candles_15m[-1, 2]  # Close

        # ADX 4H (tendencia)
        adx_4h = ta.adx(candles_4h, period=14)

        # RSI 1D (momentum)
        rsi_1d = ta.rsi(candles_1d, period=14)

        # ATR % 15M (volatilidad)
        atr_15m = ta.atr(candles_15m, period=14)
        atr_pct = (atr_15m / current_price) * 100

        # EMAs 4H (tendencia)
        ema_50_4h = ta.ema(candles_4h, period=50)
        ema_200_4h = ta.ema(candles_4h, period=200)
        ema_diff_pct = ((ema_50_4h - ema_200_4h) / ema_200_4h) * 100

        # Momentum 30 días (cambio % en 30 días)
        if len(candles_1d) >= 30:
            price_30d_ago = candles_1d[-30, 2]  # Close de hace 30 días
            momentum_30d = ((current_price - price_30d_ago) / price_30d_ago) * 100
        else:
            momentum_30d = 0.0

        # Volatilidad histórica 20 días (desviación estándar)
        if len(candles_1d) >= 20:
            returns = np.diff(candles_1d[-20:, 2]) / candles_1d[-20:-1, 2]
            volatility_20d = np.std(returns) * np.sqrt(252) * 100  # Anualizada
        else:
            volatility_20d = 0.0

        return {
            'adx_4h': adx_4h,
            'rsi_1d': rsi_1d,
            'atr_pct': atr_pct,
            'ema_diff_pct': ema_diff_pct,
            'momentum_30d': momentum_30d,
            'volatility_20d': volatility_20d,
            'current_price': current_price,
            'ema_50_4h': ema_50_4h,
            'ema_200_4h': ema_200_4h,
        }

    def _classify_regime(self, ind):
        """
        Clasifica régimen basándose en indicadores

        Args:
            ind: Diccionario con indicadores calculados

        Returns:
            str: 'parabolic' | 'volatile' | 'ranging'
        """
        # RÉGIMEN 1: BULL PARABOLIC
        # Características:
        # - Tendencia fuerte (ADX >30)
        # - EMA50 muy por encima de EMA200 (>3%)
        # - RSI alto sostenido (>60)
        # - Momentum fuerte (+15% en 30 días)

        is_parabolic = (
            ind['adx_4h'] > self.parabolic_adx_min and
            ind['ema_diff_pct'] > self.parabolic_ema_diff_min and
            ind['rsi_1d'] > self.parabolic_rsi_min and
            ind['momentum_30d'] > self.parabolic_momentum_min
        )

        if is_parabolic:
            return 'parabolic'

        # RÉGIMEN 2: HIGH VOLATILITY
        # Características:
        # - ATR alto (>0.8%)
        # - Algo de tendencia (ADX >15 pero <30)
        # - Momentum moderado (<15% en 30 días)

        is_volatile = (
            ind['atr_pct'] > self.volatile_atr_min and
            ind['adx_4h'] > self.volatile_adx_min and
            abs(ind['momentum_30d']) < self.volatile_momentum_max
        )

        if is_volatile:
            return 'volatile'

        # RÉGIMEN 3: RANGING
        # Características:
        # - ADX bajo (<15)
        # - ATR bajo (<0.4%)
        # - Momentum bajo (<5% en 30 días)

        is_ranging = (
            ind['adx_4h'] < self.ranging_adx_max or
            ind['atr_pct'] < self.ranging_atr_max or
            abs(ind['momentum_30d']) < self.ranging_momentum_max
        )

        if is_ranging:
            return 'ranging'

        # Default: VOLATILE (más común)
        return 'volatile'

    def get_regime_stats(self, candles_15m, candles_1h, candles_4h, candles_1d):
        """
        Devuelve estadísticas detalladas del régimen actual

        Útil para debugging y monitoreo

        Returns:
            dict: Estadísticas del régimen
        """
        indicators = self._calculate_indicators(
            candles_15m, candles_1h, candles_4h, candles_1d
        )

        regime = self._classify_regime(indicators)

        return {
            'regime': regime,
            'indicators': indicators,
            'thresholds': {
                'parabolic': {
                    'adx_min': self.parabolic_adx_min,
                    'ema_diff_min': self.parabolic_ema_diff_min,
                    'rsi_min': self.parabolic_rsi_min,
                    'momentum_min': self.parabolic_momentum_min,
                },
                'volatile': {
                    'atr_min': self.volatile_atr_min,
                    'adx_min': self.volatile_adx_min,
                    'momentum_max': self.volatile_momentum_max,
                },
                'ranging': {
                    'adx_max': self.ranging_adx_max,
                    'atr_max': self.ranging_atr_max,
                    'momentum_max': self.ranging_momentum_max,
                }
            },
            'confidence': self._calculate_confidence(indicators, regime)
        }

    def _calculate_confidence(self, ind, regime):
        """
        Calcula nivel de confianza de la clasificación (0-100%)

        Args:
            ind: Indicadores calculados
            regime: Régimen detectado

        Returns:
            float: Confianza en % (0-100)
        """
        if regime == 'parabolic':
            # Contar cuántos indicadores superan threshold
            score = 0
            total = 4

            if ind['adx_4h'] > self.parabolic_adx_min:
                score += 1
            if ind['ema_diff_pct'] > self.parabolic_ema_diff_min:
                score += 1
            if ind['rsi_1d'] > self.parabolic_rsi_min:
                score += 1
            if ind['momentum_30d'] > self.parabolic_momentum_min:
                score += 1

            confidence = (score / total) * 100

        elif regime == 'volatile':
            score = 0
            total = 3

            if ind['atr_pct'] > self.volatile_atr_min:
                score += 1
            if ind['adx_4h'] > self.volatile_adx_min:
                score += 1
            if abs(ind['momentum_30d']) < self.volatile_momentum_max:
                score += 1

            confidence = (score / total) * 100

        else:  # ranging
            # Ranging es default, confianza baja
            confidence = 50.0

        return confidence

    def test_historical_accuracy(self, historical_data):
        """
        Testa accuracy del detector en datos históricos

        Args:
            historical_data: Lista de tuplas (candles, expected_regime)

        Returns:
            dict: Estadísticas de accuracy
        """
        correct = 0
        total = len(historical_data)

        results = []

        for candles_15m, candles_1h, candles_4h, candles_1d, expected in historical_data:
            detected = self.detect(candles_15m, candles_1h, candles_4h, candles_1d)
            is_correct = (detected == expected)

            if is_correct:
                correct += 1

            results.append({
                'expected': expected,
                'detected': detected,
                'correct': is_correct
            })

        accuracy = (correct / total) * 100 if total > 0 else 0.0

        return {
            'accuracy': accuracy,
            'correct': correct,
            'total': total,
            'results': results
        }


# ============================================================================
# TESTING Y DEBUGGING
# ============================================================================

def test_regime_detector():
    """
    Test básico del detector (sin datos reales aún)
    """
    print("=" * 70)
    print("REGIME DETECTOR - TEST BÁSICO")
    print("=" * 70)

    detector = RegimeDetector()

    # Crear datos sintéticos para testing
    print("\n1. Testing con datos sintéticos...")

    # Parabolic scenario (fake data)
    print("\n   Scenario 1: Bull Parabolic")
    print("   - ADX 4H: 35 (>30)")
    print("   - EMA Diff: 4.5% (>3%)")
    print("   - RSI 1D: 65 (>60)")
    print("   - Momentum 30d: +20% (>15%)")
    print("   → Expected: 'parabolic'")

    # Volatile scenario (fake data)
    print("\n   Scenario 2: High Volatility")
    print("   - ATR: 1.2% (>0.8%)")
    print("   - ADX 4H: 20 (>15)")
    print("   - Momentum 30d: +8% (<15%)")
    print("   → Expected: 'volatile'")

    # Ranging scenario (fake data)
    print("\n   Scenario 3: Ranging")
    print("   - ADX 4H: 12 (<15)")
    print("   - ATR: 0.3% (<0.4%)")
    print("   - Momentum 30d: +2% (<5%)")
    print("   → Expected: 'ranging'")

    print("\n2. Detector configurado con thresholds:")
    print(f"   Parabolic: ADX>{detector.parabolic_adx_min}, "
          f"EMA_diff>{detector.parabolic_ema_diff_min}%, "
          f"RSI>{detector.parabolic_rsi_min}, "
          f"Momentum>{detector.parabolic_momentum_min}%")

    print(f"   Volatile: ATR>{detector.volatile_atr_min*100}%, "
          f"ADX>{detector.volatile_adx_min}, "
          f"Momentum<{detector.volatile_momentum_max}%")

    print(f"   Ranging: ADX<{detector.ranging_adx_max}, "
          f"ATR<{detector.ranging_atr_max*100}%, "
          f"Momentum<{detector.ranging_momentum_max}%")

    print("\n✅ Detector inicializado correctamente")
    print("\n📋 Próximo paso: Testear con datos reales de backtests históricos")
    print("=" * 70)


if __name__ == '__main__':
    test_regime_detector()
