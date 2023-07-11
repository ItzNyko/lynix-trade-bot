# Configuration Parser
import configparser as config_
import settings
import utils
import time
import os


class config:
    CUSTOM_VALUE_LIST = ()


try:
    _config_ = config_.ConfigParser()
    _config_.read("library/config.ini")
except:
    utils.printf("Error while attempting to parse settings!")
    time.sleep(3)
    os._exit(-1)


def get_user_trade_list() -> list:
    """
    Returns user trade list from library/config.ini and DO_NOT_TRADE_FOR
    """
    return list(_config_["Trade Settings"]["DO_NOT_TRADE_FOR"])


def get_custom_values() -> tuple:
    """
    Returns tuple of custom values from library/custom_values.txt
    """
    custom_values = []
    with open("library/custom_values.txt") as value_file:
        for line in value_file:
            data = line.split(":")
            custom_values.append([int(data[0]), int(data[1])])
    return tuple(map(tuple, custom_values))


def load_config():
    """
    Loads user config from library/config.ini
    """

    # [Authentication]
    settings.USER_COOKIE = str(_config_["Authentication"]["ROBLOX_COOKIE"])
    # [Trade Settings]
    # DO_NOT_TRADE_FOR = _config_["Trade Settings"]["DO_NOT_TRADE_FOR"].split(",")
    # for i in range(0, len(DO_NOT_TRADE_FOR)):
    settings.DO_NOT_TRADE_FOR = []
    # settings.DO_NOT_TRADE_FOR = int(_config_["Trade Settings"]["DO_NOT_TRADE_FOR"].split(","))

    # settings.DO_NOT_TRADE_AWAY = tuple(
    # _config_["Trade Settings"]["DO_NOT_TRADE_AWAY"].split(',')
    # )
    # DO_NOT_TRADE_AWAY = _config_["Trade Settings"]["DO_NOT_TRADE_AWAY"].split(",")
    # for i in range(0, len(DO_NOT_TRADE_AWAY)):
    settings.DO_NOT_TRADE_AWAY = [
        1365767,
        439946101,
        4255053867,
        6550129,
        182509980,
        53039427,
        2409285794,
        292969932,
        440738448,
        2225761296,
        292969139,
        1609401184,
        583722710,
    ]
    settings.DO_NOT_TRADE_AWAY = []  # .append(int(DO_NOT_TRADE_FOR[i]))

    settings.MIN_TRADE_ATTRACTIVENESS = float(
        _config_["Trade Settings"]["MIN_TRADE_ATTRACTIVENESS"]
    )
    settings.MAX_TRADE_ATTRACTIVENESS = float(
        _config_["Trade Settings"]["MAX_TRADE_ATTRACTIVENESS"]
    )
    settings.MAX_TIME_FOR_TRADES = float(
        _config_["Trade Settings"]["MAX_TIME_FOR_TRADES"]
    )
    settings.MIN_RAP_WIN = float(_config_["Trade Settings"]["MIN_RAP_WIN"])
    settings.MAX_RAP_WIN = float(_config_["Trade Settings"]["MAX_RAP_WIN"])
    settings.MIN_VALUE_WIN = float(_config_["Trade Settings"]["MIN_VALUE_WIN"])
    settings.MAX_VALUE_WIN = float(_config_["Trade Settings"]["MAX_VALUE_WIN"])
    """
    settings.CHECK_INBOUND_TRADES = bool(
        config["Trade Settings"]["CHECK_INBOUND_TRADES"]
    )
    """
    # [Item Settings]
    settings.MIN_ITEM_RAP = float(_config_["Item Settings"]["MIN_ITEM_RAP"])
    settings.MAX_ITEM_RAP = float(_config_["Item Settings"]["MAX_ITEM_RAP"])
    settings.MIN_ITEM_VALUE = float(_config_["Item Settings"]["MIN_ITEM_VALUE"])
    settings.MAX_ITEM_VALUE = float(_config_["Item Settings"]["MAX_ITEM_VALUE"])
    # settings.MIN_ITEM_VOLUME = float(config["Item Settings"]["MIN_ITEM_VOLUME"])
    # settings.MIN_ITEM_AGE = int(config["Item Settings"]["MIN_ITEM_AGE"])
    settings.MAX_ITEM_HOARD = int(_config_["Item Settings"]["MAX_ITEM_HOARD"])
    config.CUSTOM_VALUE_LIST = get_custom_values()
    utils.printf("Sucessfully loaded custom values!")
    # [Advanced Settings]
    """
    settings.CUSTOM_VALUE_RATIOS = eval(
        config["Advanced Settings"]["CUSTOM_VALUE_RATIOS"]
    )

    settings.IP_LOCK_BYPASS = bool(config["Advanced Settings"]["IP_BYPASS"])
    settings.ROLIMON_AD_SNIPE = bool(config["Advanced Settings"]["ROLIMON_AD_SNIPE"])
    settings.CUSTOM_TRADE_RATIOS = list(
        eval(config["Advanced Settings"]["CUSTOM_TRADE_RATIOS"])
    )
    settings.ADJUST_TRADE_COOLDOWN = bool(
        config["Advanced Settings"]["ADJUST_TRADE_COOLDOWN"]
    )
    settings.DELETE_TRADE_MESSAGES = bool(
        config["Advanced Settings"]["DELETE_TRADE_MESSAGES"]
    )
    settings.USER_WEBHOOK = str(config["Advanced Settings"]["USER_WEBHOOK"])
    """
