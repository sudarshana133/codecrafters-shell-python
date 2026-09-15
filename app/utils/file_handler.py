import os


class FileHandler:
    def __init__(self) -> None:
        pass

    # fetch file path from the arguments
    def get_file_path(self, args: list[str]) -> str | None:
        characters = (">", "1>", "2>", ">>", "1>>")

        for char in characters:
            if char in args:
                return args[args.index(char) + 1]
        return None

    def write_to_file(self, file_path: str, content: str, append: bool = False):
        # Create the required directory if required
        folder = os.path.dirname(file_path)
        if folder:
            os.makedirs(folder, exist_ok=True)

        with open(file_path, "w" if not append else "a") as file:
            file.write(content)


file_handler = FileHandler()
