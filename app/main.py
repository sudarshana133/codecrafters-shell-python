import os
import readline

from app.commands import change_dir, custom, echo, type_cmd
from app.utils import completer, split


def main():
    # Configure readline once before the loop starts
    readline.set_completer(completer)
    readline.set_completer_delims(" \t\n")

    # Handle macOS (libedit) vs Linux (GNU readline) bindings
    if readline.__doc__ and "libedit" in readline.__doc__:
        readline.parse_and_bind("bind ^I rl_complete")
    else:
        readline.parse_and_bind("tab: complete")

    while True:
        user_input = input("$ ")

        if not user_input:
            continue

        if user_input.strip() == "exit":
            break
        cmd, args = split(user_input)

        if cmd == "echo":
            echo(args)
            continue

        if cmd == "type":
            if args:
                output = type_cmd(args[0])
                print(output)
            continue

        if cmd == "pwd":
            output = os.getcwd()
            print(output)
            continue

        if cmd == "cd":
            change_dir(args[0])
            continue

        is_custom = custom(cmd, args)
        if is_custom:
            continue

        print(f"{user_input}: command not found")


if __name__ == "__main__":
    main()
