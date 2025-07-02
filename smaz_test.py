from smaz import compress, decompress

def encode():
    phrase = input("Enter <100 characters of text: ")
    codephrase = compress(phrase)
    print("Compressed:", codephrase)  # shows raw bytes
    print("Printable (paste into decode):", codephrase.encode('latin1'))  # for input reuse

def decode():
    codephrase = input("Enter compressed text: ")
    try:
        codebytes = codephrase.encode('latin1')  # convert string back to bytes
        phrase = decompress(codebytes)
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
