import discord
from discord.ext import commands
from replit import db
from auth import autentifica


class DataBaseComands(commands.Cog, name='Comandi DataBase'):
    ''''''
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        '''
		controllo per i comandi di questa classe, se ritorna True, il comando può essere eseguito
		'''
        return autentifica(ctx)

    @commands.command(  # Decorator to declare where a command is.
        name='dbadd',  # Name of the command, defaults to function name.
        aliases=['db_add']  # Aliases for the command.
    )
    async def db_aggiungi(self, ctx, key, value):
        '''
		Aggiunge un campo
		'''

    @commands.command(name="unload", aliases=['ul'])
    async def unload(self, ctx, cog):
        '''
		Unload a cog.
		'''
        extensions = self.bot.extensions
        if cog not in extensions:
            await ctx.send("Cog is not loaded!")
            return
        self.bot.unload_extension(cog)
        await ctx.send(f"`{cog}` has successfully been unloaded.")

    @commands.command(name="load")
    async def load(self, ctx, cog):
        '''
		Loads a cog.
		'''
        try:

            self.bot.load_extension(cog)
            await ctx.send(f"`{cog}` has successfully been loaded.")

        except commands.errors.ExtensionNotFound:
            await ctx.send(f"`{cog}` does not exist!")

    @commands.command(name="listcogs", aliases=['lc'])
    async def listcogs(self, ctx):
        '''
		Returns a list of all enabled commands.
		'''
        base_string = "```css\n"  # Gives some styling to the list (on pc side)
        base_string += "\n".join([str(cog) for cog in self.bot.extensions])
        base_string += "\n```"
        await ctx.send(base_string)


def setup(bot):
    bot.add_cog(DataBaseComands(bot))


matches = db.prefix("prefix")
