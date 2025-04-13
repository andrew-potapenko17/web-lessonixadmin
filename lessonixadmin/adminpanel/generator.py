import string, random

def unic(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))