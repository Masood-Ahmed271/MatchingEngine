'''
    Description: A program that matches buy and sell orders for a crypto exchange. Built for OSL graduate program assesment.
    Author: Masood Ahmed

    Assumption can only buy from one order_id, not from multiple order_ids
'''


#  Importing libraries
import heapq as hq

#  Defining the class for the matching engine

class MatchingEngine:

    def __init__(self, orders) -> None:

        self.sell_order_id = -1
        self.buy_order_id = -1
        self.order_book = {}   #  Dictionary to store the order book details
        self.output_queue = {}        # Dictionary to store the output queue details
        self.input_queue = []         #  List to store the input queue details
        self.acknowledged_orders = [] #  List to store the acknowledged orders
        self.executed_orders = []     #  List to store the executed orders
        self.instruments_list = []    #  List to store the instruments list


        # orderbook structure is as follows:
            # instrument | side | price | quantity | order_id
        #  Looping through the orders and adding them to the input queue
        for order in orders:
            self.input_queue.append(order)
            if order[0] not in self.instruments_list:
                self.instruments_list.append(order[0])

        # checking if the initial orders in order book can be executed and executing it
        for instrument, side, price, quantity, in self.input_queue:
            if instrument not in self.output_queue:
                self.output_queue[instrument] = {'acknowledgments': [], 'trade_messages': []}
            if side == 'buy':
                self.buy_order_id += 1
                self.output_queue[instrument]['acknowledgments'].append(f"Order acknowledged: Side: {side}, Instrument: {instrument}, Price: {price}, Quantity: {quantity}, Order ID: {self.buy_order_id}")
            elif side == 'sell':
                self.sell_order_id += 1
                self.output_queue[instrument]['acknowledgments'].append(f"Order acknowledged: Side: {side}, Instrument: {instrument}, Price: {price}, Quantity: {quantity}, Order ID: {self.sell_order_id}")
            self.check_limit_order(instrument, side, price, quantity)


    def new_orders(self, orders):
        for instrument, side, price, quantity, in orders:
            if instrument not in self.output_queue:
                self.output_queue[instrument] = {'acknowledgments': [], 'trade_messages': []}
            if side == 'buy':
                self.buy_order_id += 1
                self.output_queue[instrument]['acknowledgments'].append(f"Order acknowledged: Side: {side}, Instrument: {instrument}, Price: {price}, Quantity: {quantity}, Order ID: {self.buy_order_id}")
            elif side == 'sell':
                self.sell_order_id += 1
                self.output_queue[instrument]['acknowledgments'].append(f"Order acknowledged: Side: {side}, Instrument: {instrument}, Price: {price}, Quantity: {quantity}, Order ID: {self.sell_order_id}")
                
            self.check_limit_order(instrument, side, price, quantity)


    # Prints the input queue of orders.
    def retrieve_input_queue(self):
        return self.input_queue

    # Prints the output queue of orders of a given instrument.
    def retrieve_output_queue(self, instrument):
        if instrument in self.output_queue:
            return self.output_queue[instrument]
        else:
            return -1

    def update_input_queue(self):
        new_input_queue = []
        for instrument in self.instruments_list:
            res = self.get_order_book(instrument)
            for each in res['buy_orders']:
                new_input_queue.append((instrument, 'buy', each['price'], each['quantity'], each['order_id']))
            for each in res['sell_orders']:
                new_input_queue.append((instrument, 'sell', each['price'], each['quantity'], each['order_id']))
        self.input_queue = new_input_queue

    def check_limit_order(self, instrument, side, price, quantity):

        given_quantity = quantity

        if instrument not in self.order_book:
            self.order_book[instrument] = {'buy_orders': [], 'sell_orders': []}

        if instrument not in self.output_queue:
            self.output_queue[instrument] = {'acknowledgments': [], 'trade_messages': []}
        
        if instrument not in self.instruments_list:
            self.instruments_list.append(instrument)
        
        if side == 'buy':
            possible_matches = self.order_book[instrument]['sell_orders']
        if side == 'sell':
            possible_matches = self.order_book[instrument]['buy_orders']
        
        if possible_matches:
            if side == 'buy':
                for i in range(len(possible_matches)):
                    if possible_matches[i]["price"] <= price and possible_matches[i]["quantity"] >= given_quantity and given_quantity != 0:
                        self.output_queue[instrument]['trade_messages'].append(f"trade happened for {instrument} between buy order {self.buy_order_id} and sell order {possible_matches[i]['order_id']}")
                        possible_matches[i]["quantity"] -= quantity
                        if self.order_book[instrument]['sell_orders'][i]["quantity"] == 0:
                            self.order_book[instrument]['sell_orders'].pop(i)
                        given_quantity -= quantity
                    if given_quantity == 0:
                        break
                if given_quantity > 0:
                    self.order_book[instrument]["buy_orders"].append({"price": price, "quantity": given_quantity, "order_id": self.buy_order_id})
            if side == 'sell':
                for i in range(len(possible_matches)):
                    # print(possible_matches[i])
                    # print(given_quantity)
                    if possible_matches[i]["price"] >= price and possible_matches[i]["quantity"] >= given_quantity and given_quantity != 0:
                        self.output_queue[instrument]['trade_messages'].append(f"trade happened for {instrument} between sell order {self.sell_order_id} and buy order {possible_matches[i]['order_id']}")
                        possible_matches[i]["quantity"] -= quantity
                        if self.order_book[instrument]['buy_orders'][i]["quantity"] == 0:
                            self.order_book[instrument]['buy_orders'].pop(i)
                        given_quantity -= quantity
                    if given_quantity == 0:
                        break
                if given_quantity > 0:
                    self.order_book[instrument]["sell_orders"].append({"price": price, "quantity": given_quantity, "order_id": self.sell_order_id})
        else:
            if side == 'buy':
                self.order_book[instrument]["buy_orders"].append({"price": price, "quantity": given_quantity, "order_id": self.buy_order_id})
            if side == 'sell':
                self.order_book[instrument]["sell_orders"].append({"price": price, "quantity": given_quantity, "order_id": self.sell_order_id})

        self.update_input_queue()

    # prints the order book of a given instrument
    def get_order_book(self, instrument):
        if instrument in self.order_book:
            js = self.order_book[instrument]
            if "instrument" not in js:
                js["instrument"] = instrument
            return js
        else:
            return {"error": f"No orders found for instrument: {instrument}"}
        
    # Cancels an order from the order book for a given instrument, price, and side.
    def cancel_order(self, instrument, price, side, quantity, order_id):
        if instrument in self.order_book:
            if side == 'buy':
                for each in self.order_book[instrument]['buy_orders']:
                    if each['order_id'] == order_id and each['price'] == price and each['quantity'] == quantity:
                        self.order_book[instrument]['buy_orders'].remove(each)
                        self.update_input_queue()
                        return {"message": f"Order cancelled: Side: {side}, Instrument: {instrument}, Price: {price}, Quantity: {quantity}, Order ID: {order_id}"}
            elif side == 'sell':
                for each in self.order_book[instrument]['sell_orders']:
                    if each['order_id'] == order_id and each['price'] == price and each['quantity'] == quantity:
                        self.order_book[instrument]['sell_orders'].remove(each)
                        self.update_input_queue()
                        return {"message": f"Order cancelled: Side: {side}, Instrument: {instrument}, Price: {price}, Quantity: {quantity}, Order ID: {order_id}"}
            
        return {"message": f"No orders found for instrument: {instrument}, price: {price}, side: {side}, quantity: {quantity}, order_id: {order_id}"}
    
    def get_instruments_list(self):
        return self.instruments_list