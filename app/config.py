"""For loading and validating configs"""
import os
from dotenv import load_dotenv


def load_configs():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(os.path.join(base_dir, "../.env.dev"), verbose=True)
    if not load_dotenv(os.path.join(base_dir, "../.env.local"), verbose=True):
        print(".env.local not found")  # TODO: Log this with INFO level
    print("Priority environment:", os.getenv("PRIORITY_FLAG"))
