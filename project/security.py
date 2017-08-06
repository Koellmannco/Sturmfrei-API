#
# import the CryptContext class, used to handle all hashing...
#
from passlib.context import CryptContext
import binascii
import os

#
# create a single global instance for your app...
#
pwd_context = CryptContext(
    # Replace this list with the hash(es) you wish to support.
    # this example sets pbkdf2_sha256 as the default,
    # with additional support for reading legacy des_crypt hashes.
    schemes=["bcrypt_sha256","bcrypt"],

    # Automatically mark all but first hasher in list as deprecated.
    # (this will be the default in Passlib 2.0)
    deprecated="auto",

    # Optionally, set the number of rounds that should be used.
    # Appropriate values may vary for different schemes,
    # and the amount of time you wish it to take.
    # Leaving this alone is usually safe, and will use passlib's defaults.
    # can be btw 4 and 31, is logarithmic
     bcrypt_sha256__rounds = 12,
    )


def generate_salt():
    return binascii.hexlify(os.urandom(11)).decode()
