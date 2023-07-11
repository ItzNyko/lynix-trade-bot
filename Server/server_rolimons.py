import requests


class roli_data:
    ROLIMON_CACHED_DATA = requests.get(
        "https://www.rolimons.com/itemapi/itemdetails"
    ).json()


all_item_ids = [int(id) for id in roli_data.ROLIMON_CACHED_DATA["items"]]


def refresh_data() -> bool:
    """
    Refreshes saved ROLIMON_CACHED_DATA in Rolimon's class for bot functions
    """
    try:
        roli_data.ROLIMON_CACHED_DATA = requests.get(
            "https://www.com/itemapi/itemdetails"
        ).json()
        return True
    except:
        return False


def has_value(item_id: int) -> bool:
    """
    Returns whether an item has a value according to Rolimons
    """
    if item_id in all_item_ids:
        if int(roli_data.ROLIMON_CACHED_DATA["items"][str(item_id)][3]) != -1:
            return True
        return False


def is_rare(item_id: int) -> bool:
    """
    Returns Item's is rare by using ROLIMON_CACHED_DATA
    """
    if item_id in all_item_ids:
        if roli_data.ROLIMON_CACHED_DATA["items"][str(item_id)][9] == -1:
            return False
        return True
    return False


def is_projected(item_id: int) -> bool:
    """
    Returns whether an item is projected acording to rolimons
    """
    data = roli_data.ROLIMON_CACHED_DATA["items"][str(item_id)][7]
    if data != -1:
        return True
    return False


def get_item_rap(item_id: int) -> int:
    """
    Returns Item's RAP through ROLIMON_CACHED_DATA or ROBLOX CONCURRENT RAP!
    """
    if item_id in all_item_ids:
        return int(roli_data.ROLIMON_CACHED_DATA["items"][str(item_id)][2])
    return 0


def get_item_value(item_id: int) -> int:
    """
    Returns Item's value through ROLIMON_CACHED_DATA
    """
    if item_id in all_item_ids:
        return int(roli_data.ROLIMON_CACHED_DATA["items"][str(item_id)][4])
    return 0


def get_item_score(item_id: int) -> int:
    """
    Returns items point value
    """
    return get_item_rap(item_id) + get_item_value(item_id)
