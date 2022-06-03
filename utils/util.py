import bcrypt


def encode_pass(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def check_pass(password: str, db_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), db_password.encode())


def strtobool(value: str) -> int:
    """
    Convert a string representation of truth to true (1) or false (0)
    True values are 'y', 'yes', 't', 'true', 'on', and '1'
    False values are all other arguments
    :param value:
    :return: 1 or 0

    """
    value = value.lower()
    if value in ('y', 'yes', 't', 'true', '1'):
        return 1
    else:
        return 0


if __name__ == '__main__':
    ...
