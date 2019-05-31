import hashlib
import random
import string
from datetime import datetime

from django.utils import timezone


def random_key(size=5):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for x in range(size))


def generate_hash_key(salt, random_str_size=5):
    random_str = random_key(random_str_size)
    text = random_str + salt
    return hashlib.sha224(text.encode('utf-8')).hexdigest()


def days_from_date(date):
    if not isinstance(date, datetime):
        raise TypeError('"Date" must be a datetime type.')
    return (timezone.now() - date).days
