"""
Modified version of Lynix's projection detector
"""
import server_roblox
import server_rolimons


def mean(list: list) -> float:
    try:
        total = 0
        for data in list:
            total += data
        return total / len(list)
    except:
        return -1


def remove_data_outliers(data: list) -> list:
    """
    Removes outlier data from a set of data (Jartan's algo) well it's math
    """
    new_data = []
    average = mean(data)
    standard_deviation = get_standard_deviation(data)
    for price in data:
        if (
            price <= average + standard_deviation
            and price >= average - standard_deviation
        ):
            new_data.append(price)
    return new_data


def get_standard_deviation(data: list) -> float:
    """
    Returns standard deviation in a set of data
    """
    if len(data) > 0:
        sum_of_squared_deviation = 0
        average = mean(data)
        for hist in data:
            sum_of_squared_deviation += (hist - average) ** 2
        return (sum_of_squared_deviation / len(data)) ** 0.5
    return -1


'''
def is_projected(sales: list, item_id: int):
    """
    Returns whether item is projected using outlier system and its corrected rap
    """
    try:
        if server_rolimons.has_value(item_id):
            return False
        if server_rolimons.is_projected(item_id):
            return True
        item_data = server_roblox.get_item_data(item_id)
        item_concurrent_rap = int(item_data[1])
        item_sales_data = item_data[0]
        corrected_rap = mean(remove_data_outliers(item_sales_data))
        if (
            item_concurrent_rap >= corrected_rap * 1.085
        ):  # if concurrent rap is greater than 1.08x (8%) its normal rap
            return True
        return False
    except:
        return True
'''


def calculated_item_data(item_id: int) -> list:
    """
    Returns calculated item data:
    [is_projected, rap]
    """
    try:
        if server_rolimons.has_value(item_id):
            return (False, server_rolimons.get_item_rap(item_id))
        if server_rolimons.is_projected(item_id):
            return (True, server_rolimons.get_item_rap(item_id))
        item_data = server_roblox.get_item_data(item_id)
        item_sales_data = item_data[0]
        corrected_rap = mean(remove_data_outliers(item_sales_data))
        rolimons_rap = server_rolimons.get_item_rap(item_id)
        item_concurrent_rap = int(item_data[1])
        if (
            item_concurrent_rap >= corrected_rap * 1.085
        ):  # if concurrent rap is greater than 1.08x (8%) its normal rap
            if rolimons_rap < corrected_rap:
                return (True, rolimons_rap)
            return (True, corrected_rap)
        if rolimons_rap < corrected_rap:
            return (False, rolimons_rap)
        return (False, corrected_rap)
    except:
        return (True, -1)
