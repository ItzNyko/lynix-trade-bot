"""
Checks outbound trades that Lynix sends
"""
import cache
import trade_algo
import utils
import roblox
import warnings

warnings.filterwarnings(
    "ignore",
    message="list indices must be integers or slices, not tuple; perhaps you missed a comma?",
)


def check_outbound_trades() -> None:
    """
    Checks outbound trades from cache
    """
    outbound_trades = cache.get_trades_from_cache()
    for trade in outbound_trades:
        fit = trade_algo.check_combination(trade[1], trade[2])
        if not fit:
            decline_trade = roblox.decline_trade(trade[0])
            if decline_trade:
                utils.printf("Successfully declined outbound trade!")
                continue
            utils.printf("Error while attempting to decline outbound trade!")


def outbound_check_thread() -> None:
    """
    Thread to constantly check outbound trades
    """
    while True:
        check_outbound_trades()
