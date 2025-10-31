import wx

class Printer:

    def __init__(self, parent, title=None, canvas=None, width=6.0, margin=0.5):
        """initialize printer settings using wx methods"""
        self.parent = parent
        self.canvas = canvas
        self.pwidth = width
        self.pmargin = margin
        self.title = title
        self.printerData = wx.PrintData()
        self.printerData.SetPaperId(wx.PAPER_LETTER)
        self.printerData.SetPrintMode(wx.PRINT_MODE_PRINTER)
        self.printerPageData = wx.PageSetupDialogData()
        self.printerPageData.SetMarginBottomRight((25, 25))
        self.printerPageData.SetMarginTopLeft((25, 25))
        self.printerPageData.SetPrintData(self.printerData)

    def Setup(self, event=None):
        """set up figure for printing.  Using the standard wx Printer
        Setup Dialog. """
        if hasattr(self, 'printerData'):
            data = wx.PageSetupDialogData()
            data.SetPrintData(self.printerData)
        else:
            data = wx.PageSetupDialogData()
        data.SetMarginTopLeft((15, 15))
        data.SetMarginBottomRight((15, 15))
        dlg = wx.PageSetupDialog(None, data)
        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetPageSetupData()
            tl = data.GetMarginTopLeft()
            br = data.GetMarginBottomRight()
        self.printerData = wx.PrintData(data.GetPrintData())
        dlg.Destroy()

    def Preview(self, title=None, event=None):
        """ generate Print Preview with wx Print mechanism"""
        if title is None:
            title = self.title
        if self.canvas is None:
            self.canvas = self.parent.canvas
        po1 = PrintoutWx(self.parent.canvas, title=title, width=self.pwidth, margin=self.pmargin)
        po2 = PrintoutWx(self.parent.canvas, title=title, width=self.pwidth, margin=self.pmargin)
        self.preview = wx.PrintPreview(po1, po2, self.printerData)
        if self.preview.IsOk():
            self.preview.SetZoom(85)
            frameInst = self.parent
            while not isinstance(frameInst, wx.Frame):
                frameInst = frameInst.GetParent()
            frame = wx.PreviewFrame(self.preview, frameInst, 'Preview')
            frame.Initialize()
            frame.SetSize((850, 650))
            frame.Centre(wx.BOTH)
            frame.Show(True)

    def Print(self, title=None, event=None):
        """ Print figure using wx Print mechanism"""
        pdd = wx.PrintDialogData()
        pdd.SetPrintData(self.printerData)
        pdd.SetToPage(1)
        printer = wx.Printer(pdd)
        if title is None:
            title = self.title
        printout = PrintoutWx(self.parent.canvas, title=title, width=self.pwidth, margin=self.pmargin)
        print_ok = printer.Print(self.parent, printout, True)
        if not print_ok and (not printer.GetLastError() == wx.PRINTER_CANCELLED):
            wx.MessageBox('There was a problem printing.\n            Perhaps your current printer is not set correctly?', 'Printing', wx.OK)
        printout.Destroy()