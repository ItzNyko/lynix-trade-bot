import requests
import proxies
import time
from datetime import datetime


def get_item_data(item_id: int) -> list:
    """
    Returns sales data for itemid using economy api
    [[sales], RAP]
    """
    # TODO: add 2*append(blah) bc there is also volumeDataPoints
    try:
        proxy = proxies.get_random_proxy()

        wait = 0
        sales = []

        data = requests.get(
            "https://economy.roblox.com/v1/assets/" + str(item_id) + "/resale-data",
            proxies=proxy,
        )

        while data.status_code != 200:
            data = requests.get(
                "https://economy.roblox.com/v1/assets/" + str(item_id) + "/resale-data",
                proxies=proxy,
            )
            time.sleep(wait)
            wait += 1

        current_rap = int(data.json()["recentAveragePrice"])

        for sale in data.json()["priceDataPoints"]:
            sales.append(int(sale["value"]))

        return (sales, current_rap)

    except:
        return ()


def get_item_volume(item_id: int, days: int = 30) -> float:
    """
    Returns item volume within the last X days
    """
    try:
        proxy = proxies.get_random_proxy()
        total_volume = 0
        current_date = datetime.now()
        wait = 0
        data = requests.get(
            "https://economy.roblox.com/v1/assets/" + str(item_id) + "/resale-data",
            proxies=proxy,
        )
        while data.status_code != 200:
            data = requests.get(
                "https://economy.roblox.com/v1/assets/" + str(item_id) + "/resale-data",
                proxies=proxy,
            )
            time.sleep(wait)
            wait += 1

        for sale in data.json()["volumeDataPoints"]:
            date = datetime.strptime(sale["date"], "%Y-%m-%dT%H:%M:%SZ")
            if (current_date - date).days <= days:
                total_volume += int(sale["value"])
        return round(total_volume / days, 2)

    except:
        return -1
