import aiosqlite
from requests import get
from uuid import UUID
from datetime import datetime


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

    conn = await aiosqlite.connect("players.db")
    conn.row_factory = aiosqlite.Row
    found = await conn.execute(f"SELECT * FROM players WHERE ID LIKE '{id}'")
    found = list(await found.fetchall())
    """Pulls all instances of the user from the database, asynchroneously."""

    info = {
        "userinfo": {"name": req["name"], "id": id},
        """Returns the user's username, as per proper case and their uuid with dashes."""
        "servers": list(set([server["IP"] for server in [dict(x) for x in found]])),
        """Returns a unique list of all servers the user has played on."""
        "sorted": [
            dict(sorted(x.items(), key=lambda x: x[1]))
            for x in [
                {server["IP"]: server["TIMESTAMP"]}
                for server in [dict(x) for x in found]
            ]
        ],
        """Returns a list of dicts, each containing a server and the time the user last played on that server, all sorted chronologically."""
        "utctime": [
            {
                server["IP"]: datetime.utcfromtimestamp(
                    int(server["TIMESTAMP"] / 1000)
                ).strftime("%Y-%m-%d %H:%M:%S")
            }
            for server in [dict(x) for x in found]
        ],
        """Returns a list of dicts, each containing a server and the time the user last played on that server, chronologically sorted, but with the dates in UTC instead of UNIX."""
        "times": [server["TIMESTAMP"] for server in [dict(x) for x in found]],
        """Returns a list of all the times the user has played on a server (Useful for predicting the next time a user will log on)."""
        "success": True,  # Just added this to make sure the function doesn't break.
    }
    await conn.close()
    return info


def avg(dates) -> str:
    """Returns the average of a list of dates.

    Args:
        dates (datetime objects): A list of datetime objects.

    Returns:
        string: The average of the list of dates.
    """
    any_reference_date = datetime(1900, 1, 1)
    x = any_reference_date + sum(
        [date - any_reference_date for date in dates], datetime.timedelta()
    ) / len(dates)
    return x.strftime("%H:%M:%S")
