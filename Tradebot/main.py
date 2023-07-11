import random
from threading import Thread
import security
import utils
import proxies
import roblox
import settings
import users
import trade_algo
import bot
import outbound_checker
import time
import sys
import auth
import config
import os
import data

BOT_VERSION_ID = "v1.2"


# TODO:
# Fix custom_values problem and make it "load" rather than have it preloaded


def show_text():
    print(
        """
      █████ █                                                     
   ██████  █                                   █                  
  ██   █  █                                   ███                 
 █    █  █                                     █                  
     █  █          ██   ████                         ███    ███   
    ██ ██           ██    ███  █ ███  ████   ███    █ ███  ████ █ 
    ██ ██           ██     ████   ████ ████ █ ███      ███ █████  
    ██ ██           ██      ██     ██   ████   ██       ███  ██   
    ██ ██           ██      ██     ██    ██    ██        ███      
    ██ ██           ██      ██     ██    ██    ██       █ ███     
    █  ██           ██      ██     ██    ██    ██      █   ███    
       █            ██      ██     ██    ██    ██     █     ███   
   ████           █  █████████     ██    ██    ██    █       ███ █
  █  █████████████     ████ ███    ███   ███   ███ ██         ███ 
 █     █████████             ███    ███   ███   ███               
 █                    █████   ███                                 
  █                 ████████  ██                                  
   ██              █      ████                                    
                                                                  

    """
    )


def main():
    show_text()
    utils.set_window_name()
    bot_security_thread = Thread(target=security.security_thread, args=())
    bot_security_thread.start()

    utils.printf(
        "Welcome to Lynix Trade Bot " + BOT_VERSION_ID + " | Developed By: Nyk0"
    )

    utils.check_file_requirements()
    config.load_config()
    proxies.parse_proxies()

    #
    if roblox.check_cookie(settings.USER_COOKIE) != True:
        utils.printf("Cookie is no longer valid! Please refresh!")
        time.sleep(10)
        os._exit()
    utils.printf("Checking Authentication Services..")
    roblox.ROBLOX_ID = roblox.get_user_id(settings.USER_COOKIE)  # 3152308525
    roblox.USER_INVENTORY = roblox.get_user_limiteds(roblox.ROBLOX_ID)

    """
    if not auth.check_authentication(roblox.ROBLOX_ID):
        utils.printf("User is not authenticated!")
        time.sleep(3)
        os._exit(-1)
    utils.printf("Success!")
    """
    """
    if len(server.all_item_ids) < 1993:
        utils.printf(
            "Server is ~"
            + str((len(server.all_item_ids) / 2000) * 100)
            + "% done calculating item values.. Usually happens when server restarts! Please wait and try again later!"
        )
        utils.printf("Items scanned: " + str(len(server.all_item_ids)))
        time.sleep(3)
        os._exit(-1)
    """
    utils.printf(
        "Welcome, "
        + roblox.get_username(roblox.ROBLOX_ID)
        + "! ("
        + str(roblox.ROBLOX_ID)
        + ")"
    )

    utils.printf("Sucessfully Authenticated User!")
    utils.printf("User tradeable items: " + str(len(roblox.USER_INVENTORY)))

    update_data = Thread(
        target=data.update_data_thread,
        args=(),
    )
    update_data.start()

    send_thread = Thread(
        target=bot.send_thread,
        args=(),
    )
    send_thread.start()

    outbound_checker_thread = Thread(
        target=outbound_checker.outbound_check_thread,
        args=(),
    )
    outbound_checker_thread.start()
    utils.printf("Sucessfully loaded: " + str(len(proxies.user_proxies)) + " proxies!")
    while True:
        partners = []
        utils.printf("Scanning for users..")
        partners = list(set(users.rolimons_user_scrape()))
        for val in range(10):
            for user in users.get_users_from_resellers(
                random.choice(data.all_item_ids)
            ):
                partners.append(user)
        utils.printf("Sucessfully refreshed user queue: " + str(len(partners)))
        bot.user_threads = 0
        for user in partners:
            if len(bot.trade_queue) > 5:
                utils.printf(
                    "Maximum trade queue length reached! Waiting for trades to be sent.."
                )
                time.sleep(15)
            if bot.user_threads > 70:
                utils.printf(
                    "Maximum user threads reached! Waiting for trades to be found.."
                )
                time.sleep(30)
            random.shuffle(roblox.USER_INVENTORY)
            trade_thread = Thread(
                target=trade_algo.find_trade,
                args=(
                    roblox.USER_INVENTORY,
                    user,
                ),
            )
            bot.user_threads += 1
            trade_thread.start()

        utils.printf("Refreshing partner trade queue!")


if __name__ == "__main__":
    main()
