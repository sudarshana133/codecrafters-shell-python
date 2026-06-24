import os
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List

from app.utils import create_and_write, find_first_index


def echo(args):
    redirect_ops = {">", "1>", "2>", ">>", "2>>", "1>>"}
    idx = find_first_index(args, redirect_ops)
    if idx == -1:
        print(" ".join(args))
        return

    op = args[idx]
    file_name = args[idx + 1]

    if op in {">", "1>"}:
        create_and_write(file_name, " ".join(args[:idx]) + "\n")

    elif op in {">>", "1>>"}:
        create_and_write(file_name, " ".join(args[:idx]) + "\n", "a")

    elif op == "2>":
        create_and_write(file_name, "")
        print(" ".join(args[:idx]))

    elif op == "2>>":
        create_and_write(file_name, "")
        print(" ".join(args[:idx]))


def type_cmd(cmd_name: str) -> str:
    if cmd_name in ("echo", "type", "exit", "pwd", "cd", "complete"):
        return f"{cmd_name} is a shell builtin"

    cmd_path = shutil.which(cmd_name)
    if cmd_path:
        return f"{cmd_name} is {cmd_path}"
    return f"{cmd_name}: not found"


def custom(custom_exe, args) -> bool:
    if not shutil.which(custom_exe):
        return False

    redirect_ops = {">", "1>", "2>", ">>", "2>>", "1>>"}
    idx = find_first_index(args, redirect_ops)

    if idx == -1:
        subprocess.run([custom_exe] + args, text=True)
        return True

    op = args[idx]
    file_name = args[idx + 1]
    cmd_args = [custom_exe] + args[:idx]

    if op in {">", "1>"}:
        res = subprocess.run(cmd_args, stdout=subprocess.PIPE, text=True)
        create_and_write(file_name, res.stdout)

    elif op in {">>", "1>>"}:
        res = subprocess.run(cmd_args, stdout=subprocess.PIPE, text=True)
        create_and_write(file_name, res.stdout, "a")

    elif op == "2>":
        res = subprocess.run(cmd_args, stderr=subprocess.PIPE, text=True)
        create_and_write(file_name, res.stderr)

    elif op == "2>>":
        res = subprocess.run(cmd_args, stderr=subprocess.PIPE, text=True)
        create_and_write(file_name, res.stderr, "a")

    return True


def change_dir(path):
    try:
        if path == "~":
            path = str(Path.home())
        os.chdir(path)
    except:
        print(f"cd: {path}: No such file or directory")


def complete_cmd(args: List[str], completer_paths: Dict):
    if "-C" in args:
        completer_idx = args.index("-C")
        completer_path = args[completer_idx + 1]
        command = args[completer_idx + 2]
        completer_paths[command] = completer_path

    elif "-p" in args:
        cmd = args[-1].strip()
        result = completer_paths.get(cmd)
        if not result:
            print(f"complete: {cmd}: no completion specification")
            return

        print(f"complete -C '{result}' {cmd}")
