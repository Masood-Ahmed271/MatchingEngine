'''
    File: MatchingEngine.py
    Description: A program that matches buy and sell orders for a crypto exchange. Built for OSL graduate program assessment.
    Author: Masood Ahmed

    Assumption: Can only buy and sell from one order_id, not from multiple order_ids
'''

#  Defining the class for the matching engine

class MatchingEngine:

    def __init__(self, orders):

        '''
        Initializes variables and processes the initial orders.

        Parameters:
        - orders: List of initial orders

        '''

        # Initialize variables
        self.__sell_order_id, self.__buy_order_id = -1, -1
        self.__order_book = {}   #  Dictionary to store the order book details
        self.__output_queue = {}        # Dictionary to store the output queue details

        # 2 lists to store input queue details and instruments
        self.__input_queue, self.__instruments_list  = [], []   

        for order in orders:
            self.__input_queue.append(order)
            if order[0] not in self.__instruments_list:
                self.__instruments_list.append(order[0])

        for instrument, side, price, quantity, in self.__input_queue:
            if instrument not in self.__output_queue:
                self.__output_queue[instrument] = {'acknowledgments': [], 'trade_messages': []}
            if side == 'buy':
                self.__buy_order_id += 1
                self.__output_queue[instrument]['acknowledgments'].append(f"Order acknowledged: Side: {side}, Instrument: {instrument}, Price: {price}, Quantity: {quantity}, Order ID: {self.__buy_order_id}")
            elif side == 'sell':
                self.__sell_order_id += 1
                self.__output_queue[instrument]['acknowledgments'].append(f"Order acknowledged: Side: {side}, Instrument: {instrument}, Price: {price}, Quantity: {quantity}, Order ID: {self.__sell_order_id}")
            self.__check_limit_order(instrument, side, price, quantity)


    def new_orders(self, orders):

        '''
        Processes new orders and adds them to the input queue.

        Parameters:
        - orders: List of new orders

        '''
            
        for instrument, side, price, quantity, in orders:
            if instrument not in self.__output_queue:
                self.__output_queue[instrument] = {'acknowledgments': [], 'trade_messages': []}
            if side == 'buy':
                self.__buy_order_id += 1
                self.__output_queue[instrument]['acknowledgments'].append(f"Order acknowledged: Side: {side}, Instrument: {instrument}, Price: {price}, Quantity: {quantity}, Order ID: {self.__buy_order_id}")
            elif side == 'sell':
                self.__sell_order_id += 1
                self.__output_queue[instrument]['acknowledgments'].append(f"Order acknowledged: Side: {side}, Instrument: {instrument}, Price: {price}, Quantity: {quantity}, Order ID: {self.__sell_order_id}")
                
            self.__check_limit_order(instrument, side, price, quantity)


    def retrieve_input_queue(self):

        '''
        Return the input queue of orders.

        Returns:
        - input queue

        '''

        return self.__input_queue

    def retrieve_output_queue(self, instrument):

        '''
        Prints the output queue of orders of a given instrument.

        Parameters:
        - instrument: Name of the instrument

        Returns:
        - Output queue of orders for the given instrument or -1 if not found

        '''

        if instrument in self.__output_queue:
            return self.__output_queue[instrument]
        else:
            return -1

    def __update_input_queue(self):

        '''
        Updates the input queue based on the order book.
        
        '''

        new_input_queue = []
        for instrument in self.__instruments_list:
            res = self.get_order_book(instrument)
            for each in res['buy_orders']:
                new_input_queue.append((instrument, 'buy', each['price'], each['quantity'], each['order_id']))
            for each in res['sell_orders']:
                new_input_queue.append((instrument, 'sell', each['price'], each['quantity'], each['order_id']))
        self.__input_queue = new_input_queue

    def __instrument_related_checks(self, instrument):
        
        '''
        Performs checks related to the instrument and initializes if not present.

        Parameters:
        - instrument: Name of the instrument
        
        '''
        
        if instrument not in self.__order_book:
            self.__order_book[instrument] = {'buy_orders': [], 'sell_orders': []}

        if instrument not in self.__output_queue:
            self.__output_queue[instrument] = {'acknowledgments': [], 'trade_messages': []}
        
        if instrument not in self.__instruments_list:
            self.__instruments_list.append(instrument)

    def __check_limit_order(self, instrument, side, price, quantity):

        '''
        Checks if a limit order can be executed and executes the trade if possible.

        Parameters:
        - instrument: Name of the instrument
        - side: Side of the order (buy/sell)
        - price: Price of the order
        - quantity: Quantity of the order
        
        '''

        given_quantity = quantity

        self.__instrument_related_checks(instrument)
        
        if side == 'buy':
            possible_matches = self.__order_book[instrument]['sell_orders']
        if side == 'sell':
            possible_matches = self.__order_book[instrument]['buy_orders']
        
        if not possible_matches:
            if side == 'buy':
                self.__order_book[instrument]["buy_orders"].append({"price": price, "quantity": given_quantity, "order_id": self.__buy_order_id})
            if side == 'sell':
                self.__order_book[instrument]["sell_orders"].append({"price": price, "quantity": given_quantity, "order_id": self.__sell_order_id})
            self.__update_input_queue()
            return
        
        for i, order in enumerate(possible_matches):
           if (side == 'buy' and order["price"] <= price and order["quantity"] >= given_quantity) or (side == 'sell' and order["price"] >= price and order["quantity"] >= given_quantity):
               self.__output_queue[instrument]['trade_messages'].append(f"trade happened for {instrument} between {side} order {self.__buy_order_id if side == 'buy' else self.__sell_order_id} and {side} order {order['order_id']}")
               order["quantity"] -= quantity
               if order["quantity"] == 0:
                   possible_matches.pop(i)
               given_quantity -= quantity
               if given_quantity == 0:
                   break
            
        if given_quantity > 0:
            if side == 'buy':
                self.__order_book[instrument]["buy_orders"].append({"price": price, "quantity": given_quantity, "order_id": self.__buy_order_id})
            if side == 'sell':
                self.__order_book[instrument]["sell_orders"].append({"price": price, "quantity": given_quantity, "order_id": self.__sell_order_id})

        self.__update_input_queue()

    def get_order_book(self, instrument):

        '''
        Retrieves the order book for a given instrument.

        Parameters:
        - instrument: Name of the instrument

        Returns:
        - Order book for the given instrument or -1 if not found
        
        '''
        
        if instrument in self.__order_book:
            js = self.__order_book[instrument]
            if "instrument" not in js:
                js["instrument"] = instrument
            return js
        else:
            return {"error": f"No orders found for instrument: {instrument}"}

    def cancel_order(self, instrument, price, side, quantity, order_id):
       '''
       Cancels an order from the order book for a given instrument, price, and side.

        Parameters:
        - instrument: Name of the instrument
        - price: Price of the order to be canceled
        - side: Side (either buy/sell).
        - quantity: Quantity of shares being bought / sold
        - order_id: ID number associated with this order

        Returns:
        - A message asserting what orders have been cancelled.

       '''

       if instrument not in self.__order_book:
           return {"message": f"No orders found for instrument: {instrument}"}

       orders = self.__order_book[instrument][side + '_orders']
       for i, order in enumerate(orders):
           if order['order_id'] == order_id and order['price'] == price and order['quantity'] == quantity:
               orders.pop(i)
               self.__update_input_queue()
               return {"message": f"Order cancelled: Side: {side}, Instrument: {instrument}, Price: {price}, Quantity: {quantity}, Order ID: {order_id}"}

       return {"message": f"No orders found for instrument: {instrument}, price: {price}, side: {side}, quantity: {quantity}, order_id: {order_id}"}
    
    def get_instruments_list(self):
        
        '''
        A get method to get the instrument list

        Returns:
        - List containing all available instrument names

        '''
        return self.__instruments_list