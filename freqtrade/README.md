# Freqtrade Deployment - v9.3-RSI36 Strategy

This folder contains the Freqtrade adaptation of the v9.3-RSI36 Multitimeframe strategy, originally developed and backtested in the Jesse Trading Framework.

## Strategy Overview

**Multitimeframe_v93_Complete** is a multi-timeframe trading strategy optimized for BTC-USDT.

### Key Parameters
- **Break-Even:** 1.35R (moves SL to entry when 1.35x ATR profit reached)
- **Take Profit:** 3.0R (closes at 3x ATR profit)
- **RSI Long Threshold:** 36
- **RSI Short Threshold:** 64
- **Timeframe:** 15m with 1h/4h confirmations

### Exit Logic (CRITICAL)
The strategy uses `custom_exit()` for ALL exit management, NOT `custom_stoploss()`:

1. **Stop Loss:** Fixed at entry +/- 1 ATR (does NOT trail)
2. **Break-Even:** At 1.35R, SL moves to entry price (ONE TIME ONLY)
3. **Take Profit:** Closes position at 3.0R

This replicates Jesse's `update_position()` behavior exactly.

## Deployment

### 1. Copy Strategy
```bash
scp strategies/Multitimeframe_v93_Complete.py user@server:~/freqtrade/user_data/strategies/
```

### 2. Configuration
Create or update `config.json`:
```json
{
    "strategy": "Multitimeframe_v93_Complete",
    "timeframe": "15m",
    "dry_run": true,
    "dry_run_wallet": 10000,
    "stake_currency": "USDT",
    "stake_amount": "unlimited",
    "tradable_balance_ratio": 0.99,
    "fiat_display_currency": "USD",
    "exchange": {
        "name": "binance",
        "key": "${BINANCE_API_KEY}",
        "secret": "${BINANCE_API_SECRET}",
        "ccxt_config": {},
        "ccxt_async_config": {},
        "pair_whitelist": ["BTC/USDT"]
    },
    "pairlists": [
        {"method": "StaticPairList"}
    ],
    "force_entry_enable": true
}
```

### 3. Start Bot
```bash
freqtrade trade --config config.json --strategy Multitimeframe_v93_Complete
```

## Oracle Cloud Deployment

Current deployment details:
- **Server:** 92.5.17.169:8080
- **API Auth:** freqtrader/freqtrade123
- **Strategy Location:** ~/freqtrade/user_data/strategies/Multitimeframe_v93_Complete.py

### SSH Access
```bash
ssh -i ~/.ssh/oracle_freqtrade.key ubuntu@92.5.17.169
```

### Useful Commands
```bash
# Check bot status
curl -u freqtrader:freqtrade123 http://92.5.17.169:8080/api/v1/status

# View open trades
curl -u freqtrader:freqtrade123 http://92.5.17.169:8080/api/v1/status | jq

# View trade history
curl -u freqtrader:freqtrade123 http://92.5.17.169:8080/api/v1/trades | jq

# Restart bot
pkill -9 -f 'freqtrade trade'
cd ~/freqtrade && freqtrade trade --config user_data/config.json --strategy Multitimeframe_v93_Complete &
```

## Validated Behavior

After fixing the trailing stop issue (see CHANGELOG), the strategy now correctly:

| Trade | Type | Entry | R at Exit | Exit Reason | Status |
|-------|------|-------|-----------|-------------|--------|
| 2 | LONG | 96543 | 3.02R | tp_3.0R_hit | CORRECT |
| 3 | LONG | 102595 | -0.08R | stop_loss_hit (BE) | CORRECT |
| 4 | SHORT | 104166 | -1.03R | stop_loss_hit | CORRECT |
| 5 | LONG | 103393 | -0.05R | stop_loss_hit (BE) | CORRECT |

## Important Notes

1. **DO NOT enable `use_custom_stoploss`** - it creates trailing stop behavior
2. All SL/BE/TP logic is in `custom_exit()` function
3. The `trade_state` dictionary stores ATR and break-even status per trade
4. ATR is captured at entry and NEVER recalculated

## Files

- `strategies/Multitimeframe_v93_Complete.py` - Main strategy file
- `config.example.json` - Example configuration (create from this)
