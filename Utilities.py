SPACE = "                        "
trade = []

def get_input_queue(order):
    print("")
    print(SPACE, "Here is the input queue")
    print("")
    for each in order.retrieve_input_queue():
        print(f"{SPACE}|{each}|")
    print("")

def get_order_book(order, instrument):
    print("")
    unprocessed_order_book = order.get_order_book(instrument)
    print(SPACE, "************ Buy Orders **************")
    print("")
    for each in unprocessed_order_book['buy_orders']:
        print(SPACE, "|", end=" ")
        for key in each:
            print(f"{key}: {each[key]}", end = ", ")
        print("|")
    print("")
    print(SPACE, "************* Sell Orders *************")
    print("")
    for each in unprocessed_order_book['sell_orders']:
        print(SPACE, "|", end=" ")
        for key in each:
            print(f"{key}: {each[key]}", end = ", ")
        print("|")
    print("")


def send_new_order(order):
    print("")
    instrument = input(f"{SPACE}Enter the instrument (remember it is case sensitive): ")
    side = input(f"{SPACE}Enter the side (buy or sell) and (remember it is case sensitive): ")
    price = float(input(f"{SPACE}Enter the price: "))
    quantity = int(input(f"{SPACE}Enter the quantity: "))
    order.new_orders([
        (instrument, side, price, quantity),
    ])
    print("")
    # printing acknolwedgment message
    output_queue = order.retrieve_output_queue(instrument)
    print(SPACE, end="")
    print(output_queue["acknowledgments"][-1])
    print("")
    # printing trade message
    if output_queue["trade_messages"] == trade:
        print(SPACE, "No trade happened")
        print("")
    else:
        print(SPACE, end="")
        print(output_queue["trade_messages"][-1])
        print("")

def get_executed_orders(order):
    print("")
    print(SPACE, "Choose the instrument for which you want to see the executed orders", order.get_instruments_list())
    instrument = input(f"{SPACE}Enter the instrument (remember it is case sensitive): ")
    print("")
    print(SPACE, "************* Here are the executed orders *************")
    output_queue = order.retrieve_output_queue(instrument)
    if len(output_queue["trade_messages"]) == 0:
        print(SPACE, "No executed orders")
    else:
        for each in output_queue["trade_messages"]:
            print(f"{SPACE}|{each} |")
    print("")


def cancel_order(order):
    print(SPACE, "Caution: You can only cancel the order if it is in the order book")
    print("")
    print(SPACE, "First Select the instrument for which you want to cancel the order")
    print(SPACE, "Enter the instrument for which you want to cancel the order", order.get_instruments_list())
    instrument = input(f"{SPACE}Enter the instrument (remember it is case sensitive): ")
    print("")
    print(SPACE, "Here is the current orderbook of the choosen instrument")
    get_order_book(order, instrument)
    print("")
    print(SPACE, "Now select accordingly ")
    side = input(f"{SPACE}Enter the side (buy or sell) and (remember it is case sensitive): ")
    side = input(f"{SPACE}Enter the side (buy or sell) and (remember it is case sensitive): ")
    price = float(input(f"{SPACE}Enter the price: "))
    quantity = int(input(f"{SPACE}Enter the quantity: "))
    order_id = int(input(f"{SPACE}Enter the order id: "))
    res = order.cancel_order(instrument, price, side, quantity, order_id)
    print("")
    print(SPACE, end="")
    print(res["message"])