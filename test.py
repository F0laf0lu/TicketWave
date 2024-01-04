import random
import pyotp
import time

i = random.randint(0,1000000)

hotp = pyotp.HOTP(pyotp.random_base32())
secret_key = hotp.secret
hotp_code = hotp.at(i)

key = str(i) + '-' + secret_key
print(key)
print(hotp_code)

submitted_code = hotp_code
hotp = pyotp.HOTP(secret_key)

print(hotp.verify(submitted_code, i))
i, secret_key = key.split("-")

print(type(i), type(secret_key))