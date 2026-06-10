import sys


def echo(user_input):
    lst = user_input.split(" ")
    output = ""
    for i in range(1, len(lst)):
        output += lst[i] + " "
    return output


def main():
    while True:
        sys.stdout.write("$ ")
        user_input = input()
        if user_input == "exit":
            break

        if "echo" in user_input:
            output = echo(user_input)
            print(output)
            continue

        print(f"{user_input}: command not found")


if __name__ == "__main__":
    main()
