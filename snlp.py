import re

def __parse_to_list(path: str) -> list[str]:
    file = open(path, 'r')
    input = file.read()
    file.close()
    if (path.__contains__('symbols')):
        return input.split(' ')
    return input.split(',')

def __contractions_to_dict (path: str) -> dict[str, str]:
    file = open(path, "r")
    input = file.read().split(',')
    file.close()
    c = {}
    for w in range(0, len(input), 2):
        c.update({input[w]: input[w+1]})
    return c

def __words_to_dict (path: str) -> dict[str, str]:
    file = open(path, 'r')
    input = file.read().split(',')
    file.close()
    words = {}
    for w in input:
        words[w] = ''
    return words

# expects a raw input of type string.
# e.g -> Dataset contained in a super long string
def __tokenize (input: str) -> list[str]:
    if not input:
        raise Exception("Input must not be empty.")

    words = __words_to_dict('data/stopwords')
    numbers = __parse_to_list('data/numbers')
    contractions = __contractions_to_dict('data/contractions')

    # normalize input
    input = input.lower()
    
    # remove numbers
    for n in numbers:
        input = re.sub(n, ' ', input)

    # remove symbols
    input = re.sub(r'[\+\-\*\%\/\?\!\.\,\;\\]', '', input)
    
    # remove contractions
    for w in input.split(' '):
        if contractions.get(w):
            input = re.sub(str(w), str(contractions.get(w)), input)

    # remove words
    for w in input.split(' '):
        if words.get(w) != None:
            input = re.sub(str(w), "", input)
            
    # remove extra whitespaces and duplicates
    return list (dict().fromkeys(list(filter(lambda x: x, input.split()))))

def filter_raw (raw: str, debug: bool=False) -> str:
    tokens = __tokenize(raw)
    sentences = dict()
    s_raw = raw.lower().split('.')
    for phrase in s_raw:
        for word in tokens:
            if word in phrase.split(): # split so searches for whole word
                sentences[phrase] = word
    context = str()
    for s in sentences.keys():
        context = context + s
    if debug:
        print(f'Tokens: {tokens}')
        print(f'Context: {context}')
    return context;
