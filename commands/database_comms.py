from discord.ext import commands
import backend.feedback as feedback
import backend.db as db


class DataBaseCommands(commands.Cog, name='Comandi DataBase'):
    ''''''
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        '''controllo per i comandi di questa classe, se ritorna True, il comando può essere eseguito'''
        return ctx.author.id == self.bot.author_id or ctx.author.id in self.bot.owner_ids

    @commands.command(name="db_agg", aliases=["db_add"])
    async def db_add(self, ctx, key, value):
        ''' Aggiunge un campo ad database '''
        key = db.join_key(ctx, key)
        if db.contains(key):
            await feedback.reply_with_err_msg(
                ctx, f"esiste già una chiave `{key}` nel database!\n" +
                "puoi modificare il suo valore con `!db_mod`")
            return
        elif db.set(key, value, create_on_missing=True):
            await feedback.reply_with_success_msg(
                ctx,
                f"aggiunto con successo al database la coppia chiave, valore:\n`{key}`: `{value}`"
            )

    @commands.command(name='db_agg_sub', aliases=['db_add_sub'])
    async def db_add_sub(self, ctx, key):
        ''' Aggiunge una categoria ad database '''
        key = db.join_key(ctx, key)
        if db.contains(key):
            await feedback.reply_with_err_msg(
                ctx, f"esiste già una chiave `{key}` nel database!\n" +
                "puoi modificare il suo valore con `!db_mod`")
            return

        if db.set(key, dict(), create_on_missing=True):
            await feedback.reply_with_success_msg(
                ctx,
                f"aggiunto con successo al database la sotto cartella `{key}`")

    @commands.command(name='db_rim', aliases=['db_rem', 'db_del'])
    async def db_remove(self, ctx, key):
        ''' Rimuove un campo dal database '''
        key = db.join_key(ctx, key)
        if not db.contains(key):
            await feedback.reply_with_err_msg(
                ctx, f"non esiste nessuna chiave `{key}` nel database!")
        elif db.remove(key):
            await feedback.reply_with_success_msg(
                ctx, f"rimosso con successo dal database `{key}`")

    @commands.command(
        name='db_mod',
        # aliases=['db_mod']
    )
    async def db_modify(self, ctx, key, value):
        ''' Modifica il valore di un campo del database '''
        key = db.join_key(ctx, key)

        if not db.contains(key):
            await feedback.reply_with_err_msg(
                ctx, f"non esiste nessuna chiave `{key}` nel database!\n" +
                "puoi aggiungere un campo chiave-valore con `!db_add chiave valore`"
            )
            return

        _, old_value = db.get(key)
        if db.set(key, value, create_on_missing=False):
            await feedback.reply_with_success_msg(
                ctx,
                f"modificato con successo il valore di `{key}`,\nda: {old_value}\na: {value}"
            )

    @commands.command(name='db_append', aliases=['db_appendi', "db_app"])
    async def db_append(self, ctx, key, value):
        ''' Appende del testo alla fine di un campo del database '''

        key = db.join_key(ctx, key)
        if not db.contains(key):
            await feedback.reply_with_err_msg(
                ctx, f"non esiste nessuna chiave `{key}` nel database!\n" +
                "puoi aggiungere un campo chiave-valore con `!db_add chiave valore`"
            )
            return

        _, old_value = db.get(key)
        new_value = old_value + value
        if db.set(key, new_value, create_on_missing=False):
            await feedback.reply_with_success_msg(
                ctx,
                f"modificato con successo il valore di `{key}`,\nda: {old_value}\na: {new_value}"
            )

    @commands.command(name='db_append_start',
                      aliases=['db_appendi_inizio', "db_app_start"])
    async def db_append_start(self, ctx, key, value):
        ''' Appende del testo all'inizio di un campo del database '''

        key = db.join_key(ctx, key)
        if not db.contains(key):
            await feedback.reply_with_err_msg(
                ctx, f"non esiste nessuna chiave `{key}` nel database!\n" +
                "puoi aggiungere un campo chiave-valore con `!db_add chiave valore`"
            )
            return

        _, old_value = db.get(key)
        new_value = value + old_value
        if db.set(key, new_value, create_on_missing=False):
            await feedback.reply_with_success_msg(
                ctx,
                f"modificato con successo il valore di `{key}`,\nda: {old_value}\na: {new_value}"
            )

    @commands.command(name='db_get')
    async def db_get(self, ctx, key=None):
        ''' Mostra il valore di un campo del database '''
        key = db.join_key(ctx, key)

        if not db.contains(key):
            await feedback.reply_with_err_msg(
                ctx, f"non esiste nessuna chiave `{key}` nel database!")
            return

        valore = db.get_value(key)
        msg = "```css\n"
        msg += f"-- chiave: {key}\n"
        msg += f"-- valore: {valore}\n"
        msg += "```"

        await feedback.reply_with_success_msg(ctx, msg)

    @commands.command(name='db_list')
    async def db_list(self, ctx, key=None):
        ''' Mostra tutti i campi del database accettati dalla chiave (opzionale) '''

        key = db.join_key(ctx, key)

        msg = "chiavi : tipo(valore)\n```css\n"
        list_res = db.get_all(key)

        msg += "\n".join(
            [f"{chiave}: {type(valore)}" for chiave, valore in list_res])
        msg += "```"

        await feedback.reply_with_msg(ctx, msg)

    @commands.command(name='db_keys')
    async def db_keys(self, ctx, key=None):
        ''' Mostra tutte le chiavi del database accettate dalla chiave (opzionale) '''
        key = db.join_key(ctx, key)

        list_res = db.get_all(key)

        msg = "chiavi\n```css\n"
        if len(list_res) > 0:
            msg += "\n".join([k for k, v in list_res])
        else:
            msg += "nessuna chiave trovata"
        msg += "\n```"

        await feedback.reply_with_msg(ctx, msg)

    @commands.command(name='db_move')
    async def db_move(self, ctx, key_from, key_to):
        ''' Sposta un campo o una intera categoria del database '''

        key_from = db.join_key(ctx, key_from)
        key_to = db.join_key(ctx, key_to)

        if not db.contains(key_from):
            await feedback.reply_with_err_msg(
                ctx, f"non esiste nessuna chiave `{key_from}` nel database!")
            return

        if db.contains(key_to):
            await feedback.reply_with_err_msg(
                ctx,
                f"esiste già un campo `{key_to}` nel database!, usa `!db_remove {key_to}` per rimuoverlo"
            )
            return

        if db.move(key_from, key_to):
            await feedback.reply_with_success_msg(
                ctx,
                f"spostato con successo il campo `{key_from}` in `{key_to}`")
        else:
            await feedback.reply_with_err_msg(
                ctx,
                f"non è stato possibile spostare il campo `{key_from}` in `{key_to}`"
            )


async def setup(bot):
    await bot.add_cog(DataBaseCommands(bot))
