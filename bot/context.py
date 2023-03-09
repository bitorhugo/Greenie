from bot.role import Role

class Context:

    def __init__ (self, ctx: list[dict[str, str]] = list()):
        self.ctx = ctx
        
    def add_msg_to_ctx(self, role: Role, msg: str) -> None:
        self.ctx.append({"role" : role.value, "content" : msg})

    def __str__(self) -> str:
        return self.ctx.__str__()

