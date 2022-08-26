import discord
from discord.ext import commands


class CleaningCommands(commands.Cog, name='Comandi misti'):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        '''
        The default check for this cog whenever a command is used. Returns True if the command is allowed.
        '''
        return ctx.author.id == self.bot.author_id or ctx.author.id in self.bot.owner_ids

    @commands.command(name='clear', aliases=['wipe'])
    async def clear(self, ctx):
        await ctx.channel.purge(limit=5000)


def setup(bot):
    bot.add_cog(CleaningCommands(bot))
