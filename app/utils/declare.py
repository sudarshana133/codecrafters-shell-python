from app.utils.helpers import helpers


class Declare:
    def __init__(self):
        """
        Stores the variable and it's value
        e.g: {"var": "value"}
        """
        self.variables = {}

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
