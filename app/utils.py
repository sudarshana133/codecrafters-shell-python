import os
import readline
import shlex
from typing import Iterable, Optional, Union


def split(user_input):
    lst = shlex.split(user_input)
    return lst[0], lst[1:]


def create_and_write(file_name, content, mode="w"):
    dir_name = os.path.dirname(file_name)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)

    with open(file_name, mode) as file:
        file.write(content)


def splitter(path: str):
    directories = path.split(":")
    lst = []
    for directory in directories:
        if os.path.exists(directory):
            dir_list = os.listdir(directory)
            lst += dir_list

    return lst


def completer(text, state):
    # state = 0 indicates start of a completion request
    if state == 0:
        if readline.get_begidx() == 0:
            options = splitter(os.environ.get("PATH", ""))
            builtins = ["echo", "exit", "type", "pwd", "cd"]
            all_options = set(options + builtins)
            completer.matches = sorted(
                [o + " " for o in all_options if o.startswith(text)]
            )
        else:
            # We are completing argument (a file or directory)
            if "/" in text:
                prefix = os.path.basename(text)
                dir_prefix = text[: -len(prefix)] if prefix else text
                dir_path = dir_prefix

            else:
                prefix = text
                dir_prefix = ""
                dir_path = "."

            resolved_dir_path = os.path.expanduser(dir_path)
            completer.matches = []

            if os.path.isdir(resolved_dir_path):
                try:
                    files = os.listdir(resolved_dir_path)
                except Exception:
                    files = []

                for f in sorted(files):
                    if f.startswith(".") and not prefix.startswith("."):
                        continue
                    if f.startswith(prefix):
                        full_path = os.path.join(resolved_dir_path, f)

                        if os.path.isdir(full_path):
                            completer.matches.append(dir_prefix + f + "/")
                        else:
                            completer.matches.append(dir_prefix + f + " ")

    try:
        return completer.matches[state]
    except IndexError:
        return None


def find_first_index(args: list, targets: Union[str, Iterable[str]]) -> int:
    """
    Finds the index of the first occurrence of any item from 'targets' in 'args'.

    :param args: The list of arguments to search (e.g. ['echo', 'hello', '>', 'out.txt'])
    :param targets: A single target string (e.g. '>') or an iterable collection of targets (e.g. ['>', '1>'])
    :return: The index of the first matched target, or -1 if none of the targets are found.
    """
    if isinstance(targets, str):
        target_set = {targets}
    else:
        target_set = set(targets)

    for idx, item in enumerate(args):
        if item in target_set:
            return idx

    return -1


def get_files(path: Optional[str] = None) -> list[str]:
    files = []
    if not path:
        path = os.getcwd()

    if os.path.exists(path):
        files = os.listdir(path)

    return files
