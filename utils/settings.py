import pathlib
from typing import Final
import os
from dotenv import load_dotenv
#Load token
load_dotenv()
def get_bool(name: str) -> bool:
    true_ = ('true', '1', 't')  # Add more entries if you want, like: `y`, `yes`, `on`, ...
    false_ = ('false', '0', 'f')  # Add more entries if you want, like: `n`, `no`, `off`, ...
    value: str | None = os.getenv(name)
    if value in true_:
        return True
    elif value in false_:
        return False

TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
DEFAULT_PREFIX: str = os.getenv('DEFAULT_PREFIX')
BASE_DIR = pathlib.Path(__file__).parent
USER: str = os.getenv('DB_USER')
PASSWORD: str = os.getenv('DB_PASSWORD')
LOCAL_PASSWORD: str = os.getenv('DB_LOCAL_PASSWORD')
DATABASE: str = os.getenv('DB_NAME')
HOST: str = os.getenv('DB_HOST')
TEST_GUILD: int = os.getenv('TEST_GUILD_ID')
GAH_SERVER: int = os.getenv('GAH_SERVER_ID')
MAIN_GUILD: int = os.getenv('MAIN_GUILD_ID')
DEBUG:bool = get_bool('DEBUG')


