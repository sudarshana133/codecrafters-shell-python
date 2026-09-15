class AutoCompleter:
    def __init__(self) -> None:
        self.commands = ["echo", "exit"]

    def completer(self, text, state):
        """
        'text' is current word being completed.
        'state' is used by readline to cal this completer
        """
        matches = []
        if state == 0:
            matches = [c + " " for c in self.commands if c.startswith(text)]

        try:
            return matches[state]
        except IndexError:
            return None


auto_completer = AutoCompleter()
