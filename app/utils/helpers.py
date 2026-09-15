class Helpers:
    def __init__(self) -> None:
        pass

    def splitter(self, user_input: str) -> list[str]:
        args: list[str] = []

        tmp = ""
        is_single_quote = False
        is_double_quote = False

        i = 0
        while i < len(user_input):
            # backslash char removes next char's special meaning
            if user_input[i] == "\\" and not is_single_quote:
                if i < len(user_input) - 1:
                    i += 1
                    # don't push if it's space as later space will be introduces while joining each argument
                    if user_input != " ":
                        tmp += user_input[i]
                    i += 1
                continue

            # toggle the is_double_quote
            if user_input[i] == '"' and not is_single_quote:
                is_double_quote = not is_double_quote
                i += 1
                continue

            # toggle the is_single_quote
            if user_input[i] == "'" and not is_double_quote:
                is_single_quote = not is_single_quote
                i += 1
                continue

            if is_double_quote:
                # if it's inside double quote push everything to tmp
                if user_input[i] != '"':
                    tmp += user_input[i]
                i += 1
                continue

            if is_single_quote:
                # if it's inside single quote push everything to tmp
                if user_input[i] != "'":
                    tmp += user_input[i]
                i += 1
                continue

            # if not inside single quote then don't push spaces and quotes
            if user_input[i] not in [" ", "'", '"', "\\"]:
                tmp += user_input[i]

            if user_input[i] == " ":
                if len(tmp) > 0:
                    args.append(tmp)
                tmp = ""

            i += 1

        if tmp:
            args.append(tmp)

        return args


helpers = Helpers()
