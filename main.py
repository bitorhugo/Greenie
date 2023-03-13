#!/usr/bin/python3

import openai, snlp, asyncio
from bot.context import Context
from bot.role import Role
from bot.grennie import Greenie
from googletrans import Translator

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

async def main():
    f = open ("data/example.txt")
    raw = f.read()
    raw = raw.replace('\n', '')
    raw = raw.replace(';', '.')
    translator = Translator()
    translation = translator.translate(raw)

    q = "whats the first step in the pcb charger assembly?"
    context = Context(initial_msg = True)
    
    context.add_knowledge(Role.SYSTEM, snlp.filter_raw(translation.text))
    context.add_question(q)
    print(f'Context: {context}')
    print(f'Question: {context.get_question()}')

    bot = Greenie()
    tokens = bot.count_tokens(context)
    total = bot.req_price(tokens)
    print (f'Tokens: {tokens}')
    print (f'Total Price est ~ {total}$')
    await bot.response(context)

if __name__ == '__main__':
    asyncio.run(main())


# Openai.api_key = getenv("OPENAI_API_KEY")
# turbo = "gpt-3.5-turbo"
# custom_prompt = context # here you'll add the context plus conversation carried so far and question from user

# openai.Completion.create(
#     model = Model.TURBO,
#     prompt = context,
#     temperature = 0,
#     max_tokens = 10
# )




