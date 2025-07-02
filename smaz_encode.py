import smaz
class SmazWrapper:
    @staticmethod
    def encode(phrase: str) -> str:
        """Compress text and return a latin1-safe string."""
        compressed = smaz.compress(phrase)      # returns str in your version
        return compressed.encode('latin1').decode('latin1')

    @staticmethod
    def decode(codephrase: str) -> str:
        """Decode a latin1-safe string to original text."""
        compressed = codephrase.encode('latin1')  # back to bytes
        decompressed = smaz.decompress(compressed.decode('latin1'))
        return decompressed
