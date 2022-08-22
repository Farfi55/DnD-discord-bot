from random import randint
import discord

err_msg_prefix = "🔴 errore: "
warn_msg_prefix = "🟠 attenzione: "
info_msg_prefix = "🔵 info: "
success_msg_prefix = "🟢 successo: "


async def reply_with_msg(ctx, message):
    await ctx.send(message)


async def private_reply_with_msg(ctx, message):
    await ctx.author.send(message)


# PUBLIC MESSAGES SHORTCUTS


async def reply_with_err_msg(ctx, message):
    await reply_with_msg(ctx, err_msg_prefix + message)


async def reply_with_warn_msg(ctx, message):
    await reply_with_msg(ctx, warn_msg_prefix + message)


async def reply_with_info_msg(ctx, message):
    await reply_with_msg(ctx, info_msg_prefix + message)


async def reply_with_success_msg(ctx, message):
    await reply_with_msg(ctx, success_msg_prefix + message)


# PRIVATE MESSAGES SHORTCUTS


async def private_reply_with_err_msg(ctx, message):
    await private_reply_with_msg(ctx, err_msg_prefix + message)


async def private_reply_with_warn_msg(ctx, message):
    await private_reply_with_msg(ctx, warn_msg_prefix + message)


async def private_reply_with_info_msg(ctx, message):
    await private_reply_with_msg(ctx, info_msg_prefix + message)


async def private_reply_with_success_msg(ctx, message):
    await private_reply_with_msg(ctx, success_msg_prefix + message)
