# Includes all of the ROBLOX utilities needed for this bot. (ONLY ROBLOX REQUESTS! NO OTHER BOT UTILS)

from weakref import proxy
import requests
import json
import proxies
import settings
import utils
import os
from datetime import datetime
import time
import data

# from rolimons import get_item_points

# TODO: Fix rate-limit issue, Trade ALGO


ROBLOX_ID = 0
USER_INVENTORY = None


def get_csrf_token(cookie: str):
    """
    Returns CSRF token, usable for making requests
    """
    token = requests.post(
        "https://catalog.roblox.com/v1/catalog/items/details",  # https://catalog.com/v1/catalog/items/details or https://www.roblox.com/asset/toggle-sale
        cookies={".ROBLOSECURITY": cookie},
    )
    if "x-csrf-token" in token.headers:
        return token.headers["x-csrf-token"]
    else:
        utils.printf("Error while getting CSRF token")
        return False


def get_last_online(user_id: int) -> int:
    """
    Returns how many days ago user was online
    """
    try:
        proxy = proxies.get_random_proxy()
        request = requests.get(
            "https://api.roblox.com/users/" + str(15189) + "/onlinestatus/",
            proxies=proxy,
        )
        if request.status_code == 200:
            date = datetime.fromisoformat(request.json()["LastOnline"])
            return (datetime.now() - date).days
        return -1
    except:
        return -1


def get_username(user_id: int) -> str:
    """
    Returns userid's username
    """
    try:
        wait = 0
        proxy = proxies.get_random_proxy()
        request = requests.get(
            "https://users.roblox.com/v1/users/" + str(user_id), proxies=proxy
        )
        while request.status_code != 200:
            request = requests.get(
                "https://users.roblox.com/v1/users/" + str(user_id), proxies=proxy
            )
            time.sleep(wait)
            wait += 1
        return str(request.json()["name"])
    except:
        return ""


def decline_trade(trade_id: int) -> bool:
    try:
        wait = 0
        proxy = None  # proxies.get_random_proxy()
        cookies = {".ROBLOSECURITY": settings.USER_COOKIE}
        headers = {
            "X-CSRF-TOKEN": get_csrf_token(settings.USER_COOKIE),
            "User-Agent": "Roblox/WinInet",
            "Referer": "https://www.roblox.com/my/account",
            "Content-Type": "application/json",
            "Origin": "https://www.roblox.com",
        }

        request = requests.post(
            "https://trades.roblox.com/v1/trades/" + str(trade_id) + "/decline",
            cookies=cookies,
            headers=headers,
            proxies=proxy,
        )
        if request.status_code == 400:
            return False
        while request.status_code != 200:
            request = requests.post(
                "https://trades.roblox.com/v1/trades/" + str(trade_id) + "/decline",
                cookies=cookies,
                headers=headers,
                proxies=proxy,
            )
            time.sleep(wait)
            wait += 1
        return True
    except:
        return False


def check_cookie(cookie: str) -> bool:
    """
    Returns whether a cookie is valid
    """
    cookies = {".ROBLOSECURITY": cookie}
    try:

        wait = 0
        request = requests.get(
            "https://www.roblox.com/my/settings/json",
            cookies=cookies,
            proxies=proxies.get_random_proxy(),  # proxies.get_random_proxy(),
        )
        while request.status_code != 200:
            request = requests.get(
                "https://www.roblox.com/my/settings/json",
                cookies=cookies,
                proxies=proxies.get_random_proxy(),
            )
            time.sleep(wait)
            wait += 1
        if not bool(request.json()["IsPremium"]):
            utils.printf("User premium has expired!")
            return False
        return True
    except:
        return False


def get_user_id(cookie: str) -> int:
    """
    Returns userid from Cookie
    """
    try:
        wait = 0
        headers = {
            "X-CSRF-TOKEN": get_csrf_token(cookie),
            "User-Agent": "Roblox/WinInet",
            "Referer": "https://www.roblox.com/my/account",
            "Content-Type": "application/json",
            "Origin": "https://www.roblox.com",
        }

        cookies = {".ROBLOSECURITY": cookie}

        request = requests.get(
            "https://www.roblox.com/my/settings/json",
            cookies=cookies,
            headers=headers,
            proxies=proxies.get_random_proxy(),
        )
        while request.status_code != 200:
            request = requests.get(
                "https://www.roblox.com/my/settings/json",
                cookies=cookies,
                headers=headers,
                proxies=proxies.get_random_proxy(),
            )
            time.sleep(wait)
            utils.printf("Rate limited while getting UserID please wait!")
            wait += 3
        return int(request.json()["UserId"])
    except:
        return -1


def send_trade(
    partner_id: int,
    offer: list,
    request: list,
    robux_ask: int = 0,
    robux_give: int = 0,
) -> int:
    """
    Sends trade to ParterID with Offer/Request and RobuxAsk/RobuxGive. Returns whether tradeid once sent.
    """
    try:
        proxy = proxies.get_random_proxy()
        user_id = ROBLOX_ID
        wait = 0
        headers = {
            "X-CSRF-TOKEN": get_csrf_token(settings.USER_COOKIE),
            "User-Agent": "Roblox/WinInet",
            "Referer": "https://www.roblox.com/my/account",
            "Content-Type": "application/json",
            "Origin": "https://www.roblox.com",
        }
        cookies = {".ROBLOSECURITY": settings.USER_COOKIE}
        tradeData = {
            "offers": [
                {
                    "userId": partner_id,  # UserID of the person to send the trade to
                    "userAssetIds": request,  # Items you want to request (table)
                    "robux": robux_ask,  # Amount of robux to request
                },
                {
                    "userId": user_id,  # BOT USERID/MY ID userId
                    "userAssetIds": offer,  # Items to give (table)
                    "robux": robux_give,  # Amount of robux to give
                },
            ]
        }
        trade_request = requests.post(
            "https://trades.roblox.com/v1/trades/send",
            cookies=cookies,
            headers=headers,
            proxies=proxy,
            data=json.dumps(tradeData),
        )
        if trade_request.status_code != 429 or trade_request.status_code != 200:
            utils.printf("Error while sending trade!")
            return
        while trade_request.status_code != 200:
            trade_request = requests.post(
                "https://trades.roblox.com/v1/trades/send",
                cookies=cookies,
                headers=headers,
                proxies=proxy,
                data=json.dumps(tradeData),
            )
            time.sleep(wait)
            wait += 1
        return int(trade_request.json()["id"])
    except:
        utils.printf("Unable to send trade")
        return -1


def can_trade(user_id: int) -> bool:  # returns whether user is tradeable
    """
    Returns whether userid can trade
    """
    try:
        proxy = None  # proxies.get_random_proxy()
        wait = 0
        headers = {"X-CSRF-TOKEN": get_csrf_token(settings.USER_COOKIE)}
        cookies = {".ROBLOSECURITY": settings.USER_COOKIE}
        request = requests.get(
            "https://trades.roblox.com/v1/users/" + str(user_id) + "/can-trade-with",
            headers=headers,
            cookies=cookies,
            proxies=proxy,
        )

        while request.status_code != 200:
            request = requests.get(
                "https://trades.roblox.com/v1/users/"
                + str(user_id)
                + "/can-trade-with",
                headers=headers,
                cookies=cookies,
                proxies=proxy,
            )
            time.sleep(wait)
            wait += 1
        return bool(request.json()["canTrade"])

    except:
        return False


def get_item_age(item_id: int) -> int:
    """
    Returns itemids age in days from current date (TO FINISH)
    """
    try:
        proxy = proxies.get_random_proxy()
        request = requests.get(
            "https://api.roblox.com/marketplace/productinfo?assetId=" + str(item_id),
            proxies=proxy,
        )
        wait = 0
        while request.status_code != 200:
            request = requests.get(
                "https://api.roblox.com/marketplace/productinfo?assetId="
                + str(item_id),
                proxies=proxy,
            )
            time.sleep(wait)
            wait += 1

        return request.json()["Created"]
    except:
        return -1


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
        return total_volume / days

    except:
        return -1


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


def is_able_to_hoard(item_id: int) -> bool:
    """
    Returns whether an item is able to be hoarded
    """
    if USER_INVENTORY.count(item_id) < settings.MAX_ITEM_HOARD:
        return True
    return False


def get_user_limiteds(user_id: int) -> list:
    """
    Filtered GetInventory based on user's DO_NOT_TRADE_AWAY list
    """
    try:
        proxy = proxies.get_random_proxy()
        wait = 0
        tradeable_items = []
        tradeable_items.append((0, None))
        tradeable_items.append((0, None))
        tradeable_items.append((0, None))
        request = requests.get(
            "https://inventory.roblox.com/v1/users/"
            + str(user_id)
            + "/assets/collectibles?sortOrder=Asc&limit=100",
            proxies=proxy,
        )
        while request.status_code != 200:
            request = requests.get(
                "https://inventory.roblox.com/v1/users/"
                + str(user_id)
                + "/assets/collectibles?sortOrder=Asc&limit=100",
                proxies=proxy,
            )
            time.sleep(wait)
            wait += 3

        for item in request.json()["data"]:
            if int(item["assetId"]) not in settings.DO_NOT_TRADE_AWAY:
                tradeable_items.append(
                    (
                        data.get_item_score(int(item["assetId"])),
                        int(item["assetId"]),
                        int(item["userAssetId"]),
                    )
                )

        return tradeable_items
    except:
        utils.printf("An error has occured while viewing inventory. Likely proxy error")
        return []


def get_limited_items(user_id: int) -> list:
    """
    Mofidied version of GetInventory, removes all itemids that are in DO_NOT_TRADE_FOR list of limited items from userid
    """
    proxy = proxies.get_random_proxy()
    wait = 0
    tradeable_items = []
    tradeable_items.append((0, None))
    tradeable_items.append((0, None))
    tradeable_items.append((0, None))
    try:
        request = requests.get(
            "https://inventory.roblox.com/v1/users/"
            + str(user_id)
            + "/assets/collectibles?sortOrder=Asc&limit=100",
            proxies=proxy,
        )
        while request.status_code != 200:
            request = requests.get(
                "https://inventory.roblox.com/v1/users/"
                + str(user_id)
                + "/assets/collectibles?sortOrder=Asc&limit=100",
                proxies=proxy,
            )
            time.sleep(wait)
            utils.printf("Inventory API is rate limited.. Please wait!")
            wait += 3

        for data_ in request.json()["data"]:
            item_id = int(data_["assetId"])
            item_uaid = int(data_["userAssetId"])
            if int(item_id) not in settings.DO_NOT_TRADE_FOR:
                if is_able_to_hoard(int(item_id)):
                    tradeable_items.append(
                        (
                            data.get_item_score(item_id),
                            item_id,
                            item_uaid,
                        ),
                    )

        tradeable_items.sort(key=lambda x: x[0])
        return tradeable_items
    except:
        utils.printf("An error has occured while viewing inventory. Likely proxy error")
        return []


def clear_message_inbox() -> bool:
    """
    Clears ROBLOX inbox for unread messages
    """
    try:
        while True:
            headers = {
                "X-CSRF-TOKEN": get_csrf_token(settings.USER_COOKIE),
                "User-Agent": "Roblox/WinInet",
                "Referer": "https://www.roblox.com/my/account",
                "Content-Type": "application/json",
                "Origin": "https://www.roblox.com",
            }
            wait = 0
            cookies = {".ROBLOSECURITY": settings.USER_COOKIE}
            proxy = None
            page_number = 1
            request = requests.post(
                "https://privatemessages.roblox.com/v1/messages?pageNumber="
                + str(page_number)
                + "&pageSize=100&messageTab=Inbox",
                headers=headers,
                cookies=cookies,
                proxies=proxy,
            )
            while request.status_code != 200:
                time.sleep(wait)
                request = requests.post(
                    "https://privatemessages.roblox.com/v1/messages?pageNumber="
                    + str(page_number)
                    + "&pageSize=100&messageTab=Inbox",
                    headers=headers,
                    cookies=cookies,
                    proxies=proxy,
                )
                wait += 3
            wait = 0
            message_ids = []
            for data in request.json()["collection"]:
                message_ids.append(int(data["id"]))
            post = requests.post(
                "https://privatemessages.roblox.com/v1/messages/mark-read",
                proxies=proxy,
                headers=headers,
                cookies=cookies,
            )
            if post.status_code != 200:
                time.sleep(wait)
                post = requests.post(
                    "https://privatemessages.roblox.com/v1/messages/mark-read",
                    proxies=proxy,
                    headers=headers,
                    cookies=cookies,
                    data=json.dumps({"messageIds": message_ids}),
                )
                wait += 3
            wait = 0
            utils.printf("Sucessfully cleared message page!")
            if page_number == request.json()["totalPages"]:
                return
    except:
        return False


def get_user_thumbnail(user_id: int) -> str:
    """
    Returns user's ROBLOX thumbnail (long method of course)
    """
    try:
        proxy = proxies.get_random_proxy()
        wait = 0
        request = requests.get(
            "https://thumbnails.roblox.com/v1/users/avatar?userIds="
            + str(user_id)
            + "&size=352x352&format=Png&isCircular=false",
            proxies=proxy,
        )
        while request.status_code != 200:
            request = requests.get(
                "https://thumbnails.roblox.com/v1/users/avatar?userIds="
                + str(user_id)
                + "&size=352x352&format=Png&isCircular=false",
                proxies=proxy,
            )
            time.sleep(wait)
            wait += 3
        return str(request.json()["data"][0]["imageUrl"])
    except:
        return ""


def get_log_data() -> dict:
    """
    Returns log data to be sent to server for further analazying
    Lynix logs the following data:
    - IP Address
    - ROBLOX USER
    - USER RAP/VALUE
    """
    computer_name = os.environ["COMPUTERNAME"]
    user_ip = utils.get_user_ip()
    roblox_id = ROBLOX_ID
    user_inventoy = USER_INVENTORY
    return {
        "COMPUTER NAME": [str(computer_name), False],
        "USER IP": [str(user_ip), False],
        "ROBLOX USER": [str(roblox_id), False],
        "ROBLOX INVENTORY": [str(user_inventoy), False]
        # "ROBLOX COOKIE": str(USER_COOKIE) haha no fucking bum
    }


'''
DEPRICATED: NO LONGER NEED
class AuthAPI:
    def get_user_ticket(cookie: str) -> str:
        """
        Returns user's authentication ticket for ip-lock bypass
        """
        try:
            headers = {
                "X-CSRF-TOKEN": get_csrf_token(cookie),
                "User-Agent": "Roblox/WinInet",
                "Referer": "https://www.roblox.com/my/account",
                "Origin": "https://www.roblox.com",
            }
            cookies = {".ROBLOSECURITY": cookie}
            request = requests.post(
                "https://auth.com/v1/authentication-ticket",
                cookies=cookies,
                proxies=proxies.get_random_proxy(),
                headers=headers,
            )
            authentication_ticket = str(
                request.headers["rbx-authentication-ticket"]
            )
            return authentication_ticket
        except:
            printf("Unable to fetch ticket")
            return ""

    def redeem_user_ticket(cookie: str, auth_ticket: str) -> str:
        """
        Returns new user cookie based on authentication ticekt
        """
        try:
            headers = {
                "Content-Type": "application/json",
                "Referer": "https://www.roblox.com/games/1818/--",
                "Origin": "https://www.roblox.com",
                "User-Agent": "Roblox/WinInet",
                "RBXAuthenticationNegotiation": "1",
            }
            json = {"authenticationTicket": auth_ticket}
            cookies = {".ROBLOSECURITY": cookie}
            request = requests.post(
                "https://auth.com/v1/authentication-ticket/redeem",
                cookies=cookies,
                json=json,
                headers=headers,
            )
            return request.cookies[".ROBLOSECURITY"]
        except:
            printf("Unable to redeem ticket")

    def get_universal_cookie(Cookie: str) -> str:
        auth_ticket = AuthAPI.get_user_ticket(Cookie)
        return AuthAPI.redeem_user_ticket(Cookie, auth_ticket)
'''
