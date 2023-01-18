import re
import pathlib
import argparse

COMMIT_SYNTAX = re.compile(r"^(update\:)|^(create\:)|^(delete\:)|^(hotfix\:)")
FAIL = 1
SUCCESS = 0


def main() -> int:
    parser = argparse.ArgumentParser()
    print(parser)
    return FAIL
