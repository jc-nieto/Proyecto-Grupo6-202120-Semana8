from argon2 import PasswordHasher

ph = PasswordHasher()


def encryptPassword(stringPassword):
    hashPassword = ph.hash(stringPassword)
    print(hashPassword)
    return hashPassword
