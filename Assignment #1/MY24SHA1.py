# Raymundo Romero Arenas
# ID = 2369764
# Network Security & Cryptography
# Teacher = Mark Ryan

import hashlib

# Hash dicitionary
hash_dictionary = {}

# Find a collision when hashing the numbers from 0 to 10000
def collision():
    for i in range(0,10000):
        # Hash the number, extract its first six characters and add them to the dictionary
        hash_dictionary[i] = hashlib.sha1(str(i).encode('UTF-8')).hexdigest()[0:6]

        for j in range(0,10000):
            # Hash the number, extract its first six characters and store in an auxiliar variable
            hash_comp = hashlib.sha1(str(j).encode('UTF-8')).hexdigest()[0:6]

            # If the actual hash is on the dictionary, there's a collision
            # Print the numbers that generate the collision and its value
            if hash_dictionary[i] == hash_comp and i != j:
                print('Messages {} and {} generate a collision with a value of {}'.format(i,j,hash_dictionary[i]))
                return
    
    # If all hashes in the dictionary are distinct, then there's no collisions
    print('No collisions were found')

collision()


# COLLISION PROOF
# -------------------------------------------------------------
# hash1 = hashlib.sha1('1889'.encode('UTF-8')).hexdigest()[0:6]
# print('Message "1889" generate a hash of {}'.format(hash1))

# hash2 = hashlib.sha1('8172'.encode('UTF-8')).hexdigest()[0:6]
# print('Message "8172" generate a hash of {}'.format(hash2))