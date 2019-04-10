import hashlib
import datetime


def unique_id(length=8):
    s = str(datetime.datetime.now())
    salt = hashlib.sha1(s.encode('utf-8')).hexdigest()[:5]
    return hashlib.sha1(salt.encode('utf-8')).hexdigest()[:length]
