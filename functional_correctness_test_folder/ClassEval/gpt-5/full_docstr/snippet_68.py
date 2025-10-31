class Order:
    """
    The class manages restaurant orders by allowing the addition of dishes, calculation of the total cost, and checkout.
    """

    def __init__(self):
        """
        Initialize the order management system
        self.menu stores the dishes of resturant inventory
        menu = [{"dish": dish name, "price": price, "count": count}, ...]
        self.selected_dishes stores the dished selected by customer
        selected_dish = {"dish": dish name, "count": count, price: price}
        self.sales stores the sales of each dish
        sales = {dish name: sales}
        """
        self.menu = []
        self.selected_dishes = []
        self.sales = {}

    def add_dish(self, dish):
        """
        Check the self.menu and add into self.selected_dish if the dish count is valid.
        And if the dish has successfully been added, change the count in self.menu.
        :param dish: dict, the information of dish. dish = {"dish": dish name, "count": count, price: price}
        :return: True if successfully added, or False otherwise.
        >>> order = Order()
        >>> order.menu.append({"dish": "dish1", "price": 10, "count": 5})
        >>> order.add_dish({"dish": "dish1", "price": 10, "count": 3})
        True
        """
        if not isinstance(dish, dict):
            return False
        name = dish.get("dish")
        count = dish.get("count")
        price = dish.get("price")
        if not isinstance(name, str) or not isinstance(count, (int, float)) or not isinstance(price, (int, float)):
            return False
        if count <= 0:
            return False

        menu_item = None
        for item in self.menu:
            if item.get("dish") == name:
                menu_item = item
                break
        if menu_item is None:
            return False

        available = menu_item.get("count", 0)
        if count > available:
            return False

        menu_price = menu_item.get("price", price)
        # Reduce inventory
        menu_item["count"] = available - count

        # Add to selected_dishes (aggregate if already present)
        for sel in self.selected_dishes:
            if sel.get("dish") == name:
                sel["count"] += count
                sel["price"] = menu_price
                return True

        self.selected_dishes.append(
            {"dish": name, "count": count, "price": menu_price})
        return True

    def calculate_total(self):
        """
        Calculate the total price of dishes that have been ordered. Multiply the count, price and sales.
        :return total: float, the final total price.
        >>> order = Order()
        >>> order.menu.append({"dish": "dish1", "price": 10, "count": 5})
        >>> order.sales = {"dish1": 0.8}
        >>> order.add_dish({"dish": "dish1", "price": 10, "count": 4})
        True
        >>> order.calculate_total()
        32.0
        """
        total = 0.0
        for sel in self.selected_dishes:
            name = sel.get("dish")
            count = sel.get("count", 0)
            price = sel.get("price", 0.0)
            sale = self.sales.get(name, 1.0)
            total += float(count) * float(price) * float(sale)
        return float(total)

    def checkout(self):
        """
        Check out the dished ordered. IF the self.selected_dishes is not empty, invoke the calculate_total
        method to check out.
        :return Flase if the self.selected_dishes is empty, or total(return value of calculate_total) otherwise.
        >>> order = Order()
        >>> order.menu.append({"dish": "dish1", "price": 10, "count": 5})
        >>> order.sales = {"dish1": 0.8}
        >>> order.add_dish({"dish": "dish1", "price": 10, "count": 4})
        True
        >>> order.checkout()
        32.0
        """
        if not self.selected_dishes:
            return False
        return self.calculate_total()
