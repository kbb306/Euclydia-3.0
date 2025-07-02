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
    def decode(codephrase: str) -> str:
        print("[DEBUG] Decoding input:", repr(codephrase))
        print("[DEBUG] Type of codephrase:", type(codephrase))
        for i, c in enumerate(codephrase[:10]):
            print(f"[DEBUG] Char {i}: {repr(c)}, type={type(c)}")
        decoded = b91_decode(codephrase)
        return smaz.decompress(decoded)

        
