import os
import shutil
import subprocess


class Commands:
    def __init__(self):
        self.builtins = ["echo", "type", "exit", "pwd", "cd"]

    def get_command_args(self, user_input: str) -> list[str]:
        args: list[str] = []

        tmp = ""
        is_single_quote = False
        is_double_quote = False

        i = 0
        while i < len(user_input):
            # backslash char removes next char's special meaning
            if user_input[i] == "\\" and not is_single_quote:
                if i < len(user_input) - 1:
                    i += 1
                    if user_input != " ":
                        tmp += user_input[i]
                    i += 1
                continue

            # toggle the is_double_quote
            if user_input[i] == '"' and not is_single_quote:
                is_double_quote = not is_double_quote
                i += 1
                continue

            # toggle the is_single_quote
            if user_input[i] == "'" and not is_double_quote:
                is_single_quote = not is_single_quote
                i += 1
                continue

            if is_double_quote:
                # if it's inside double quote push everything to tmp
                if user_input[i] != '"':
                    tmp += user_input[i]
                i += 1
                continue

            if is_single_quote:
                # if it's inside single quote push everything to tmp
                if user_input[i] != "'":
                    tmp += user_input[i]
                i += 1
                continue

            # if not inside single quote then don't push spaces and quotes
            if user_input[i] not in [" ", "'", '"', "\\"]:
                tmp += user_input[i]

            if user_input[i] == " ":
                if len(tmp) > 0:
                    args.append(tmp)
                tmp = ""

            i += 1

        if tmp:
            args.append(tmp)

        return args[1:]

    def get_command(self, user_input: str) -> str:
        tmp = user_input.split()
        return tmp[0]

    def is_custom(self, cmd: str) -> bool:
        executable_path = shutil.which(cmd)

        return bool(executable_path and os.access(executable_path, os.X_OK))

    def echo(self, user_input: str):
        args = self.get_command_args(user_input)
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
        result = subprocess.run(
            user_input,
            check=False,
            shell=True,
            capture_output=True,
            text=True,
        )
        print(result.stdout, end="")


commands = Commands()
