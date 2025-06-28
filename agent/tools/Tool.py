# Basic tool class for defining tools
class Tool:
    def __init__(self, name: str, description: str, inp: dict[str, type], outp: type, func: any):
        self.name = name
        self.description = description
        self.input = inp
        self.output = outp
        self.func = func

    def __call__(self, *args, **kwargs) -> any:
        return self.func(*args, **kwargs)

    def run(self, *args, **kwargs) -> any:
        return self.func(*args, **kwargs)