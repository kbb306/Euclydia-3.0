import smaz
class smaz_wrapper:
    @staticmethod
    def encode(phrase: str) -> str:
        """Compress text and return a latin1-safe string."""
        compressed = smaz.compress(phrase)      # returns str in your version
        return compressed

    @staticmethod
    def decode(codephrase: str) -> str:
        """Decode a latin1-safe string to original text."""
        compressed = codephrase.encode('latin1')  # back to bytes
        decompressed = smaz.decompress(compressed)
        return decompressed
