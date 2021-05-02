DEBUG = False


def toggle_debug(enabled):
    global DEBUG
    DEBUG = enabled


def error(text):
    print(f"\u001b[31merror: {text}\u001b[0m")


def warn(text):
    print(f"\u001b[33mwarning: {text}\u001b[0m")


def debug(text):
    if DEBUG:
        print(f"\u001b[32m{text}\u001b[0m")