import smaz
class smaz_wrapper:
    @staticmethod
    def encode(phrase: str) -> str:
        """Compress text and return a latin1-safe string."""
        compressed = smaz.compress(phrase).encode('latin1').decode('latin1')      # returns str in your version
        return compressed

    @staticmethod
    def decode(codephrase: str) -> str:
        """Decode a latin1-safe string to original text."""
        decompressed = smaz.decompress(codephrase.encode('latin1'))
        return decompressed
