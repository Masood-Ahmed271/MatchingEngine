from MatchingEngine import MatchingEngine
from Utilities import get_input_queue, send_new_order, cancel_order, get_order_book, get_executed_orders

def main():

    SPACE = "                        "

    is_running = True

    print("")
    print("**************************************************** Welcome to the Crypto Matching Engine ****************************************************")
    print("")
    # Create an instance of the OrderBook
    order_book = MatchingEngine([
    ('BTC', 'buy', 99.0, 5),
    ('BTC', 'buy', 101.0, 6),
    ('BTC', 'sell', 105.0, 7),
    ('BTC', 'sell', 102.0, 8),
    ])

    print(SPACE, "Here is the input queue after initialization")
    get_input_queue(order_book)

    while is_running:
        print(SPACE, "Press '1' to send a new order")
        print(SPACE, "Press '2' to cancel an order")
        print(SPACE, "Press '3' to print the order book of specific instrument")
        print(SPACE, "Press '4' to view the input queue")
        print(SPACE, "Press '5' to retrieve all executed trades of specific instrument")
        print(SPACE, "Press 'q' or 'Q' to quit")
        print("")
        user_input = input(f"{SPACE}Enter your choice: ")
        print("")
        if user_input == '1':
            send_new_order(order_book)
        elif user_input == '2':
            cancel_order(order_book)
        elif user_input == '3':
            print(SPACE, "Choose the instrument for which you want to see the order book", order_book.get_instruments_list())
            print("")
            instrument = input(f"{SPACE}Enter the instrument (remember it is case sensitive): ")
            print("")
            get_order_book(order_book, instrument)
        elif user_input == '4':
            get_input_queue(order_book)
        elif user_input == '5':
            get_executed_orders(order_book)
        elif user_input == 'q' or user_input == 'Q':
            is_running = False
        else:
            print(SPACE, "Invalid Input")
            print("")

if __name__ == '__main__':
    main()