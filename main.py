from Secret import Constants
from Calculations import sma_trade_logic_hourly_oneday, ma, log
from binance import Client
from datetime import datetime


# open connection with api
client = Client(Constants.api_key, Constants.api_secret)

# LUNA - BUSD closing last past 24h hourly
bars = client.get_historical_klines('LUNABUSD', Client.KLINE_INTERVAL_1HOUR, "1 day ago UTC")
closing_list = sma_trade_logic_hourly_oneday(bars)

# BUSD free balance
balance_BUSD_dict = client.get_asset_balance(asset='BUSD')
balance_BUSD = float(balance_BUSD_dict['free'])

# LUNA
balance_LUNA_dict = client.get_asset_balance(asset='LUNA')
balance_LUNA = float(balance_LUNA_dict['free'])
prices = client.get_all_tickers()

LUNA_price = 1000000000000
for h in prices:
    if h['symbol'] == "LUNABUSD":
        LUNA_price = float(h['price'])
buy_amount = int((0.98 * balance_BUSD) / LUNA_price)

# Determine the MA's
ma_6 = round(ma(closing_list, 6), 8)
ma_18 = round(ma(closing_list, 18), 8)

# Buy or Sell? that's the question
log_list = []
if (ma_6 >= ma_18) & (balance_LUNA == 0):
    # Buy order
    buy_order = client.order_market_buy(
        symbol='LUNABUSD',
        quantity=buy_amount)
    log_list.append('Buy LUNA')
elif (ma_6 > ma_18) & (balance_LUNA != 0):
    # sell order
    sell_order = client.order_market_sell(
        symbol='LUNABUSD',
        quantity=balance_LUNA)
    log_list.append('Sell LUNA')
    buy_amount = int(0)
else:
    log_list.append('No action')
    buy_amount = int(0)


# register al off the action
log_list.append(str(buy_amount))
log_list.append(str(LUNA_price))
log_list.append(str(ma_6))
log_list.append(str(ma_18))
log_list.append(str(balance_LUNA))
log_list.append(str(balance_BUSD))
log_list.append(str(datetime.now()))
log(log_list)
