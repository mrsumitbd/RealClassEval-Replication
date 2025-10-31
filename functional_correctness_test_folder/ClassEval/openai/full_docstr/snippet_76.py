class ShoppingCart:
    """
    The class manages items, their prices, quantities, and allows to for add, removie, view items, and calculate the total price.
    """

    def __init__(self):
        """
        Initialize the items representing the shopping list as an empty dictionary
        """
        self.items = {}

    def add_item(self, item, price, quantity=1):
        """
        Add item information to the shopping list items, including price and quantity. The default quantity is 1
        :param item: string, Item to be added
        :param price: float, The price of the item
        :param quantity:int, The number of items, defaults to 1
        :return:None
        >>> shoppingcart = ShoppingCart()
        >>> shoppingcart.add_item("apple", 1, 5)
        >>> shoppingcart.items
        {'apple': {'price': 1, 'quantity': 5}}
        """
        if quantity <= 0:
            return
        if item in self.items:
            self.items[item]["quantity"] += quantity
            self.items[item]["price"] = price
        else:
            self.items[item] = {"price": price, "quantity": quantity}

    def remove_item(self, item, quantity=1):
        """
        Subtract the specified quantity of item from the shopping list items
        :param item:string, Item to be subtracted in quantity
        :param quantity:int, Quantity to be subtracted
        :return:None
        >>> shoppingcart = ShoppingCart()
        >>> shoppingcart.add_item("apple", 1, 5)
        >>> shoppingcart.remove_item("apple", 3)
        >>> shoppingcart.items
        {'apple': {'price': 1, 'quantity': 2}}
        """
        if quantity <= 0 or item not in self.items:
            return
        current_qty = self.items[item]["quantity"]
        new_qty = current_qty - quantity
        if new_qty > 0:
            self.items[item]["quantity"] = new_qty
        else:
            del self.items[item]

    def view_items(self) -> dict:
        """
        Return the current shopping list items
        :return:dict, the current shopping list items
        >>> shoppingcart = ShoppingCart()
        >>> shoppingcart.add_item("apple", 1, 5)
        >>> shoppingcart.remove_item("apple", 3)
        >>> shoppingcart.view_items()
        {'apple': {'price': 1, 'quantity': 2}}
        """
        return self.items

    def total_price(self) -> float:
        """
        Calculate the total price of all items in the shopping list, which is the quantity of each item multiplied by the price
        :return:float, the total price of all items in the shopping list
        >>> shoppingcart = ShoppingCart()
        >>> shoppingcart.add_item("apple", 1, 5)
        >>> shoppingcart.add_item("banana", 2, 3)
        >>> shoppingcart.total_price()
        11.0
        """
        total = 0.0
        for item_info in self.items.values():
            total += item_info["price"] * item_info["quantity"]
        return total

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     cart = ShoppingCart()
#     cart.add_item("apple", 1, 5)
#     cart.add_item("banana", 2, 3)
#     print(cart.view_items())
#     print(cart.total_price())
#     cart.remove_item("apple", 2)
#     print(cart.view_items())
#     print(cart.total_price())
