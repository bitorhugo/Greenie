import pprint
from bot.role import Role

class Context:

    __initial_msg = "You are a helpful, pattern-following assistant that helps field operators and citizens of a smart city. If you don't know the answer to a question say, I don't know."

    def __init__ (self, ctx: list[dict[str, str]] = list(), initial_msg: bool = False):
        self.__ctx = ctx
        if initial_msg:
            self.add_knowledge(Role.SYSTEM, self.__initial_msg)

    def get_ctx(self) -> list[dict[str, str]]:
        return self.__ctx
        
    def add_knowledge(self, role: Role, msg: str) -> None:
        '''
        Appends a message to the context with given role
        param: role -> role of the messenger (e.g. user or system)
        param: msg -> message to append
        '''
        self.__ctx.append({"role" : role.value, "content" : msg})

    def get_question(self) -> str:
        '''
        Returns question if present
        '''
        # question is always last content added to context
        if self.__ctx[len(self.__ctx) - 1]['role'] == "user":
            return self.__ctx[len(self.__ctx) - 1]['content']
        else:
            return ""
    
    def add_question(self, q: str) -> None:
        self.__ctx.append({"role" : Role.USER._value_, "content" : q})
        
    def __str__(self) -> str:
        return pprint.pformat(self.__ctx, sort_dicts=False, indent=1)

