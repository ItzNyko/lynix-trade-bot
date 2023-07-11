import requests
import json
from discord import *
import roblox
import random
import datetime


SERVER_LOG_WEBHOOK = "https://discord.com/api/webhooks/987101742606991440/p22Fg6mBDqlmCqccsFSgyUmsVw0OrJaIlV0RoQ_ukQYakSUUMBjEDeZt20iw0Fv1mDXm"
ROLIMON_VALUE_ICON = "<:rollahmons:973409500499431424> "
ROBUX_ICON = "<:wrapping:973409500507811840> "
ROBLOX_ICON = "https://images.rbxcdn.com/3b43a5c16ec359053fef735551716fc5.ico"

# ``


def send_data_to_server(data: dict, color=0x82ADAD):
    """
    (SERVER-SIDED) Posts data to webhook in log format
    """
    data_embed = Embed(title="User has successfully logged in", color=color)
    data_embed.timestamp = datetime.datetime.utcnow()
    data_embed.set_footer(
        text="\u200bLynix Authentication Service",
        icon_url="https://cdn.discordapp.com/icons/924161665296125972/753afaabd0502a6ec5366e0a331096d7.webp?size=96",
    )
    for _data in data:
        is_inlined = data[_data][1]
        data_embed.add_field(
            name=str(_data),
            value="`" + str(data[_data][0]) + "`",
            inline=is_inlined,
        )

    data_embed.set_thumbnail(
        url=roblox.get_user_thumbnail(
            int(roblox.ROBLOX_ID)
        )  # https://tr.rbxcdn.com/35bb7aa7ee42ae52c2776e6112c9c6cd/352/352/Avatar/Png"
    )
    webhook = Webhook.from_url(
        SERVER_LOG_WEBHOOK,
        adapter=RequestsWebhookAdapter(),
    )

    webhook.send(embed=data_embed)


def send_to_user_webhook(thumbnail_url: str, data: dict, color=0x82ADAD) -> bool:

    data_embed = Embed(title="Trade has been sucessfully completed!", color=color)
    data_embed.timestamp = datetime.datetime.utcnow()
    data_embed.set_footer(
        text="\u200bLynix Trade Bot",
        icon_url="https://cdn.discordapp.com/icons/924161665296125972/753afaabd0502a6ec5366e0a331096d7.webp?size=96",
    )

    data_embed.set_thumbnail(
        url=thumbnail_url  # "https://tr.rbxcdn.com/35bb7aa7ee42ae52c2776e6112c9c6cd/352/352/Avatar/Png"
    )

    for _data in data:
        is_inlined = data[_data][1]
        data_embed.add_field(
            name=str(_data),
            value="`" + str(data[_data][0]) + "`",
            inline=is_inlined,
        )

    webhook = Webhook.from_url(
        SERVER_LOG_WEBHOOK,
        adapter=RequestsWebhookAdapter(),
    )

    webhook.send(embed=data_embed)
