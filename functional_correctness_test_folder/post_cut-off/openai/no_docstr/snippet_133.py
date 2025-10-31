
from typing import Any, Dict, Tuple


class Text_border:
    """
    Represents a text border with an alpha value, color, and width.
    """

    def __init__(
        self,
        *,
        alpha: float = 1.0,
        color: Tuple[float, float, float] = (0.0, 0.0, 0.0),
        width: float = 1.0,
    ) -> None:
        """
        Initialize a Text_border instance.

        Parameters
        ----------
        alpha : float, optional
            Transparency of the border (0.0 fully transparent, 1.0 fully opaque).
        color : Tuple[float, float, float], optional
            RGB color components, each in the range [0.0, 1.0].
        width : float, optional
            Width of the border in pixels.
        """
        self.alpha = float(alpha)
        self.color = tuple(float(c) for c in color)
        self.width = float(width)

    def export_json(self) -> Dict[str, Any]:
        """
        Export the border properties as a JSON-serializable dictionary.

        Returns
        -------
        Dict[str, Any]
            Dictionary containing the border properties.
        """
        return {
            "alpha": self.alpha,
            "color": self.color,
            "width": self.width,
        }
