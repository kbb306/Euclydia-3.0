import smaz
import base64
from base91 import encode as b91_encode, decode as b91_decode
class smaz_wrapper:
    @staticmethod
    def encode(phrase: str) -> str:
        """Compress text and return a base91 string"""
        compressed = smaz.compress(phrase)
        if isinstance(compressed, str):
            compressed = compressed.encode("latin1")
        encoded = b91_encode(compressed)
        return encoded

    @staticmethod
    def decode(codephrase: bytes) -> str:
        """Decode a base91-smaz string to original text."""
        if isinstance(codephrase, bytes):
            codephrase = codephrase.decode('latin1')
        decoded = b91_decode(codephrase)
        decompressed = smaz.decompress(decoded)
        return decompressed
        
