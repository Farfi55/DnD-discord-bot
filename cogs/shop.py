
# richieste

# livelli custom di mercato
# caricare lista di oggetti da messaggio
# inviare lista di oggetti in privato
# modo per vedere gli oggetti di un mercato
# comprare oggetti e segnarli come acquistati
# feedback

# 🟢 indica disponibile
# 🔴 indica acquistato

from inspect import CO_OPTIMIZED
from discord.ext import commands
import shop_utils
import db_utils
import utils


class ShopCommands(commands.Cog, name='Comandi mercati'):
    ''''''

    lvl1 = "lvl1"
    lvl2 = "lvl2"
    lvl3 = "lvl3"

    breacher = "breacher"
    extra1 = "EXTRA 1"
    extra2 = "EXTRA 2"

    lvl1_markets = [lvl1, breacher, extra1, extra2]
    lvl2_markets = [lvl2, *lvl1_markets]
    lvl3_markets = [lvl3, *lvl2_markets]

    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        '''controllo per i comandi di questa classe, se ritorna True, il comando può essere eseguito'''
        return ctx.author.id == self.bot.author_id or ctx.author.id in self.bot.owner_ids

    @commands.command(name="lvl1")
    async def get_lvl1_shop_items(self, ctx):
        await self.get_shop_items(ctx, self.lvl1)

    @commands.command(name="lvl2")
    async def get_lvl2_shop_items(self, ctx):
        await self.get_shop_items(ctx, self.lvl2)

    @commands.command(name="lvl3")
    async def get_lvl3_shop_items(self, ctx):
        await self.get_shop_items(ctx, self.lvl3)

    @commands.command(name="breacher")
    async def get_breacher_shop_items(self, ctx):
        await self.get_shop_items(ctx, self.breacher)

    @commands.command(
        name='mercato',
    )
    async def get_shop_items(self, ctx, shop_name):
        '''
        Manda in privato la lista degli oggetti nel mercato
        '''

        if(not await self.authorize_shop_access(ctx, shop_name)):
            return

        shop_items = await self.bot.db.get_shop_items(shop_name)
        if not shop_items:
            await utils.reply_with_err_msg(
                ctx, f"il mercato `{shop_name}` non esiste!")
            return
        return shop_items

    async def authorize_shop_access(self, ctx, shop_name) -> bool:
        full_user_key = db_utils.join_key("users", ctx.author.id, "shop_lvl")
        user_lvl = db_utils.get(full_user_key)

        if user_lvl == None:
            await utils.reply_with_err_msg(ctx, f"non sei registrato a nessun livello!")
            return False
        if user_lvl == self.lvl1 and shop_name in self.lvl1_markets:
            return True
        elif user_lvl == self.lvl2 and shop_name in self.lvl2_markets:
            return True
        elif user_lvl == self.lvl3 and shop_name in self.lvl3_markets:
            return True
        else:
            await utils.reply_with_err_msg(
                ctx, f"non hai accesso al mercato `{shop_name}`!")
            return False


def setup(bot):
    bot.add_cog(ShopCommands(bot))
