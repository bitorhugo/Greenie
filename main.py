#!/usr/bin/python3

import openai
from snlp import tokenize, build_context
from bot.grennie import Greenie

raw = "Luciano Pavarotti (born October 12, 1935, Modena, Italy—died September 6, 2007, Modena), Italian operatic lyric tenor who was considered one of the finest bel canto opera singers of the 20th century. Even in the highest register, his voice was noted for its purity of tone, and his concerts, recordings, and television appearances—which provided him ample opportunity to display his ebullient personality—gained him a wide popular following."

messages = [
    {"role": "system", "content": "You are a helpful, pattern-following assistant that translates corporate jargon into plain English."},
    {"role": "system", "name":"example_user", "content": "New synergies will help drive top-line growth."},
    {"role": "system", "name": "example_assistant", "content": "Things working well together will increase revenue."},
    {"role": "system", "name":"example_user", "content": "Let's circle back when we have more bandwidth to touch base on opportunities for increased leverage."},
    {"role": "system", "name": "example_assistant", "content": "Let's talk later when we're less busy about how to do better."},
    {"role": "user", "content": "This late pivot means we don't have time to boil the ocean for the client deliverable."},
]

if __name__ == '__main__':
    q = "Who's Luciano ?"
    print(f'Before: {q}')
    tok = tokenize(q)
    print(f'After: {tok}')

    context = build_context(raw, tok)
    print(f'Context: {context}')

    bot = Greenie()
    tokens = bot.count_tokens(messages)
    total = bot.req_price(tokens)
    print (f'Tokens: {tokens}')
    print (f'Total Price: {total}$')

# openai.api_key = getenv("OPENAI_API_KEY")
# turbo = "gpt-3.5-turbo"
# custom_prompt = context # here you'll add the context plus conversation carried so far and question from user

# openai.Completion.create(
#     model = Model.TURBO,
#     prompt = context,
#     temperature = 0,
#     max_tokens = 10
# )




