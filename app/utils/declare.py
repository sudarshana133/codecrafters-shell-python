from app.utils.helpers import helpers


class Declare:
    def __init__(self):
        pass

    def run_declare(self, args: list[str]):
        # index of -p
        pIndex = helpers.get_index(args, "-p")
        if pIndex != -1:
            var = args[pIndex + 1]
            print(f"declare: {var}: not found")


declare = Declare()
