import hashlib
from pathlib import Path


def create_password(password, username, loc='data/'):
    """
    create a hashed password

    Parameters
    ----------
    password : str
    username : str
    loc : str, default = 'data/'
        location where the hashed password is saved on the server.
    """
    location = get_location(username, loc)
    with open(location, 'wb') as f:
        f.write(hashlib.sha256(password.encode()).digest())


def get_hashed_password(username, loc='data/'):
    location = get_location(username, loc)
    if Path(location).is_file():
        with open(location, 'rb') as f:
            data = f.read()
        return data
    else:
        return None


def get_location(username, loc):
    return str(Path(loc) / str(username + '.dat'))
