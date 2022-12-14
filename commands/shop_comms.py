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

from discord.ext import commands
from discord import Embed
import backend.shop as shop
import backend.db as db
import backend.feedback as feedback

lvl1 = "lvl1"
lvl2 = "lvl2"
lvl3 = "lvl3"

breacher = "breacher"
commom_chest = "common_chest"
uncommon_chest = "uncommon_chest"
rare_chest = "rare_chest"
common_uncommon_chest = "common_uncommon_chest"
common_uncommon_rare_chest = "common_uncommon_rare_chest"

lvl1_shops = [lvl1, breacher, commom_chest, uncommon_chest, rare_chest]
lvl2_shops = [lvl2, *lvl1_shops]
lvl3_shops = [lvl3, *lvl2_shops]

unavaliable_on_buy_shops = [lvl1, lvl2, lvl3]


class ShopCommands(commands.Cog, name='Comandi mercati'):
    ''''''
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        '''controllo per i comandi di questa classe, se ritorna True, il comando può essere eseguito'''
        return True

    @commands.command(name="lvl1")
    async def get_lvl1_shop_items(self, ctx):
        await self.get_shop_items(ctx, lvl1)

    @commands.command(name="lvl2")
    async def get_lvl2_shop_items(self, ctx):
        await self.get_shop_items(ctx, lvl2)

    @commands.command(name="lvl3")
    async def get_lvl3_shop_items(self, ctx):
        await self.get_shop_items(ctx, lvl3)

    @commands.command(name="breacher")
    async def get_breacher_shop_items(self, ctx):
        """Gli oggetti possono essere acquistati solo 1 volta ma è possibile che più giocatori acquistino lo stesso oggetto. Il sito di riferimento per molti degli oggetti è https://www.dandwiki.com/wiki/5e_Cursed_Items"""

        random_items = shop.get_random_shop_items(ctx, "breacher", 10)
        if random_items == None:
            await feedback.reply_with_err_msg(
                ctx, f"non è stato possibile prendere gli item dal breacher")
            return
        descrizione = "descrizione\n"
        e = Embed(title="Items del breacher", description=descrizione)
        for i, item in enumerate(random_items, start=1):
            e.add_field(name=f"item {i}", value=f"{item}", inline=False)
        e.set_image(url="https://i.imgur.com/dDfL29o.jpeg")

        await feedback.reply_with_embed_msg(ctx, e)

    @commands.command(name="common_chest", alias=["ComChest"])
    async def get_common_chest_items(self, ctx):
        random_items = shop.get_random_shop_items(ctx, "common_chest", 3)
        if random_items == None:
            await feedback.reply_with_err_msg(
                ctx,
                f"non è stato possibile prendere gli item dalla cassa comune")
            return

        msg = "Items della cassa comune\n```css\n"
        msg += "\n".join(
            [f"{i+1}: {item}" for i, item in enumerate(random_items)])
        msg += "\n```"
        await feedback.reply_with_success_msg(ctx, msg)

    @commands.command(name="uncommon_chest", alias=["UncChest"])
    async def get_uncommon_chest_items(self, ctx):
        random_items = shop.get_random_shop_items(ctx, "uncommon_chest", 1)
        random_items += shop.get_random_shop_items(ctx,
                                                   "common_uncommon_chest", 1)
        if random_items == None:
            await feedback.reply_with_err_msg(
                ctx,
                f"non è stato possibile prendere gli item dalla cassa non comune"
            )
            return

        msg = "Items dalla cassa non comune\n```css\n"
        msg += "\n".join(
            [f"{i}: {item}" for i, item in enumerate(random_items, start=1)])
        msg += "\n```"
        await feedback.reply_with_success_msg(ctx, msg)

    @commands.command(name="rare_chest", alias=["RarChest"])
    async def get_rare_chest_items(self, ctx):
        random_items = shop.get_random_shop_items(ctx, "rare_chest", 1)
        random_items += shop.get_random_shop_items(
            ctx, "common_uncommon_rare_chest", 1)
        if random_items == None:
            await feedback.reply_with_err_msg(
                ctx,
                f"non è stato possibile prendere gli item dalla cassa rara")
            return

        msg = "Items della cassa rara\n```css\n"
        msg += "\n".join(
            [f"{i}: {item}" for i, item in enumerate(random_items, start=1)])
        msg += "\n```"
        await feedback.reply_with_success_msg(ctx, msg)

    @commands.command(name="mercato", alias=["shop", "market"])
    async def get_shop_items(self, ctx, shop_name):
        '''
        Manda in privato la lista degli oggetti nel mercato
        '''

        if (not await self.authorize_shop_access(ctx, shop_name)):
            return

        shop_items_avariable = shop.get_shop_items_avariable(ctx, shop_name)
        if shop_items_avariable == None:
            await feedback.reply_with_err_msg(
                ctx, f"il mercato {shop_name} non esiste")
            return
        shop_items_unavariable = shop.get_shop_items_unavariable(
            ctx, shop_name)

        msg = f"oggetti disponibili del mercato {shop_name}:\n```css\n"
        msg += "\n".join(shop_items_avariable)
        msg += "```"

        if len(shop_items_unavariable) > 0:
            msg += f"\noggetti non disponibili del mercato {shop_name}:\n```css\n"
            msg += "\n".join(shop_items_unavariable)
            msg += "```"

        await feedback.private_reply_with_success_msg(ctx, msg)
        await feedback.reply_with_success_msg(
            ctx, "lista degli item inviata nei messaggi privati")

    async def authorize_shop_access(self, ctx, shop_name) -> bool:
        full_user_key = db.join_key(ctx, "utenti", str(ctx.author.id),
                                    "shop_lvl")

        user_shop_lvl = db.get_value(full_user_key)
        print(user_shop_lvl)

        if user_shop_lvl == None:
            await feedback.reply_with_err_msg(
                ctx, f"non sei registrato a nessun livello!")
            return False
        if user_shop_lvl == lvl1 and shop_name in lvl1_shops:
            return True
        elif user_shop_lvl == lvl2 and shop_name in lvl2_shops:
            return True
        elif user_shop_lvl == lvl3 and shop_name in lvl3_shops:
            return True
        else:
            await feedback.reply_with_err_msg(
                ctx, f"non hai accesso al mercato `{shop_name}`!")
            return False

    @commands.command(name="imposta_casa")
    async def set_user_shop_lvl(self, ctx, shop_lvl):
        full_user_key = db.join_key(ctx, "utenti", str(ctx.author.id),
                                    "shop_lvl")
        if db.set(full_user_key, shop_lvl, True):
            await feedback.reply_with_success_msg(
                ctx, f"Ora {ctx.author} vive a {shop_lvl}")
        else:
            await feedback.reply_with_err_msg(
                ctx,
                f"non è stato possibile impostare il livello di {ctx.author}")

    @commands.command(name="rimpiazza", alias=["replace"])
    async def set_shop_items(self, ctx, shop_name, items):
        """Usami per sostituire gli oggetti """
        shop.clear_shop_items(ctx, shop_name)
        shop.add_shop_items_from_str(ctx, shop_name, items)
        await feedback.reply_with_success_msg(
            ctx, f"oggetti del mercato {shop_name} aggiornati")

    @commands.command(name="aggiungi", alias=["add_items"])
    async def add_shop_items(self, ctx, shop_name, items):
        """Usami se gli oggetti occupano più caratteri del previsto"""
        shop.add_shop_items_from_str(ctx, shop_name, items)
        await feedback.reply_with_success_msg(
            ctx, f"oggetti del mercato {shop_name} aggiornati")

    @commands.command(name="compra", alias=["buy"])
    async def buy_item(self, ctx, shop_name, item_name):
        set_unavailable = shop_name in unavaliable_on_buy_shops

        if (shop.buy_item(ctx, shop_name, item_name, set_unavailable)):
            await feedback.reply_with_success_msg(
                ctx, f"{ctx.author} ha comprato {item_name} da {shop_name}!")

            shop_channel_id = db.get_value(
                db.join_key(ctx, "canali", "mercato"))

            if (shop_channel_id != None):
                shop_channel = self.bot.get_channel(int(shop_channel_id))
                await feedback.reply_with_msg(
                    ctx,
                    f"{ctx.author} ha comprato {item_name} da {shop_name}!",
                    channel=shop_channel)
            else:
                await feedback.reply_with_info_msg(
                    ctx,
                    f"usa `{ctx.prefix}imposta_canale_mercato` per impostare il canale del mercato"
                )
        else:
            await feedback.reply_with_err_msg(
                ctx,
                f"{item_name} non è presente dentro {shop_name} o non è disponibile"
            )

    @commands.command(name="imposta_canale_mercato")
    async def set_shop_channel(self, ctx):
        channel_key = db.join_key(ctx, "canali", "mercato")

        print(ctx.channel, ctx.channel.id)
        id_channel = str(ctx.channel.id)
        if db.set(channel_key, id_channel, True):
            await feedback.reply_with_success_msg(
                ctx, f"il canale {ctx.channel} è ora il canale di mercato")
        else:
            await feedback.reply_with_err_msg(
                ctx, f"non è stato possibile impostare il canale di mercato")


async def setup(bot):
    await bot.add_cog(ShopCommands(bot))
