import sqlite3, requests, uuid, json, datetime
def returnServerJson(usern:str):
    req = requests.get("https://api.mojang.com/users/profiles/minecraft/" + usern).json()
    id = str(
        uuid.UUID(
            req[
                "id"
            ]
        )
    )
    conn = sqlite3.connect("players.db")
    conn.row_factory = sqlite3.Row
    found = list(
        conn.cursor().execute(f"SELECT * FROM players WHERE ID LIKE '{id}'").fetchall()
    )
    info = {
        "userinfo": {"name":req['name'],"id":id},
        "servers": list(set([server["IP"] for server in [dict(x) for x in found]])),
        "sorted": [
            dict(sorted(x.items(), key=lambda x: x[1]))
            for x in [
                {server["IP"]: server["TIMESTAMP"]} for server in [dict(x) for x in found]
            ]
        ],
        "utctime": [{server['IP']:
            datetime.datetime.utcfromtimestamp(
                int(server["TIMESTAMP"]/1000)
            ).strftime("%Y-%m-%d %H:%M:%S")}
            for server in [dict(x) for x in found]
        ],
        "times": [server["TIMESTAMP"] for server in [dict(x) for x in found]],
    }
    conn.close()
    return info
    
def avg(dates):
  any_reference_date = datetime.datetime(1900, 1, 1)
  x = any_reference_date + sum([date - any_reference_date for date in dates], datetime.timedelta()) / len(dates)
  return x.strftime("%H:%M:%S")