"""

Lynix's functionality includes 2 different types of proxy parsing
1. dkmwdckk:zdo37eu16s06@45.142.28.83:8094 (semi-converted proxy format)
2. 138.128.97.239:7829:dohtvdoc:5ma6i9k8m8la (webshare.io format)

"""
# {'https': str(random.choice(Settings.proxies))}
from random import random
import random

user_proxies = [None]


def parse_proxies() -> None:
    """
    Parses user proxies from proxies.txt and appends them into user_proxies
    """
    try:
        with open("library/proxies.txt") as proxy_file:
            for line in proxy_file:
                if (
                    line.find("@") != -1
                ):  # If the line is in semi-converted proxy format
                    # dkmwdckk:zdo37eu16s06@45.142.28.83:8094
                    user_proxies.append(
                        {"https": "http://" + str(line.replace("\n", ""))}
                    )
                else:  # Webshare.io format
                    # 138.128.97.239:7829:dohtvdoc:5ma6i9k8m8la
                    proxy = line.split(":")
                    proxy_ip = str(proxy[0])
                    proxy_port = str(proxy[1])
                    proxy_user = str(proxy[2])
                    proxy_pass = str(proxy[3])
                    user_proxies.append(
                        {
                            "https": "http://"
                            + proxy_user
                            + ":"
                            + proxy_pass
                            + "@"
                            + proxy_ip
                            + ":"
                            + proxy_port
                        }
                    )
    except:
        print("Unable to parse proxies. Please try again!")
        return


def get_random_proxy() -> dict:
    """
    Returns random proxy from saved user_proxies list
    """
    return random.choice(user_proxies)
