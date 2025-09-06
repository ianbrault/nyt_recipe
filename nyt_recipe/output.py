# (c) 2021 Ian Brault
# This code is licensed under the MIT License (see LICENSE.txt for details)

import sys

DEBUG = False


def toggle_debug(enabled: bool):
    global DEBUG
    DEBUG = enabled


def error(text: str):
    sys.stderr.write(f"\u001b[31merror: {text}\u001b[0m\n")


def warn(text: str):
    sys.stderr.write(f"\u001b[33mwarning: {text}\u001b[0m\n")


def debug(text: str):
    if DEBUG:
        sys.stderr.write(f"\u001b[32m{text}\u001b[0m\n")
