from decimal import Decimal
import openai, tiktoken
import csv, re, asyncio
import os, math
from bot.context import Context
from bot.models import Model
from sklearn.metrics import f1_score


class Greenie:

    _TEMP = 0
    __log_qa_path = 'logs/qa.csv'
    __log_prpx_path = 'logs/prpx.csv'
    
    def __init__(self, model: Model = Model.TURBO) -> None:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.__model = model
        

    async def response(self, ctx: Context, debug=False) -> str:
        '''
        Request for Chat Completion API
        param: ctx -> context for request
        '''
        if (not ctx):
            raise Exception('Empty')
        
        response = openai.ChatCompletion.create(
            model=self.__model.value,
            messages=ctx.get_ctx(),
            temperature=self._TEMP
        )

        res = str(response.choices[0]['message']['content'])

        # log QnA
        asyncio.create_task(self.__log(c=ctx, r=res, prpx=True))

        if debug:
            print (f'Response: {res}')
        return res
    

    # The number of tokens used affects:
    # 1) the cost of the request
    # 2) the time it takes to generate the response
    # 3) when the reply gets cut off from hitting the maximum token limit (4096 for gpt-3.5-turbo)
    def count_tokens(self, ctx: Context) -> int:
        '''
        Counts tokens in given context
        param: ctx -> chatbot context
        returns: token amount
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
        Calculates approximate of price to pay for request
        param: ctx -> context to send to chatbot
        returns: price of request
        '''
        return int(Decimal(0.002/1000) * tokens) # price of 1K tokens = 0.002


    async def __log(self, **args) -> None:
        '''
        Logs request question, answer and/or perplexity
        param: *args -> named arguments for context (c), answer(r), perplexity(p: boolean)
        '''
        res = re.sub(',', '', args['r']) # normalize data for logging
        if len(args) == 3:
            perplexity = self.calculate_perplexity(args['c'], args['r'])
            with open(self.__log_prpx_path, 'a+t', newline='') as f:
                writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
                if os.stat(self.__log_prpx_path).st_size == 0: # file is empty, write headers
                    writer.writerow(['question', 'answer', 'perplexity'])
                writer.writerow([args['c'].get_question(), res, perplexity])

        with open(self.__log_qa_path, 'a+t', newline='') as f:
            writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            if os.stat(self.__log_qa_path).st_size == 0: # file is empty, write headers
                writer.writerow(['question', 'answer'])
            writer.writerow([args['c'].get_question(), res])
        print ("Logging Successful")


    def calculate_perplexity(self, ctx: Context, res: str, debug: bool=False) -> float:
        '''
        Calculates perplexity metric of model tokens
        param: ctx -> context of request
        param: res -> response of request
        '''
        tokens = ctx.tokens()
        # Extract the probabilities for the tokens
        token_probs = [res.split().count(token) / len(res.split()) for token in tokens]
        print (f'perp:{token_probs}')
        # Calculate the log-probabilities
        log_probs = [-math.log2(prob) for prob in token_probs if prob != 0]
        # Calculate the perplexity
        perplexity = 2 ** (sum(log_probs) / len(tokens))
        if debug:
            print(perplexity)
        return perplexity


    def f1_score(self, actual: list[str], expected: list[str]) -> float:
        '''
        Calculates f1 score given a list of actual and expected answers
        ''' 
        f1_scores = []
        for i in range(len(actual)):
            answer = actual[i]
            predicted_answer = expected[i]
            f1 = f1_score([answer], [predicted_answer], average='weighted')
            f1_scores.append(f1)
        # Calculate the average F1 score across all question and answer pairs
        return sum(f1_scores) / len(f1_scores)
