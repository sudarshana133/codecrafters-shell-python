import os
import readline

from app.utils.file_handler import file_handler


class AutoCompleter:
    def __init__(self) -> None:
        self.builtins = ["echo", "type", "exit", "pwd", "cd"]

    def get_executables(self):
        directories = os.environ.get("PATH", "").split(":")
        executables = []

        for directory in directories:
            if os.path.exists(directory):
                dir_list = os.listdir(directory)
                executables += dir_list

        return executables

    def completer(self, text, state):
        """
        'text' is current word being completed.
        'state' is used by readline to cal this completer
        """

        executables = self.get_executables()
        all_options = set(self.builtins + executables)

        matches = []
        if readline.get_begidx() == 0:
            matches = [c + " " for c in all_options if c.startswith(text)]
        else:
            files = file_handler.get_files(os.getcwd())
            matches = [f + " " for f in files if f.startswith(text)]

        try:
            return matches[state]
        except IndexError:
            return None


auto_completer = AutoCompleter()
