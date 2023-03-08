import openai
from os import getenv
from models import Model


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


