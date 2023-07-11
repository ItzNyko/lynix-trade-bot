# Combination between sever and Rolimons

import settings
import requests
import config
import time
import utils


SERVER_DATA_LINK = "https://nykolynix.herokuapp.com/itemdata"
ROLIMONS_DATA_LINK = "https://www.rolimons.com/itemapi/itemdetails"


class data:
    ROLIMON_CACHED_DATA = requests.get(ROLIMONS_DATA_LINK).json()
    SERVER_DATA = requests.get(SERVER_DATA_LINK).json()


all_item_ids = [int(id) for id in data.ROLIMON_CACHED_DATA["items"]]


def has_value(item_id: int) -> bool:
    """
    Returns whether an item has value based from Rolimon
    """
    if int(data.ROLIMON_CACHED_DATA["items"][str(item_id)][3]) != -1:
        return True
    return False


def get_item_rap(item_id: int) -> int:
    """
    Returns Item's RAP through ROLIMON_CACHED_DATA or ROBLOX CONCURRENT RAP!
    """
    try:
        if has_value(item_id):
            return int(data.ROLIMON_CACHED_DATA["items"][str(item_id)][2])
        return int(data.SERVER_DATA["data"][str(item_id)][2])
    except:
        return 0


def get_item_value(item_id: int) -> int:
    """
    Returns Item's value through ROLIMON_CACHED_DATA
    """
    if not item_id in config.config.CUSTOM_VALUE_LIST:
        return int(data.ROLIMON_CACHED_DATA["items"][str(item_id)][4])
    for item in config.config.CUSTOM_VALUE_LIST:
        if item[0] == item_id:
            return item[1]


def get_combo_rap(combo: list) -> int:
    """
    Returns combination RAP
    """
    total = 0
    for item in combo:
        if item[1] != None:
            total += get_item_rap(item[1])
    return total


def get_combo_value(combo: list):
    """
    Returns combination value
    """
    total = 0
    for item in combo:
        if item[1] != None:
            total += get_item_value(item[1])
    return total


def get_item_score(item_id: int) -> int:
    """
    Returns items score (Value + RAP)
    """
    return get_item_rap(item_id) + get_item_value(item_id)


def get_name_by_id(item_id: int) -> str:
    """
    Returns Item's name by the itemid through ROLIMON_CACHED_DATA
    """
    return str(data.ROLIMON_CACHED_DATA["items"][str(item_id)][0])


def is_rare(item_id: int) -> bool:
    """
    Returns Item's is rare by using ROLIMON_CACHED_DATA
    """

    if data.ROLIMON_CACHED_DATA["items"][str(item_id)][9] == -1:
        return False
    return True


def get_trade_score(list: list) -> int:
    """
    Returns total trade score
    """
    total = 0
    for item in list:
        if item[1] != None:
            total += get_item_score(item[1])
    return total


def is_roli_projected(item_id: int) -> bool:
    """
    Returns whether item is projected based on rolimons
    """
    try:
        if int(data.ROLIMON_CACHED_DATA["items"][str(item_id)][7]) == -1:
            return False
        return True
    except:
        return True


def is_projected(item_id: int) -> bool:
    """
    Returns whether an item is projected from lynix server
    """
    try:
        if not has_value(item_id):
            if is_roli_projected(item_id):
                return True
            for item in data.SERVER_DATA["data"]:
                if int(item) == item_id:
                    return bool(data.SERVER_DATA["data"][str(item)][0])
            return False
        return False
    except:
        return False


def get_item_volume(item_id: int) -> float:
    """
    Returns items volume from lynix server
    """

    return data.SERVER_DATA["data"][str(item_id)][1]


def contains_projected(combo: list) -> bool:
    """
    Returns whether combination contains projected
    """
    for item in combo:
        if is_projected(item):
            return True
    return False


def check_item_volumes(combination: list) -> bool:
    """
    Returns whether all items in the combination fit in the users min_volume setting
    """
    for item in combination:
        if get_item_volume(item) < settings.MIN_ITEM_VOLUME:
            return False
    return True


def update_trade_list() -> None:
    """
    Updates users DO_NOT_TRADE_FOR list with items
    """
    utils.printf("Total Rolimon items: " + str(len(all_item_ids)))
    trade_list = []
    for item in all_item_ids:
        if is_projected(item):
            trade_list.append(item)
            continue
        if (
            get_item_rap(item) < settings.MIN_ITEM_RAP
            or get_item_rap(item) > settings.MAX_ITEM_RAP
        ):
            trade_list.append(item)
            continue
        if (
            get_item_value(item) < settings.MIN_ITEM_RAP
            or get_item_value(item) > settings.MAX_ITEM_RAP
        ):
            trade_list.append(item)
            continue

    for item in config.get_user_trade_list():
        trade_list.append(item)

    settings.DO_NOT_TRADE_FOR = trade_list
    utils.printf(
        "Sucessfully updated DO_NOT_TRADE with: "
        + str(len(settings.DO_NOT_TRADE_FOR))
        + " items!"
    )


def update_data_thread() -> None:
    """
    Thread that updates data save
    """
    while True:
        data.ROLIMON_CACHED_DATA = requests.get(ROLIMONS_DATA_LINK).json()
        data.SERVER_DATA = requests.get(SERVER_DATA_LINK).json()
        update_trade_list()
        utils.printf("Sucessfully updated saved data!")
        # print(settings.DO_NOT_TRADE_FOR)
        time.sleep(5000)
