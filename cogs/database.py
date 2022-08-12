import discord
from discord.ext import commands
import db_utils
import utils


class DataBaseComands(commands.Cog, name='Comandi DataBase'):
    ''''''
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        '''
		controllo per i comandi di questa classe, se ritorna True, il comando può essere eseguito
		'''
        return ctx.author.id in bot.owner_ids

    @commands.command(  # Decorator to declare where a command is.
        name='db_add',  # Name of the command, defaults to function name.
        aliases=['db_agg']  # Aliases for the command.
    )
    async def db_aggiungi(self, ctx, key, value):
        '''
		Aggiunge un campo ad database
		'''
		if(db_utils.contains(key)):
			utils.reply_with_err_msg(ctx, f"esiste già una chiave {key} nel database!\n"
									+"puoi modificare il suo valore con !db_mod")
			return
			
		db_utils.set(key, value)
    


def setup(bot):
    bot.add_cog(DataBaseComands(bot))

