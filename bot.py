import discord, aiohttp, asyncio, regex, sqlite3, pyfade, socket, DiscordUtils, requests
from mctools import PINGClient
from discord.ext import commands
db = sqlite3.connect('basicpings.db')
cur = db.cursor()

bot = commands.Bot(commands.when_mentioned_or("mp!"), intents=discord.Intents.all(), description="Meant for the Ether Project. Manages queries to database from Discord and general administrative tasks.", case_inensitive=True)


@bot.event
async def on_ready():
    r = """
 ______ _          ___     _                 __                        
(_) |  | |        / (_)   | |             /|/  \           o           
    |  | |   _    \__  _|_| |   _  o _     |___/ o _   __    _  __  _|_
    |  |/ \ |/    /     | |/ \ |/  /  |   _|     /  | /  \ ||/ /     | 
 (_/\_/|   ||__  /\___/ |_|   ||__/   |_   |    /   |_\__//||__\___/ |_
                                                          /|           
                                                          \|           

    """
    c = "𝕄𝕣𝔹𝕣𝕦𝕙, 𝕊𝕚𝕘𝕟𝕒𝕞, ℤ𝕤𝕖, 𝕋𝕙𝕖𝕆𝕟𝕝𝕪𝕎𝕒𝕪𝕌𝕡"
    print(pyfade.Fade.Vertical(pyfade.Colors.purple_to_red, r))
    print(f'''                                             - Made by {pyfade.Fade.Vertical(pyfade.Colors.green_to_yellow, c)}.''')

def returnArgs(command):
    args = {}
    cmd = command.split(",")
    for c in cmd:
        if c.startswith("--"):
            args[c.lstrip("--")] = cmd[cmd.index(c) + 1]

    return args
# def bin2text(s): return "".join([chr(int(s[i:i+8],2)) for i in xrange(0,len(s),8)])

bot.load_extension("errorhandler")
@bot.command(help="Shows you basic serverinfo as stored in the database.")
@commands.cooldown(1,5)
async def server(ctx, *, args):
    search = returnArgs(args)
    print(search)
    e = discord.Embed(title="Information", description=f"Here are the results.")
    r = []
    ip = socket.gethostbyname(search['ip']) if "ip" in search.keys() else None
    online = search['online'] if "online" in search.keys() else None
    version = search['version'] if "version" in search.keys() else None
    motd = search['motd'] if "motd" in search.keys() else None
    #Yeah I know I can do if x in search, but I prefer search.keys
    if ip is not None:
        for row in cur.execute(f'SELECT * FROM BASIC_PINGS WHERE IP LIKE "{ip}" ORDER BY timestamp DESC'):
            r.append(row)
    elif online is not None:
        for row in cur.execute(f'SELECT * FROM BASIC_PINGS WHERE ONLINE LIKE "{online}" ORDER BY timestamp DESC'):
            r.append(row)
    elif version is not None:
        for row in cur.execute(f'SELECT * FROM BASIC_PINGS WHERE VERSION LIKE "{version}" ORDER BY timestamp DESC'):
            r.append(row)
    elif motd is not None:
        for row in cur.execute(f'SELECT * FROM BASIC_PINGS WHERE MOTD LIKE "{motd}" ORDER BY timestamp DESC'):
            r.append(row)
    else:
        await ctx.send("Args must be ip, motd, version or online. Enjoy the cooldown.")  
        return
    embedList = []
    for x in r:
        e = discord.Embed(title="Info", description="Your results -")
        try:
            e.add_field(name=f"{x[1]}", value=f"IP - `{x[1]}:{x[2]}`\nVersion - `{x[3]}`\nMOTD - `{x[4]}`\nPlayer Count - `{x[5]}/{x[6]}`")
        except IndexError:
            e.add_field(name="Error", value="Couldn't find any information regarding your request.")
        e.set_footer(text="The Ether Project")
        embedList.append(e)
    paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
    paginator.add_reaction('⏮️', "first")
    paginator.add_reaction('⏪', "back")
    paginator.add_reaction('🔐', "lock")
    paginator.add_reaction('⏩', "next")
    paginator.add_reaction('⏭️', "last")
    await paginator.run(embedList)



@bot.command(help="Pings a server. Usage - ping <ip> [port, defaults to 25565]. If the minecraft server doesn't exist, your message will be deleted.")
async def ping(ctx, ip, port=25565):
    try:
        ping = PINGClient(host=ip, timeout=5, port=port)
        ping.stop()
        stats = ping.get_stats()
        motd = ""
        try:
            motd = "".join([motd["text"] for motd in requests.get(f"https://eu.mc-api.net/v3/server/ping/{ip}").json()["description"]["extra"]])
        except KeyError:
            motd = "No MOTD."
        except:
            motd = requests.get(f"https://eu.mc-api.net/v3/server/ping/{ip}").json()["description"]["text"]
        stats_embed = discord.Embed(title=ip.upper(), description=motd, color=0x76a5af)
        stats_embed.add_field(name="Max", value=f"{stats['players']['online'] if stats['players']['online'] else 0}/{stats['players']['max'] if stats['players']['max'] else None}")
        if "sample" in stats['players']:
            if stats['players']['online'] != 0:
                stats_embed.add_field(name="Players", value="\n".join(f"`{player[0][:-4]}`" for player in stats['players']['sample']))
        else:
            stats_embed.add_field(name="Players", value="None")
        stats_embed.add_field(name="Version", value=stats['version']['name'] if stats['version']['name'] else None)
        stats_embed.add_field(name="Info", value="[TheOnlyWayUp](https://twitch.tv/TheOnlyWayUp)  |  [Invite The bot](https://discord.com/oauth2/authorize?client_id=893908485891317800&scope=bot+applications.commands&permissions=274878000128)  \|  [View the Code](https://github.com/TheOnlyWayUp/MinecraftServerInfo-Discord)")
        await ctx.reply(embed=stats_embed, mention_author=False)
    except Exception as e:
        stats_embed = discord.Embed(title="Error, couldn't retreive information.", description=f"Cause: {e}.", color=0xcc6666)
        stats_embed.add_field(name="Info", value=f"[TheOnlyWayUp](https://twitch.tv/TheOnlyWayUp)  |  [Invite The bot](https://discord.com/oauth2/authorize?client_id={bot.user.id}&scope=bot+applications.commands&permissions=274878000128)  \|  [View the Code](https://github.com/TheOnlyWayUp/MinecraftServerInfo-Discord)")
        await ctx.reply(embed=stats_embed, mention_author=False)


bot.run("token")