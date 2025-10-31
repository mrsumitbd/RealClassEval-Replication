
class StockPortfolioTracker:
    """
    This is a class as StockPortfolioTracker that allows to add stocks, remove stocks, buy stocks, sell stocks, calculate the total value of the portfolio, and obtain a summary of the portfolio.
    """

    def __init__(self, cash_balance):
        """
        Initialize the StockPortfolioTracker class with a cash balance and an empty portfolio.
        """
        self.portfolio = []
        self.cash_balance = cash_balance

    def add_stock(self, stock):
        """
        Add a stock to the portfolio.
        :param stock: a dictionary with keys "name", "price", and "quantity"
        """
        self.portfolio.append(stock)

    def remove_stock(self, stock):
        """
        Remove a stock from the portfolio.
        :param stock: a dictionary with keys "name", "price", and "quantity"
        :return: True if removed, False otherwise
        """
        try:
            self.portfolio.remove(stock)
            return True
        except ValueError:
            return False

    def buy_stock(self, stock):
        """
        Buy a stock and add it to the portfolio.
        :param stock: a dictionary with keys "name", "price", and "quantity"
        :return: True if the stock was bought successfully, False if the cash balance is not enough.
        """
        total_cost = stock["price"] * stock["quantity"]
        if self.cash_balance >= total_cost:
            self.cash_balance -= total_cost
            # Check if stock already exists in portfolio (by name and price)
            for s in self.portfolio:
                if s["name"] == stock["name"] and s["price"] == stock["price"]:
                    s["quantity"] += stock["quantity"]
                    return True
            self.portfolio.append(stock.copy())
            return True
        else:
            return False

    def sell_stock(self, stock):
        """
        Sell a stock and remove it from the portfolio and add the cash to the cash balance.
        :param stock: a dictionary with keys "name", "price", and "quantity"
        :return: True if the stock was sold successfully, False if the quantity of the stock is not enough.
        """
        for s in self.portfolio:
            if s["name"] == stock["name"] and s["price"] == stock["price"]:
                if s["quantity"] >= stock["quantity"]:
                    s["quantity"] -= stock["quantity"]
                    self.cash_balance += stock["price"] * stock["quantity"]
                    if s["quantity"] == 0:
                        self.portfolio.remove(s)
                    return True
                else:
                    return False
        return False

    def calculate_portfolio_value(self):
        """
        Calculate the total value of the portfolio.
        :return: the total value of the portfolio, float.
        """
        total = self.cash_balance
        for s in self.portfolio:
            total += s["price"] * s["quantity"]
        return total

    def get_portfolio_summary(self):
        """
        Get a summary of the portfolio.
        :return: a tuple of the total value of the portfolio and a list of dictionaries with keys "name" and "value"
        """
        summary = []
        for s in self.portfolio:
            summary.append(
                {"name": s["name"], "value": s["price"] * s["quantity"]})
        return (self.calculate_portfolio_value(), summary)

    def get_stock_value(self, stock):
        """
        Get the value of a stock.
        :param stock: a dictionary with keys "name", "price", and "quantity"
        :return: the value of the stock, float.
        """
        return stock["price"] * stock["quantity"]
