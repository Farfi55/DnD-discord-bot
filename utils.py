from random import randint
import discord


def d(facce=6, volte=1):
    val = 0
    for _ in range(volte):
        val += randint(1, facce)
    return val


async def reply_with_msg(ctx, message):
    ctx.reply(content=message)


async def reply_with_err_msg(ctx, message):
    await reply_with_msg(ctx, "🔴 errore: " + message)


async def reply_with_warn_msg(ctx, message):
    await reply_with_msg(ctx, "🟠 attenzione: " + message)


async def reply_with_info_msg(ctx, message):
    await reply_with_msg(ctx, "🔵 info: " + message)


