import hashlib

test = ("client").encode()
print(hashlib.sha256(test).hexdigest())

test = ("server").encode()
print(hashlib.sha256(test).hexdigest())