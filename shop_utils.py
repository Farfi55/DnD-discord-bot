import re
import db_utils

shop_key = "mercati"

avariable_indicator = "🟢"
unavariable_indicator = "🔴"

item_regex = re.compile("^(.+?)( \((.+)\))?( \((.+), (.+)\))$")


def get_full_item_key(shop_name: str, item_name: str) -> str:
    return db_utils.join_key(shop_key, shop_name, item_name)


def get_shop_items(shop_name: str) -> dict(str, str):
    key = db_utils.join_key(shop_key, shop_name)
    search = db_utils.search_info(key, False, True, True)
    (key, shop_dict) = db_utils.search_full_key(search)

    return shop_dict


def get_shop_items_avariable(shop_name: str) -> list(str):
    avariable_items = list()
    for item_key, item_data in get_shop_items(shop_name):
        if avariable_indicator in item_data:
            item = item_key.removeprefix(f"{shop_key}.{shop_name}.")
            avariable_items.append(item)
    return avariable_items


def get_shop_items_unavariable(shop_name: str) -> list(str):
    unavariable_items = list()
    for item_key, item_data in get_shop_items(shop_name):
        if unavariable_indicator in item_data:
            item = item_key.removeprefix(f"{shop_key}.{shop_name}.")
            unavariable_items.append(item)
    return unavariable_items


def clear_shop_items(shop_name: str):
    full_shop_key = db_utils.join_key(shop_key, shop_name)
    db_utils.set(full_shop_key, {})


def add_shop_items_from_str(shop_name: str, items_raw: str):
    items_list_raw = items_raw.splitlines()

    for item_name in items_list_raw:
        match = item_regex.fullmatch(item_name)
        if match:
            db_utils.set(get_full_item_key(shop_name, item_name),
                         avariable_indicator, True)


def buy_item(shop_name: str, item: str):
    avariable_items = get_shop_items_avariable(shop_name)

    if item in avariable_items:
        db_utils.get()
        return True
    else:
        return False
        # raise ItemNotFound


# class ItemNotFound(Exception):
#     pass
