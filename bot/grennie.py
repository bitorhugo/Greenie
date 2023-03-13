from ctypes import sizeof
from decimal import Decimal
import openai, tiktoken
import csv, re, asyncio
import os
from bot.context import Context
from bot.models import Model


class Greenie:

    _TEMP = 0
    __log_path = 'logs/qa.csv'

    _ENCODING_MODEL_NAME = "gpt-3.5-turbo"
    
    def __init__(self, model: Model = Model.TURBO) -> None:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.__model = model
        
    async def response(self, ctx: Context, debug=False) -> str:
        '''
        answer question from user using ChatCompletion
        param: q -> context contained in JSON format
        '''
        if (not ctx):
            raise Exception('Empty')
        
        response = openai.ChatCompletion.create(
            model=self.__model.value,
            messages=ctx.get_ctx(),
            temperature=self._TEMP
        )
        res = str(response['choices'][0]['message']['content'])

        asyncio.create_task(self.log(ctx.get_question(), res))

        if debug:
            print (res)
        return res
    

    # The number of tokens used affects:
    # 1) the cost of the request
    # 2) the time it takes to generate the response
    # 3) when the reply gets cut off from hitting the maximum token limit (4096 for gpt-3.5-turbo)
    def count_tokens(self, ctx: Context) -> int:
        '''
        counts tokens in the given context
        params: ctx -> chatbot context
        '''
        try:
            encoding = tiktoken.encoding_for_model(self.__model.value)
        except KeyError:
            encoding = tiktoken.get_encoding("cl100k_base")
            
        num_tokens = 0
        for message in ctx.get_ctx():
            num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":  # if there's a name, the role is omitted
                    num_tokens += -1  # role is always required and always 1 token
                    num_tokens += 2  # every reply is primed with <im_start>assistant
        return num_tokens
    
    def req_price(self, tokens: int) -> int:
        '''
        Returns apprx of price to pay for tokens
        param: ctx -> context to send to chatbot
        '''
        # price of 1K tokens = 0.002
        return int(Decimal(0.002/1000) * tokens)

    async def log(self, q: str, res: str):
        print("Logging..")
        res = re.sub(',', '', res) # normalize data for logging
        with open(self.__log_path, 'a+t', newline='') as f:
            writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            if os.stat(self.__log_path).st_size == 0: # file is empty, write headers
                writer.writerow(['question', 'answer'])
            writer.writerow([q, res])
        print ("Logging Successful")
