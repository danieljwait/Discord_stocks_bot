#!/usr/bin/env python

import logging
import os
import stocks  # stocks.py


# Exits code when necessary modules are missing
def missing_package() -> None:
    print("Some modules required to run this program are missing\n"
          "Run setup.cmd and try again\n\n"
          "Press any key to continue . . . ", end="")
    input()
    exit()


try:
    import discord
    from discord.ext import commands
except ImportError:
    missing_package()

try:
    from dotenv import load_dotenv
except ImportError:
    missing_package()

# Logs information and warnings about the bot to a .log file
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s'))
logger.addHandler(handler)

# Fetches bot token from then .env file
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Initiates bot (prefix comes before any commands)
bot = commands.Bot(command_prefix="£")


@bot.event
async def on_ready():
    # Confirmation of log on in console
    print("You have logged on as {0}".format(bot.user))


@bot.command(name="update")
async def update_stocks(ctx):
    print("Command: Update stocks")
    stocks.update_stocks()


# Outputs a summary table of the day's stocks
@bot.command(name="table")
async def summary_table(ctx):
    print("Command: Summary table")
    # Outputs summary table in code block for monospaced font
    await ctx.channel.send("Summary table:```\n" + stocks.summary_table() + "\n```")


# Outputs a graphs for the stocks to a specified number of days (default of 50)
@bot.command(name="graph")
async def graph(ctx, days=50):
    print("Command: Graphs of {0} days".format(days))
    stocks.update_plots(days)

    stock_images = []
    for stock_name in stocks.STOCKS_LIST:
        with open(stocks.graph_path(stock_name) + ".png", "rb") as file:
            stock_images.append(discord.File(file))

    # Sends all the plots in one message
    await ctx.channel.send(files=stock_images)


bot.run(DISCORD_TOKEN)
