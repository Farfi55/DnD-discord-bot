
# richieste


# DA FARE

# DA CONTROLLARE

# comprare oggetti e segnarli come acquistati
# feedback
# modo per vedere gli oggetti di un mercato
# inviare lista di oggetti in privato
# livelli di mercato
# caricare lista di oggetti da messaggio

# FATTO

# 🟢 indica disponibile
# 🔴 indica acquistato

from ast import alias
from inspect import CO_OPTIMIZED
from discord.ext import commands
import shop_utils
import db_utils
import feedback


class ShopCommands(commands.Cog, name='Comandi mercati'):
    ''''''

    lvl1 = "lvl1"
    lvl2 = "lvl2"
    lvl3 = "lvl3"

    breacher = "breacher"
    extra1 = "EXTRA 1"
    extra2 = "EXTRA 2"

    lvl1_shops = [lvl1, breacher, extra1, extra2]
    lvl2_shops = [lvl2, *lvl1_shops]
    lvl3_shops = [lvl3, *lvl2_shops]

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
        name="mercato",
        alias=["shop", "market"]
    )
    async def get_shop_items(self, ctx, shop_name):
        '''
        Manda in privato la lista degli oggetti nel mercato
        '''

        if(not await self.authorize_shop_access(ctx, shop_name)):
            return

        shop_items = await shop_utils.get_shop_items(shop_name)
        if not shop_items:
            await feedback.reply_with_err_msg(
                ctx, f"il mercato {shop_name} non esiste!")
            return

        msg = f"oggetti del mercato {shop_name}:\n"
        msg += "\n".join(shop_items)

        await feedback.private_reply_with_success_msg(ctx, msg, self.bot)
        await feedback.reply_with_success_msg(ctx, "lista degli item inviata nei messaggi privati")

    async def authorize_shop_access(self, ctx, shop_name) -> bool:
        full_user_key = db_utils.join_key("users", ctx.author.id, "shop_lvl")
        user_shop_lvl = db_utils.get(full_user_key)

        if user_shop_lvl == None:
            await feedback.reply_with_err_msg(ctx, f"non sei registrato a nessun livello!")
            return False
        if user_shop_lvl == self.lvl1 and shop_name in self.lvl1_shops:
            return True
        elif user_shop_lvl == self.lvl2 and shop_name in self.lvl2_shops:
            return True
        elif user_shop_lvl == self.lvl3 and shop_name in self.lvl3_shops:
            return True
        else:
            await feedback.reply_with_err_msg(
                ctx, f"non hai accesso al mercato `{shop_name}`!")
            return False

    @commands.command(name="imposta_casa")
    def set_user_shop_lvl(self, ctx, shop_lvl):
        full_user_key = db_utils.join_key("users", ctx.author.id, "shop_lvl")
        db_utils.set(full_user_key, shop_lvl)

    @commands.command(name="rimpiazza", alias=["replace"])
    def set_shop_items(self, ctx, shop_name, items):
        shop_utils.clear_shop_items(shop_name)
        shop_utils.add_shop_items_from_str(shop_name, items)

    @commands.command(name="compra", alias=["buy"])
    def buy_item(self, ctx, shop_name, item_name):
        if(shop_utils.buy_item(shop_name, item_name)):
            feedback.reply_with_success_msg(
                f"Hai comprato {item_name} da {shop_name}!")
        else:
            feedback.reply_with_err_msg(
                ctx, f"{item_name} non è presente dentro {shop_name} o non è disponibile")


def setup(bot):
    bot.add_cog(ShopCommands(bot))
