from bot.role import Role

class Context:

    __initial_msg = "You are a helpful, pattern-following assistant that helps field operators and citizens of a smart city."

    def __init__ (self, ctx: list[dict[str, str]] = list(), initial_msg: bool = False):
        self.ctx = ctx
        if initial_msg:
            self.add_msg_to_ctx(Role.SYSTEM, self.__initial_msg)
        
    def add_msg_to_ctx(self, role: Role, msg: str) -> None:
        self.ctx.append({"role" : role.value, "content" : msg})

    def __str__(self) -> str:
        return self.ctx.__str__()

