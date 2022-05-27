def ma(input_list, length):
    input_list = input_list[:-1]  # pop off last (=incomplete) time-period
    short_list = input_list[-length::]  # shorten list to requested length
    try:
        result = sum(short_list)/len(short_list)
    except Exception as e:
        print(e)
        result = 0
    return result


def ma_trade_logic(bar_list):
    return [float(i[4]) for i in bar_list]  # list of pos[4] (is closing price) per time period, also str to float


def log(log_list):
    final_string = ",".join(log_list)
    try:
        open('Secret/log.csv')
    except FileNotFoundError:
        with open('Secret/log.csv', 'w') as g:
            g.write("Action," +
                    "ALTcoin," +
                    "BASEcoin," +
                    "Buy amount," +
                    "Altcoin price," +
                    "MA_6h," +
                    "MA_18h," +
                    "balance ALTcoin," +
                    "balance BASE_coin," +
                    "datetime\n")
            g.close()
    with open('Secret/log.csv', 'a') as f:
        f.write(final_string + '\n')
        f.close()
    return


def buy_sell_action_log(stringer):
    try:
        open('Secret/action.csv')
    except FileNotFoundError:
        with open('Secret/action.csv', 'w') as g:
            g.write('Action,' +
                    'Pair,' +
                    'Altcoin price,' +
                    'Quantity,' +
                    'DateTime,' +
                    'Error\n')
            g.close()
    with open('Secret/action.csv', 'a') as f:
        f.write(stringer + '\n')
        f.close()
    return
