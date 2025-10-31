
import json
from typing import Any, Dict, Type, TypeVar

T = TypeVar('T', bound='Serializable')


class Serializable:
    '''This is the superclass of all serializable objects.'''

    def save(self, out_file: str) -> None:
        """
        Serialize the object's __dict__ to a JSON file.

        Parameters
        ----------
        out_file : str
            Path to the output file where the JSON representation will be written.
        """
        with open(out_file, 'w', encoding='utf-8') as f:
            json.dump(self.__dict__, f, ensure_ascii=False, indent=4)

    @classmethod
    def load(cls: Type[T], in_file: str, instantiate: bool = True) -> Any:
        """
        Load a JSON file and optionally instantiate an object of the class.

        Parameters
        ----------
        in_file : str
            Path to the input JSON file.
        instantiate : bool, default True
            If True, return an instance of the class initialized with the data.
            If False, return the raw dictionary loaded from the file.

        Returns
        -------
        Union[T, Dict[str, Any]]
            Either an instance of the class or the raw data dictionary.
        """
        with open(in_file, 'r', encoding='utf-8') as f:
            data: Dict[str, Any] = json.load(f)

        if instantiate:
            return cls(**data)  # type: ignore[arg-type]
        return data

    @classmethod
    def _instantiated_load(cls: Type[T], in_file: str, **kwargs: Any) -> T:
        """
        Load a JSON file, merge it with additional keyword arguments, and instantiate.

        Parameters
        ----------
        in_file : str
            Path to the input JSON file.
        **kwargs : Any
            Additional keyword arguments that override or extend the loaded data.

        Returns
        -------
        T
            An instance of the class initialized with the merged data.
        """
        with open(in_file, 'r', encoding='utf-8') as f:
            data: Dict[str, Any] = json.load(f)

        data.update(kwargs)
        return cls(**data)  # type: ignore[arg-type]
