import pyotp

mock_hotp = pyotp.HOTP('s')

print(mock_hotp.digits)