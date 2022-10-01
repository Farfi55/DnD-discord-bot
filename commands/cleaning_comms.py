import discord
from discord.ext import commands
import backend.feedback as feedback


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

    @commands.command(name='test')
    async def embed(ctx):
        embed = discord.Embed(
            title="Sample Embed",
            url="https://realdrewdata.medium.com/",
            description=
            "This is an embed that will show how to build an embed and the different components",
            color=0xFF5733)
        await feedback.reply_with_embed_msg(ctx, embed)


async def setup(bot):
    await bot.add_cog(CleaningCommands(bot))
