import os
import readline
import shlex
from typing import Iterable, Union


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
    if readline.get_begidx() == 0:
        options = splitter(os.environ.get("PATH", ""))
        builtins = ["echo", "exit", "type", "pwd", "cd"]
        all_options = set(options + builtins)
        matches = sorted([o + " " for o in all_options if o.startswith(text)])

    else:
        line = readline.get_line_buffer()
        words = line.split()

        if len(words) < 2:
            matches = [f + " " for f in get_files() if f.startswith(text)]
        else:
            second_word = words[1]
            dir_path = os.path.dirname(second_word)
            prefix = os.path.basename(second_word)

            path = os.getcwd() + "/" + dir_path

            if os.path.isdir(path):
                files = get_files(path)
                matches = []
                for f in files:
                    if f.startswith(prefix):
                        if os.path.isdir(path + "/" + f):
                            matches.append(f + "/")
                        else:
                            matches.append(f + " ")
            else:
                matches = [f + " " for f in get_files() if f.startswith(text)]
    try:
        return matches[state]
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


def get_files(path: str = os.getcwd()) -> list[str]:
    files = []

    if os.path.exists(path):
        files = os.listdir(path)

    return files
