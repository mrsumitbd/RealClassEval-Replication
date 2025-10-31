
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
            r = carry
            r += 1 if num1[i] == '1' else 0
            r += 1 if num2[i] == '1' else 0

            result.append('1' if r % 2 == 1 else '0')
            carry = 0 if r < 2 else 1

        if carry != 0:
            result.append('1')

        result.reverse()

        return ''.join(result)

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
        max_len = max(len(num1), len(num2))
        num1 = num1.zfill(max_len)
        num2 = num2.zfill(max_len)

        borrow = 0
        result = []

        for i in range(max_len - 1, -1, -1):
            r = int(num1[i]) - int(num2[i]) - borrow
            if r < 0:
                r += 2
                borrow = 1
            else:
                borrow = 0
            result.append(str(r))

        result.reverse()

        # Remove leading zeros
        result_str = ''.join(result).lstrip('0')
        if not result_str:
            result_str = '0'

        # Check if the result is negative
        if len(result_str) < max_len:
            result_str = '-' + result_str

        return result_str

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
        len1, len2 = len(num1), len(num2)
        if len1 == 0 or len2 == 0:
            return "0"

        result = [0] * (len1 + len2)

        i_n1 = 0
        i_n2 = 0

        for i in range(len1 - 1, -1, -1):
            carry = 0
            n1 = int(num1[i])
            i_n2 = 0

            for j in range(len2 - 1, -1, -1):
                n2 = int(num2[j])
                sum = n1 * n2 + result[i_n1 + i_n2] + carry
                carry = sum // 2
                result[i_n1 + i_n2] = sum % 2

                i_n2 += 1

            if carry > 0:
                result[i_n1 + i_n2] += carry

            i_n1 += 1

        i = len(result) - 1
        while i >= 0 and result[i] == 0:
            i -= 1

        if i == -1:
            return "0"

        result_str = []
        while i >= 0:
            result_str.append(str(result[i]))
            i -= 1

        return ''.join(result_str)
