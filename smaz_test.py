from smaz import compress, decompress

def encode():
   phrase = input("Enter <100 characters of text: ")
   codephrase = compress(phrase)
   print(codephrase)

def decode():
   codephrase = input("Enter compressed text: ")
   phrase = decompress(codephrase)
   print(phrase)

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