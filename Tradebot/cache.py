# Controls caches for outbound trades and value lists
from utils import *
from time import sleep


def update_item_data(item_id: int, item_rap: int, item_value: int) -> bool:
    """
    Updates/adds item data from values.txt
    [item_id, item_rap, item_value]
    """
    try:
        new_data = []
        with open("library/values.txt", "r") as values_file:
            contains_id = values_file.read().find(str(item_id))

        if contains_id != -1:
            with open("library/values.txt", "r") as values_file:
                for line in values_file:
                    if line.find(str(item_id)) != -1:
                        new_data.append([item_id, item_rap, item_value])
                    else:
                        new_data.append(eval(line))

            with open("library/values.txt", "w") as values_file:
                for line in new_data:
                    values_file.write(str(line) + "\n")
        else:
            with open("library/values.txt", "r") as values_file:
                for line in values_file:
                    new_data.append(eval(line))
            new_data.append([item_id, item_rap, item_value])
            with open("library/values.txt", "w") as values_file:
                for data in new_data:
                    values_file.write(str(data) + "\n")
        return True
    except:
        return False


def get_trades_from_cache() -> list:
    """
    Returns list with all cached trades
    [trade_id, [user_combo], [partner_combo]]
    """
    data = []
    try:
        with open("library/outbound_cache.txt", "r") as cache_file:
            for line in cache_file:
                data.append(eval(line))
        return data
    except:
        return data


def add_trade_to_cache(trade_id: int, user_combo: list, partner_combo: list) -> bool:
    """
    Appends trade to outbound cache (cache.txt)
    [trade_id, [user_combo], [partner_combo]]
    """
    try:
        with open("library/outbound_cache.txt", "a") as cache_file:
            cache_file.write(str([trade_id, user_combo, partner_combo]) + "\n")
            return True
    except:
        return False


def remove_trade_from_cache(trade_id: int) -> bool:
    """
    Removes trade from cache (outbound_cache.txt)
    [trade_id, [user_combo], [partner_combo]]
    """

    new_data = []
    try:
        with open("library/outbound_cache.txt", "r") as cache_file:
            for line in cache_file:
                if int(eval(line)[0]) != int(trade_id):
                    new_data.append(line)

        with open("library/outbound_cache.txt", "w") as cache_file:
            for data in new_data:
                cache_file.write(str(data) + "\n")
        return True
    except:
        return False
