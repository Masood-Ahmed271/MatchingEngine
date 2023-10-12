# MatchingEngine Documentation

The `MatchingEngine` class represents a matching engine for processing buy and sell orders. It matches buy orders with corresponding sell orders based on the instrument, price, and quantity. The class provides functions to add new orders, retrieve the input queue, retrieve the output queue for a specific instrument, retrieve the order book for a specific instrument, cancel an order from the order book, and retrieve the list of instruments.

## Class Methods

### `__init__(self, orders)`
This method is the constructor of the `MatchingEngine` class. It initializes the variables and processes the initial orders.

**Parameters:**
- `orders` (list): A list of orders represented as tuples. Each tuple contains the instrument, side (buy/sell), price, and quantity.

**Time Complexity:** The time complexity of this method depends on the number of initial orders. If there are n initial orders, the time complexity is O(n).

### `new_orders(self, orders)`
This method adds new orders to the matching engine and processes them.

**Parameters:**
- `orders` (list): A list of orders represented as tuples. Each tuple contains the instrument, side (buy/sell), price, and quantity.

**Time Complexity:** The time complexity of this method depends on the number of new orders. If there are m new orders, the time complexity is O(m).

### `retrieve_input_queue(self)`
This method retrieves the input queue of orders.

**Returns:** The input queue of orders.

**Time Complexity:** The time complexity of this method is O(1).

### `retrieve_output_queue(self, instrument)`
This method retrieves the output queue of orders for a given instrument.

**Parameters:**
- `instrument` (str): The instrument for which to retrieve the output queue.

**Returns:** The output queue of orders for the given instrument.

**Time Complexity:** The time complexity of this method is O(1).

### `get_order_book(self, instrument)`
This method retrieves the order book for a given instrument.

**Parameters:**
- `instrument` (str): The instrument for which to retrieve the order book.

**Returns:** The order book for the given instrument.

**Time Complexity:** The time complexity of this method is O(1).

### `cancel_order(self, instrument, price, side, quantity, order_id)`
This method cancels an order from the order book for a given instrument, price, side, quantity, and order ID.

**Parameters:**
- `instrument` (str): The instrument of the order to cancel.
- `price` (float): The price of the order to cancel.
- `side` (str): The side (buy/sell) of the order to cancel.
- `quantity` (int): The quantity of the order to cancel.
- `order_id` (int): The ID of the order to cancel.

**Returns:** A message indicating whether the order was successfully cancelled or if no matching order was found.

**Time Complexity:** The time complexity of this method depends on the number of orders in the order book for the given instrument. If there are k orders, the time complexity is O(k).

### `get_instruments_list(self)`
This method retrieves the list of instruments.

**Returns:** The list of instruments.

**Time Complexity:** The time complexity of this method is O(1).

## Private Methods

### `__update_input_queue(self)`
This private method updates the input queue based on the order book.

**Time Complexity:** The time complexity of this method depends on the number of instruments. If there are p instruments, the time complexity is O(p).

### `__instrument_related_checks(self, instrument)`
This private method performs checks related to the instrument, such as initializing the order book and output queue if they don't exist.

**Parameters:**
- `instrument` (str): The instrument for which to perform the checks.

**Time Complexity:** The time complexity of this method is O(1).

### `__check_limit_order(self, instrument, side, price, quantity)`
This private method checks if a given limit order can be executed and executes it if possible.

**Parameters:**
- `instrument` (str): The instrument of the limit order.
- `side` (str): The side (buy/sell) of the limit order.
- `price` (float): The price of the limit order.
- `quantity` (int): The quantity of the limit order.

**Time Complexity:** The time complexity of this method depends on the number of possible matches in the order book for the given instrument. If there are q matches, the time complexity is O(q).

## Time Complexity Summary

- `__init__(self, orders)`: O(n)
- `new_orders(self, orders)`: O(m)
- `retrieve_input_queue(self)`: O(1)
- `retrieve_output_queue(self, instrument)`: O(1)
- `get_order_book(self, instrument)`: O(1)
- `cancel_order(self, instrument, price, side, quantity, order_id)`: O(k)
- `get_instruments_list(self)`: O(1)
- Private methods:
  - `__update_input_queue(self)`: O(p)
  - `__instrument_related_checks(self, instrument)`: O(1)
  - `__check_limit_order(self, instrument, side, price, quantity)`: O(q)
