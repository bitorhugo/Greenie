#!/usr/bin/python3

import openai, snlp
from bot.context import Context
from bot.role import Role
from bot.grennie import Greenie
from googletrans import Translator, constants

f = open ("data/example.txt")
raw = f.read()
raw = raw.replace('\n', '')
raw = raw.replace(';', '.')


# init the Google API translator
translator = Translator()
# translate a spanish text to english text (by default)
translation = translator.translate(raw)

# messages will be a json array
# json object -> dict[str, str]
# e.g.
# context = [
#     {"role": "system", "content": "You are a helpful, pattern-following assistant that helps field operators and citizens on a smart city."},
#     {"role": "system", "content": "If you don't know the answer to a question say, I don't know."},
#     {"role": "system", "content": f'{raw}'},
#     {"role": "user", "content": "Tell me the first item needed"},
# ]
# context will be composed of a list of dictionaries

context = Context()
context.add_msg_to_ctx(Role.SYSTEM, "You are a helpful, pattern-following assistant that helps field operators and citizens on a smart city.")
context.add_msg_to_ctx(Role.USER, "What is dog coin?")
print (context.ctx)

if __name__ == '__main__':
    # q = "whats the first step in the pcb charger assembly?"
    # print(f'Before: {q}')
    # tok = snlp.tokenize(q)
    # print(f'After: {tok}')
    # context = snlp.build_context(raw, tok)
    # print(f'Context: {context}')

    bot = Greenie()
    tokens = bot.count_tokens(context)
    total = bot.req_price(tokens)
    print (f'Tokens: {tokens}')
    print (f'Total Price est ~ {total}$')

    # print (bot.response(messages))

# Openai.api_key = getenv("OPENAI_API_KEY")
# turbo = "gpt-3.5-turbo"
# custom_prompt = context # here you'll add the context plus conversation carried so far and question from user

# openai.Completion.create(
#     model = Model.TURBO,
#     prompt = context,
#     temperature = 0,
#     max_tokens = 10
# )




