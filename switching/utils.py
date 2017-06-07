from switching import defs


def get_description(code, table_name):
    table = getattr(defs, table_name, None)
    if not table:
        raise ValueError(
            "The table with the name '{}' doesn't exist".format(table_name)
        )
    res = dict(table).get(code, None)
    if not res:
        raise ValueError(
            "The key '{}' in the table '{}' doesn't exist".format(
                code, table_name
            )
        )
    return res
