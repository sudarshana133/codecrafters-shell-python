class History:
    def __init__(self) -> None:
        self.command_history = []

    def add_command(self, cmd: str):
        self.command_history.append(cmd)

    def run_history(self, args: list[str]):
        total = len(self.command_history)
        if args:
            n = total - int(args[0])
        else:
            n = 0
        for i in range(n, len(self.command_history)):
            print(f"{i + 1} {self.command_history[i]}")


history = History()
