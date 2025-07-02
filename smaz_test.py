from smaz_encode import *
translator = smaz_wrapper()
phrase = input("Enter a phrase: ")
codephrase = translator.encode(phrase)
decode = translator.decode(codephrase)
print("You entered:",phrase)
print("Smaz gave me:",codephrase)
print("Which translates to:",decode)
if decode == phrase:
    print("Test passsed! ")
else:
    print("Test failed!")