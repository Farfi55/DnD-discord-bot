from replit import db

KEY_PART_SEPARATOR = "."


def split_key(key: str) -> list():
    return key.split(sep=KEY_PART_SEPARATOR)


def join_key(ctx, *key_parts) -> str:
    if key_parts == (None, ):
        return str(ctx.guild.id)
    else:
        key_parts = [str(ctx.guild.id), *key_parts]
        key = KEY_PART_SEPARATOR.join(key_parts)
        print(key)
        return key


class search_info:
    def __init__(self,
                 key: str,
                 allow_multiple_matches=True,
                 require_complete_key=False,
                 create_on_missing=False) -> None:
        self.original_key = key
        self.key_components = split_key(key)
        # lista di tuple (chiave, valore)
        self.matches = list()

        self.allow_multiple_matches = allow_multiple_matches
        self.require_complete_key = require_complete_key
        self.create_on_missing = create_on_missing

        self.partial_match_components = list()
        self.partial_match_depth = 0

    def has_matches(self) -> bool:
        return self.get_n_matches() > 0

    def has_multiple_matches(self) -> bool:
        return self.get_n_matches() > 1

    def get_n_key_components(self) -> int:
        return len(self.key_components)

    def get_n_matches(self) -> int:
        return len(self.matches)

    def get_first_match(self):
        return self.matches[0] if self.has_matches() else None

    def get_partial_key_str(self) -> str:
        return KEY_PART_SEPARATOR.join(self.partial_match_components)


def find_first(key: str):
    """returns tuple (key, value) or None"""

    s = find(key, False)
    return s.get_first_match()


def find_all(key: str):
    """returns list of tuples (key, value)"""

    s = find(key, True)
    return s.matches


def find(key: str, allow_multiple_matches=True) -> search_info:
    s = search_info(key=key,
                    allow_multiple_matches=allow_multiple_matches,
                    require_complete_key=False)
    search(s)
    return s


def find_complete(key: str) -> search_info:
    s = search_info(key=key,
                    allow_multiple_matches=False,
                    require_complete_key=True)

    search(s)
    return s


def get_all(key=None):
    if key is None:
        return db.items()
    return find_all(key + KEY_PART_SEPARATOR)


def get(full_key):
    s = search_info(full_key,
                    allow_multiple_matches=False,
                    require_complete_key=True,
                    create_on_missing=False)
    search(s)
    return s.get_first_match()


def get_value(full_key):
    res = get(full_key)
    return None if res is None else res[1]


def contains(full_key) -> bool:
    return find_complete(full_key).has_matches()


def search(s: search_info, db_level: dict = db):
    if s.partial_match_components:
        search_prefix_key(s, db_level)
    else:
        search_full_key(s, db_level)


def search_full_key(s: search_info, db_level: dict = db):
    """
    ricerca semplice, richiede la chiave al completo
    """

    for key in s.key_components:
        if key not in db_level.keys():
            if s.create_on_missing:
                db_level[key] = {}
            else:
                return

        s.partial_match_depth += 1
        if s.partial_match_depth < s.get_n_key_components():
            db_level = db_level[key]
        else:
            s.matches.append((s.original_key, db_level[key]))


def search_prefix_key(s: search_info, db_level: dict = db):
    """ricerca con abbreviazioni, molto più complesso"""

    # la parte della chiave che dobbiamo cercare questa iterazione
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
                search(s, db_level[db_key])
            else:
                # abbiamo trovato quello che cercavamo
                s.matches.append((s.get_partial_key_str(), db_level[db_key]))

            s.partial_match_components.pop()
            s.partial_match_depth -= 1

            # usciamo subito dalla funzione se abbiamo già un risultato
            # e non ne vogliamo oltre
            if s.has_matches() and not s.allow_multiple_matches:
                return


def add(full_key, value):
    set(full_key, value, True)


def replace(full_key, to_replace: str, replace_with: str):

    val = str(get_value(full_key))
    val.replace(to_replace, replace_with)
    set(full_key, val)


def set(full_key, value, create_on_missing=False):

    db_level = db
    key_components = split_key(full_key)

    assert len(key_components) > 0, "la chiave non può essere vuota"

    for depth, full_key in enumerate(key_components):
        if full_key not in db_level.keys():
            if create_on_missing:
                if depth == len(key_components) - 1:
                    db_level[full_key] = value
                else:
                    db_level[full_key] = {}
                    db_level = db_level[full_key]
            else:
                return False
        else:
            if depth == len(key_components) - 1:
                db_level[full_key] = value
            else:
                db_level = db_level[full_key]
    return True


def remove(full_key):
    db_level = db
    key_components = split_key(full_key)

    assert len(key_components) > 0, "la chiave non può essere vuota"

    for depth, key in enumerate(key_components):
        if key not in db_level.keys():
            return False
        else:
            if depth == len(key_components) - 1:
                del db_level[key]
            else:
                db_level = db_level[key]
    return True


def move(full_key, new_full_key):
    val = get_value(full_key)
    if val is None:
        return False
    elif not set(new_full_key, val):
        return False
    elif not remove(full_key):
        return False
    else:
        return True
