import re

import bcrypt

from utils.data_classes import TableRow


def encode_pass(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def check_pass(password: str, db_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), db_password.encode())


def delete_tag(rows: 'TableRow') -> 'TableRow':
    not_empty_tag = r'^<td(.*)>(.+)<\/td>$'
    clear_row = TableRow(
        re.match(not_empty_tag, rows.begin_ip).group(2),
        re.match(not_empty_tag, rows.end_ip).group(2),
        re.match(not_empty_tag, rows.amount).group(2))

    return clear_row


def strtobool(value: str) -> bool | str:
    """
    Convert a string representation of truth to true or false
    True values are 'y', 'yes', 't', 'true', and '1'
    False values are 'n', 'no', 'f', 'false' and '0'
    All other values will be returned
    @param value: input value
    @return: True, False or input value
    """
    value = value.lower()
    if value in ('y', 'yes', 't', 'true', '1'):
        return True
    elif value in ('n', 'no', 'f', 'false', '0'):
        return False

    return value


if __name__ == '__main__':
    ...
