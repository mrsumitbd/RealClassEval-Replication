import numpy

class SVMConverter:
    """
    Converts a SVM model trained with *svmlib*.
    """

    @staticmethod
    def validate(svm_node):
        try:
            hasattr(svm_node, 'param')
            hasattr(svm_node, 'SV')
            hasattr(svm_node, 'nSV')
            hasattr(svm_node, 'sv_coef')
            hasattr(svm_node, 'l')
            hasattr(svm_node.param, 'gamma')
            hasattr(svm_node.param, 'coef0')
            hasattr(svm_node.param, 'degree')
            hasattr(svm_node.param, 'kernel_type')
            hasattr(svm_node, 'rho')
        except AttributeError as e:
            raise RuntimeError('Missing type from svm node:' + str(e))

    @staticmethod
    def get_sv(svm_node):
        labels = svm_node.get_labels()
        sv = svm_node.get_SV()
        if len(sv) == 0:
            raise RuntimeError('No support vector machine. This usually happens with very small datasets or the training failed.')
        maxk = max(max((row.keys() for row in sv)))
        mat = numpy.zeros((len(sv), maxk + 1), dtype=numpy.float32)
        for i, row in enumerate(sv):
            for k, v in row.items():
                if k == -1:
                    k = 0
                try:
                    mat[i, k] = v
                except IndexError:
                    raise RuntimeError('Issue with one dimension\nlabels={0}\n#sv={1}\nshape={2}\npos={3}x{4}-maxk={5}-svm.l={6}\nrow={7}'.format(labels, sv, mat.shape, i, k, maxk, svm_node.l, row))
        mat = mat[:, 1:]
        return numpy.array(mat.ravel(), dtype=float)

    @staticmethod
    def convert(operator, scope, container, svm_node, inputs, model_name, nb_class):
        kt = svm_node.param.kernel_type
        if kt == svm.RBF:
            kt = 'RBF'
        elif kt == svm.SIGMOID:
            kt = 'SIGMOID'
        elif kt == svm.POLY:
            kt = 'POLY'
        elif kt == svm.LINEAR:
            kt = 'LINEAR'
        else:
            raise RuntimeError('Unexpected value for kernel: {0}'.format(kt))

        def copy_sv_coef(sv_coef):
            nrc = svm_node.nr_class - 1
            res = numpy.zeros((svm_node.l, nrc), dtype=numpy.float64)
            for i in range(0, svm_node.l):
                for j in range(nrc):
                    res[i, j] = svm_node.sv_coef[j][i]
            return res.T
        if nb_class > 2:
            coef = copy_sv_coef(svm_node.sv_coef)
        else:
            coef = numpy.array(svm_node.get_sv_coef()).ravel()
        atts = dict(kernel_type=kt, kernel_params=[float(_) for _ in [svm_node.param.gamma, svm_node.param.coef0, svm_node.param.degree]], coefficients=list(coef.ravel()))
        return dict(node='SVMConverter', inputs=operator.input_full_names, outputs=[o.full_name for o in operator.outputs], op_domain='ai.onnx.ml', attrs=atts)