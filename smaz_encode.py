import smaz
import base64
from base91 import encode as b91_encode, decode as b91_decode
class smaz_wrapper:
    @staticmethod
    def encode(phrase: str) -> str:
        """Compress text and return a latin1-safe string."""
        compressed = smaz.compress(phrase)
        encoded = b91_encode(compressed)
        return encoded

    @staticmethod
    def decode(codephrase: str) -> str:
        """Decode a latin1-safe string to original text."""
        decoded = b91_decode(codephrase)
        decompressed = smaz.decompress(decoded)
        return decompressed
        
