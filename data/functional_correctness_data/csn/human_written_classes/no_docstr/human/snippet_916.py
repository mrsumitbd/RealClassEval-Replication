class PrintState:

    def __init__(self, sep='\n', add='    ', printFirst=True, callSource=None, definedVars=[], globalVars=[], functionScope='', indexRef=True):
        self.sep = sep
        self.add = add
        self.printFirst = printFirst
        self.callSource = callSource
        self.definedVars = definedVars
        self.globalVars = globalVars
        self.functionScope = functionScope
        self.indexRef = indexRef

    def copy(self, sep=None, add=None, printFirst=None, callSource=None, definedVars=None, globalVars=None, functionScope=None, indexRef=None):
        return PrintState(self.sep if sep is None else sep, self.add if add is None else add, self.printFirst if printFirst is None else printFirst, self.callSource if callSource is None else callSource, self.definedVars if definedVars is None else definedVars, self.globalVars if globalVars is None else globalVars, self.functionScope if functionScope is None else functionScope, self.indexRef if indexRef is None else indexRef)