import io
import os
import shutil
import subprocess
import sys

from app.utils.declare import declare
from app.utils.file_handler import file_handler
from app.utils.helpers import helpers
from app.utils.history_command import history
from app.utils.jobs_command import jobs


class Commands:
    def __init__(self):
        self.builtins = [
            "echo",
            "type",
            "exit",
            "pwd",
            "cd",
            "complete",
            "jobs",
            "history",
            "declare",
        ]
        # complete command registrations -> Store {completer_command, completer_path}
        self.completers = {}

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

        job_num = jobs.add_job(process.pid, "Running", user_input)
        print(f"[{job_num}] {process.pid}")

    def run_in_pipeline(self, user_input: str):
        commands = user_input.split("|")

        processes = []
        builtin_output = None

        for i, command in enumerate(commands):
            cmd = self.get_command(command.strip())
            args = self.get_command_args(command.strip())

            if cmd in self.builtins:
                # Builtins finish immediately, so we can still capture their output as a string.
                old_stdout = sys.stdout
                sys.stdout = io.StringIO()
                self.builtin_runner(command.strip())
                builtin_output = sys.stdout.getvalue()
                sys.stdout = old_stdout
            else:
                # External command! We must chain them together.

                # 1. Determine where stdin comes from
                if processes:
                    stdin_source = processes[-1].stdout  # Read from previous process
                else:
                    stdin_source = subprocess.PIPE  # Read from our parent shell

                # 2. Determine where stdout goes
                is_last = i == len(commands) - 1
                stdout_dest = None if is_last else subprocess.PIPE

                # Start the process without waiting for it to finish!
                process = subprocess.Popen(
                    [cmd, *args], stdin=stdin_source, stdout=stdout_dest, text=True
                )

                # If a builtin ran right before this first external command (e.g. `echo "hi" | cat`)
                # we feed the builtin's string into this process's stdin, then close it.
                if not processes and builtin_output is not None:
                    if process.stdin:
                        process.stdin.write(builtin_output)
                        process.stdin.close()
                    builtin_output = None

                # 3. Very Important: Close the previous process's stdout in the parent shell.
                # This ensures that when `head` closes its end of the pipe, `tail` gets the SIGPIPE
                # signal and correctly stops running!
                if processes and processes[-1].stdout:
                    processes[-1].stdout.close()

                processes.append(process)

        # Wait ONLY for the last process in the pipeline to finish
        if processes:
            processes[-1].wait()
        if builtin_output is not None:
            # Fallback if the pipeline was only built-in commands
            print(builtin_output, end="")

    def echo(self, user_input: str):
        args = self.get_command_args(user_input)

        if "|" in args:
            self.run_in_pipeline(user_input)
            return

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

        if "|" in args:
            self.run_in_pipeline(user_input)
            return

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

        if "|" in args:
            self.run_in_pipeline(user_input)
            return

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

        if "|" in args:
            self.run_in_pipeline(user_input)
            return

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
        jobs.clean_complete_jobs()

    def execute_custom_command(self, user_input: str):
        command = self.get_command(user_input)
        args = self.get_command_args(user_input)

        if "|" in args:
            self.run_in_pipeline(user_input)
            return

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

    def builtin_runner(self, user_input: str):
        user_command = user_input.strip()
        history.add_command(user_command)

        if user_command == "exit":
            history.write_history_to_file()
            sys.exit(0)

        command = self.get_command(user_command)

        if command == "echo":
            self.echo(user_input)
            return

        if command == "type":
            self.type(user_input)
            return

        if command == "pwd":
            self.pwd()
            return

        if command == "cd":
            self.change_dir(user_input)
            return

        if command == "complete":
            self.complete(user_input)
            return

        if command == "jobs":
            self.jobs_command(user_input)
            return

        if command == "history":
            args = self.get_command_args(user_input)
            history.run_history(args)
            return

        if command == "declare":
            args = self.get_command_args(user_input)
            declare.run_declare(user_input, args)
            return

        if self.is_custom(command):
            self.execute_custom_command(user_input)
            return

        print(f"{command}: command not found")


commands = Commands()
