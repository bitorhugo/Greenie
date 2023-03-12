from decimal import Decimal
import re
import openai, tiktoken
from os import getenv
from bot.context import Context
from bot.models import Model
import csv

class Greenie:

    _TEMP = 0
    __log_path = 'logs/qa.csv'

    _ENCODING_MODEL_NAME = "gpt-3.5-turbo"
    
    def __init__(self, model: Model = Model.TURBO) -> None:
        openai.api_key = getenv("OPENAI_API_KEY")
        self.__model = model
        
    def response(self, ctx: Context) -> str:
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
        self.log(ctx.get_question(), res) # TODO: make this async
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

    def log(self, q: str, res: str):
        res = re.sub(',', '', res)
        with open(self.__log_path, 'w', newline='') as f:
            writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([q, res])
            
