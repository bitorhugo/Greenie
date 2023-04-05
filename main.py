#!/usr/bin/python3

import snlp, asyncio, csv
from bot.context import Context
from bot.role import Role
from bot.grennie import Greenie

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

def to_en(input: str) -> str:
    input = input.replace('\n', '')
    input = input.replace(';', '.')
    return ""


async def main():
    f = open ("data/en/pcb.txt")
    data = f.read()

    q = "whats the last step in the pcb charger assembly?"
    context = Context(initial_msg=True)
    
    context.add_knowledge(Role.SYSTEM, snlp.filter_raw(data, debug=True))
    context.add_question(q)
    context.tokens(debug=False)
    print(f'Context: {context}')
    print(f'Question: {context.get_question()}')

    bot = Greenie()
    tokens = bot.count_tokens(context)
    total = bot.req_price(tokens)
    print (f'Tokens: {tokens}')
    print (f'Total Price est ~ {total}$')
    await bot.response(context, debug=True)

    
if __name__ == '__main__':
    asyncio.run(main())
