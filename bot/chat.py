import discord
from discord.ext import commands
import matplotlib.pyplot as plt

bot = commands.Bot(command_prefix='!')

text_channel_list = []

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    for guild in bot.guilds:
        for channel in guild.text_channels:
            text_channel_list.append(channel)
    print('------')

@bot.command()
async def all_messages(ctx):
    d = {}
    for channel in text_channel_list:
        count = 0
        async for message in channel.history(limit=None):
            count += 1
        d[channel.name] = count
    await ctx.send(d)
    plt.plot(d.keys(), d.values())
    plt.title('Activity')
    plt.xlabel('Channels')
    plt.ylabel('Messages')
    plt.fill_between(d.keys(), d.values())
    plt.savefig('activity.png')
    await ctx.send(file=discord.File('activity.png'))

@tasks.loop(seconds=30.0)
async def check_msg():
    ctx = bot.get_channel(876055600839159855)
    d = {}
    for channel in text_channel_list:
        count = 0
        async for message in channel.history(limit=None):
            count += 1
        d[channel.name] = count
    await ctx.send(d)
    plt.plot(d.keys(), d.values())
    plt.title('Activity')
    plt.xlabel('Channels')
    plt.ylabel('Messages')
    plt.fill_between(d.keys(), d.values())
    plt.savefig('activity.png')
    await ctx.send(file=discord.File('activity.png'))

@check_msg.before_loop
async def before_check_msg(self):
    await self.bot.wait_until_ready()

check_msg.start()
    
bot.run("ODg4ODM0NzEyMjQ2ODI5MTA3.YUYd1Q.qpdzqQ7GLdQw2WPEKR0B4vvHfvU")
