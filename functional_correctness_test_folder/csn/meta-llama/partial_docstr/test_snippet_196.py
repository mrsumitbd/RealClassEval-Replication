import snippet_196 as module_0

def test_case_0():
    bool_0 = False
    module_0.Mechanism(bool_0)

def test_case_1():
    bool_0 = False
    mechanism_0 = module_0.Mechanism(bool_0)
    mechanism_0.to_native()

def test_case_2():
    bytes_0 = b'\tc\xf8\x14\x9a<so\xcf\x02\xf9b;'

def test_case_3():
    bool_0 = True
    mechanism_0 = module_0.Mechanism(bool_0)
    mechanism_0.to_native()
    module_0.Mechanism(bool_0, mechanism_0)