import os
import readline
import subprocess

from app.utils.command import commands
from app.utils.file_handler import file_handler


class AutoCompleter:
    def __init__(self) -> None:
        self.builtins = ["echo", "type", "exit", "pwd", "cd", "complete"]

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

        cmd = readline.get_line_buffer().split()[0].strip()

        if readline.get_begidx() == 0:
            matches = [c + " " for c in all_options if c.startswith(text)]

        elif cmd in commands.completers:
            if cmd in commands.completers:
                # find the argv[1], argv[2], argv[3]
                raw_line = readline.get_line_buffer()
                line_buffer = raw_line.split()
                argv1 = line_buffer[0]

                # For argv2 (word being completed):
                # If length is >= 3 (e.g. ['git', 'remote', 'set']), it's index 2 ('set')
                # If length is 2 (e.g. ['git', 'set']), it's index 1 ('set')
                argv2 = (
                    line_buffer[2]
                    if len(line_buffer) >= 3
                    else (line_buffer[1] if len(line_buffer) >= 2 else "")
                )

                # For argv3 (word before the one being completed):
                # If length is >= 3 (e.g. ['git', 'remote', 'set']), preceding word is index 1 ('remote')
                # If length is < 3 (e.g. ['git', 'set']), there is no preceding word, so ""
                argv3 = line_buffer[1] if len(line_buffer) >= 3 else ""

                cmd_args = [argv1, argv2, argv3]

                env_vars = {
                    "COMP_LINE": raw_line,
                    "COMP_POINT": len(line_buffer),
                }

                result = subprocess.run(
                    [commands.completers[cmd], *cmd_args],
                    capture_output=True,
                    check=False,
                    text=True,
                    shell=False,
                    env=env_vars,
                )
                if result.returncode == 0:
                    results = result.stdout.splitlines()
                    matches = [c + " " for c in results if c.startswith(text)]

        else:
            head, tail = os.path.split(text)
            items = file_handler.get_files_and_folders(head)

            for item in items:
                if item.startswith(tail):
                    full_path = os.path.join(head, item)
                    if os.path.isdir(full_path):
                        matches.append(full_path + "/")
                    else:
                        matches.append(full_path + " ")

        try:
            return matches[state]
        except IndexError:
            return None


auto_completer = AutoCompleter()
