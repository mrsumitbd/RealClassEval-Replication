import copy
import ROOT

class MeritSkimmer:
    """
    Adapted from Luca B.'s fermiMusic code...
    """

    def __init__(self, chain):
        print('Loading input chain...')
        self.InputChain = chain
        self.OutputChain = None
        print('Done, %d event(s) found.' % self.InputChain.Draw('', '', 'goff'))

    def skim(self, outputFilePath, cut='', branches=None):
        if isinstance(outputFilePath, ROOT.TFile):
            outputFile = outputFilePath
        else:
            outputFile = ROOT.TFile(outputFilePath, 'RECREATE')
        if branches is not None and branches:
            self.InputChain.SetBranchStatus('*', False)
            for b in branches:
                self.InputChain.SetBranchStatus(b, True)
        outputChain = self.InputChain.CopyTree(cut)
        self.outputChain = copy.copy(outputChain)
        outputChain.Write()
        print('Done, %d event(s) written to file.' % self.outputChain.GetEntries())
        if not isinstance(outputFilePath, ROOT.TFile):
            outputFile.Close()
        return self.outputChain