"""For loading and validating configs"""
import os
from dotenv import load_dotenv


def load_configs():
    env_mode = os.getenv("ENVIRONMENT")
    base_dir = os.path.abspath(os.path.dirname(__file__))
    files = [".env"]

    if env_mode == "development":
        files = [".env.dev.local", ".env.local", ".env.dev"] + files
    elif env_mode == "production":
        files = [".env.prod.local", ".env.local", ".env.prod"] + files
    else:
        print("Could not identify environment ($ENVIRONMENT), assuming development")
        files = [".env.dev.local", ".env.local", ".env.dev"] + files

    for file in files:
        if not load_dotenv(os.path.join(base_dir, f"../{file}"), verbose=True):
            print(f"{file} not found")  # TODO: Log this with INFO level

    print("Priority environment:", os.getenv("PRIORITY_FLAG"))
