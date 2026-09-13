import sys


def main():

    while True:
        sys.stdout.write("$ ")
        user_command = input()

        user_command = user_command.strip()

        if user_command == "exit":
            break

        print(f"{user_command}: command not found")


if __name__ == "__main__":
    main()
