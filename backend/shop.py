import re
import backend.db as db
import random

shop_key = "mercati"

avariable_indicator = "🟢"
unavariable_indicator = "🔴"

item_regex = re.compile("^(.+?)( \((.+)\))?( \((.+), (.+)\))$")


def get_full_shop_key(ctx, shop_name: str) -> str:
    return db.join_key(ctx, shop_key, shop_name)


def get_full_item_key(ctx, shop_name: str, item_name: str) -> str:
    return db.join_key(ctx, shop_key, shop_name, item_name)


def get_shop_items(ctx, shop_name: str) -> dict():
    key = get_full_shop_key(ctx, shop_key, shop_name)

    search_res = db.find_complete(key)

    if search_res.has_matches():
        # ritorna un dizionario di item - valori
        return search_res.get_first_match()[1]
    else:
        print(f"{key} not found in db")
        return None


def get_random_shop_items(ctx, shop_name: str, n_items: int) -> list():
    item_list = get_shop_items_avariable(ctx, shop_name)
    if item_list == None:
        return None
    random_item_list = random.sample(item_list, n_items)
    return random_item_list


def get_shop_items_avariable(ctx, shop_name: str) -> list():
    avariable_items = list()
    items = get_shop_items(ctx, shop_name)
    if items == None:
        print(f"no items for shop {shop_name}")
        return None
    for item_name in items:
        item_key = get_full_item_key(ctx, shop_name, item_name)
        item_data = db.get(item_key)
        if avariable_indicator in item_data:
            avariable_items.append(item_name)
    return avariable_items


def get_shop_items_unavariable(ctx, shop_name: str) -> list():
    unavariable_items = list()
    items = get_shop_items(ctx, shop_name)
    if items == None:
        print(f"no items for shop {shop_name}")
        return None
    for item_name in items:
        item_key = get_full_item_key(ctx, shop_name, item_name)
        item_data = db.get(item_key)
        if unavariable_indicator in item_data:
            unavariable_items.append(item_name)
    return unavariable_items


def clear_shop_items(ctx, shop_name: str):
    full_shop_key = get_full_shop_key(ctx, shop_name)
    db.set(full_shop_key, {})


def add_shop_items_from_str(ctx, shop_name: str, items_raw: str):
    items_list_raw = items_raw.splitlines()

    for item_name in items_list_raw:
        match = item_regex.fullmatch(item_name)
        if match:
            db.set(get_full_item_key(ctx, shop_name, item_name),
                   avariable_indicator, True)


def buy_item(ctx, shop_name: str, item: str, set_unavariable=True):
    avariable_items = get_shop_items_avariable(ctx, shop_name)

    if item in avariable_items:
        item_key = get_full_item_key(ctx, shop_name, item)
        if set_unavariable:
            db.replace(item_key, avariable_indicator, unavariable_indicator)
        return True
    else:
        return False
