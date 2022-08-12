import os
from keep_alive import keep_alive
from discord.ext import commands

bot = commands.Bot(
    command_prefix="!",  # Change to desired prefix
    case_insensitive=True  # Commands aren't case-sensitive
)


def set_owner_ids():
    raw_str_ids = os.environ.get("OWNERS_IDS")
    str_ids = raw_str_ids.split(",")
    ids = [int(id) for id in str_ids]
    bot.owner_ids = ids


@bot.event
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier


extensions = [
    # Same name as it would be if you were importing it
    'cogs.cog_example'
    'cogs.cog_database'
]

if __name__ == '__main__':  # Ensures this is the file being ran
    set_owner_ids()
    for extension in extensions:
        bot.load_extension(extension)  # Loades every extension.

keep_alive()  # Starts a webserver to be pinged.
token = os.environ.get("DISCORD_BOT_SECRET")
bot.run(token)  # Starts the bot
