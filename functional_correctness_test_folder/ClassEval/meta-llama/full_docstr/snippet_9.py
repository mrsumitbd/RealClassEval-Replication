
class BankAccount:
    """
    This is a class as a bank account system, which supports deposit money, withdraw money, view balance, and transfer money.
    """

    def __init__(self, balance=0):
        """
        Initializes a bank account object with an attribute balance, default value is 0.
        """
        self.balance = balance

    def deposit(self, amount):
        """
        Deposits a certain amount into the account, increasing the account balance, return the current account balance.
        If amount is negative, raise a ValueError("Invalid amount").
        :param amount: int
        """
        if amount < 0:
            raise ValueError("Invalid amount")
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        """
        Withdraws a certain amount from the account, decreasing the account balance, return the current account balance.
        If amount is negative, raise a ValueError("Invalid amount").
        If the withdrawal amount is greater than the account balance, raise a ValueError("Insufficient balance.").
        :param amount: int
        """
        if amount < 0:
            raise ValueError("Invalid amount")
        if amount > self.balance:
            raise ValueError("Insufficient balance.")
        self.balance -= amount
        return self.balance

    def view_balance(self):
        """
        Return the account balance.
        """
        return self.balance

    def transfer(self, other_account, amount):
        """
        Transfers a certain amount from the current account to another account.
        :param other_account: BankAccount
        :param amount: int
        >>> account1 = BankAccount()
        >>> account2 = BankAccount()
        >>> account1.deposit(1000)
        >>> account1.transfer(account2, 300)
        account1.balance = 700 account2.balance = 300
        """
        if not isinstance(other_account, BankAccount):
            raise TypeError("other_account must be of type BankAccount")
        self.withdraw(amount)
        other_account.deposit(amount)


# Example usage:
def main():
    account1 = BankAccount(1000)
    account2 = BankAccount()

    print("Initial balance of account1:", account1.view_balance())
    print("Initial balance of account2:", account2.view_balance())

    account1.transfer(account2, 300)

    print("Balance of account1 after transfer:", account1.view_balance())
    print("Balance of account2 after transfer:", account2.view_balance())

    try:
        account2.withdraw(500)
    except ValueError as e:
        print(e)

    try:
        account1.transfer(account2, -100)
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()
