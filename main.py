#!/usr/bin/python3

import openai
from snlp import tokenize
from os import getenv

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

q = "Who's Luciano ?"
print(f'Before: {q}')
tok = tokenize(q)
print(f'After: {tok}')

raw = "Luciano Pavarotti (born October 12, 1935, Modena, Italy—died September 6, 2007, Modena), Italian operatic lyric tenor who was considered one of the finest bel canto opera singers of the 20th century. Even in the highest register, his voice was noted for its purity of tone, and his concerts, recordings, and television appearances—which provided him ample opportunity to display his ebullient personality—gained him a wide popular following."

context = build_context(raw, tok)
print(f'Context: {context}')

# openai.api_key = getenv("OPENAI_API_KEY")
# turbo = "gpt-3.5-turbo"
# custom_prompt = context # here you'll add the context plus conversation carried so far and question from user

# openai.Completion.create(
#     model = Model.TURBO,
#     prompt = context,
#     temperature = 0,
#     max_tokens = 10
# )

from greenie import Greenie

bot = Greenie()

messages = [
    {"role": "system", "content": "You are a helpful, pattern-following assistant that translates corporate jargon into plain English."},
    {"role": "system", "name":"example_user", "content": "New synergies will help drive top-line growth."},
    {"role": "system", "name": "example_assistant", "content": "Things working well together will increase revenue."},
    {"role": "system", "name":"example_user", "content": "Let's circle back when we have more bandwidth to touch base on opportunities for increased leverage."},
    {"role": "system", "name": "example_assistant", "content": "Let's talk later when we're less busy about how to do better."},
    {"role": "user", "content": "This late pivot means we don't have time to boil the ocean for the client deliverable."},
]

tokens = bot.count_tokens(messages)
total = bot.req_price(tokens)
print (f'Tokens: {tokens}')
print (f'Total Price: {total}$')
