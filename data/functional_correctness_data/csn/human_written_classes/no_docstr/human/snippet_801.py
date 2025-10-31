import glob
from datetime import datetime
from matplotlib.backends.backend_pdf import PdfPages
import os
from matplotlib import pyplot as plt
from astropy.io import fits
import json

class Datasets:

    def __init__(self, parent_dir, num_levels=1):
        levels = os.path.sep.join('*' * num_levels)
        dirnames = os.path.join(parent_dir, levels)
        self.parent_dir = os.path.split(os.path.abspath(parent_dir))[1]
        self.dirnames = dirnames
        drznames = glob.glob(os.path.join(dirnames, '*drz.fits'))
        prodnames = glob.glob(os.path.join(dirnames, '*drc.fits'))
        for drz in drznames:
            drzc = drz.replace('drz.fits', 'drc.fits')
            if drzc not in prodnames:
                prodnames.append(drz)
        self.prodnames = [d for d in prodnames if 'current' not in d]
        self.wcsnames = []
        self.instruments = []
        self.detectors = []
        self.targnames = []
        self.texptimes = []
        print('Processing {} products'.format(len(self.prodnames)))
        for p in self.prodnames:
            with fits.open(p) as prod:
                phdu = prod[0].header
                sci = prod[1].header if len(prod) > 1 else phdu
                self.wcsnames.append(sci['wcsname'])

    def create_summary(self):
        font_size = 12
        first_page = plt.figure(figsize=(8.5, 11))
        first_page.clf()
        txt = 'Summary of Alignment Results from {}'.format(self.parent_dir)
        first_page.text(0.5, 0.95, txt, transform=first_page.transFigure, size=font_size, ha='center')
        txt = 'Total Datasets : {}'.format(len(self.prodnames))
        first_page.text(0.1, 0.85, txt, transform=first_page.transFigure, size=font_size, ha='left')
        apost = len([w for w in self.wcsnames if 'FIT' in w])
        defwcs = len([w for w in self.wcsnames if '-' not in w or 'None' in w or w.strip() == ''])
        apri = len(self.wcsnames) - apost - defwcs
        relonly = len([w for w in self.wcsnames if 'NONE' in w])
        txt = 'Datasets with a posteriori WCS : {}'.format(apost)
        first_page.text(0.1, 0.8, txt, transform=first_page.transFigure, size=font_size, ha='left')
        txt = 'Datasets with a posteriori relative alignment : {}'.format(relonly)
        first_page.text(0.1, 0.75, txt, transform=first_page.transFigure, size=font_size, ha='left')
        txt = 'Datasets with a priori WCS : {}'.format(apri)
        first_page.text(0.1, 0.7, txt, transform=first_page.transFigure, size=font_size, ha='left')
        txt = 'Datasets with pipeline-default WCS : {}'.format(defwcs)
        first_page.text(0.1, 0.65, txt, transform=first_page.transFigure, size=font_size, ha='left')
        now = datetime.now()
        rtime = datetime.strftime(now, '%b %d %Y  %H:%M:%S')
        txt = 'Report created at {}'.format(rtime)
        first_page.text(0.1, 0.1, txt, transform=first_page.transFigure, size=font_size, ha='left')
        return first_page

    def create(self, pdfname='multipage_pdf.pdf', num_datasets=None):
        if num_datasets is not None:
            prodnames = self.prodnames[:num_datasets]
            wcsnames = self.wcsnames[:num_datasets]
        else:
            prodnames = self.prodnames
            wcsnames = self.wcsnames
        json_summary = {}
        with PdfPages(pdfname) as pdf:
            first_page = self.create_summary()
            pdf.savefig(first_page)
            plt.close()
            plt.ioff()
            for p, w in zip(prodnames, wcsnames):
                result, summary = create_product_page(p, wcsname=w)
                if result is not None:
                    pdf.savefig(result)
                    plt.close()
                    json_summary[os.path.basename(p)] = summary
            plt.ion()
        with open(pdfname.replace('.pdf', '_summary.json'), 'w') as jsonfile:
            json.dump(json_summary, jsonfile)