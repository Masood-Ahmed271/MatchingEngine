"""
File: Utilities.py
Description: This file contains a various supplementary functions in order to visualize the matching engine.
Author: Masood Ahmed

Global Variables Used:
- SPACE: A string of spaces used for formatting the output.
- trade: A list used to check if any trades have occurred.
"""

SPACE = "                        "
trade = []


def print_input_queue(order):
    
    """
    Prints the input queue containing pending orders.

    Parameters:
    - order: An instance of the Order class.

    Returns:
    - None

    """

    print("")
    print(SPACE, "Here is the input queue")
    print("")
    for each in order.retrieve_input_queue():
        print(f"{SPACE}| {each} |")
    print("")

def print_order_book(order, instrument):

    """
    Prints the order book for a given instrument.

    Parameters:
    - order: An instance of the Order class.
    - instrument: The name of the instrument.

    Returns:
    - None

    """
        
    print("")
    unprocessed_order_book = order.get_order_book(instrument)
    print(SPACE, "************ Buy Orders **************")
    print("")
    for each in unprocessed_order_book['buy_orders']:
        print(SPACE, "|", end=" ")
        for key in each:
            print(f"{key}: {each[key]}", end = ", ")
        print(" |")
    print("")
    print(SPACE, "************* Sell Orders *************")
    print("")
    for each in unprocessed_order_book['sell_orders']:
        print(SPACE, "|", end=" ")
        for key in each:
            print(f"{key}: {each[key]}", end = ", ")
        print(" |")
    print("")


def send_new_order(order):
        
    """
    Sends a new order to be added to the order book.

    Parameters:
    - order: An instance of the Order class.

    Returns:
    - None

    """
        
    print("")
    instrument = input(f"{SPACE} Enter the instrument (remember it is case sensitive): ")
    side = input(f"{SPACE} Enter the side (buy or sell) and (remember it is case sensitive): ")
    price = float(input(f"{SPACE} Enter the price: "))
    quantity = int(input(f"{SPACE} Enter the quantity: "))
    order.new_orders([
        (instrument, side, price, quantity),
    ])
    print("")

    output_queue = order.retrieve_output_queue(instrument)
    print(SPACE, end="")
    print(output_queue["acknowledgments"][-1])
    print("")

    if output_queue["trade_messages"] == trade:
        print(SPACE, "No trade happened")
        print("")
    else:
        print(SPACE, end="")
        print(output_queue["trade_messages"][-1])
        print("")

def print_executed_orders(order):
    
    """
    Prints the executed orders for a specific instrument.

    Parameters:
    - order: An instance of the Order class.

    Returns:
    - None
    
    """

    print("")
    instruments = order.get_instruments_list()
    print(SPACE, "Enter the instrument for which you want to cancel the order", instruments)
    instrument = input(f"{SPACE} Enter the instrument (remember it is case sensitive): ")

    while instrument not in instruments:
        print(SPACE, "Invalid Instrument typed!")
        instrument = input(f"{SPACE} Enter the instrument (remember it is case sensitive): ")

    print("")
    print(SPACE, "************* Here are the executed orders *************")
    print("")
    output_queue = order.retrieve_output_queue(instrument)
    if len(output_queue["trade_messages"]) == 0:
        print(SPACE, "No executed orders")
    else:
        for each in output_queue["trade_messages"]:
            print(f"{SPACE}|{each} |")
    print("")


def cancel_order(order):

    """
    Cancels an order from the order book.

    Parameters:
    - order: An instance of the Order class.

    Returns:
    - None
    
    """

    print(SPACE, "Caution: You can only cancel the order if it is in the order book")
    print("")
    print(SPACE, "First Select the instrument for which you want to cancel the order")
    instruments = order.get_instruments_list()
    print(SPACE, "Enter the instrument for which you want to cancel the order", instruments)
    instrument = input(f"{SPACE} Enter the instrument (remember it is case sensitive): ")

    while instrument not in instruments:
        print(SPACE, "Invalid Instrument typed!")
        instrument = input(f"{SPACE} Enter the instrument (remember it is case sensitive): ")

    print("")
    print(SPACE, "Here is the current orderbook of the chosen instrument")
    print_order_book(order, instrument)
    print("")
    print(SPACE, "Now select accordingly ")
    side = input(f"{SPACE} Enter the side (buy or sell) and (remember it is case sensitive): ")
    price = float(input(f"{SPACE} Enter the price: "))
    quantity = int(input(f"{SPACE} Enter the quantity: "))
    order_id = int(input(f"{SPACE} Enter the order id: "))
    res = order.cancel_order(instrument, price, side, quantity, order_id)
    print("")
    print(SPACE, end="")
    print(res["message"])