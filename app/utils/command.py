import os
import shutil
import subprocess

from app.utils.file_handler import file_handler
from app.utils.helpers import helpers


class Commands:
    def __init__(self):
        self.builtins = ["echo", "type", "exit", "pwd", "cd"]

    def get_command_args(self, user_input: str) -> list[str]:
        args = helpers.splitter(user_input)
        return args[1:]

    def get_command(self, user_input: str) -> str:
        args = helpers.splitter(user_input)
        return args[0]

    def is_custom(self, cmd: str) -> bool:
        executable_path = shutil.which(cmd)

        return bool(executable_path and os.access(executable_path, os.X_OK))

    # Redirect standard output to a file
    def redirect(self, args, output: str):
        file_path = file_handler.get_file_path(args)

        if file_path:
            file_handler.write_to_file(file_path, output)

        else:
            print(output)

    def echo(self, user_input: str):
        args = self.get_command_args(user_input)

        if ">" in args or "1>" in args:
            # get index of > or 1>
            if ">" in args:
                index = args.index(">")
            else:
                index = args.index("1>")

            self.redirect(args, " ".join(args[:index]) + "\n")
            return

        print(" ".join(args))

    def type(self, user_input: str):
        args = self.get_command_args(user_input)
        if args[0] in self.builtins:
            print(f"{args[0]} is a shell builtin")
        elif shutil.which(args[0]):
            print(f"{args[0]} is {shutil.which(args[0])}")
        else:
            print(f"{args[0]}: not found")

    def pwd(self):
        print(os.getcwd())

    def change_dir(self, user_input: str):
        args = self.get_command_args(user_input)

        if args[0] == "~":
            os.chdir(os.path.expanduser("~"))
            return
        if args[0] and os.path.isdir(args[0]):
            os.chdir(args[0])
            return
        print(f"cd: {args[0]}: No such file or directory")

    def execute_custom_command(self, user_input: str):
        command = self.get_command(user_input)
        args = self.get_command_args(user_input)

        index = None

        if ">" in args or "1>" in args:
            # get index of > or 1>
            if ">" in args:
                index = args.index(">")
            else:
                index = args.index("1>")

        cmd_args = args[:index] if index is not None else args
        result = subprocess.run(
            [command, *cmd_args],
            check=False,
            shell=False,
            text=True,
            capture_output=True,
        )

        if ">" in args or "1>" in args:
            if result.stderr:
                print(result.stderr, end="")

            self.redirect(
                args, output=result.stdout if result.stdout is not None else ""
            )
            return

        if result.stdout:
            print(result.stdout, end="")

        if result.stderr:
            print(result.stderr, end="")


commands = Commands()
