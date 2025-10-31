
class BigNumCalculator:
    """
    This is a class that implements big number calculations, including adding, subtracting and multiplying.
    """

    @staticmethod
    def add(num1, num2):
        """
        Adds two big numbers.
        :param num1: The first number to add,str.
        :param num2: The second number to add,str.
        :return: The sum of the two numbers,str.
        >>> bigNum = BigNumCalculator()
        >>> bigNum.add("12345678901234567890", "98765432109876543210")
        '111111111011111111100'
        """
        max_len = max(len(num1), len(num2))
        num1 = num1.zfill(max_len)
        num2 = num2.zfill(max_len)
        carry = 0
        result = []
        for i in range(max_len - 1, -1, -1):
            digit_sum = int(num1[i]) + int(num2[i]) + carry
            carry = digit_sum // 10
            result.append(str(digit_sum % 10))
        if carry > 0:
            result.append(str(carry))
        return ''.join(reversed(result))

    @staticmethod
    def subtract(num1, num2):
        """
        Subtracts two big numbers.
        :param num1: The first number to subtract,str.
        :param num2: The second number to subtract,str.
        :return: The difference of the two numbers,str.
        >>> bigNum = BigNumCalculator()
        >>> bigNum.subtract("12345678901234567890", "98765432109876543210")
        '-86419753208641975320'
        """
        def _subtract(a, b):
            max_len = max(len(a), len(b))
            a = a.zfill(max_len)
            b = b.zfill(max_len)
            borrow = 0
            result = []
            for i in range(max_len - 1, -1, -1):
                digit_diff = int(a[i]) - int(b[i]) - borrow
                if digit_diff < 0:
                    digit_diff += 10
                    borrow = 1
                else:
                    borrow = 0
                result.append(str(digit_diff))
            return ''.join(reversed(result)).lstrip('0') or '0'

        if len(num1) < len(num2) or (len(num1) == len(num2) and num1 < num2):
            return '-' + _subtract(num2, num1)
        else:
            return _subtract(num1, num2)

    @staticmethod
    def multiply(num1, num2):
        """
        Multiplies two big numbers.
        :param num1: The first number to multiply,str.
        :param num2: The second number to multiply,str.
        :return: The product of the two numbers,str.
        >>> bigNum = BigNumCalculator()
        >>> bigNum.multiply("12345678901234567890", "98765432109876543210")
        '1219326311370217952237463801111263526900'
        """
        if num1 == '0' or num2 == '0':
            return '0'
        len1 = len(num1)
        len2 = len(num2)
        result = [0] * (len1 + len2)
        for i in range(len1 - 1, -1, -1):
            for j in range(len2 - 1, -1, -1):
                product = int(num1[i]) * int(num2[j])
                total = product + result[i + j + 1]
                result[i + j + 1] = total % 10
                result[i + j] += total // 10
        result_str = ''.join(map(str, result))
        return result_str.lstrip('0') or '0'
