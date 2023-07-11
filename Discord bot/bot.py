"""
LYNIX DISCORD BOT
"""
from discord import *
import requests

BOT_PREFIX = "$"
DISCORD_TOKEN = "OTg4MjYxODEyNjgyMjI3Nzky.GHuHzB.4PoJTgOLInyZvJhOTWrcngL_FQjKT1kxr01-OI"
WHITELIST_FILE = "whitelists.txt"
client = Client()


def has_admin(roles: list) -> bool:
    """
    Returns whether user has admin role
    """
    for role in roles:
        if str(role) == "Owner":
            return True
    return False


def has_buyer(roles: list) -> bool:
    """
    Returns whether user has buyer role
    """
    for role in roles:
        if str(role) == "buyer":
            return True
    return False


def is_valid_roblox_user(user_id: int) -> bool:
    """
    Returns whether userid is valid
    """
    try:
        if (
            requests.get(
                "https://users.roblox.com/v1/users/" + str(user_id)
            ).status_code
            == 200
        ):
            return True
        return False
    except:
        return -1


def has_whitelist(discord_id: str) -> bool:
    """
    Returns whether user has whitelist already
    """
    with open(WHITELIST_FILE) as f:
        text = f.readline()
        if text.find(discord_id) != -1:
            return True
        return False


def get_roblox_id(discord_id: str) -> str:
    with open(WHITELIST_FILE, "r") as whitelist:
        for line in whitelist:
            if line.find(discord_id) != -1:
                return str(line.split(":")[1].replace("\n", ""))
    return ""


def write_to_whitelist(discord_id: str, roblox_id: str):
    with open(WHITELIST_FILE, "a") as whitelist:
        whitelist.write(discord_id + ":" + roblox_id + "\n")


def remove_whitelist(discord_id: str) -> bool:
    """
    Removes whitelist from text file
    """
    new_data = []
    try:
        with open(WHITELIST_FILE, "r") as cache_file:
            for line in cache_file:
                if line.split(":")[0] != str(discord_id):
                    new_data.append(str(line.replace("\n", "")))

        with open(WHITELIST_FILE, "w") as cache_file:
            for data in new_data:
                cache_file.write(str(data) + "\n")
        return True
    except:
        return False


@client.event
async def on_ready():
    print("Lynix Bot has successfully logged in!")
    await client.change_presence(status=Status.do_not_disturb)


@client.event
async def on_message(message):  # $whitelist
    message_content = str(message.content)
    if message_content.find(BOT_PREFIX + "whitelist") != -1:
        if has_buyer(message.author.roles):
            if len(message_content.split(" ")) != 2:
                await message.channel.send(
                    str(message.author.mention)
                    + " `In order to whitelist your user, please type in: '$whitelist ROBLOX_USER_ID'`"
                )
                return

            whitelist_user = message_content.split(" ")[1]
            user_discord_id = str(message.author.id)
            if has_whitelist(user_discord_id) != True:
                try:
                    if not is_valid_roblox_user(int(whitelist_user)):
                        await message.channel.send(
                            str(message.author.mention)
                            + " `You are attempting to whitelist an invalid roblox id!`"
                        )
                        return
                    else:
                        write_to_whitelist(user_discord_id, str(whitelist_user))
                        await message.channel.send(
                            str(message.author.mention)
                            + " `'"
                            + str(whitelist_user)
                            + "' has been successfully whitelisted and added to the database!`"
                        )
                        return
                except:
                    await message.channel.send(
                        str(message.author.mention)
                        + " `Please enter a userid, not a username!`"
                    )
                    return
            elif has_admin(message.author.roles):
                try:
                    if not is_valid_roblox_user(int(whitelist_user)):
                        await message.channel.send(
                            str(message.author.mention)
                            + " `You are attempting to whitelist an invalid roblox id!`"
                        )
                        return
                    else:

                        write_to_whitelist(user_discord_id, str(whitelist_user))
                        await message.channel.send(
                            str(message.author.mention)
                            + " `ADMIN OVERWRITE: '"
                            + str(whitelist_user)
                            + "' has been successfully whitelisted and added to the database!`"
                        )
                        return
                except:
                    await message.channel.send(
                        str(message.author.mention)
                        + " `Please enter a userid, not a username!`"
                    )
                    return
            else:
                await message.channel.send(
                    str(message.author.mention)
                    + " `You already have a whitelist! Type '$mydata' for more information!`"
                )
                return

    if message_content.find(BOT_PREFIX + "clear") != -1:
        if has_admin(message.author.roles):
            if len(message_content.split(" ")) != 2:
                await message.channel.send(
                    str(message.author.mention)
                    + " `In order to clear all whitelisted userids from a whitelist, please type: '$clear DISCORD_ID' `"
                )
                return
            remove_user = message_content.split(" ")[1]
            if has_whitelist(str(remove_user)):
                if remove_whitelist(str(remove_user)):
                    await message.channel.send(
                        str(message.author.mention)
                        + " ` ADMIN OVERWRITE: Successfully removed whitelist from Discord ID: "
                        + str(remove_user)
                        + "`"
                    )
                    return
            await message.channel.send(
                str(message.author.mention)
                + " `Discord ID: '"
                + str(remove_user)
                + "' was unable to be removed from database as it was not found!`"
            )
            return
        else:
            if has_whitelist(str(message.author.id)):
                if len(message_content.split(" ")) != 1:
                    await message.channel.send(
                        str(message.author.mention)
                        + " `In order to remove all userids from whitelist, please type: '$remove'`"
                    )
                    return

                if remove_whitelist(str(message.author.id)):
                    await message.channel.send(
                        str(message.author.mention)
                        + " `Successfully removed userids with Discord ID: "
                        + str(message.author.id)
                        + "`"
                    )
                    return

    if message_content.find(BOT_PREFIX + "mydata") != -1:
        if has_buyer(message.author.roles):
            if has_whitelist(str(message.author.id)):
                await message.channel.send(
                    str(message.author.mention)
                    + " `If you would like to replace your whitelist please type '$clear' and then '$whitelist ROBLOX_ID'. If you need any help please ask staff!"
                    + " Your current whitelist is to: '"
                    + str(get_roblox_id(str(message.author.id)))
                    + "'`"
                )
                return
            else:
                await message.channel.send(
                    str(message.author.mention)
                    + " `You currently dont have a whitelist, please type '$whitelist ROBLOX_ID'`"
                )
                return


client.run(DISCORD_TOKEN)
