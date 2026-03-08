import sqlite3
import sys

db_path = sys.argv[1] if len(sys.argv) > 1 else '/home/ubuntu/freqtrade/tradesv3.dryrun.sqlite'
conn = sqlite3.connect(db_path)
c = conn.cursor()

q = """SELECT strftime('%W', open_date) as week, COUNT(*),
       SUM(CASE WHEN close_profit > 0 THEN 1 ELSE 0 END),
       ROUND(SUM(close_profit_abs),2)
       FROM trades WHERE is_open = 0 GROUP BY week ORDER BY week"""
c.execute(q)
print('=== TRADES POR SEMANA ===')
print('Semana | Trades | Wins | Profit USDT')
for r in c.fetchall():
    wr = (r[2]/r[1]*100) if r[1]>0 else 0
    print(f'  W{r[0]}   |   {r[1]:3}  |  {r[2]:2}  | {r[3]:>9} ({wr:.0f}% WR)')

c.execute('SELECT COUNT(*), SUM(CASE WHEN close_profit > 0 THEN 1 ELSE 0 END) FROM trades WHERE is_open = 0')
total, wins = c.fetchone()
losses = total - (wins or 0)

c.execute('SELECT id, close_profit_abs FROM trades WHERE is_open = 0 ORDER BY close_date')
cumulative = 0
milestones = []
for r in c.fetchall():
    cumulative += r[1]
    if r[0] % 25 == 0 or r[0] == total:
        milestones.append((r[0], cumulative))
print(f'\n=== PROFIT ACUMULADO ===')
for m in milestones:
    print(f'  Trade #{m[0]}: {m[1]:.2f} USDT')

c.execute('SELECT id, pair, open_date, close_date, exit_reason, close_profit*100 FROM trades WHERE is_open = 0 ORDER BY close_date DESC LIMIT 5')
print(f'\n=== ULTIMOS 5 TRADES ===')
for r in c.fetchall():
    print(f'  #{r[0]} {r[1]} | {r[4]} | {r[5]:.2f}%')

c.execute('SELECT AVG(CASE WHEN close_profit > 0 THEN close_profit END)*100, AVG(CASE WHEN close_profit <= 0 THEN close_profit END)*100 FROM trades WHERE is_open = 0')
r = c.fetchone()
avg_win = r[0]
avg_loss = r[1]
wr = wins/total if total > 0 else 0
exp = wr * avg_win + (1-wr) * avg_loss
be_wr = abs(avg_loss)/(avg_win+abs(avg_loss))*100

print(f'\n=== EXPECTATIVA MATEMATICA ===')
print(f'Avg Win: +{avg_win:.2f}%')
print(f'Avg Loss: {avg_loss:.2f}%')
print(f'Ratio Win/Loss: {avg_win/abs(avg_loss):.2f}')
print(f'Win Rate actual: {wr*100:.1f}%')
print(f'Expectativa por trade: {exp:.4f}%')
print(f'WR minimo breakeven: {be_wr:.1f}%')
print(f'Jesse backtest WR esperado: 25.14%')
if wr*100 < be_wr:
    print(f'>> PROBLEMA: WR actual ({wr*100:.1f}%) < breakeven ({be_wr:.1f}%)')
