import smaz
#print("Using smaz from:", smaz.__file__)

class smaz_wrapper(smaz):
    def __init__(self):
        super.__init__(self)
        
    def encode(self,phrase):
        codephrase = self.compress(phrase)
        bytes = codephrase.encode('latin1')
        out = bytes.decode('latin1')
        return out

    def decode(self,codephrase):
        out = self.decompress(codephrase)
        return out




