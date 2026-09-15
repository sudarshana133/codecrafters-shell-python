#!/usr/bin/env python3
import sys

# argv[1] = command (e.g., git)
# argv[2] = word being completed (e.g., set)
# argv[3] = preceding word (e.g., remote)

cmd = sys.argv[1] if len(sys.argv) > 1 else ""
cur = sys.argv[2] if len(sys.argv) > 2 else ""
prev = sys.argv[3] if len(sys.argv) > 3 else ""

if prev == "remote":
    candidates = ["set-head", "set-branches", "set-url", "show", "add"]
else:
    candidates = ["status", "clone", "remote", "commit", "push", "pull"]

for candidate in candidates:
    if candidate.startswith(cur):
        print(candidate)
