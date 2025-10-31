import snippet_246 as module_0
import inspect as module_1

def test_case_0():
    secure_serializer_0 = module_0.SecureSerializer()
    secure_serializer_0.serialize(secure_serializer_0)

def test_case_1():
    secure_serializer_0 = module_0.SecureSerializer()
    secure_serializer_0.deserialize(secure_serializer_0)

def test_case_2():
    module_0.SecureSerializer()

def test_case_3():
    secure_serializer_0 = module_0.SecureSerializer()
    var_0 = module_1.trace(secure_serializer_0)
    secure_serializer_0.deserialize(var_0, allow_high_risk=secure_serializer_0)

def test_case_4():
    secure_serializer_0 = module_0.SecureSerializer()
    var_0 = module_1.trace(secure_serializer_0)
    secure_serializer_0.serialize(var_0)

def test_case_5():
    secure_serializer_0 = module_0.SecureSerializer()
    var_0 = module_1.getcoroutinelocals(secure_serializer_0)
    secure_serializer_0.deserialize(var_0, allow_high_risk=secure_serializer_0)

def test_case_6():
    secure_serializer_0 = module_0.SecureSerializer()
    var_0 = module_1.getcoroutinelocals(secure_serializer_0)
    secure_serializer_0.deserialize(var_0, allow_high_risk=secure_serializer_0)
    secure_serializer_0.serialize(var_0, secure_serializer_0)

def test_case_7():
    secure_serializer_0 = module_0.SecureSerializer()
    secure_serializer_1 = module_0.SecureSerializer()
    secure_serializer_0.serialize(secure_serializer_1)
    var_0 = module_1.getmembers(secure_serializer_1)
    secure_serializer_1.deserialize(var_0)

def test_case_8():
    secure_serializer_0 = module_0.SecureSerializer()
    secure_serializer_1 = module_1.formatannotationrelativeto(secure_serializer_0)
    secure_serializer_0.serialize(secure_serializer_1)