async def autentifica(messaggio):
    id_nico = 219921156591976450
    id_edo = 418443872335560714
    id_farfi = 185258590901239808
    return messaggio.author.id in [id_nico, id_edo, id_farfi]
