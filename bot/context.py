import pprint
from bot.role import Role

class Context:

    __initial_msg = "You are a helpful, pattern-following assistant that helps field operators and citizens of a smart city."

    def __init__ (self, ctx: list[dict[str, str]] = list(), initial_msg: bool = False):
        self.ctx = ctx
        if initial_msg:
            self.add_msg_to_ctx(Role.SYSTEM, self.__initial_msg)
        
    def add_msg_to_ctx(self, role: Role, msg: str) -> None:
        '''
        Appends a message to the context with given role
        param: role -> role of the messenger (e.g. user or system)
        param: msg -> message to append
        '''
        self.ctx.append({"role" : role.value, "content" : msg})

    def __str__(self) -> str:
        return pprint.pformat(self.ctx, sort_dicts=False, indent=1)

