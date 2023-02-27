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
    if (path.__contains__('symbols')):
        return input.split(' ')
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
def cleanse (input: str) -> list[str]:
    if not input:
        raise Exception("String 'raw' is empty.")

    words = parseToList('data/stopwords')
    #symbols = parseToList('data/symbols')
    numbers = parseToList('data/numbers')
    contractions = parseToDict('data/contractions')

    input = input.lower()
    
    # remove numbers
    for n in numbers:
        input = re.sub(n, ' ', input)

    # remove symbols
    # for s in symbols:
    #     input = re.sub(s, '', input)

    # remove contractions
    tmp = input.split(' ')
    for w in tmp:
        if contractions.get(w):
            input = re.sub(str(w), str(contractions.get(w)), input)
    
    return input.split(' ')

# 1 -> Gather context for GPT-3
context = "What's the weather like in four days ain't ?"

# 2 -> get human input and cleanse it
cleansed = cleanse (context)

# 3 -> for each word of cleansed, search for it in context and extract the paragraph
