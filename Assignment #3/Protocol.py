# Raymundo Romero Arenas
# ID = 2369764
# Network Security & Cryptography
# Teacher = Pascal Berrang

import hashlib
from datetime import date, timedelta
from binascii import unhexlify

# Known data
ciphertext = 'a75da6155e61662665dfdec2264097b460cea3eb09c84461b5f728d9b0058361'
plaintext = b'Our secret PIN code is: XXXX....'
IV = 15304484387517434811 

# Byte XOR operation (1)
def byte_xor(ba1, ba2): 
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

def crack(IV, c):
    # Transform IV to bytes
    byteIV = IV.to_bytes(8, "big")

    # Generate a list from a range of dates to concatenate to the IV (2)
    list_date = []                      # List of dates
    start_date = date(2000, 1, 1)       # Starting date
    end_date = date(2021, 12, 31)       # Ending date
    delta = end_date - start_date       
    for day in range(delta.days + 1):   # Insert each date into the list
        a_date = (start_date + timedelta(days=day)).isoformat()
        list_date.append(a_date)

    # Retrieve the message by brute force (try all possible dates from the list of dates)
    for day in list_date:
        # Encode the date in ASCII
        ascii_date = day.encode('ascii')

        # Concatenate the IV and date
        s = byteIV + ascii_date
        
        # Hash the concatenated bytes
        hash_s = hashlib.sha256(s).digest()

        # XOR the ciphertext and hash
        m = byte_xor(unhexlify(c), hash_s)

        # If the message contains the plaintext known data, then it is the correct one
        # Print the date Alice and Bob first met
        # Print the message with the PIN number
        if m[:23] == b'Our secret PIN code is:':
            print("Date = {}".format(day))
            print("Plaintext = {}".format(m.decode("UTF-8")))
            break

# Main call
crack(IV, ciphertext)

# Code references: 
# (1) Nitratine, 2019, "XOR Python Byte Strings" (30/11/2021), Recovered from: https://nitratine.net/blog/post/xor-python-byte-strings/
# (2) Kite, 2021, "How to create a range of dates in Python" (30/11/2021), Recovered from: https://www.kite.com/python/answers/how-to-create-a-range-of-dates-in-python
