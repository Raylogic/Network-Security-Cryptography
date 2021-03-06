# Raymundo Romero Arenas
# ID = 2369764
# Network Security & Cryptography
# Teacher = Mark Ryan

import binascii
import re

class AES(object):
    def __init__(self, mode, input_type, iv=None):
        self.mode = mode
        self.input = input_type
        self.iv = iv
        self.Nb = 0
        self.Nk = 0
        self.Nr = 0

        # Rijndael S-box
        self.sbox = [
            0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67,
            0x2b, 0xfe, 0xd7, 0xab, 0x76, 0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59,
            0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0, 0xb7,
            0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1,
            0x71, 0xd8, 0x31, 0x15, 0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05,
            0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75, 0x09, 0x83,
            0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29,
            0xe3, 0x2f, 0x84, 0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b,
            0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf, 0xd0, 0xef, 0xaa,
            0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c,
            0x9f, 0xa8, 0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc,
            0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2, 0xcd, 0x0c, 0x13, 0xec,
            0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19,
            0x73, 0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee,
            0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb, 0xe0, 0x32, 0x3a, 0x0a, 0x49,
            0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
            0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4,
            0xea, 0x65, 0x7a, 0xae, 0x08, 0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6,
            0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a, 0x70,
            0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9,
            0x86, 0xc1, 0x1d, 0x9e, 0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e,
            0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf, 0x8c, 0xa1,
            0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0,
            0x54, 0xbb, 0x16]

        self.rcon = [0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36]

    # Padding method for data
    @staticmethod
    def pad(data, block=16):
        if block < 2 or block > 255:
            raise ValueError("Block Size must be < 2 and > 255")

        if len(data) is block: return data
        pads = block - (len(data) % block)
        return data + binascii.unhexlify(('%02x' % int(pads)).encode()) + b'\x00' * (pads - 1)

    # Unpadding method for data
    @staticmethod
    def unpad(data):
        p = None
        for x in data[::-1]:
            if x == 0:
                continue
            elif x != 0:
                p = x; break
        data = data[::-1]
        data = data[p:]
        return data[::-1]

    # Unblock binary data
    @staticmethod
    def unblock(data, size=16):
        return [data[x:x + size] for x in range(0, len(data), size)]

    # Cycle the word [a0, a1, a2, a3] into [a1, a2, a3, a0].
    @staticmethod
    def RotWord(word):
        return int(word[2:] + word[0:2], 16)

    # Format a State Matrix into a list
    @staticmethod
    def StateMatrix(state):
        new_state = []
        split = re.findall('.' * 2, state)
        for x in range(4):
            new_state.append(split[0:4][x]); new_state.append(split[4:8][x])
            new_state.append(split[8:12][x]); new_state.append(split[12:16][x])
        return new_state

    # Revert State Matrix into a string
    @staticmethod
    def RevertStateMatrix(state):
        columns = [state[x:x + 4] for x in range(0, 16, 4)]
        return ''.join(''.join([columns[0][x], columns[1][x], columns[2][x], columns[3][x]]) for x in range(4))

    # Galois multiplication of 8 bit characters a and b
    @staticmethod
    def galois(a, b):
        p = 0
        for counter in range(8):
            if b & 1: p ^= a
            hi_bit_set = a & 0x80
            a <<= 1
            # keep a 8 bit
            a &= 0xFF
            if hi_bit_set:
                a ^= 0x1b
            b >>= 1
        return p

    # Add Round Key to the State using an XOR operation
    @staticmethod
    def AddRoundKey(state, key):
        return ['%02x' % (int(state[x], 16) ^ int(key[x], 16)) for x in range(16)]

    # Shift the last three rows of the State by different offsets
    def ShiftRows(self, state):
        offset = 0
        for x in range(0, 16, 4):
            state[x:x + 4] = state[x:x + 4][offset:] + state[x:x + 4][:offset]
            offset += 1
        return state

    # Apply S-box on a 4-byte word
    def SubWord(self, byte):
        return ((self.sbox[(byte >> 24 & 0xff)] << 24) + (self.sbox[(byte >> 16 & 0xff)] << 16) +
                (self.sbox[(byte >> 8 & 0xff)] << 8) + self.sbox[byte & 0xff])

    # Transform the State Matrix with a S-box
    def SubBytes(self, state):
        return ['%02x' % self.sbox[int(state[x], 16)] for x in range(16)]

    # Treat columns as polynomials over GF(2^8) and multiply them modulo x^4 + 1 with a fixed polynomial a(x)
    def MixColumns(self, state):
        fixed = [2, 1, 1, 3]
        columns = [state[x:x + 4] for x in range(0, 16, 4)]
        row = [0, 3, 2, 1]
        col = 0
        output = []
        for _ in range(4):
            for _ in range(4):
                output.append('%02x' % (
                    self.galois(int(columns[row[0]][col], 16), fixed[0]) ^
                    self.galois(int(columns[row[1]][col], 16), fixed[1]) ^
                    self.galois(int(columns[row[2]][col], 16), fixed[2]) ^
                    self.galois(int(columns[row[3]][col], 16), fixed[3])))
                row = [row[-1]] + row[:-1]
            col += 1
        return output

    # 1) Copy input into State Matrix
    # 2) Transform the State Matrix with the round funtion 10 times
    # 3) Copy Final State Matrix as output
    def Cipher(self, expandedKey, data):
        state = self.AddRoundKey(self.StateMatrix(data), expandedKey[0])
        for r in range(self.Nr - 1):
            print("Round #{} Subkey = ".format(r) + ' '.join(expandedKey[r]))
            print("Round #{} Output = ".format(r) + ' '.join(state))
            print('')
            state = self.SubBytes(state)
            state = self.ShiftRows(state)
            state = self.StateMatrix(''.join(self.MixColumns(state)))
            state = self.AddRoundKey(state, expandedKey[r + 1])

        state = self.SubBytes(state)
        state = self.ShiftRows(state)
        state = self.AddRoundKey(state, expandedKey[self.Nr])
        return self.RevertStateMatrix(state)

    # Take the Cipher Key and perform a Key Expansion routine to generate the key schedule
    def ExpandKey(self, key):
        w = ['%08x' % int(x, 16) for x in re.findall('.' * 8, key)]
        i = self.Nk
        while i < self.Nb * (self.Nr + 1):
            temp = w[i - 1]
            if i % self.Nk == 0:
                temp = '%08x' % (self.SubWord(self.RotWord(temp)) ^ (self.rcon[i // self.Nk] << 24))
            elif self.Nk > 6 and i % self.Nk == 4:
                temp = '%08x' % self.SubWord(int(temp, 16))
            w.append('%08x' % (int(w[i - self.Nk], 16) ^ int(temp, 16)))
            i += 1
        return [self.StateMatrix(''.join(w[x:x + 4])) for x in range(0, len(w), self.Nk)]

    # Gets the key length and sets Nb, Nk, Nr accordingly
    def key_handler(self, key):
        if len(key) == 32:
            self.Nb = 4; self.Nk = 4; self.Nr = 10
        else: 
            raise AssertionError("%s Is an invalid Key!\nUse a 128-bit!" % key)
        return self.ExpandKey(key)

    # Handle Encryption
    def aes_main(self, data, key):
        expanded_key = self.key_handler(key)
        if self.mode == 'ecb': 
            return self.ecb(data, expanded_key)
        else: 
            raise AttributeError("\n\n\tSupported AES Modes of Operation are ['ecb']")

    # Main AES Encryption function
    def encryption(self, data, key):
        return self.aes_main(data, key)

    # Encryption in ECB Mode
    def ecb(self, data, expanded_key):
        if self.input == 'hex':
            return self.Cipher(expanded_key, data)
        else: 
            raise AttributeError("\n\n\tSupported Input types are ['hex']")

import unittest

# Test Encryption
class Test_aes_ecb(unittest.TestCase):
    def test_hex(self):
        key = '00000000000000000000000000000000'
        aes = AES(mode='ecb', input_type='hex')
        cyphertext = aes.encryption('00000000000000000000000000000000', key)
        print(cyphertext)

if __name__ == '__main__':
    unittest.TestProgram()

# Code reference: 
# Riek, J. 2017, ???AES-128 Bit??? (15/10/2021), Recovered from: https://github.com/Joshua-Riek/AES-128bit