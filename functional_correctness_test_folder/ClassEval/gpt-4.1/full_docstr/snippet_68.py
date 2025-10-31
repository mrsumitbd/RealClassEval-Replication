
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
        """
        dish_name = dish.get("dish")
        dish_count = dish.get("count")
        dish_price = dish.get("price")
        # Find the dish in menu
        for menu_item in self.menu:
            if menu_item["dish"] == dish_name and menu_item["price"] == dish_price:
                if menu_item["count"] >= dish_count and dish_count > 0:
                    # Check if already in selected_dishes
                    for sel in self.selected_dishes:
                        if sel["dish"] == dish_name and sel["price"] == dish_price:
                            sel["count"] += dish_count
                            menu_item["count"] -= dish_count
                            return True
                    # Not in selected_dishes, add new
                    self.selected_dishes.append({
                        "dish": dish_name,
                        "count": dish_count,
                        "price": dish_price
                    })
                    menu_item["count"] -= dish_count
                    return True
                else:
                    return False
        return False

    def calculate_total(self):
        """
        Calculate the total price of dishes that have been ordered. Multiply the count, price and sales.
        :return total: float, the final total price.
        """
        total = 0.0
        for sel in self.selected_dishes:
            dish_name = sel["dish"]
            count = sel["count"]
            price = sel["price"]
            sale = self.sales.get(dish_name, 1.0)
            total += count * price * sale
        return total

    def checkout(self):
        """
        Check out the dished ordered. IF the self.selected_dishes is not empty, invoke the calculate_total
        method to check out.
        :return Flase if the self.selected_dishes is empty, or total(return value of calculate_total) otherwise.
        """
        if not self.selected_dishes:
            return False
        return self.calculate_total()
