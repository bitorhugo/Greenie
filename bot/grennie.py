import openai, tiktoken
from os import getenv


class Greenie:

    _TEMP = 0
    
    def __init__(self, model: Model = Model.TURBO) -> None:
        openai.api_key = getenv("OPENAI_API_KEY")
        self.model = model
        
    def asnwer(self, q: str) -> str:
        '''
        answer a question from user using ChatCompletion
        '''
        if (not q):
            raise Exception('Empty Question')
        response = openai.ChatCompletion.create(
            model=self.model.value,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Knock knock."},
                {"role": "assistant", "content": "Who's there?"},
                {"role": "user", "content": "Orange."},
            ],
            temperature=self._TEMP
        )
        return str(response['choices'][0]['message']['content'])

    def count_tokens(self, ctx) -> int:
        '''
        The number of tokens used affects:
        1) the cost of the request
        2) the time it takes to generate the response
        3) when the reply gets cut off from hitting the maximum token limit (4096 for gpt-3.5-turbo)
        '''
        try:
            encoding = tiktoken.encoding_for_model(self.model.value)
        except KeyError:
            encoding = tiktoken.get_encoding("cl100k_base")
        if self.model.value == "gpt-3.5-turbo-0301":  # note: future models may deviate from this
            num_tokens = 0
            for message in ctx:
                num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
                for key, value in message.items():
                    num_tokens += len(encoding.encode(value))
                    if key == "name":  # if there's a name, the role is omitted
                        num_tokens += -1  # role is always required and always 1 token
            num_tokens += 2  # every reply is primed with <im_start>assistant
            return num_tokens
        else:
            raise Exception("failed")

