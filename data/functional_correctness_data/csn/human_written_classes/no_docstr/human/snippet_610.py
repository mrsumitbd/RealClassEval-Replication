class ArtificialTaxon:
    count = 0

    def __init__(self):
        self.name = f'x{ArtificialTaxon.count}'
        ArtificialTaxon.count += 1

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name