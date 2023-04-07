from decimal import Decimal
import openai, tiktoken
import csv, re, asyncio
import os, math
from bot.context import Context
from bot.metric import Metric
from bot.models import Model
from bot.role import Role
from sklearn.metrics import f1_score
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer


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
        # Calculate the log-probabilities
        log_probs = [-math.log2(prob) for prob in token_probs if prob != 0]
        # Calculate the perplexity
        perplexity = 2 ** (sum(log_probs) / len(tokens))
        if debug:
            print (f'prpx-per-tokens:{token_probs}')
            print(f'prpx:{perplexity}')
        return perplexity


    async def accuracy(self, metric: Metric, debug: bool=False):
        '''
        Test the accuracy of the bot responses
        Beware, it may run several questions through GPT to obtain responses
        @param metric: Metric used to measure accuracy e.g. Cossine-Similarity
        '''
        # check to see if test files are available
        if os.stat('logs/accuracy.csv').st_size == 0: # file is empty, write headers
            await self.log_accuracy(debug) # run questions
        if metric is Metric.COSSINE:
            self.cossine_similarity()
        if metric is Metric.F1:
            self.f1()

    
    async def log_accuracy(self, debug: bool=False):
        accuracy_path = 'logs/accuracy.csv'
        f = open ("data/en/pcb.txt")
        data = f.read()
        # run questions through chatbot
        qna = self.load_QnA_F1()
        rows = []
        for item in qna:
            a, q = item.pop(), item.pop()
            context = Context(initial_msg=True)
            context.add_knowledge(Role.SYSTEM, snlp.filter_raw(data, debug=False))
            context.add_question(q)
            context.tokens(debug=False)
            print(f'Question: {context.get_question()}')
            r = await self.response(context, debug=False)
            print(f'bot-answer:{r}')
            print(f'human-answer:{a}')
            rows.append([q, a, r])

        with open(accuracy_path, 'a+t', newline='') as f:
            w = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            if os.stat(accuracy_path).st_size == 0: # file is empty, write headers
                w.writerow(['question', 'human-answer', 'bot-answer'])
                w.writerows(rows)    
        

    def load_QnA_F1(self, debug: bool=False) -> list[list[str]]:
        qna = []
        with open('data/QnA/qa.csv') as f:
            r = csv.reader(f)
            for row in r:            # each row is a list containing a question and its answer
                if debug:
                    print(f'qna:{row}')
                qna.append(row)
        return qna

    
    def f1(self):
        questions = []
        human = []
        bot = []
        f1_scores = []
        with open('logs/accuracy.csv') as f:
            r = csv.reader(f)
            next(r)
            for row in r:
                b, h, q = row.pop(), row.pop(), row.pop()
                questions.append(q)
                human.append(h)
                bot.append(re.sub('\n', '', b))
        for i in range(min(len(questions), len(human))):
            question = questions[i]
            answer = human[i]
            predicted_answer = bot[i]
            print(f'question:{question}')
            print(f'human:{answer}')
            print(f'bot:{predicted_answer}')
            f1 = f1_score([answer], [predicted_answer], average='weighted')
            f1_scores.append(f1)
        # Calculate the average F1 score across all question and answer pairs
        average_f1 = sum(f1_scores) / len(f1_scores)
        print(f'f1:{average_f1}')

        
    def cossine_similarity(self):
        # define two example sentences
        sentence1 = "I like pizza"
        sentence2 = "I like pizza"
        # create a CountVectorizer object
        vectorizer = CountVectorizer()
        # fit the vectorizer on the sentences
        vectorizer.fit_transform([sentence1, sentence2])
        # transform the sentences into vectors
        vector1 = vectorizer.transform([sentence1]).toarray()
        vector2 = vectorizer.transform([sentence2]).toarray()
        # calculate cosine similarity between the two vectors
        cosine_sim = cosine_similarity(vector1, vector2)
        print("Cosine similarity:", cosine_sim[0][0])
