import sys

from app.utils.command import commands


def main():

    while True:
        sys.stdout.write("$ ")
        user_input = input()

        user_command = user_input.strip()

        if user_command == "exit":
            break

        command = commands.get_command(user_command)

        if command == "echo":
            commands.echo(user_input)
            continue

        print(f"{command}: command not found")


if __name__ == "__main__":
    main()
