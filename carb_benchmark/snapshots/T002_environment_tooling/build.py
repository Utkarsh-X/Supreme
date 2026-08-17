import sys
import os
from cli_runner.helpers import build_target

if __name__ == '__main__':
    print("Starting build process...")
    result = build_target("main")
    print(f"Build result: {result}")
