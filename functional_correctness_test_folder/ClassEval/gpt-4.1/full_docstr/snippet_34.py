
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
        """
        self.customer = customer
        self.cart = cart
        self.promotion = promotion
        self._total = None
        self.total()

    def total(self):
        """
        Calculate the total cost of items in the cart.
        :return: float, total cost of items
        """
        if self._total is None:
            self._total = sum(item['quantity'] * item['price']
                              for item in self.cart)
        return self._total

    def due(self):
        """
        Calculate the final amount to be paid after applying the discount.
        :return: float, final amount to be paid
        """
        if self.promotion is None:
            discount = 0.0
        else:
            discount = self.promotion(self)
        return self.total() - discount

    @staticmethod
    def FidelityPromo(order):
        """
        Calculate the discount based on the fidelity points of the customer.Customers with over 1000 points can enjoy a 5% discount on the entire order.
        :param order: object, the order to apply the discount to
        :return: float, discount amount
        """
        if order.customer.get('fidelity', 0) >= 1000:
            return order.total() * 0.05
        return 0.0

    @staticmethod
    def BulkItemPromo(order):
        """
        Calculate the discount based on bulk item quantity in the order.In the same order, if the quantity of a single item reaches 20 or more, each item will enjoy a 10% discount.
        :param order: object, the order to apply the discount to
        :return: float, discount amount
        """
        discount = 0.0
        for item in order.cart:
            if item['quantity'] >= 20:
                discount += item['quantity'] * item['price'] * 0.1
        return discount

    @staticmethod
    def LargeOrderPromo(order):
        """
        Calculate the discount based on the number of different products in the order.If the quantity of different products in the order reaches 10 or more, the entire order will enjoy a 7% discount.
        :param order: object, the order to apply the discount to
        :return: float, discount amount
        """
        products = {item['product'] for item in order.cart}
        if len(products) >= 10:
            return order.total() * 0.07
        return 0.0
