import pyotp

secret = pyotp.random_base32()
print(f"Secret key: {secret}")