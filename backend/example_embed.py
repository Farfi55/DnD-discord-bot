from turtle import title
from discord import Embed

e = Embed(title="nessun titolo",
          description="nessuna descrizione",
          color=0x00ff00)

e.add_field(name="nome campo", value="valore campo", inline=False)
e.clear_fields()  # elimina tutti i campi
e.set_author(name="nome autore", url="https://www.google.com",
             icon_url="https://www.google.com/favicon.ico")
e.set_footer(text="testo footer",
             icon_url="https://www.google.com/favicon.ico")
e.set_image(url="https://www.google.com/favicon.ico")
e.set_thumbnail(url="https://www.google.com/favicon.ico")


async def send(ctx):
    await ctx.send(embed=e)


# title: str
#     The title of the embed. This can be set during initialisation.
# type: str
#     The type of embed. Usually "rich". This can be set during initialisation. Possible strings for embed types can be found on discord's
# description: str
#     The description of the embed. This can be set during initialisation.
# url: str
#     The URL of the embed. This can be set during initialisation.
# timestamp: datetime.datetime
#     The timestamp of the embed content. This could be a naive or aware datetime.
# colour: Union[Colour, int]
#     The colour code of the embed. Aliased to color as well. This can be set during initialisation.
