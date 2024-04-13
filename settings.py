import pathlib
from typing import Final
import os
from dotenv import load_dotenv

#Load token
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
PREFIX: str = os.getenv('DEFAULT_PREFIX')
BASE_DIR = pathlib.Path(__file__).parent
