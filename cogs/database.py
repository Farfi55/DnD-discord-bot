from discord.ext import commands
import feedback
import db_utils


class DataBaseCommands(commands.Cog, name='Comandi DataBase'):
    ''''''

    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        '''controllo per i comandi di questa classe, se ritorna True, il comando può essere eseguito'''
        return ctx.author.id == self.bot.author_id or ctx.author.id in self.bot.owner_ids

    @commands.command(  # Decorator to declare where a command is.
        name='db_add',  # Name of the command, defaults to function name.
        aliases=['db_agg']  # Aliases for the command.
    )
    async def db_add(self, ctx, key, value):
        ''' Aggiunge un campo ad database '''
        if db_utils.contains(key):
            await feedback.reply_with_err_msg(
                ctx, f"esiste già una chiave `{key}` nel database!\n" +
                "puoi modificare il suo valore con `!db_mod`")
            return

        if db_utils.set(key, value, create_on_missing=True):
            await feedback.reply_with_success_msg(
                ctx,
                f"aggiunto con successo al database la coppia chiave, valore:\n`{key}`: `{value}`"
            )

    @commands.command(  # Decorator to declare where a command is.
        name='db_add_sub',  # Name of the command, defaults to function name.
        aliases=['db_agg_sub']  # Aliases for the command.
    )
    async def db_add_sub(self, ctx, key):
        ''' Aggiunge una categoria ad database '''
        if db_utils.contains(key):
            await feedback.reply_with_err_msg(
                ctx, f"esiste già una chiave `{key}` nel database!\n" +
                "puoi modificare il suo valore con `!db_mod`")
            return

        if db_utils.set(key, dict(), create_on_missing=True):
            await feedback.reply_with_success_msg(
                ctx,
                f"aggiunto con successo al database la sotto cartella `{key}`")

    @commands.command(name='db_rem', aliases=['db_rim', 'db_del'])
    async def db_remove(self, ctx, key):
        ''' Rimuove un campo dal database '''

        if not db_utils.contains(key):
            await feedback.reply_with_err_msg(
                ctx, f"non esiste nessuna chiave `{key}` nel database!")
            return

        if db_utils.remove(key):
            await feedback.reply_with_success_msg(
                ctx, f"rimosso con successo dal database `{key}`")

    @commands.command(
        name='db_mod',
        # aliases=['db_mod']
    )
    async def db_modify(self, ctx, key, value):
        ''' Modifica il valore di un campo del database '''

        if not db_utils.contains(key):
            await feedback.reply_with_err_msg(
                ctx, f"non esiste nessuna chiave `{key}` nel database!\n" +
                "puoi aggiungere un campo chiave-valore con `!db_add chiave valore`"
            )
            return

        _, old_value = db_utils.get(key)
        if db_utils.set(key, value, create_on_missing=False):
            await feedback.reply_with_success_msg(
                ctx,
                f"modificato con successo il valore di `{key}`,\nda: {old_value}\na: {value}"
            )

    @commands.command(name='db_append', aliases=['db_appendi', "db_app"])
    async def db_append(self, ctx, key, value):
        ''' Appende del testo alla fine di un campo del database '''

        if not db_utils.contains(key):
            await feedback.reply_with_err_msg(
                ctx, f"non esiste nessuna chiave `{key}` nel database!\n" +
                "puoi aggiungere un campo chiave-valore con `!db_add chiave valore`"
            )
            return

        _, old_value = db_utils.get(key)
        new_value = old_value + value
        if db_utils.set(key, new_value, create_on_missing=False):
            await feedback.reply_with_success_msg(
                ctx,
                f"modificato con successo il valore di `{key}`,\nda: {old_value}\na: {new_value}"
            )

    @commands.command(name='db_append_start',
                      aliases=['db_appendi_inizio', "db_app_start"])
    async def db_append_start(self, ctx, key, value):
        ''' Appende del testo all'inizio di un campo del database '''

        if not db_utils.contains(key):
            await feedback.reply_with_err_msg(
                ctx, f"non esiste nessuna chiave `{key}` nel database!\n" +
                "puoi aggiungere un campo chiave-valore con `!db_add chiave valore`"
            )
            return

        _, old_value = db_utils.get(key)
        new_value = value + old_value
        if db_utils.set(key, new_value, create_on_missing=False):
            await feedback.reply_with_success_msg(
                ctx,
                f"modificato con successo il valore di `{key}`,\nda: {old_value}\na: {new_value}"
            )

    @commands.command(name='db_get')
    async def db_get(self, ctx, key):
        ''' Mostra il valore di un campo del database '''

        if not db_utils.contains(key):
            await feedback.reply_with_err_msg(
                ctx, f"non esiste nessuna chiave `{key}` nel database!")
            return

        chiave, valore = db_utils.find_complete(key).get_first_match()
        await feedback.reply_with_success_msg(
            ctx, f"il valore di `{chiave}` è `{valore}`")

    @commands.command(name='db_list')
    async def db_list(self, ctx, key=None):
        ''' Mostra tutti i campi del database accettati dalla chiave (opzionale) '''

        if key is None:
            await feedback.reply_with_msg(
                ctx, f"\n```css\n" + "chiavi : valore\n" + "\n".join([
                    f"{chiave}: {valore}"
                    for chiave, valore in db_utils.get_all()
                ]) + "```")
            return

        await feedback.reply_with_msg(
            ctx, f"\n```css\n" + "chiavi : valore\n" + "\n".join([
                f"{chiave}: {valore}"
                for chiave, valore in db_utils.find_all(key)
            ]) + "```")
        return

    @commands.command(name='db_keys')
    async def db_keys(self, ctx, key=None):
        ''' Mostra tutte le chiavi del database accettate dalla chiave (opzionale) '''

        if key is None:
            await feedback.reply_with_msg(
                ctx, f"```css\n" + "chiavi: \n" +
                "\n".join([chiave
                           for chiave, _ in db_utils.get_all()]) + "```")
            return

        await feedback.reply_with_msg(
            ctx, f"\n```css\n" + "chiavi : valore\n" +
            ",\t".join([chiave
                        for chiave, _ in db_utils.find_all(key)]) + "```")
        return


def setup(bot):
    bot.add_cog(DataBaseCommands(bot))
