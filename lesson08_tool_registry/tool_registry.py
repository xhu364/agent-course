class ToolRegistry:

    def __init__(self):
        self.tools = {}

    def register(self, name, func):
        self.tools[name] = func

    def execute(self, name, args):

        if name not in self.tools:
            raise Exception(f"Unknown tool {name}")

        return self.tools[name](**args)
