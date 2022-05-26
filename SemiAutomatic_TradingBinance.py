from Secret import Constants
from Calculations import ma_trade_logic, ma, log, buy_sell_action_log
from binance import Client
from datetime import datetime
import sys

# Command Line Argument
arg_list = sys.argv
symbol_altcoin = "LUNA"  # default altcoin
symbol_basecoin = "BUSD"  # default basecoin
try:
    symbol_altcoin = str(arg_list[1])
    symbol_basecoin = str(arg_list[2])
except IndexError:
    pass
pair = str(symbol_altcoin + symbol_basecoin)

# open connection with api, collect coins data
client = Client(Constants.api_key, Constants.api_secret)
closing_list = ma_trade_logic(
    client.get_historical_klines(pair, Client.KLINE_INTERVAL_5MINUTE, "1 day ago UTC"))
prices = client.get_all_tickers()

# basecoin and altcoin free balance
balance_basecoin_dict = client.get_asset_balance(asset=symbol_basecoin)
balance_basecoin = float(balance_basecoin_dict['free'])
balance_alt_dict = client.get_asset_balance(asset=symbol_altcoin)
balance_altcoin = float(balance_alt_dict['free'])

# ALT-BASE price
altcoin_price = 100000000000000000000  # alternative price
for each in prices:
    if each['symbol'] == pair:
        altcoin_price = float(each['price'])

# Determine the MA's
ma_6 = round(ma(closing_list, 12 * 6), 8)  # use 12* (6 hours) b.o. 5min interval
ma_18 = round(ma(closing_list, 12 * 18), 8)  # use 12 * (18 hours) b.o. 5min interval
print(f'MA-6 {pair}: {ma_6}')
print(f'MA-18 {pair}: {ma_18}')

# Buy or Sell? that's the question
log_list = []
buy_amount = int(0)
if (ma_6 >= ma_18) & (balance_altcoin == 0) & (balance_basecoin != 0):  # Buy order
    try:
        buy_amount = 0.99 * balance_basecoin  # amount of BASEcoin to spend, ie 99%
        buy_order = client.order_market_buy(symbol=pair, quoteOrderQty=buy_amount)
        log_list.append('Buy')
        buy_sell_action_log(f'Buy,{pair},{altcoin_price},BASEcoin {buy_amount},{datetime.now()},none')
        print('Action = Buy')
    except Exception as e:
        buy_sell_action_log(f'Buy failed,{pair},{altcoin_price},BASEcoin {buy_amount},{datetime.now()},{e}')
        log_list.append('Buy failed')
        print('Buy failed')

elif (ma_6 < ma_18) & (balance_altcoin != 0):  # sell order
    try:
        sell_order = client.order_market_sell(symbol=pair, quantity=balance_altcoin)
        log_list.append('Sell')
        buy_sell_action_log(f'Sell,{pair},{altcoin_price},ALTcoin {balance_altcoin},{datetime.now()},none')
        print('Action = Sell')
    except Exception as e:
        buy_sell_action_log(f'Sell failed,{pair},{altcoin_price},ALTcoin {balance_altcoin},{datetime.now()},{e}')
        log_list.append('Sell failed')
        print('Sell failed')

else:
    log_list.append('No action')
    print('Action = Do nothing')

# register all the action
log_list.append(str(symbol_altcoin))
log_list.append(str(symbol_basecoin))
log_list.append(str(buy_amount))
log_list.append(str(altcoin_price))
log_list.append(str(ma_6))
log_list.append(str(ma_18))
log_list.append(str(balance_altcoin))
log_list.append(str(balance_basecoin))
log_list.append(str(datetime.now()))
log(log_list)
