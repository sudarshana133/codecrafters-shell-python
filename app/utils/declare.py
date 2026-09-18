from app.utils.helpers import helpers


class Declare:
    def __init__(self):
        """
        Stores the variable and it's value
        e.g: {"var": "value"}
        """
        self.variables = {}

    def get_value(self, var: str):
        """Return the value of variable"""
        if var in self.variables:
            return self.variables[var]
        return None

    def expand_with_braces(self, args: list[str]) -> list[str]:
        new_args = []
        for i, arg in enumerate(args):
            if "${" in arg:
                j = arg.index("{") + 1
                tmp = ""
                # get the index of }
                while arg[j] != "}":
                    tmp += arg[j]
                    j += 1

                var = tmp
                value = self.get_value(var)
                if value is not None:
                    args[i] = arg.replace(f"${{{var}}}", str(value))
                else:
                    args[i] = arg.replace(f"${{{var}}}", "")

            # Don't push arg if it's empty
            if args[i] == "":
                continue

            new_args.append(args[i])

        return new_args

    def replace_values(self, args: list[str]) -> list[str]:
        new_args = []
        for i, arg in enumerate(args):
            if "$" in arg:
                parts = arg.split("$")
                prefix = parts[0]  # Get the prefix
                var = parts[1]  # Get the variable name

                value = self.get_value(var)
                if value is not None:
                    args[i] = prefix + str(value)
                else:
                    args[i] = prefix

            # Don't push arg if it's empty
            if args[i] == "":
                continue

            new_args.append(args[i])

        return new_args

    def run_declare(self, args: list[str]):
        # index of -p
        pIndex = helpers.get_index(args, "-p")
        if pIndex != -1:
            var = args[pIndex + 1]
            if var in self.variables:
                val = self.variables[var]
                print(f'declare -- {var}="{val}"')
            else:
                print(f"declare: {var}: not found")
            return

        # get index of =
        for arg in args:
            if "=" in arg:
                var = arg.split("=")[0]
                value = arg.split("=")[1]

                # validating if the variable name is correct or not
                if not var.isidentifier():
                    print(f"declare: `{var}={value}': not a valid identifier")
                    return

                self.variables[var] = value


declare = Declare()
