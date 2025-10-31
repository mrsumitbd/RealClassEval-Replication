
import pickle
from typing import Any, Type, TypeVar, Union, IO

T = TypeVar('T', bound='Serializable')


class Serializable:
    """
    A simple mixin that provides pickle‑based serialization.
    """

    def save(self, out_file: Union[str, IO[bytes]]) -> None:
        """
        Serialize the instance to the given file object or file path.

        Parameters
        ----------
        out_file : str or file-like object
            Destination for the pickled data. If a string is provided,
            it is treated as a file path and opened in binary write mode.
        """
        if isinstance(out_file, str):
            with open(out_file, 'wb') as f:
                pickle.dump(self, f)
        else:
            pickle.dump(self, out_file)

    @classmethod
    def load(cls: Type[T], in_file: Union[str, IO[bytes]], instantiate: bool = True) -> Union[T, Any]:
        """
        Load a pickled object from the given file object or file path.

        Parameters
        ----------
        in_file : str or file-like object
            Source of the pickled data. If a string is provided,
            it is treated as a file path and opened in binary read mode.
        instantiate : bool, default True
            If True, return the deserialized instance.
            If False, return the raw data (useful for custom handling).

        Returns
        -------
        T or Any
            The deserialized object or raw data.
        """
        if isinstance(in_file, str):
            with open(in_file, 'rb') as f:
                data = pickle.load(f)
        else:
            data = pickle.load(in_file)

        if instantiate:
            return cls._instantiated_load(data)
        return data

    @classmethod
    def _instantiated_load(cls: Type[T], data: Any, **kwargs: Any) -> T:
        """
        Helper that returns an instance of the class from the loaded data.
        Any keyword arguments are applied as attributes to the instance.

        Parameters
        ----------
        data : Any
            The object returned by pickle.load.
        **kwargs : Any
            Attributes to set on the instance after loading.

        Returns
        -------
        T
            The instance of the class.
        """
        if not isinstance(data, cls):
            raise TypeError(
                f"Loaded object is not an instance of {cls.__name__}")
        for key, value in kwargs.items():
            setattr(data, key, value)
        return data
