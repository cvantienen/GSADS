"""
Base settings to build other settings files upon.
Example Usage:
    # getting base dir
    from settings import BASE_DIR
    print(BASE_DIR)
    # getting excel configs
    from settings import EXCEL_CONFIGS
"""
from pathlib import Path
import environ
import json


BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
print(BASE_DIR)
env = environ.Env()

READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=False)
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .envs
    env.read_env(str(BASE_DIR / ".envs"))

    # Path to the JSON file
    EXCEL_CONFIG_PATH = BASE_DIR / "settings" / "excel.json"

    # Read and parse the JSON file
    with open(EXCEL_CONFIG_PATH, 'r', encoding='utf-8') as file:
        EXCEL_CONFIGS = json.load(file)
