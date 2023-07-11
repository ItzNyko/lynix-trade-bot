"""
Includes base_utility functions. Logging and such. Based on Jartan's logging used in MM BOT commission (me and him)
"""


import logging
import os
import time
import requests
import random
import string

REQUIRED_DIRECTORIES = ("library",)

REQUIRED_FILES = (
    "library/config.ini",
    "library/custom_values.txt",
    "library/outbound_cache.txt",
    "library/proxies.txt",
    "library/config.ini",
)


log = logging.getLogger(__name__)


def setup_logging(path: str, level: int = 1) -> None:
    logs_folder_path = os.path.join(path)
    if not os.path.exists(logs_folder_path):
        os.makedirs(logs_folder_path)
        printf("Successfully created log system")
    log_path = os.path.join(
        logs_folder_path, time.strftime("%Y-%m-%d", time.localtime())
    )
    logging.basicConfig(
        filename=f"{log_path}.log",
        level=level,
        format="%(asctime)s:%(levelname)s:%(message)s",
    )


def printf(text: str, log_level: int = None) -> None:
    formatted_text = time.strftime("%H:%M:%S | ", time.localtime()) + str(text)
    print(str(formatted_text))
    if isinstance(log_level, int):
        log.log(log_level, text)


def get_user_ip() -> str:
    """
    Returns user's IP address
    """
    try:
        return requests.get("https://api.ipify.org/").text
    except:
        return ""


DEFAULT_CONFIG_DATA = """
[Authentication]
ROBLOX_COOKIE = 

[Trade Settings]

# Items on this list will not be traded away nor traded for
# seperated by commas
DO_NOT_TRADE_FOR = 

# Items on this list will not be traded away
# seperated by commas
DO_NOT_TRADE_AWAY = 

# Ratio determining how attractive trade is for user
# Equation: (total_partner_offer - total_user_offer) / (total_partner_offer + total_user_offer)
MIN_TRADE_ATTRACTIVENESS = -0.05
MAX_TRADE_ATTRACTIVENESS = 0.1

# Maximum amount of time that can be spent searching for trades with a single partner (in seconds)
MAX_TIME_FOR_TRADES = 7

# Currently only supports constants

MIN_RAP_WIN = -3000
MAX_RAP_WIN = 9000

MIN_VALUE_WIN = 1
MAX_VALUE_WIN = 5000

[Item Settings]

# Minimum item rap required for requesting items
MIN_ITEM_RAP = 0
MAX_ITEM_RAP = 9999999

# Minimum item value required for requesting items
MIN_ITEM_VALUE = 0
MAX_ITEM_VALUE = 99999999

# Maximum allowed items of one id allowed in your inventory
MAX_ITEM_HOARD = 2

"""


def check_file_requirements():
    """
    Checks Lynix file requirments and created any files missing
    """
    setup_logging("logs")
    needs_restart = False
    for directory in REQUIRED_DIRECTORIES:
        if not os.path.exists(directory):
            os.makedirs(directory)
            needs_restart = True

    for file in REQUIRED_FILES:
        if not os.path.exists(file):
            with open(file, "x"):
                needs_restart = True
                pass
            if file == "library/config.ini":
                with open(file, "w") as config_file:
                    config_file.write(DEFAULT_CONFIG_DATA)
    if needs_restart:
        printf("Created dependency files.. Please restart!")
        time.sleep(3)
        os._exit(-1)


def set_window_name() -> None:
    """
    Sets window name to random string. This is to prevent types of hooking and such and prevent it as much as possible.
    """
    res = "".join(random.choices(string.ascii_uppercase + string.digits, k=12))
    os.system("title " + res)
