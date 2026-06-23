# How Shell Autocompletion Works in Python

This document explains how Python's `readline` library handles autocompletion, how our custom `completer` function works, and step-by-step traces for every common completion scenario.

---

## 1. How Python `readline` Queries the Completer

When a user typing in the terminal presses `[TAB]`, the following handshake occurs between the operating system's `readline` library and Python:

1. **Token Identification**: `readline` looks at the characters immediately before the cursor to find the word being completed (the "token"). It splits the line using word delimiters (which we configured as `" \t\n"`).
2. **First Call (`state = 0`)**: `readline` calls `completer(text, state=0)`.
   * `text` is the string representing the token under the cursor.
   * `state` starts at `0`.
3. **Looping**: `readline` keeps calling `completer(text, state)` with `state = 1`, `state = 2`, etc.
4. **End of Loop**: When `completer` returns `None`, `readline` stops calling it.
5. **Execution**:
   * If exactly **one** match was returned, `readline` automatically updates the command line with that match.
   * If **multiple** matches were returned, `readline` updates the command line to the longest common prefix. If the user presses `[TAB]` again, it prints all matches on the screen.
   * If **no** matches were returned, nothing changes.

---

## 2. Why We Changed Delimiters

By default, `readline` splits words using characters like `/` (slash), `-` (hyphen), and `@`. 

### The Problem:
If the user types `cat app/main.py` and presses `[TAB]`:
* Default delimiters treat `/` as a separator.
* `readline` splits the token into `"app"` and `"main.py"`.
* It calls `completer` with `text="main.py"`.
* Your code has no idea that `"main.py"` is inside the `"app/"` directory, making relative or absolute path completion impossible.

### The Solution:
By running `readline.set_completer_delims(" \t\n")` in `app/main.py`, we tell `readline` to **only split words by spaces, tabs, and newlines**. Now:
* `app/main.py` is treated as a single token.
* `readline` calls `completer` with `text="app/main.py"`, letting us parse the path correctly.

---

## 3. Visual Traces for Each Use Case

### Case A: Command Completion
**User Types:** `ec` ➡️ `[TAB]`
**State of terminal:** `readline.get_begidx() == 0` (Cursor is at the start of the line).

```
1. readline calls completer(text="ec", state=0)
2. begidx is 0, so it searches system $PATH and builtins:
   - Matches starting with "ec": ["echo"]
   - Adds space to matches: ["echo "]
3. Returns "echo "
4. readline calls completer(text="ec", state=1)
   - Cache check finds no index 1
5. Returns None
6. Result: Line updates to "$ echo "
```

---

### Case B: File Completion (Current Directory)
**User Types:** `echo your_` ➡️ `[TAB]`
**State of terminal:** `readline.get_begidx() == 5` (Word starts at index 5, which is $> 0$).

```
1. readline calls completer(text="your_", state=0)
2. Since there is no "/" in text:
   - prefix = "your_"
   - dir_path = "."
3. List directory "." and find files starting with "your_":
   - Found: "your_program.sh" (regular file)
   - Cache matches: ["your_program.sh "] (added space since it's a file)
4. Returns "your_program.sh "
5. readline calls completer(text="your_", state=1)
6. Returns None
7. Result: Line updates to "$ echo your_program.sh "
```

---

### Case C: Subdirectory Completion
**User Types:** `cd ap` ➡️ `[TAB]`
**State of terminal:** `readline.get_begidx() == 3` ($> 0$).

```
1. readline calls completer(text="ap", state=0)
2. Since there is no "/" in text:
   - prefix = "ap"
   - dir_path = "."
3. List directory "." and find files starting with "ap":
   - Found: "app" (directory)
   - Cache matches: ["app/"] (added slash since it's a folder, no space)
4. Returns "app/"
5. readline calls completer(text="ap", state=1)
6. Returns None
7. Result: Line updates to "$ cd app/" (no space, user can keep typing!)
```

---

### Case D: Path Completion in Subdirectory
**User Types:** `cat app/m` ➡️ `[TAB]`
**State of terminal:** `readline.get_begidx() == 4` ($> 0$).

```
1. readline calls completer(text="app/m", state=0)
2. "/" is present in text:
   - prefix = os.path.basename("app/m") = "m"
   - dir_prefix = text[:-len(prefix)] = "app/m"[:-1] = "app/"
   - dir_path = "app/"
3. List files in "app/" starting with "m":
   - Found: "main.py" (regular file)
   - Match: dir_prefix + f + " " -> "app/" + "main.py" + " " -> "app/main.py "
   - Cache matches: ["app/main.py "]
4. Returns "app/main.py "
5. readline calls completer(text="app/m", state=1)
6. Returns None
7. Result: Line updates to "$ cat app/main.py "
```

---

### Case E: Folder Search ending in Slash
**User Types:** `cat app/` ➡️ `[TAB]`
**State of terminal:** `readline.get_begidx() == 4` ($> 0$).

```
1. readline calls completer(text="app/", state=0)
2. "/" is present in text:
   - prefix = os.path.basename("app/") = ""
   - Since prefix is empty:
     dir_prefix = text = "app/"
     dir_path = "app/"
3. List all files in "app/" (since prefix is "", everything matches):
   - Found: "commands.py", "main.py", "utils.py"
   - Cache matches: ["app/commands.py ", "app/main.py ", "app/utils.py "]
4. Returns "app/commands.py "
5. readline calls completer(text="app/", state=1)
   - Returns "app/main.py "
6. readline calls completer(text="app/", state=2)
   - Returns "app/utils.py "
7. readline calls completer(text="app/", state=3)
   - Returns None
8. Result: Since multiple options matched, terminal shows them as options!
```

---

### Case F: Multiple Arguments Completion
**User Types:** `echo foo bar app/u` ➡️ `[TAB]`
**State of terminal:** `readline.get_begidx() == 13` ($> 0$).

```
1. readline calls completer(text="app/u", state=0)
   (Note: Readline correctly identifies "app/u" as the active token!)
2. "/" is present:
   - prefix = "u"
   - dir_prefix = "app/"
   - dir_path = "app/"
3. List files in "app/" starting with "u":
   - Found: "utils.py" (file)
   - Cache matches: ["app/utils.py "]
4. Returns "app/utils.py "
5. readline calls completer(text="app/u", state=1)
6. Returns None
7. Result: Line updates to "$ echo foo bar app/utils.py "
```

---

## 4. Key Python String Operations Used

1. **`os.path.basename(path)`**: Extracts the final name component of a path.
   * `os.path.basename("app/main.py")` ➡️ `"main.py"`
   * `os.path.basename("app/")` ➡️ `""`
2. **`os.path.dirname(path)`**: Extracts the directory prefix of a path.
   * `os.path.dirname("app/main.py")` ➡️ `"app"`
   * `os.path.dirname("app/")` ➡️ `"app"`
3. **Ternary Slice Expression**: `text[:-len(prefix)] if prefix else text`
   * Prevents `TypeError` when `prefix` is empty by bypassing slicing and returning the directory prefix directly.
4. **`os.path.expanduser(path)`**: Expands `~` to the absolute home directory path (e.g. `/Users/username`).
