import readline

from app.utils.auto_completer import auto_completer
from app.utils.command import commands


def main():
    readline.set_completer_delims(" \t\n")
    readline.set_completer(auto_completer.completer)

    if readline.__doc__ and "libedit" in readline.__doc__:
        readline.parse_and_bind("bind ^I rl_complete")
    else:
        readline.parse_and_bind("tab: complete")

    while True:
        user_input = input("$ ")

        user_command = user_input.strip()

        if user_command == "exit":
            break

        command = commands.get_command(user_command)

        if command == "echo":
            commands.echo(user_input)
            continue

        if command == "type":
            commands.type(user_input)
            continue

        if command == "pwd":
            commands.pwd()
            continue

        if command == "cd":
            commands.change_dir(user_input)
            continue

        if command == "complete":
            commands.complete(user_input)
            continue

        if commands.is_custom(command):
            commands.execute_custom_command(user_input)
            continue

        print(f"{command}: command not found")


if __name__ == "__main__":
    main()
