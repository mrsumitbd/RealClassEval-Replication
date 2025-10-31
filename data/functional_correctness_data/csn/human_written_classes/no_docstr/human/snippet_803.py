class IdentityMap:

    def __init__(self, input, output):
        print('Applying identity transformation...')
        self.input = input
        self.output = output

    def forward(self, pixx, pixy):
        return (pixx, pixy)