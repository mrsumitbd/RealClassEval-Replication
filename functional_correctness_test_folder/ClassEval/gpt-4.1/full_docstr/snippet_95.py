
class VendingMachine:
    """
    This is a class to simulate a vending machine, including adding products, inserting coins, purchasing products, viewing balance, replenishing product inventory, and displaying product information.
    """

    def __init__(self):
        """
        Initializes the vending machine's inventory and balance.
        """
        self.inventory = {}
        self.balance = 0

    def add_item(self, item_name, price, quantity):
        """
        Adds a product to the vending machine's inventory.
        """
        self.inventory[item_name] = {'price': price, 'quantity': quantity}

    def insert_coin(self, amount):
        """
        Inserts coins into the vending machine.
        """
        self.balance += amount
        return self.balance

    def purchase_item(self, item_name):
        """
        Purchases a product from the vending machine and returns the balance after the purchase and display purchase unsuccessful if the product is out of stock.
        """
        if item_name not in self.inventory:
            return False
        item = self.inventory[item_name]
        if item['quantity'] <= 0:
            return False
        if self.balance < item['price']:
            return False
        item['quantity'] -= 1
        self.balance -= item['price']
        # To avoid floating point issues, round to 2 decimals
        self.balance = round(self.balance, 2)
        return self.balance

    def restock_item(self, item_name, quantity):
        """
        Replenishes the inventory of a product already in the vending machine.
        """
        if item_name in self.inventory:
            self.inventory[item_name]['quantity'] += quantity
            return True
        else:
            return False

    def display_items(self):
        """
        Displays the products in the vending machine.
        """
        if not self.inventory:
            return False
        items = []
        for name, info in self.inventory.items():
            items.append(f"{name} - ${info['price']:.2f} [{info['quantity']}]")
        return '\n'.join(items) if len(items) > 1 else items[0]
