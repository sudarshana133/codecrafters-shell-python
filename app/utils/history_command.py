class History:
    def __init__(self) -> None:
        self.command_history = []

    def add_command(self, cmd: str):
        self.command_history.append(cmd)

    def run_history(self):
        for i, command in enumerate(self.command_history):
            print(f"{i + 1} {command}")


history = History()
