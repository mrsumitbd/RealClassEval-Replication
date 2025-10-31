class AnyLibSvmConverter:

    @staticmethod
    def select(svm_node):
        if svm_node.param.svm_type in (svm.C_SVC, svm.NU_SVC):
            return SVCConverter
        if svm_node.param.svm_type in (svm.EPSILON_SVR, svm.NU_SVR):
            return SVRConverter
        raise RuntimeError("svm_node type is unexpected '{0}'".format(svm_node.param.svm_type))

    @staticmethod
    def validate(svm_node):
        sel = AnyLibSvmConverter.select(svm_node)
        sel.validate(svm_node)

    @staticmethod
    def convert(operator, scope, container, svm_node, inputs):
        sel = AnyLibSvmConverter.select(svm_node)
        sel.convert(operator, scope, container, svm_node, inputs)