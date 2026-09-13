class Commands:
    def __init__(self):
        self.builtins = ["echo", "type", "exit"]

    def get_command_args(self, user_input: str) -> list[str]:
        tmp = user_input.split()

        return tmp[1:]

    def get_command(self, user_input: str) -> str:
        tmp = user_input.split()
        return tmp[0]

    def echo(self, user_input: str):
        args = self.get_command_args(user_input)
        print(" ".join(args))

    def type(self, user_input: str):
        args = self.get_command_args(user_input)
        if args[0] in self.builtins:
            print(f"{args[0]} is a shell builtin")
        else:
            print(f"{args[0]}: not found")


commands = Commands()
