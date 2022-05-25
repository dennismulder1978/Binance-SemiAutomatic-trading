from Secret import Constants
from Calculations import sma_trade_logic_hourly_oneday, ma, log, buy_sell_action
from binance import Client
from datetime import datetime
import sys

# Command Line Argument
symbol_altcoin = "LUNA"
symbol_base_coin = "BUSD"
pair = "LUNABUSD"

# open connection with api
client = Client(Constants.api_key, Constants.api_secret)

# LUNA - BUSD closing last past 24h hourly
bars = client.get_historical_klines(pair, Client.KLINE_INTERVAL_15MINUTE, "1 day ago UTC")
closing_list = sma_trade_logic_hourly_oneday(bars)

# BUSD free balance
balance_BUSD_dict = client.get_asset_balance(asset=symbol_base_coin)
balance_BUSD = float(balance_BUSD_dict['free'])

# LUNA free balance and price
balance_alt_dict = client.get_asset_balance(asset=symbol_altcoin)
balance_altcoin = float(balance_alt_dict['free'])
prices = client.get_all_tickers()

altcoin_price = 100000000000000000000
for h in prices:
    if h['symbol'] == symbol_altcoin:
        altcoin_price = float(h['price'])
buy_amount = int((0.98 * balance_BUSD) / altcoin_price)  # amount of LUNAs to buy

# Determine the MA's
ma_6 = round(ma(closing_list, 6), 8)
ma_18 = round(ma(closing_list, 18), 8)
print(f'MA6 {pair}: {ma_6}')
print(f'MA18 {pair}: {ma_18}')

# Buy or Sell? that's the question
log_list = []
if (ma_6 >= ma_18) & (balance_altcoin == 0):
    # Buy order
    buy_order = client.order_market_buy(
        symbol=pair,
        quantity=buy_amount)
    log_list.append(f'Buy {symbol_altcoin}-{symbol_base_coin}')
    buy_sell_action("Buy", altcoin_price, buy_amount, datetime.now())
    print('Buy')

elif (ma_6 < ma_18) & (balance_altcoin != 0):
    # sell order
    sell_order = client.order_market_sell(
        symbol=pair,
        quantity=balance_altcoin)
    log_list.append(f'Sell {symbol_altcoin}{symbol_base_coin}')
    buy_sell_action("Sell", altcoin_price, balance_altcoin, datetime.now())
    buy_amount = int(0)
    print('Sell')

else:
    log_list.append('No action')
    buy_amount = int(0)
    print('Do nothing')

# register al off the action
log_list.append(str(buy_amount))
log_list.append(str(altcoin_price))
log_list.append(str(ma_6))
log_list.append(str(ma_18))
log_list.append(str(balance_altcoin))
log_list.append(str(balance_BUSD))
log_list.append(str(datetime.now()))
log(log_list)
