import sys
import shutil
import subprocess
import os


def echo(user_input):
    lst = user_input.split(" ")
    output = ""
    for i in range(1, len(lst)):
        output += lst[i] + " "
    return output


def type_cmd(user_input) -> str:
    lst = user_input.split(" ")
    lst.pop(0)
    cmd = lst[0]
    if cmd in ("echo", "type", "exit", "pwd"):
        return f"{cmd} is a shell builtin"
    if shutil.which(cmd):
        return f"{cmd} is {shutil.which(cmd)}"
    return f"{cmd}: not found"


def custom(user_input) -> bool:
    lst = user_input.split(" ")
    custom_exe = lst[0]

    if shutil.which(custom_exe):
        res = subprocess.run(lst, text=True)
        return True

    return False


def main():
    while True:
        sys.stdout.write("$ ")
        user_input = input()
        if user_input == "exit":
            break
        cmd = user_input.split(" ")[0]

        if cmd == "echo":
            output = echo(user_input)
            print(output)
            continue

        if cmd == "type":
            output = (type_cmd(user_input))
            print(output)
            continue

        if cmd == "pwd":
            output = os.getcwd()
            print(output)
            continue

        is_custom = custom(user_input)
        if is_custom:
            continue

        print(f"{user_input}: command not found")


if __name__ == "__main__":
    main()
