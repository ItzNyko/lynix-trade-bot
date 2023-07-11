"""
Lynix's Data Generator: 
Functions as a way for clients to recieve itemdata within seconds, rather than taking time to calculate on client side
Also allows security towards item evaluation in certain circumstances
{"data": {"item_id":[item_score, is_rare, is_projected, item_volume, rap, value], }}
"""

# from tracemalloc import start # What is tracemalloc
import server_rolimons
import server_proj
import server_roblox
import time

data_values = {"data": {}}


def generate_values() -> None:
    """
    Generates list of data for items
    {"1028606": [5982, false, true, 19.37, 1744.7654320987654, 2991],
    """
    while True:
        start_time = time.time()
        print("Generating values started at: " + str(start_time))
        for item in server_rolimons.all_item_ids:
            if not server_rolimons.has_value(item) and not server_rolimons.is_projected(
                item
            ):
                try:
                    item_data = server_proj.calculated_item_data(item)
                    data_values["data"][str(item)] = [
                        bool(item_data[0]),
                        float(server_roblox.get_item_volume(item)),
                        int(item_data[1]),
                    ]
                except:
                    print("Error while fetching data for: " + str(item))
                    pass
        print("Sucessfully refreshed all item data!")
        print("Execution time: " + str(time.time() - start_time))


def generation_thread() -> None:
    """
    Generation thread for datagen
    """
    while True:
        generate_values()
