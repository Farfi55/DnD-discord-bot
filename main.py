import os
from keep_alive import keep_alive
import discord
from discord.ext import commands
import asyncio
import logging


class MyBot(commands.Bot):
    def __init__(self):
        log_handler = logging.FileHandler(filename='discord.log',
                                          encoding='utf-8',
                                          mode='w')

        bot_intents = discord.Intents.all()

        super().__init__(
            command_prefix=".",  # Change to desired prefix
            intents=bot_intents,
            case_insensitive=True,  # Commands aren't case-sensitive
            log_handler=log_handler,
            log_level=logging.DEBUG)

    async def setup_hook(self):
        extensions = [
            # Same name as it would be if you were importing it
            'commands.dev_comms',
            'commands.database_comms',
            #'commands.cleaning_comms',
            'commands.shop_comms',
        ]

        for extension in extensions:
            await self.load_extension(extension)  # Loades every extension.

    def set_owner_ids(self):
        raw_str_ids = os.environ.get("OWNERS_IDS")
        str_ids = raw_str_ids.split(" ")
        ids = [int(id) for id in str_ids]
        bot.author_id = ids[0]
        bot.owner_ids = ids


bot = MyBot()


async def main():
    keep_alive()  # Starts a webserver to be pinged.

    async with bot:
        bot.set_owner_ids()

        token = os.environ.get("DISCORD_BOT_SECRET")
        await bot.start(token)  # Starts the bot


asyncio.run(main())


@bot.event
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier
