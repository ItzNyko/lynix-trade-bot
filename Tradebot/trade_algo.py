"""
Lynix's Advanced trade algo, please dont leak to many ppl

Based on trade_score. Base trade score is based from an items value + items rap
For each user_combo in UniqueCombinations, the score is retrieved for the trade
Then, a generator is created and a filter returns the valid range for "acceptable" combinations to filter through (Lynix splits the combinations in 4 sections)
Lynix then searches through the possible combinations and returns the first trade that fits in the user settings

Credits: Jartan, Nyko ofc, special people on StackOverflow
</3 ninrado (aka nina)

Hello script kidies I see you have found me!
"""


from typing import Generator, Iterator
from collections import Counter
from itertools import islice
import roblox
import settings
import bot
import utils
import threading
import time
import data


class UniqueCombinations:
    def __init__(self, iterable, r):
        values, counts = zip(*Counter(iterable).items())
        self.values = values
        self.counts = counts
        self.r = r

        # dp[i][k] := # of unique combinations of length k or shorter with elements values[i:]
        dp = [[1] * (r + 1) for c in range(len(counts) + 1)]
        for i in reversed(range(len(counts))):
            cnt = self.counts[i]
            for k in range(1, r + 1):
                dp[i][k] = (
                    dp[i][k - 1]
                    + dp[i + 1][k]
                    - (dp[i + 1][k - cnt - 1] if k >= cnt + 1 else 0)
                )
        self.dp = dp

    def __getitem__(self, ind):
        res = []
        for i in range(len(self.counts)):
            for k in reversed(range(1, min(self.r - len(res), self.counts[i]) + 1)):
                t = self.dp[i + 1][self.r - len(res) - k] - (
                    self.dp[i + 1][self.r - len(res) - k - 1]
                    if self.r - len(res) >= k + 1
                    else 0
                )
                if ind < t:
                    res.extend(self.values[i] for _ in range(k))
                    break
                else:
                    ind -= t
        if not res:
            raise StopIteration
        return tuple(res)

    def __len__(self):
        return self.dp[0][self.r] - self.dp[0][self.r - 1]


def seperate_chunk_sizes(
    chunk_size: int, target_chunk: int, combinations: UniqueCombinations
) -> Iterator:
    """
    Calculates range for trade calculations
    """
    chunks = []
    combination_length = combinations.__len__() - 1

    if combination_length < chunk_size:
        return combinations
    while combination_length >= 0:
        if combination_length - chunk_size < 0:
            chunk_value = data.get_trade_score(combinations.__getitem__(0))
            chunks.append((chunk_value, 0, combination_length))
            break
        chunk_value = data.get_trade_score(
            combinations.__getitem__(combination_length - chunk_size)
        )
        chunks.append(
            (chunk_value, combination_length - chunk_size, combination_length)
        )
        combination_length -= chunk_size
    best_chunk = min(chunks, key=lambda x: abs(x[0] - target_chunk))

    return islice(combinations, best_chunk[1], best_chunk[2])


def check_combination(user_combo: tuple, partner_combo: tuple) -> bool:
    """
    Returns whether combination fits in user settings
    """

    rap_profit = data.get_combo_rap(partner_combo) - data.get_combo_rap(user_combo)
    value_profit = data.get_combo_value(partner_combo) - data.get_combo_value(
        user_combo
    )

    if (
        value_profit >= settings.MIN_VALUE_WIN
        and value_profit <= settings.MAX_VALUE_WIN
    ):
        if rap_profit >= settings.MIN_RAP_WIN and rap_profit <= settings.MAX_RAP_WIN:
            return True
    return False


def find_trade(
    user_inventory: list,
    partner_id: int,
):
    """
    Returns best possible trade from user based on user settings
    """
    p_inven = roblox.get_limited_items(partner_id)
    if len(p_inven) < 3:
        utils.printf("Skipping user, they have no items..")
        return

    utils.printf("Searching for trades with: " + str(partner_id))
    partner_combinations = UniqueCombinations(p_inven, 4)

    start_time = time.time()
    for user_combination in UniqueCombinations(user_inventory, 4):
        for items in user_combination:
            if items in partner_combinations:
                return

        user_trade_score = data.get_trade_score(user_combination)
        # print(partner_combinations.__len__())
        partner_ranged_combinations = seperate_chunk_sizes(
            10, user_trade_score, partner_combinations
        )

        for partner_combination in partner_ranged_combinations:
            process_time = time.time()
            if process_time - start_time >= settings.MAX_TIME_FOR_TRADES:
                utils.printf("Maximum time looking for trade reached!")
                bot.user_threads -= 1
                return
            partner_trade_score = data.get_trade_score(partner_combination)
            trade_attractiveness = (user_trade_score - partner_trade_score) / (
                user_trade_score + partner_trade_score
            )

            if (
                trade_attractiveness >= settings.MIN_TRADE_ATTRACTIVENESS
                and trade_attractiveness <= settings.MAX_TRADE_ATTRACTIVENESS
            ):
                if check_combination(user_combination, partner_combination):
                    bot.trade_queue.append(
                        (partner_id, user_combination, partner_combination)
                    )
                    utils.printf(
                        "Successfully found trade with: "
                        + str(partner_id)
                        + " and added to queue! ["
                        + str(trade_attractiveness)
                        + "]"
                    )
                    bot.user_threads -= 1
                    return
            continue


def find_trade_thread(user_inventory: list, partner_id: int):
    trade_thread = threading.Thread(
        target=find_trade,
        args=(
            user_inventory,
            partner_id,
        ),
    )
    trade_thread.start()
    time.sleep(settings.MAX_TIME_FOR_TRADES)
    trade_thread.join()


"""
inv = roblox.get_user_limiteds(1530946960)
inv.sort(key=lambda x: x[0])
x = UniqueCombinations(inv, 4)
print(seperate_chunk_sizes(1000, 253123, x))
"""
