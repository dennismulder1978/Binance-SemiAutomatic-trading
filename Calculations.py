def ma(input_list, length):
    """
    Moving average
    :param input_list: is the list of closing prices
    :param length: is the backtrack-length.
    :return: the average of the closing prices is the backtrack-length
    """
    length = length * 4  # correct hourly rate to 15 minute

    if length == 96:
        short_list = input_list
    else:
        short_list = input_list[95 - length:-1:]
    # print(short_list)

    length_list = len(short_list)
    summery = float(0.0)
    for j in short_list:
        summery += float(j)
    avg = summery / length_list
    return avg


def sma_trade_logic_hourly_oneday(bar_list):
    """
    Calculation
    :param bar_list: is binance trading set data
    :return: list of hourly of past 24h closing prices
    """
    closing_list = []
    for i in bar_list:
        closing_list.append(i[4])
    return closing_list


def log(log_list):
    final_string = ",".join(log_list)
    try:
        open('Secret/log.csv')
    except:
        with open('Secret/log.csv', 'w') as g:
            g.write("Action,Buy amount,LUNA price,MA_6h,MA_18h,balance LUNA,balance BUSD,datetime\n")
            g.close()
    with open('Secret/log.csv', 'a') as f:
        f.write(final_string + '\n')
        f.close()
    return


def buy_sell_action(action, price_LUNA, amount, datetime):
    try:
        open('Secret/action.csv')
    except:
        with open('Secret/action.csv', 'w') as g:
            g.write("Action,LUNA price,Amount,DateTime\n")
            g.close()
    with open('Secret/log.csv', 'a') as f:
        f.write(action + "," + price_LUNA + "," + amount + "," + datetime + '\n')
        f.close()
    return
