import utils
import cache
import requests
import json
import roblox
import data

trade_queue = []  # (partner_id, user_combination, partner_combination)
user_queue = []
user_threads = 0


def format_trade_data(user_combo: list, partner_combo: list) -> dict:
    """
    Formats trade data to be able to be sent to user's desired webhook
    """
    ROLIMON_VALUE_ICON = "<:rollahmons:973409500499431424> "
    ROBUX_ICON = "<:wrapping:973409500507811840> "

    rap_profit = data.get_combo_rap(partner_combo) - data.get_combo_rap(user_combo)
    value_profit = data.get_combo_value(partner_combo) - data.get_combo_value(
        user_combo
    )
    return {
        "Items you gave: ": [user_combo, False],
        "Items you received: ": [
            partner_combo,
            False,
        ],
        ROLIMON_VALUE_ICON + "Value Win: ": [str(rap_profit) + " R$", True],
        ROBUX_ICON + "RAP Win: ": [str(value_profit) + " R$", True],
    }


def has_all_items(items: list) -> bool:
    """
    Returns whether items are found in user_inventory
    USED FOR POSSIBLE TRADE SNIPES
    """
    for item in items:
        if item not in roblox.USER_INVENTORY:
            return False
    return True


def possible_trade_snipes() -> list:
    """
    Returns a list of trade ads from Rolimons in [partner_id, [user_combo], [partner_combo]] which fit the user's settings
    """
    try:
        possible_snipes = []
        request = requests.get(
            "https://www.rolimons.com/tradeadsapi/getrecentads"
        ).json()["trade_ads"]
    except:
        return []

    for trade in request:
        parnter_data = json.dumps(trade[4])
        user_data = json.dumps(trade[5])
        if "items" not in user_data or "items" not in parnter_data:
            continue

        possible_user_combo = eval(user_data)["items"]
        partner_combo = eval(parnter_data)["items"]

        if has_all_items(possible_user_combo):
            possible_snipes.append([int(trade[2]), possible_user_combo, partner_combo])
    return possible_snipes


def get_uaids(list: list) -> list:
    """
    Returns uaids within a trade
    """
    uaids = []
    for item in list:
        if item[1] != None:
            uaids.append(item[2])
    return uaids


def get_ids(list: list) -> list:
    """
    Returns IDs within a trade
    """
    ids = []
    for item in list:
        if item[1] != None:
            ids.append(item[1])
    return ids


def send_thread():
    while True:
        copy_queue = trade_queue
        if copy_queue:
            for trade in copy_queue:
                user_uaids = get_uaids(trade[1])
                partner_uaids = get_uaids(trade[2])
                partner_id = int(trade[0])
                trade_id = roblox.send_trade(partner_id, user_uaids, partner_uaids)

                if trade_id != -1:
                    utils.printf(
                        "Sucessfully sent trade to "
                        + str(partner_id)
                        + " ("
                        + str(trade_id)
                        + ")"
                    )
                    cache.add_trade_to_cache(
                        trade_id,
                        trade[1],
                        trade[2],
                    )
                    utils.printf(
                        "There are currently "
                        + str(len(trade_queue))
                        + " trades in queue!"
                    )
                    trade_queue.remove(trade)
