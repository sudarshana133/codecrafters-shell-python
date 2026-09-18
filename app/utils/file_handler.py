import os


class FileHandler:
    def __init__(self) -> None:
        pass

    # fetch file path from the arguments
    def get_file_path(self, args: list[str]) -> str | None:
        characters = (">", "1>", "2>", ">>", "1>>", "2>>")

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

    def get_files(self, path) -> list[str]:
        """
        Return all the files present in path
        """
        files = os.listdir(path)
        files = [f for f in files if os.path.isfile(f)]
        return files

    def get_files_and_folders(self, path: str | None) -> list[str]:
        """
        Return all the entries from the folder
        """
        if not path:
            path = os.getcwd()
        items = os.listdir(path)
        return items

    def get_file_content(self, path: str) -> str:
        """
        Return the contents of the file
        """
        if not os.path.isfile(path):
            return ""

        with open(path, "r") as file:
            content = file.read().strip()

        return content


file_handler = FileHandler()
