#!/usr/bin/env python3
import sys

# Dynamic completion options for testing
CANDIDATES = [
    "build",
    "branch",
    "run",
    "restart",
    "remove",
    "start",
    "stop",
    "status",
]

# If an argument was passed to the script, filter candidates by that argument prefix
prefix = sys.argv[1] if len(sys.argv) > 1 else ""

for candidate in CANDIDATES:
    if candidate.startswith(prefix):
        print(candidate)

