from argon2 import PasswordHasher

ph = PasswordHasher()


def checkPassword(hashed, stringPassword):
    if ph.verify(hashed, stringPassword):
        return True
    else:
        return False
