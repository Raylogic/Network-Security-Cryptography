# Raymundo Romero Arenas
# ID = 2369764
# Network Security & Cryptography
# Teacher = Mark Ryan

import hashlib

# Hash dicitionary
hash_dictionary = {}

def collision():
    for i in range(0,10000):
        hash_dictionary[i] = hashlib.sha1(str(i).encode('UTF-8')).hexdigest()[0:6]
        for j in range(0,10000):
            hash_comp = hashlib.sha1(str(j).encode('UTF-8')).hexdigest()[0:6]
            if hash_dictionary[i] == hash_comp and i != j:
                print('Messages {} and {} generate a collision with a value of {}'.format(i,j,hash_dictionary[i]))
                return
    print('No collisions were found')

collision()


# COLLISION PROOF
# -------------------------------------------------------------
# hash1 = hashlib.sha1('1889'.encode('UTF-8')).hexdigest()[0:6]
# print('Message "1889" generate a hash of {}'.format(hash1))
# hash2 = hashlib.sha1('8172'.encode('UTF-8')).hexdigest()[0:6]
# print('Message "8172" generate a hash of {}'.format(hash2))