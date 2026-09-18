from app.utils.file_handler import file_handler


class History:
    def __init__(self) -> None:
        self.command_history = []

    def add_command(self, cmd: str):
        self.command_history.append(cmd)

    def run_history(self, args: list[str]):
        total = len(self.command_history)

        # read history from a file path
        if "-r" in args:
            # get index of -r
            index = args.index("-r")
            file_path = args[index + 1]
            file_content = file_handler.get_file_content(file_path)

            lines = file_content.split("\n")
            self.command_history.extend(lines)
            return

        if "-w" in args:
            # get index of -w
            index = args.index("-w")
            file_path = args[index + 1]
            file_handler.write_to_file(
                file_path, "\n".join(self.command_history) + "\n"
            )
            return

        n = total - int(args[0]) if args else 0

        for i in range(n, len(self.command_history)):
            print(f"{i + 1} {self.command_history[i]}")


history = History()
