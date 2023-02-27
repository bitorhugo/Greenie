#!/usr/bin/python3

# Pipiline:
#     1) Data preprocessing: cleaning the data, removing stop words, and converting the text to lowercase.
#     2) Tokenization:
#     3) Encoding:
#     4) Classification
import re
    
def parseToList(path: str) -> list[str]:
    file = open(path, 'r')
    input = file.read()
    file.close()
    return input.split(',')

def parseToDict (path: str) -> dict[str, str]:
    file = open(path, "r")
    input = file.read()
    input = input.split(',')
    file.close()
    c = {}
    for w in range(0, len(input), 2):
        c.update({input[w]: input[w+1]})
    return c


# expects a raw input of type string.
# e.g -> Dataset contained in a super long string
def cleanse (raw: str):
    if not raw:
        raise Exception("String 'raw' is empty.")

    words = parseToList('data/stopwords')
    symbols = parseToList('data/symbols')
    numbers = parseToList('data/numbers')
    contractions = parseToDict('data/contractions')

    # remove contractions
    for c in contractions:
        raw = re.sub(c, str(contractions.get(c)), raw)

    # remove numbers
    for n in numbers:
        raw = re.sub(n, ' ', raw)

    # remove symbols
    # for s in symbols:
    #     raw = re.sub(s, '', raw)

    print (raw)
    
cleanse("hello there, you've got a message ain't it champ")
