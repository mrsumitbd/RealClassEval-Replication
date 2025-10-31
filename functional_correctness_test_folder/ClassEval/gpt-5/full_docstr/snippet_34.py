class DiscountStrategy:
    """
    This is a class that allows to use different discount strategy based on shopping credit or shopping cart in supermarket.
    """

    def __init__(self, customer, cart, promotion=None):
        """
        Initialize the DiscountStrategy with customer information, a cart of items, and an optional promotion.
        :param customer: dict, customer information
        :param cart: list of dicts, a cart of items with details
        :param promotion: function, optional promotion applied to the order
        >>> customer = {'name': 'John Doe', 'fidelity': 1200}
        >>> cart = [{'product': 'product', 'quantity': 14, 'price': 23.5}]
        >>> DiscountStrategy(customer, cart, DiscountStrategy.FidelityPromo)

        """
        self.customer = customer
        self.cart = cart
        self.promotion = promotion
        self._total = self.total()

    def total(self):
        """
        Calculate the total cost of items in the cart.
        :return: float, total cost of items
        >>> customer = {'name': 'John Doe', 'fidelity': 1200}
        >>> cart = [{'product': 'product', 'quantity': 14, 'price': 23.5}]
        >>> ds = DiscountStrategy(customer, cart)
        >>> ds.total()
        329.0

        """
        total = 0.0
        for item in self.cart:
            total += item.get('quantity', 0) * item.get('price', 0.0)
        self._total = total
        return total

    def due(self):
        """
        Calculate the final amount to be paid after applying the discount.
        :return: float, final amount to be paid
        >>> customer = {'name': 'John Doe', 'fidelity': 1200}
        >>> cart = [{'product': 'product', 'quantity': 14, 'price': 23.5}]
        >>> ds = DiscountStrategy(customer, cart, DiscountStrategy.FidelityPromo)
        >>> ds.due()
        312.55

        """
        total = self._total if hasattr(self, "_total") else self.total()
        discount = 0.0
        if self.promotion is not None:
            discount = self.promotion(self)
        return total - discount

    @staticmethod
    def FidelityPromo(order):
        """
        Calculate the discount based on the fidelity points of the customer.Customers with over 1000 points can enjoy a 5% discount on the entire order.
        :param order: object, the order to apply the discount to
        :return: float, discount amount
        >>> customer = {'name': 'John Doe', 'fidelity': 1200}
        >>> cart = [{'product': 'product', 'quantity': 14, 'price': 23.5}]
        >>> order = DiscountStrategy(customer, cart, DiscountStrategy.FidelityPromo)
        >>> DiscountStrategy.FidelityPromo(order)
        16.45

        """
        fidelity = order.customer.get('fidelity', 0)
        total = order._total if hasattr(order, "_total") else order.total()
        if fidelity > 1000:
            return total * 0.05
        return 0.0

    @staticmethod
    def BulkItemPromo(order):
        """
        Calculate the discount based on bulk item quantity in the order.In the same order, if the quantity of a single item reaches 20 or more, each item will enjoy a 10% discount.
        :param order: object, the order to apply the discount to
        :return: float, discount amount
        >>> customer = {'name': 'John Doe', 'fidelity': 1200}
        >>> cart = [{'product': 'product', 'quantity': 20, 'price': 23.5}]
        >>> order = DiscountStrategy(customer, cart, DiscountStrategy.BulkItemPromo)
        >>> DiscountStrategy.BulkItemPromo(order)
        47.0

        """
        discount = 0.0
        for item in order.cart:
            qty = item.get('quantity', 0)
            price = item.get('price', 0.0)
            if qty >= 20:
                discount += qty * price * 0.10
        return discount

    @staticmethod
    def LargeOrderPromo(order):
        """
        Calculate the discount based on the number of different products in the order.If the quantity of different products in the order reaches 10 or more, the entire order will enjoy a 7% discount.
        :param order: object, the order to apply the discount to
        :return: float, discount amount
        >>> customer = {'name': 'John Doe', 'fidelity': 1200}
        >>> cart = [{'product': 'product', 'quantity': 14, 'price': 23.5}]
        >>> order = DiscountStrategy(customer, cart, DiscountStrategy.LargeOrderPromo)
        >>> DiscountStrategy.LargeOrderPromo(order)
        0.0

        """
        products = {item.get('product') for item in order.cart}
        if len(products) >= 10:
            total = order._total if hasattr(order, "_total") else order.total()
            return total * 0.07
        return 0.0
