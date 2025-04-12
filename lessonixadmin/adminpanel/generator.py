import string, random

def unic(k=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k))