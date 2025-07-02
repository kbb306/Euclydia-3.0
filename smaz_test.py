import smaz
print("Using smaz from:", smaz.__file__)
from smaz import compress
print(compress("test"), type(compress("test")))

def encode():
    phrase = input("Enter <100 characters of text: ")
    codephrase = smaz.compress(phrase)
    out = codephrase.encode('latin1')
    print("Compressed type:", type(out))
    print("Compressed:", out)  # shows raw bytes
    print("Printable (paste into decode):", out.decode('latin1'))  # for input reuse

def decode():
    codephrase = input("Enter compressed text: ").encode('latin1')
    try:
        codebytes = codephrase.decode('latin1')  # convert string back to bytes
        phrase = smaz.decompress(codebytes)
        print("Decompressed:", phrase)
    except Exception as e:
        print("Error during decompression:", e)

def main():
    while True:
        selection = input("Encode or Decode (Or Quit)? ")
        if selection.upper() == "E":
            encode()
        elif selection.upper() == "D":
            decode()
        elif selection.upper() == "Q":
            print("Goodbye!")
            break

main()
