from replit import db

KEY_PART_SEPARATOR = "."


class search_info:
    def __init__(self,
                 key: str,
                 allow_multiple_matches=True,
                 require_complete_key=False) -> None:
        self.original_key = key
        self.key_components = key.split(KEY_PART_SEPARATOR)
        # lista di tuple (chiave, valore)
        self.matches = list()
        self.allow_multiple_matches = allow_multiple_matches
        self.require_complete_key = require_complete_key

        self.partial_match_components = list()
        self.partial_match_depth = 0

    def has_matches(self) -> bool:
        return self.get_n_matches > 0

    def has_multiple_matches(self) -> bool:
        return self.get_n_matches > 1

    def get_n_key_components(self) -> int:
        return len(self.key_components)

    def get_n_matches(self) -> int:
        return len(self.key_matches)

    def get_first_match(self):
        return self.key_matches[0] if self.has_matches() else None


async def find_first(key: str):
    s = await find(key, False)
    return s.get_first_match()


async def find_all(key: str):
    s = await find(key, True)
    return s.key_matches


async def find(key: str, allow_multiple_matches=True) -> search_info:
    s = search_info(key, allow_multiple_matches)
    return await search(s)


async def find_complete(key: str) -> search_info:
    s = search_info(key,
                    allow_multiple_matches=False,
                    require_complete_key=True)

    return search(s)


async def contains(key) -> bool:
    return find_complete(key).has_matches()


async def search(s: search_info, db_level: dict = db):

    # ricerca semplice, richiede la chiave al completo

    if s.require_complete_key:
        for key in s.key_components:
            if key in db_level.keys():
                s.partial_match_depth += 1
                if s.partial_match_depth < s.get_n_key_components():
                    db_level = db_level[key]
                else:

                    s.key_matches.append((db_level[key]))

    # ricerca con abbreviazioni, molto più complesso
    else:
        # la parte della chiave che
        key = s.key_components[s.partial_match_depth]
        for db_key in db_level.keys():
            if db_key.startswith(key):
                s.partial_match_components.append(db_key)
                s.partial_match_depth += 1

                # se non siamo alla profondità desiderata
                if s.partial_match_depth < s.get_n_key_components():
                    # ripetiamo la ricerca a un livello più profondo
                    # NOTA BENE: stiamo chiamando la funzione search, all'interno di essa stessa
                    # questo concetto si chiama ricorsione
                    await search(s, db_level[db_key])
                else:
                    # abbiamo trovato quello che cercavamo
                    s.key_matches.append(db_level[db_key])

                s.partial_match_components.pop()
                s.partial_match_depth -= 1

                # usciamo subito dalla funzione se abbiamo già un risultato
                # e non ne vogliamo oltre
                if s.has_matches() and not s.allow_multiple_matches:
                    return
