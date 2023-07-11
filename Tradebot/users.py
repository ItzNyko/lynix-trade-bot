# This file includes all of the scraping methods in which Lynix fetches its users.
# Currently it is basic and includes users from limited sources, but it gets the job done!

# from roblox import ROBLOX
import requests
import settings


def rolimons_user_scrape() -> list:
    """
    Returns a list of users scraped from Rolimons
    """
    users = []
    try:
        request = requests.get(
            "https://www.rolimons.com/tradeadsapi/getrecentads"
        ).json()["trade_ads"]
        for trade_ad in request:
            users.append(int(trade_ad[2]))
        return users
    except:
        return users


def get_users_from_resellers(itemid: int) -> list:
    """
    Returns top 100 resellers based on itemid
    """
    users = []
    proxy = None
    try:
        cookies = {".ROBLOSECURITY": settings.USER_COOKIE}
        request = requests.get(
            "https://economy.roblox.com/v1/assets/"
            + str(itemid)
            + "/resellers?limit=100",
            cookies=cookies,
            proxies=proxy,
        )
        for data in request.json()["data"]:
            user = data["seller"]["id"]  # int(data[0])  # ["id"])
            users.append(user)
        return users
    except:
        return users


def group_scrape(groupid: int) -> list:
    """
    Returns all premium
    """
