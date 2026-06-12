import sys
import shutil
import subprocess
import os
from pathlib import Path
import shlex


def split(user_input):
    lst = shlex.split(user_input)
    return lst[0], lst[1:]


def create_and_write(file_name, content):
    dir_name = os.path.dirname(file_name)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)

    with open(file_name, 'w') as file:
        file.write(content)


def echo(args):
    if '>' in args or '1>' in args:
        idx = args.index('>') if '>' in args else args.index('1>')
        file_name = args[idx + 1]
        create_and_write(file_name, " ".join(args[:idx]) + "\n")

    elif '2>' in args:
        idx = args.index('2>')
        file_name = args[idx + 1]
        create_and_write(file_name, "")
        print(" ".join(args[:idx]))
    else:
        print(" ".join(args))


def type_cmd(cmd_name: str) -> str:
    if cmd_name in ("echo", "type", "exit", "pwd", "cd"):
        return f"{cmd_name} is a shell builtin"

    cmd_path = shutil.which(cmd_name)
    if cmd_path:
        return f"{cmd_name} is {cmd_path}"
    return f"{cmd_name}: not found"


def custom(custom_exe, args) -> bool:
    if shutil.which(custom_exe):
        if '>' in args or '1>' in args:
            idx = args.index('>') if '>' in args else args.index('1>')
            file_name = args[idx + 1]
            cmd_args = [custom_exe] + args[:idx]

            res = subprocess.run(cmd_args, stdout=subprocess.PIPE, text=True)
            create_and_write(file_name, res.stdout)

        elif '2>' in args:
            idx = args.index('2>')
            file_name = args[idx + 1]
            cmd_args = [custom_exe] + args[:idx]

            res = subprocess.run(cmd_args, stderr=subprocess.PIPE, text=True)
            if res.stderr:
                create_and_write(file_name, res.stderr + "\n")
        else:
            subprocess.run([custom_exe] + args, text=True)
        return True

    return False


def change_dir(path):
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
