#!/usr/bin/env python3
"""
🔍 Market Regime Monitor for v9.3-RSI36
==========================================

Detects if market regime is changing from:
- FAVORABLE: High volatility (2022-2025 style) → Bot performs EXCELLENT
- DANGEROUS: Parabolic bull (2020-2021 style) → Bot will FAIL

Run this script WEEKLY to monitor regime health.

Author: Claude Code
Version: 1.0
Date: 2025-12-27
"""

import ccxt
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys

def print_header():
    """Print monitoring header"""
    print("=" * 70)
    print("🔍 MARKET REGIME MONITOR - v9.3-RSI36".center(70))
    print("=" * 70)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    print()

def fetch_btc_data(days=90):
    """Fetch BTC/USDT daily candles from Binance"""
    try:
        exchange = ccxt.binance()
        candles = exchange.fetch_ohlcv('BTC/USDT', '1d', limit=days)
        df = pd.DataFrame(candles, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df
    except Exception as e:
        print(f"❌ Error fetching data: {e}")
        sys.exit(1)

def calculate_atr_pct(df, period=14):
    """Calculate ATR as percentage of close"""
    df['tr'] = df['high'] - df['low']
    df['atr'] = df['tr'].rolling(period).mean()
    df['atr_pct'] = (df['atr'] / df['close']) * 100
    return df

def calculate_metrics(df, period_days=30):
    """Calculate regime metrics for given period"""
    df_period = df.tail(period_days).copy()

    # ATR% average
    atr_avg = df_period['atr_pct'].mean()

    # Max pullback (peak to trough)
    high_max = df_period['high'].max()
    low_min = df_period['low'].min()
    # Find if low came after high
    high_idx = df_period['high'].idxmax()
    low_after_high = df_period.loc[high_idx:, 'low'].min()
    pullback = ((low_after_high - high_max) / high_max) * 100 if low_after_high < high_max else 0

    # BTC % change
    btc_change = ((df_period['close'].iloc[-1] - df_period['close'].iloc[0]) / df_period['close'].iloc[0]) * 100

    # Current BTC price
    btc_price = df_period['close'].iloc[-1]

    return {
        'atr_avg': atr_avg,
        'pullback': pullback,
        'btc_change': btc_change,
        'btc_price': btc_price
    }

def assess_regime(metrics_30d, metrics_60d):
    """Assess current market regime"""

    # Thresholds
    ATR_FAVORABLE = 0.6
    ATR_WARNING = 0.5
    ATR_CRITICAL = 0.4

    PULLBACK_HEALTHY = -8.0

    BTC_CHANGE_WARNING = 30.0  # +30% in 30d without pullback
    BTC_CHANGE_CRITICAL = 50.0  # +50% in 60d without pullback

    alerts = []
    status = "FAVORABLE"  # Default

    # Check ATR (most important)
    if metrics_30d['atr_avg'] >= ATR_FAVORABLE:
        atr_status = "✅ FAVORABLE"
    elif metrics_30d['atr_avg'] >= ATR_WARNING:
        atr_status = "⚠️ WARNING"
        alerts.append("⚠️ ATR declining - Monitor closely")
        status = "WARNING"
    else:
        atr_status = "🔴 CRITICAL"
        alerts.append("🔴 ATR very low - Possible parabolic regime")
        status = "CRITICAL"

    # Check pullback
    if metrics_30d['pullback'] <= PULLBACK_HEALTHY:
        pullback_status = "✅ Healthy"
    else:
        pullback_status = "⚠️ Shallow"
        if metrics_30d['btc_change'] > BTC_CHANGE_WARNING:
            alerts.append("⚠️ Strong trend without deep pullbacks")

    # Check parabolic trend
    if metrics_30d['btc_change'] > BTC_CHANGE_WARNING and metrics_30d['pullback'] > PULLBACK_HEALTHY:
        alerts.append("🔴 Parabolic trend detected - Regime may be changing")
        status = "CRITICAL"

    if metrics_60d['btc_change'] > BTC_CHANGE_CRITICAL and metrics_60d['pullback'] > -10:
        alerts.append("🔴 Extended parabolic trend (60d) - HIGH RISK of regime change")
        status = "CRITICAL"

    return {
        'status': status,
        'atr_status': atr_status,
        'pullback_status': pullback_status,
        'alerts': alerts
    }

def print_metrics(metrics, period_name):
    """Print metrics for a period"""
    print(f"\n{period_name}:")
    print(f"  BTC Price:         ${metrics['btc_price']:,.2f}")
    print(f"  BTC Change:        {metrics['btc_change']:+.2f}%")
    print(f"  ATR% (avg):        {metrics['atr_avg']:.3f}%")
    print(f"  Max Pullback:      {metrics['pullback']:.2f}%")

def print_assessment(assessment):
    """Print regime assessment"""
    print("\n" + "=" * 70)
    print("REGIME ASSESSMENT".center(70))
    print("=" * 70)

    # Status color coding
    if assessment['status'] == "FAVORABLE":
        status_icon = "✅"
        status_msg = "Bot should perform EXCELLENT"
    elif assessment['status'] == "WARNING":
        status_icon = "⚠️"
        status_msg = "Monitor closely for regime change"
    else:  # CRITICAL
        status_icon = "🔴"
        status_msg = "HIGH RISK - Consider pausing bot"

    print(f"\n{status_icon} Overall Status: {assessment['status']}")
    print(f"   → {status_msg}")

    print(f"\n📊 Indicators:")
    print(f"   ATR% Level:     {assessment['atr_status']}")
    print(f"   Pullback:       {assessment['pullback_status']}")

    # Alerts
    if assessment['alerts']:
        print(f"\n⚠️ ALERTS ({len(assessment['alerts'])}):")
        for alert in assessment['alerts']:
            print(f"   {alert}")
    else:
        print(f"\n✅ No alerts - Regime is FAVORABLE for v9.3-RSI36")

def print_recommendations(assessment):
    """Print actionable recommendations"""
    print("\n" + "=" * 70)
    print("RECOMMENDATIONS".center(70))
    print("=" * 70)

    if assessment['status'] == "FAVORABLE":
        print("""
✅ CONTINUE TRADING
   - Market regime is favorable for v9.3-RSI36
   - High volatility supports BE=1.35R and TP=3.0R
   - Continue normal monitoring

📋 Actions:
   - Continue trading as normal
   - Run this monitor again next week
   - Monitor daily drawdown and win rate
        """)

    elif assessment['status'] == "WARNING":
        print("""
⚠️ MONITOR CLOSELY
   - Market regime showing early signs of change
   - Not critical yet, but watch for deterioration
   - Increased monitoring recommended

📋 Actions:
   - Run this monitor DAILY (not weekly)
   - Check bot performance daily (win rate, DD)
   - Prepare to pause if status becomes CRITICAL
   - Review last 20 trades for patterns (many BE exits?)
        """)

    else:  # CRITICAL
        print("""
🔴 CONSIDER PAUSING BOT
   - Market regime may be changing to parabolic (2020-2021 style)
   - v9.3-RSI36 is NOT optimized for this regime
   - HIGH RISK of significant losses

📋 IMMEDIATE Actions:
   1. ⏸️ PAUSE trading (do NOT wait)
   2. 📊 Analyze last 50 trades:
      - How many closed in BE? (if >30%, regime changed)
      - Win rate trending down?
      - Losing streak >15?
   3. 📈 Confirm with BTC chart:
      - Is BTC in parabolic uptrend?
      - Low volatility, smooth trend up?
   4. ✅ Decision:
      - If regime changed → STOP, wait for v10.0-ROBUST
      - If uncertain → Pause 1 week, re-run monitor
      - If false alarm → Resume with DAILY monitoring
        """)

    print("\n" + "=" * 70)

def main():
    """Main monitoring function"""
    print_header()

    print("📡 Fetching BTC/USDT data from Binance...")
    df = fetch_btc_data(days=90)
    print(f"✅ Fetched {len(df)} daily candles")

    print("\n📊 Calculating metrics...")
    df = calculate_atr_pct(df)

    # Calculate for different periods
    metrics_30d = calculate_metrics(df, period_days=30)
    metrics_60d = calculate_metrics(df, period_days=60)

    # Print metrics
    print_metrics(metrics_30d, "📅 Last 30 Days")
    print_metrics(metrics_60d, "📅 Last 60 Days")

    # Assess regime
    assessment = assess_regime(metrics_30d, metrics_60d)

    # Print assessment
    print_assessment(assessment)

    # Print recommendations
    print_recommendations(assessment)

    print("\n" + "=" * 70)
    print(f"Monitor completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Next run: 1 week (or DAILY if status is WARNING/CRITICAL)")
    print("=" * 70)

    # Exit code based on status
    if assessment['status'] == "CRITICAL":
        sys.exit(2)  # Critical status
    elif assessment['status'] == "WARNING":
        sys.exit(1)  # Warning status
    else:
        sys.exit(0)  # All good

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Monitoring cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
