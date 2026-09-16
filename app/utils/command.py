import os
import shutil
import subprocess

from app.utils.file_handler import file_handler
from app.utils.helpers import helpers
from app.utils.jobs_command import jobs


class Commands:
    def __init__(self):
        self.builtins = ["echo", "type", "exit", "pwd", "cd", "complete", "jobs"]
        # complete command registrations -> Store {completer_command, completer_path}
        self.completers = {}
        # to track job number
        self.job_num = 1
        """
         To track the jobs -> tracker will follow this format
         job_num -> (pid, status, user_input)
        """
        self.jobs: dict[int, tuple[int, str, str]] = {}

    def get_command_args(self, user_input: str) -> list[str]:
        args = helpers.splitter(user_input)
        return args[1:]

    def get_command(self, user_input: str) -> str:
        args = helpers.splitter(user_input)
        return args[0]

    def is_custom(self, cmd: str) -> bool:
        executable_path = shutil.which(cmd)

        return bool(executable_path and os.access(executable_path, os.X_OK))

    # Redirect standard output to a file
    def redirect(self, args, output: str, append: bool = False):
        file_path = file_handler.get_file_path(args)

        if file_path:
            file_handler.write_to_file(file_path, output, append)

        else:
            print(output)

    # handle background jobs
    def run_in_background(self, cmd: str, args: list[str], user_input: str):
        # remove the & first
        args.remove("&")
        process = subprocess.Popen(cmd + " " + " ".join(args), shell=True)

        self.jobs[self.job_num] = (process.pid, "Running", user_input)
        print(f"[{self.job_num}] {process.pid}")
        self.job_num += 1

    def echo(self, user_input: str):
        args = self.get_command_args(user_input)

        if "&" in args:
            self.run_in_background("echo", args, user_input)
            return

        if ">" in args or "1>" in args or ">>" in args or "1>>" in args:
            # get index of > or 1>
            if ">" in args:
                index = args.index(">")
            elif "1>" in args:
                index = args.index("1>")
            elif ">>" in args:
                index = args.index(">>")
            else:
                index = args.index("1>>")

            self.redirect(
                args, " ".join(args[:index]) + "\n", ">>" in args or "1>>" in args
            )
            return

        if "2>" in args or "2>>" in args:
            index = args.index("2>") if "2>" in args else args.index("2>>")
            self.redirect(args, "", "2>>" in args)
            print(" ".join(args[:index]))
            return

        print(" ".join(args))

    def type(self, user_input: str):
        args = self.get_command_args(user_input)

        if "&" in args:
            self.run_in_background("type", args, user_input)
            return

        if args[0] in self.builtins:
            print(f"{args[0]} is a shell builtin")
        elif shutil.which(args[0]):
            print(f"{args[0]} is {shutil.which(args[0])}")
        else:
            print(f"{args[0]}: not found")

    def pwd(self):
        print(os.getcwd())

    def change_dir(self, user_input: str):
        args = self.get_command_args(user_input)

        if "&" in args:
            self.run_in_background("cd", args, user_input)
            return

        if args[0] == "~":
            os.chdir(os.path.expanduser("~"))
            return
        if args[0] and os.path.isdir(args[0]):
            os.chdir(args[0])
            return
        print(f"cd: {args[0]}: No such file or directory")

    def complete(self, user_input: str):
        args = self.get_command_args(user_input)

        if "&" in args:
            self.run_in_background("complete", args, user_input)
            return

        if "-p" in args:
            # get index of -p
            index = args.index("-p")
            command = args[index + 1]

            if self.completers.get(command):
                print(f"complete -C '{self.completers[command]}' {command}")
                return
            print(f"complete: {command}: no completion specification")

        elif "-C" in args:
            # get index of -C
            index = args.index("-C")
            completer_path = args[index + 1]
            completer_command = args[index + 2]
            self.completers[completer_command] = completer_path

        # remove the completer
        elif "-r" in args:
            # get the index of -r
            index = args.index("-r")
            command = args[index + 1]
            if command in self.completers:
                del self.completers[command]

    def jobs_command(self, user_input: str):
        for job_num in list(self.jobs):
            pid, _, command = self.jobs[job_num]
            marker = jobs.get_marker(job_num, self.job_num)
            job_status = jobs.get_job_status(pid)

            print(f"[{job_num}]{marker}  {job_status:<24}{command}")

            if job_status == "Done":
                del self.jobs[job_num]

    def execute_custom_command(self, user_input: str):
        command = self.get_command(user_input)
        args = self.get_command_args(user_input)

        if "&" in args:
            self.run_in_background(command, args, user_input)
            return

        index = None

        if (
            ">" in args
            or "1>" in args
            or "2>" in args
            or ">>" in args
            or "1>>" in args
            or "2>>" in args
        ):
            # get index of > or 1>
            if ">" in args:
                index = args.index(">")
            elif "1>" in args:
                index = args.index("1>")
            elif "2>" in args:
                index = args.index("2>")
            elif ">>" in args:
                index = args.index(">>")
            elif "1>>" in args:
                index = args.index("1>>")
            elif "2>>" in args:
                index = args.index("2>>")

        cmd_args = args[:index] if index is not None else args
        result = subprocess.run(
            [command, *cmd_args],
            check=False,
            shell=False,
            text=True,
            capture_output=True,
        )

        if "2>" in args or "2>>" in args:
            if result.stdout:
                print(result.stdout, end="")

            self.redirect(
                args,
                output=result.stderr if result.stderr is not None else "",
                append="2>>" in args,
            )
            return

        if ">" in args or "1>" in args or ">>" in args or "1>>" in args:
            if result.stderr:
                print(result.stderr, end="")

            self.redirect(
                args,
                output=result.stdout if result.stdout is not None else "",
                append=">>" in args or "1>>" in args,
            )
            return

        if result.stdout:
            print(result.stdout, end="")

        if result.stderr:
            print(result.stderr, end="")


commands = Commands()
