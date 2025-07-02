from smaz_encode import smaz_wrapper
translator = smaz_wrapper()
phrase = input()
print(translator.decode(phrase))