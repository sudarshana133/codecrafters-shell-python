import sys
import shutil
import subprocess
import os
from pathlib import Path
import shlex

def echo(user_input):
   lst = shlex.split(user_input)
   lst.pop(0)
   return " ".join(lst)


def type_cmd(user_input) -> str:
    lst = user_input.split(" ")
    lst.pop(0)
    cmd = lst[0]
    if cmd in ("echo", "type", "exit", "pwd", "cd"):
        return f"{cmd} is a shell builtin"
    if shutil.which(cmd):
        return f"{cmd} is {shutil.which(cmd)}"
    return f"{cmd}: not found"


def custom(user_input) -> bool:
    lst = user_input.split(" ")
    custom_exe = lst[0]

    if shutil.which(custom_exe):
        subprocess.run(lst, text=True)
        return True

    return False


def change_dir(user_input):
    lst = user_input.split()
    path = lst[1]

    try:
        if path == "~":
            path = str(Path.home())
        os.chdir(path)
    except:
        print(f"cd: {path}: No such file or directory")


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

        if cmd == "cd":
            change_dir(user_input)
            continue

        is_custom = custom(user_input)
        if is_custom:
            continue

        print(f"{user_input}: command not found")


if __name__ == "__main__":
    main()
