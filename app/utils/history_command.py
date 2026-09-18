import os

from app.utils.file_handler import file_handler


class History:
    def __init__(self) -> None:
        self.command_history = []
        self.append_pending_history = []

    def overrite_history(self, content: str):
        if not content:
            self.command_history = []
        else:
            lines = content.split("\n")
            self.command_history = lines

    def write_history_to_file(self):
        """
        Write in memory history on exit
        """
        file_path = os.environ.get("HISTFILE")
        if file_path:
            content = "\n".join(self.command_history) + "\n"
            file_handler.write_to_file(file_path, content)

    def add_command(self, cmd: str):
        self.command_history.append(cmd)
        self.append_pending_history.append(cmd)

    def run_history(self, args: list[str]):
        total = len(self.command_history)

        # read history from a file path
        if "-r" in args:
            # get index of -r
            index = args.index("-r")
            file_path = args[index + 1]
            file_content = file_handler.get_file_content(file_path)

            if file_content:
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
            self.append_pending_history = []
            return

        # append only the new commands which were not already in the history
        if "-a" in args:
            # get index of -a
            index = args.index("-a")
            file_path = args[index + 1]

            file_handler.write_to_file(
                file_path,
                "\n".join(self.append_pending_history) + "\n",
                append=True,
            )
            self.append_pending_history = []
            return

        n = total - int(args[0]) if args else 0

        for i in range(n, len(self.command_history)):
            print(f"{i + 1} {self.command_history[i]}")


history = History()
