import readline

from app.utils.auto_completer import auto_completer
from app.utils.command import commands
from app.utils.jobs_command import jobs


def main():
    readline.set_completer_delims(" \t\n")
    readline.set_completer(auto_completer.completer)

    if readline.__doc__ and "libedit" in readline.__doc__:
        readline.parse_and_bind("bind ^I rl_complete")
    else:
        readline.parse_and_bind("tab: complete")

    while True:
        jobs.clean_complete_jobs(is_background=True)
        user_input = input("$ ")

        commands.builtin_runner(user_input)


if __name__ == "__main__":
    main()
