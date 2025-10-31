
from decimal import Decimal, getcontext, ROUND_HALF_UP
from typing import Any, Dict, Optional


class PrecisionPreservingDataHandler:
    """
    A utility class for handling price data with precision preservation.
    """

    # In‑memory storage for price data keyed by an identifier.
    _storage: Dict[Any, Decimal] = {}

    @staticmethod
    def validate_system_precision() -> Dict[str, Any]:
        """
        Inspect the current Decimal context and return its configuration.
        """
        ctx = getcontext()
        return {
            "precision": ctx.prec,
            "rounding": ctx.rounding,
            "capitals": ctx.capitals,
            "Emax": ctx.Emax,
            "Emin": ctx.Emin,
        }

    @staticmethod
    def store_price_data(data: Any) -> Any:
        """
        Store a price value in the internal dictionary.

        Parameters
        ----------
        data : dict
            Must contain at least the keys 'id' and 'price'.
            'price' can be a float, int, str, or Decimal.

        Returns
        -------
        dict
            The stored record with the price converted to Decimal.
        """
        if not isinstance(data, dict):
            raise TypeError("data must be a dict with 'id' and 'price' keys")

        if "id" not in data or "price" not in data:
            raise ValueError("data must contain 'id' and 'price' keys")

        record_id = data["id"]
        price = Decimal(str(data["price"]))  # Convert to Decimal safely

        # Store the price in the internal dictionary
        PrecisionPreservingDataHandler._storage[record_id] = price

        return {"id": record_id, "price": price}

    @staticmethod
    def retrieve_price_data(record_id: Any) -> Optional[Decimal]:
        """
        Retrieve a stored price by its identifier.

        Parameters
        ----------
        record_id : Any
            The key used when storing the price.

        Returns
        -------
        Decimal | None
            The stored price, or None if the key does not exist.
        """
        return PrecisionPreservingDataHandler._storage.get(record_id)

    @staticmethod
    def preserve_calculation_precision(result: float, operation: str) -> float:
        """
        Quantize a calculation result to a precision that depends on the operation.

        Parameters
        ----------
        result : float
            The raw result of a calculation.
        operation : str
            One of 'add', 'subtract', 'multiply', 'divide'.

        Returns
        -------
        float
            The result rounded to the appropriate number of decimal places.
        """
        # Define decimal places per operation
        places_map = {
            "add": Decimal("0.01"),
            "subtract": Decimal("0.01"),
            "multiply": Decimal("0.0001"),
            "divide": Decimal("0.0001"),
        }

        # Default to 2 decimal places if operation is unknown
        quantize_exp = places_map.get(operation.lower(), Decimal("0.01"))

        dec_result = Decimal(str(result))
        quantized = dec_result.quantize(quantize_exp, rounding=ROUND_HALF_UP)
        return float(quantized)
