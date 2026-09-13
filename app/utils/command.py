class Commands:
    def __init__(self):
        pass

    def get_command_args(self, user_input: str) -> list[str]:
        tmp = user_input.split()

        return tmp[1:]

    def get_command(self, user_input: str) -> str:
        tmp = user_input.split()
        return tmp[0]

    def echo(self, user_input: str):
        args = self.get_command_args(user_input)
        print(" ".join(args))


commands = Commands()
