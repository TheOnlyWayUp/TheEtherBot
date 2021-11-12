import aiosqlite, datetime, requests
from requests import get
from uuid import UUID
from mctools import PINGClient


# with open ("C:\Users\dhanu\OneDrive\Desktop\code\TheEtherProject\config.json") as configF:
#     config = json.loads(configF)

# class Embed(discord.Embed):
#     def __init__(self, color=config['embed']['color'], fields=(), field_inline=False, footer=f"Version {config['embed']['version']} of TheEtherBot.", **kwargs):
#         super().__init__(color=color, **kwargs)
#         for n, v in fields:
#             self.add_field(name=n, value=v, inline=field_inline)


async def returnUserJson(usern: str) -> dict:
    """Returns a dict containing all instances of the user, predicted future playing times, and more.

    Args:
        usern (str): The user to get data for.

    Returns:
        dict: A dict containing all instances of the user, predicted future playing times, and more.
    """

    req = get("https://api.mojang.com/users/profiles/minecraft/" + usern).json()
    id = str(UUID(req["id"]))
    """Gets the UUID of the user."""

    PlayerCon = await aiosqlite.connect("players.db")
    PlayerCon.row_factory = aiosqlite.Row
    found = await PlayerCon.execute(f"SELECT * FROM players WHERE ID LIKE '{id}'")
    found = list(await found.fetchall())
    """Pulls all instances of the user from the database, asynchroneously."""

    info = {
        "userinfo": {"name": req["name"], "id": id},
        "servers": list({server["IP"] for server in [dict(x) for x in found]}),
        "sorted": [
            dict(sorted(x.items(), key=lambda x: x[1]))
            for x in [
                {server["IP"]: server["TIMESTAMP"]}
                for server in [dict(x) for x in found]
            ]
        ],
        "utctime": [
            {
                server["IP"]: datetime.datetime.utcfromtimestamp(
                    int(server["TIMESTAMP"] / 1000)
                ).strftime("%Y-%m-%d %H:%M:%S")
            }
            for server in [dict(x) for x in found]
        ],
        "times": [server["TIMESTAMP"] for server in [dict(x) for x in found]],
        "success": True,  # Just added this to make sure the function doesn't break.
    }
    """Returns the user's username, as per proper case and their uuid with dashes."""
    """Returns a unique list of all servers the user has played on."""
    """Returns a list of dicts, each containing a server and the time the user last played on that server, all sorted chronologically."""
    """Returns a list of dicts, each containing a server and the time the user last played on that server, chronologically sorted, but with the dates in UTC instead of UNIX."""
    """Returns a list of all the times the user has played on a server (Useful for predicting the next time a user will log on)."""
    await PlayerCon.close()
    return info


def avg(dates) -> str:
    """Returns the average of a list of dates.

    Args:
        dates (datetime objects): A list of datetime objects.

    Returns:
        string: The average of the list of dates.
    """
    any_reference_date = datetime.datetime(1900, 1, 1)
    x = any_reference_date + sum(
        [date - any_reference_date for date in dates], datetime.timedelta()
    ) / len(dates)
    return x.strftime("%H:%M:%S")


async def returnHostname(server: str) -> str:
    """Returns the hostname of a server.

    Args:
        server (str): The server to get data for.
    """
    DNSCon = await aiosqlite.connect("dns.db")
    DNSCon.row_factory = aiosqlite.Row
    try:
        found = await DNSCon.execute(
            f"SELECT * FROM DNS_TABLE WHERE ip LIKE '{server}' ORDER BY timestamp DESC LIMIT 1"
        )
        found = list(await found.fetchall())
        found = [dict(info) for info in found][0]
        return found["DNS"]
    except Exception:
        return None
    await DNSCon.close()


async def returnServerJson(server: str) -> dict:
    """Returns a dict containing basic server information.

    Args:
        server (str): The server to get data for.

    Returns:
        dict: A dict containing basic server information.
    """

    ServerCon = await aiosqlite.connect("videlicet.db")
    ServerCon.row_factory = aiosqlite.Row
    found = await ServerCon.execute(
        f"SELECT * FROM BASIC_PINGS WHERE ip LIKE '{server}' ORDER BY timestamp DESC LIMIT 1"
    )
    found = list(await found.fetchall())
    if found == []:
        return False
    found = [dict(info) for info in found][0]
    info = {
        "ip": {
            "ip": found["IP"],
            "port": found["PORT"],
            "hostname": await returnHostname(server)
            if await returnHostname(server)
            else found["IP"],
        },
        "version": found["VERSION"],
        "players": {"online": found["PLAYERS_ONLINE"], "max": found["MAX_PLAYERS"]},
        "motd": found["MOTD"],
        "success": True,
    }
    await ServerCon.close()
    return info


async def returnPingJson(server: str) -> dict:
    ping = PINGClient(host=server, timeout=5)
    ping.stop()
    stats = ping.get_stats()
    try:
        motd = "".join(
            [
                motd["text"]
                for motd in requests.get(
                    f"https://eu.mc-api.net/v3/server/ping/{server}"
                ).json()["description"]["extra"]
            ]
        )
    except KeyError:
        motd = "No MOTD."
    except:
        motd = requests.get(f"https://eu.mc-api.net/v3/server/ping/{server}").json()[
            "description"
        ]["text"]
    info = {
        "ip": {
            "ip": server,
            "port": "25565",
            "hostname": await returnHostname(server)
            if await returnHostname(server)
            else server,
        },
        "version": stats["version"]["name"] if stats["version"]["name"] else None,
        "players": {
            "online": stats["players"]["online"],
            "max": stats["players"]["max"],
        },
        "motd": motd,
        "success": True,
    }
    if stats["players"]["online"] != 0:
        info["players"]["players"] = "\n".join(
            [x[0] for x in stats["players"]["sample"]]
        )
    else:
        info["players"]["players"] = "No one online."
    return info


async def returnTotals() -> dict:
    info = {}
    ServerCon = await aiosqlite.connect("videlicet.db")
    ServerCon.row_factory = aiosqlite.Row
    found = await ServerCon.execute("SELECT COUNT(*) FROM BASIC_PINGS")
    info["servers"] = dict(list(await found.fetchall())[0])["COUNT(*)"]
    await ServerCon.close()

    PlayerCon = await aiosqlite.connect("players.db")
    PlayerCon.row_factory = aiosqlite.Row
    found = await PlayerCon.execute("SELECT COUNT(*) FROM PLAYERS")
    info["players"] = dict(list(await found.fetchall())[0])["COUNT(*)"]
    await PlayerCon.close()

    DNSCon = await aiosqlite.connect("dns.db")
    DNSCon.row_factory = aiosqlite.Row
    found = await DNSCon.execute("SELECT COUNT(*) FROM DNS_TABLE")
    info["dns"] = dict(list(await found.fetchall())[0])["COUNT(*)"]
    await DNSCon.close()

    return info
