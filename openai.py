#!/usr/bin/python3

# Pipiline:
#     1) Data preprocessing: cleaning the data, removing stop words, and converting the text to lowercase.
#     2) Tokenization:
#     3) Encoding:
#     4) Classification

from nlptok import tokenize

def build_context (raw: str,tokens: list[str]) -> str:
    sentences = dict()
    s_raw = raw.lower().split('.')
    for phrase in s_raw:
        for word in tokens:
            if word in phrase.split(): # split so searches for whole word
                sentences[phrase] = word
    context = str()
    for s in sentences.keys():
        context = context + s
    return context;

# 1 -> gather raw paragraph e.g. dataset

# 2 -> get human input and cleanse it
human_input = "Who's Luciano ?"
print(f'Before: {human_input}')
tok = tokenize(human_input)
print(f'After: {tok}')

# 3 -> for each word of cleansed, search for it in raw and extract the sentence
#      1) split raw by sentence
#      2) search for cleansed word in each phrase



# actual prompt to send to gpt-3
# Prompt: set up how bot works (e.g role: assistant)
#         context:
#         conversation carried out so far
#         user input

import openai
from os import getenv
from enum import Enum

class Model(Enum):
    TURBO = "gpt-3.5-turbo"
    REINFORCED_DAVINCI = "text-davinci-003"
    SUPERVISED_DAVINCI = "text-davinci-002"
    
raw = "Luciano Pavarotti (born October 12, 1935, Modena, Italy—died September 6, 2007, Modena), Italian operatic lyric tenor who was considered one of the finest bel canto opera singers of the 20th century. Even in the highest register, his voice was noted for its purity of tone, and his concerts, recordings, and television appearances—which provided him ample opportunity to display his ebullient personality—gained him a wide popular following."

context = build_context(raw, tok)
print(f'Context: {context}')

openai.api_key = getenv("OPENAI_API_KEY")
turbo = "gpt-3.5-turbo"
custom_prompt = context # here you'll add the context plus conversation carried so far and question from user

openai.Completion.create(model=Model.TURBO, prompt=context, temperature=0, max_tokens=10)

