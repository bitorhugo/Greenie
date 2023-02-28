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

def parseContractionsToDic (path: str) -> dict[str, str]:
    file = open(path, "r")
    input = file.read().split(',')
    file.close()
    c = {}
    for w in range(0, len(input), 2):
        c.update({input[w]: input[w+1]})
    return c

def parseWordToDic (path: str) -> dict[str, str]:
    file = open(path, 'r')
    input = file.read().split(',')
    file.close()
    words = {}
    for w in input:
        words[w] = ''
    return words

# expects a raw input of type string.
# e.g -> Dataset contained in a super long string
def cleanse (input: str) -> list[str]:
    if not input:
        raise Exception("String 'raw' is empty.")

    words = parseWordToDic('data/stopwords')
    symbols = parseToList('data/symbols')
    numbers = parseToList('data/numbers')
    contractions = parseContractionsToDic('data/contractions')

    # normalize input
    input = input.lower()
    
    # remove numbers
    for n in numbers:
        input = re.sub(n, ' ', input)

    # remove symbols
    input = re.sub(r'[\+\-\*\%\/\?\!\.\,\;\\]', '', input)
    
    # remove contractions
    tmp = input.split(' ')
    for w in tmp:
        if contractions.get(w):
            input = re.sub(str(w), str(contractions.get(w)), input)

    # remove words
    for w in input.split(' '):
        if words.get(w) != None:
            input = re.sub(str(w), "", input)

    return input.strip().split(' ')

# 1 -> gather raw paragraph
raw = "Luciano Pavarotti. (born October 12, 1935, Modena, Italy—died September 6, 2007, Modena), Italian operatic lyric tenor who was considered one of the finest bel canto opera singers of the 20th century. Even in the highest register, his voice was noted for its purity of tone, and his concerts, recordings, and television appearances—which provided him ample opportunity to display his ebullient personality—gained him a wide popular following."

# 2 -> get human input and cleanse it
human_input = "Who's Luciano, Pavarotti ?"
print(f'Before: {human_input}')
cleansed = cleanse(human_input)
print(f'After: {cleansed}')

# 3 -> for each word of cleansed, search for it in raw and extract the sentence
#   1) split raw by sentence
#   2) search for cleansed word in each phrase
#   3) build context for gpt-3
sentences = dict()
s_raw = raw.lower().split('.')
for phrase in s_raw:
    for word in cleansed:
        if word in phrase.split(): # split so searches for whole word
            sentences[phrase] = word

context = str()
for s in sentences.keys():
    context = context + s

