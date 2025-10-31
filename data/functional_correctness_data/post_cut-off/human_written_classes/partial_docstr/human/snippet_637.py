from typing import List, Optional
import re
from wave_lang.support.ir_imports import Context, F64Type, IntegerType, IrType, Location, Operation, RankedTensorType, ShapedType, Value, tensor_d
import functools

class NativeTypeConverter:

    def __init__(self, context: Context):
        self._context = context
        self.torch_type_to_native = functools.lru_cache(maxsize=None)(self.torch_type_to_native)

    def torch_type_to_native(self, torch_type: IrType, signless: bool=True) -> IrType:
        """Converts a presumed torch type to a corresponding native type.

        This mirrors the type conversion in torch-mlir's BackendTypeConversion.cpp.

        As an example:
          !torch.int -> i64
          !torch.float -> f64
          !torch.bool -> i1
          !torch.vtensor -> tensor

        If `signless=False`, then integer types will retain their signs.
        """
        m = re.match(DECOMPOSE_TORCH_TYPE_PATTERN, str(torch_type))
        if m:
            name, _, params_str = m.groups()
            with self._context:
                if name == 'bool':
                    return IntegerType.get_signless(1)
                if name == 'int':
                    return IntegerType.get_signless(64) if signless else IntegerType.get_signed(64)
                elif name == 'float':
                    return F64Type.get()
                elif name == 'vtensor':
                    tm = re.match(DECOMPOSE_TENSOR_PARAMS_PATTERN, params_str)
                    assert tm, f'Could not parse !torch.vtensor params: {params_str}'
                    dim_list_str, dtype_str = tm.groups()
                    dim_list = parse_tensor_dim_list(dim_list_str)
                    dtype = self.convert_torch_element_type_to_native(IrType.parse(dtype_str), signless=signless)
                    with Location.unknown():
                        return RankedTensorType.get(dim_list, dtype)
        raise TypeError(f'Unsupported torch type conversion for {torch_type}')

    def convert_torch_element_type_to_native(self, torch_type: IrType, signless: bool=True) -> IrType:
        if signless:
            if IntegerType.isinstance(torch_type):
                signed_int_type = IntegerType(torch_type)
                return IntegerType.get_signless(signed_int_type.width)
        return torch_type

    def materialize_native_to_torch(self, native_value: Value, torch_type: IrType, *, static_info_cast: bool=False) -> Value:
        native_type = native_value.type
        if RankedTensorType.isinstance(native_type):
            if static_info_cast:
                required_native_type = self.torch_type_to_native(torch_type)
                if required_native_type != native_type:
                    native_value = tensor_d.cast(required_native_type, native_value)
            return Operation.create('torch_c.from_builtin_tensor', results=[torch_type], operands=[native_value]).result
        elif IntegerType.isinstance(native_type):
            int_type = IntegerType(native_type)
            width = int_type.width
            if width == 1:
                op_name = 'torch_c.from_i1'
            elif width == 64:
                op_name = 'torch_c.from_i64'
            else:
                raise TypeError(f'Unsupported integer bit width for native->torch ABI: {int_type}')
            return Operation.create(op_name, results=[torch_type], operands=[native_value]).result
        elif F64Type.isinstance(native_type):
            return Operation.create('torch_c.from_f64', results=[torch_type], operands=[native_type]).result
        else:
            raise TypeError(f'Unsupported native->torch ABI type conversion: {native_type} -> {torch_type}')

    def materialize_torch_to_native(self, torch_value: Value, *, static_info_cast_to: Optional[IrType]=None) -> Value:
        native_type = self.torch_type_to_native(torch_value.type)
        if RankedTensorType.isinstance(native_type):
            builtin_tensor_value = Operation.create('torch_c.to_builtin_tensor', results=[native_type], operands=[torch_value]).result
            if static_info_cast_to is not None and static_info_cast_to != native_type:
                builtin_tensor_value = tensor_d.cast(static_info_cast_to, builtin_tensor_value)
            return builtin_tensor_value
        elif IntegerType.isinstance(native_type):
            int_type = IntegerType(native_type)
            width = int_type.width
            if width == 1:
                op_name = 'torch_c.to_i1'
            elif width == 64:
                op_name = 'torch_c.to_i64'
            else:
                raise TypeError(f'Unsupported integer bit width for torch->native ABI: {int_type}')
            return Operation.create(op_name, results=[native_type], operands=[torch_value]).result
        elif F64Type.isinstance(native_type):
            return Operation.create('torch_c.to_f64', results=[native_type], operands=[torch_value]).result
        else:
            raise TypeError(f'Unsupported torch->native ABI type conversion: {native_type} -> {native_type}')