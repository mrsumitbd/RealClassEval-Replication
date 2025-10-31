import torch
from typing import Optional, Union

class PackedTensor:
    """Wrapper around a list of torch tensors and a dimension along which to pack the tensors.

    This class is used to wrap a list of tensors along with a `dim_to_pack` parameter.
    It can be used for data that can be packed along different dimensions (such as multimodal data).

    `dim_to_pack` is used to specify the dimension along which to pack the tensors.

    The list of tensors can be returned as a single packed tensor by calling `as_tensor` which will concatenate the tensors along the `dim_to_pack` dimension.
    """

    def __init__(self, tensors: Union[torch.Tensor, list[torch.Tensor]], dim_to_pack: int) -> None:
        assert tensors is not None, 'Input tensors to PackedTensor cannot be None'
        if isinstance(tensors, torch.Tensor):
            self.tensors: list[torch.Tensor] = [tensors]
        elif isinstance(tensors, list):
            assert len(tensors) > 0, 'Input tensors to PackedTensor must be a non-empty list'
            self.tensors: list[torch.Tensor] = tensors
        else:
            raise ValueError(f'Unsupported type for input tensors to PackedTensor: {type(tensors)}')
        self.dim_to_pack = dim_to_pack

    def as_tensor(self, device: Optional[torch.device]=None) -> torch.Tensor:
        if device is not None:
            self.tensors = [item.to(device) for item in self.tensors]
        return torch.cat(self.tensors, dim=self.dim_to_pack).to(device)

    def __len__(self) -> int:
        return len(self.tensors)

    def to(self, device: str | torch.device) -> 'PackedTensor':
        self.tensors = [item.to(device) for item in self.tensors]
        return self

    def slice(self, indices: Union[list[int], torch.Tensor]) -> 'PackedTensor':
        idx = indices.tolist() if isinstance(indices, torch.Tensor) else indices
        tensors = [self.tensors[i] for i in idx]
        return PackedTensor(tensors, self.dim_to_pack)

    @classmethod
    def concat(cls, from_packed_tensors: list['PackedTensor']) -> 'PackedTensor':
        """Concatenate a list of PackedTensor objects into a single PackedTensor.

        The underlying tensors from the PackedTensors are combined into a single list of tensors and used to create a new PackedTensor.

        Each batch must have the same dim_to_pack.

        Example:
        ```{doctest}
        >>> import torch
        >>> from nemo_rl.data.multimodal_utils import PackedTensor
        >>> p1 = PackedTensor([torch.tensor([1, 2, 3]), torch.tensor([4, 5, 6])], dim_to_pack=0)
        >>> p2 = PackedTensor([torch.tensor([7, 8, 9])], dim_to_pack=0)
        >>> p3 = PackedTensor.concat([p1, p2])
        >>> p3.tensors
        [tensor([1, 2, 3]), tensor([4, 5, 6]), tensor([7, 8, 9])]
        >>> p3.as_tensor()
        tensor([1, 2, 3, 4, 5, 6, 7, 8, 9])
        >>>
        ```
        """
        dim_to_packs = [batch.dim_to_pack for batch in from_packed_tensors]
        assert len(set(dim_to_packs)) == 1, 'All packed tensors must have the same dim_to_pack'
        tensors = []
        for packed_tensor in from_packed_tensors:
            tensors.extend(packed_tensor.tensors)
        dim_to_pack = dim_to_packs[0]
        return cls(tensors, dim_to_pack)

    @classmethod
    def flattened_concat(cls, from_packed_tensors: list['PackedTensor']) -> 'PackedTensor':
        """Given a list of PackedTensor objects, flattens each PackedTensor and then concatenates them into a single PackedTensor.

        Each PackedTensor is first flattened by packing along the PackedTensor's `dim_to_pack` dimension. Then, the resulting flattened tensors are used to create a new PackedTensor.

        This is different from `PackedTensor.concat` which simply extends the underlying list of tensors. This is important because the `slice` and `__len__` methods operate on the underlying list of tensors. Note, however, that calling `as_tensor` on the resulting PackedTensor will result in the same tensor as `concat`.

        Each batch must have the same dim_to_pack.

        Example:
        ```{doctest}
        >>> import torch
        >>> from nemo_rl.data.multimodal_utils import PackedTensor
        >>> p1 = PackedTensor([torch.tensor([1, 2, 3]), torch.tensor([4, 5, 6])], dim_to_pack=0)
        >>> p2 = PackedTensor([torch.tensor([7, 8, 9])], dim_to_pack=0)
        >>> p3 = PackedTensor.flattened_concat([p1, p2])
        >>> p3.tensors
        [tensor([1, 2, 3, 4, 5, 6]), tensor([7, 8, 9])]
        >>> p3.as_tensor()
        tensor([1, 2, 3, 4, 5, 6, 7, 8, 9])
        >>>
        ```
        """
        dim_to_packs = [batch.dim_to_pack for batch in from_packed_tensors]
        assert len(set(dim_to_packs)) == 1, 'All packed tensors must have the same dim_to_pack'
        tensors = [p.as_tensor() for p in from_packed_tensors]
        return cls(tensors, from_packed_tensors[0].dim_to_pack)