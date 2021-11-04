"""
    When executed, this will generate 5 random valid pins for 2FA
"""
import pyotp
for i in range(5):
    print(pyotp.random_base32())