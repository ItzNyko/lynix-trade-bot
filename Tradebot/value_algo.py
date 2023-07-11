# Valuation algorthym for items. Uses Rolimon's discord valuation
from settings import *
import re
from proxies import *
import requests
from datetime import datetime
from datetime import date
from math import floor
from proj import Data
import rolimons

MAXIMUM_DAY_DIFFERENCE = 45  # Maximum day difference for proofs
MIN_RANGE = 200000  # Item range low
MAX_RANGE = 700000  # Item range high
DEFAULT_WAIT_TIME = 5  # Default wait between rate limit, this is incremented and reset after (For discord)
PROOF_DIFFERENCE_MULTIPLIER = 0.188  # 18.8% is default

# Most messy code ive seen or made, but too annoying to remake


class saved_data:
    inaccurate_values = []


def avg(list: list) -> float:
    """
    Simply returns average of list
    """
    total = 0
    for value in list:
        total += value
    return total / len(list)


def days_between(d1, d2):
    return abs(
        (datetime.strptime(d2, "%Y-%m-%d") - datetime.strptime(d1, "%Y-%m-%d")).days
    )


def has_valid_timestamp(
    message: str,
) -> bool:  # Returns whether value is within a timestamp
    todays_time_stamp = str(date.today())
    discordDate = str(message[0]["timestamp"])  # Get the timestamp
    msg_yr = discordDate.split("-")[0]
    msg_month = discordDate.split("-")[1]
    msg_day = str(discordDate.split("-")[2][0]) + str(discordDate.split("-")[2][1])
    msg_time_stamp = msg_yr + "-" + msg_month + "-" + msg_day
    if int(days_between(todays_time_stamp, msg_time_stamp) <= MAXIMUM_DAY_DIFFERENCE):
        return True
    return False


def remove_punctuation(text: str):
    """
    Returns new text without grammer
    """
    return re.sub(r"[^\w\s]", "", text)


def find_numbers(text: str) -> list:
    """
    Returns all numbers found within a set of text into a list
    """
    return re.findall("\d*\.?\d+", text)


def contains_kop(text) -> bool:
    """
    Returns whether a string contains "k op" within it or not (since re does return '' at times)
    """
    if text.find("k op") != -1:
        return True
    return False


def check_saved_values(mean: float = 0.0) -> list:
    accurate_saved_values = []
    for value in saved_data.inaccurate_values:
        if abs(mean - value[0]) < abs(
            mean - value[1]
        ):  # If K_VALUE is closer to mean than add that
            accurate_saved_values.append(value[0])
        else:  # Else, add the 2_index method
            accurate_saved_values.append(value[1])
    saved_data.inaccurate_values = []
    return accurate_saved_values


def is_item_from_proof(text: str, item: str):
    if text.split("\n")[0].find(str(item).lower()) != -1:
        return True
    return False


def find_value(text: str) -> float:
    """
    Returns most OP values from within text
    """

    # Check if item is in exceptions
    list = find_numbers(text)  # Returns all numbers in text
    if len(list) > 0:  # If any type of numbers are found
        if (
            len(list) == 1
        ):  # If the length of the numbers is less than 2, than the only number in the array is the value
            return float(list[0])

        k_ops = re.findall("....kop|...kop|..kop|....k op|...k op|..k op|", text)
        for word in k_ops:
            if contains_kop(word) and word[0] != str(0):
                if len(find_numbers(word)) > 0:
                    return float(find_numbers(word)[0])

        # VS method -> 300 vs 300

        vs = re.findall(
            "...k vs ...k|.... vs ....|.... v ....|...v...|..v..|... v ...|.. v ..|... vs ...|.. vs ..|. v .|.v.|........ v ........|....... v .......|........ vs ........|....... vs .......|",
            text,
        )  # Find all occurances of __ vs __ EX> 200k vs 300k
        for value in vs:  # For all the occurances of "vs"
            if contains_kop(value):
                return float(re.sub("[^0-9.]", "", value))  # Return all numbers

        # If neither of the 3 methods work, we go on to the last 2:
        # These two methods are used but are used in a later time.
        # These are 2 methods which sometimes work

        # Using _k value
        # K method, returns the first instance of __k
        two_index_value = float(
            abs(float(find_numbers(text)[0]) - float(find_numbers(text)[1]))
        )
        __k = re.findall("..k|.k|...k|....k|..k with|...k with", text)
        for value in __k:
            if len(find_numbers(value)) > 0:
                __k_value = float(find_numbers(value)[0])
                saved_data.inaccurate_values.append([__k_value, two_index_value])
                break
        return -1
    else:
        return -1


USER_VALUE_EXCEPTIONS = {}


def generate_item_value(item_id: int) -> float:
    item_name = rolimons.Rolimons.get_name_by_id(item_id).lower()
    values = []
    headers = {"authorization": DISCORD_TOKEN}
    proxy = None
    discord_request = requests.get(
        'https://discord.com/api/v9/guilds/415246288779608064/messages/search?channel_id=535250426061258753&content="'
        + item_name
        + "'",
        headers=headers,
        proxies=proxy,
    )

    if discord_request.status_code != 200:
        return -1.0

    for messages in discord_request.json()["messages"]:
        if has_valid_timestamp(messages):
            message_content = str(messages[0]["content"]).lower()
            if len(message_content.split("\n")) < 2:
                continue
            if is_item_from_proof(message_content, item_name) or is_item_from_proof(
                message_content, remove_punctuation(item_name)
            ):
                found_value = find_value(message_content)
                if found_value != -1:
                    values.append(found_value)
    if len(values) > 0:
        newValues = check_saved_values(Data.mean(Data.remove_data_outliers(values)))
        for value in newValues:
            values.append(value)
        avg = Data.avg(Data.remove_data_outliers(values))
        return floor(int(avg * 1000) - (int(avg * 1000) * PROOF_DIFFERENCE_MULTIPLIER))
    elif (len(saved_data.inaccurate_values)) > 0:
        for value in saved_data.inaccurate_values:
            values.append(value[0])
        avg = Data.avg(Data.remove_data_outliers(values))
        return floor(int(avg * 1000) - (int(avg * 1000) * PROOF_DIFFERENCE_MULTIPLIER))
    return 0.0


print(generate_item_value(130213380))
