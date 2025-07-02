import smaz
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
    def decode(codephrase: str) -> str:
        decoded = b91_decode(codephrase)
        # smaz.decompress expects str, not bytes
    
        decoded = decoded.decode("latin1")  # or utf-8 if consistent
        return smaz.decompress(decoded)

        
