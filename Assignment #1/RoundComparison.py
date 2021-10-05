# Raymundo Romero Arenas
# ID = 2369764
# Network Security & Cryptography
# Teacher = Mark Ryan

def hex2bin(s):
    mp = {'0' : "0000",
          '1' : "0001",
          '2' : "0010",
          '3' : "0011",
          '4' : "0100",
          '5' : "0101",
          '6' : "0110",
          '7' : "0111",
          '8' : "1000",
          '9' : "1001",
          'A' : "1010",
          'B' : "1011",
          'C' : "1100",
          'D' : "1101",
          'E' : "1110",
          'F' : "1111" }
    bin = ""
    for i in range(len(s)):
        bin = bin + mp[s[i]]
    return bin
     
# Binary to hexadecimal conversion
def bin2hex(s):
    mp = {"0000" : '0',
          "0001" : '1',
          "0010" : '2',
          "0011" : '3',
          "0100" : '4',
          "0101" : '5',
          "0110" : '6',
          "0111" : '7',
          "1000" : '8',
          "1001" : '9',
          "1010" : 'A',
          "1011" : 'B',
          "1100" : 'C',
          "1101" : 'D',
          "1110" : 'E',
          "1111" : 'F' }
    hex = ""
    for i in range(0,len(s),4):
        ch = ""
        ch = ch + s[i]
        ch = ch + s[i + 1]
        ch = ch + s[i + 2]
        ch = ch + s[i + 3]
        hex = hex + mp[ch]
         
    return hex

# Code reference: 
# Jain, A. 2021, “Data encryption standard (DES) | Set 1” (01/10/2021), Recovered from: https://www.geeksforgeeks.org/data-encryption-standard-des-set-1/

def bitXOR(s1,s2):
    ans = ""
    for i in range(0,len(s1)):
        if s1[i] == s2[i]:
            ans = ans + '0'
        else:
            ans = ans + '1'
    return ans

# Round 1
outputA = "5BFA6BA65E45E257"
outputB = "87D702363D14F53C"

# Round 2
# outputA = "5BFA6BA65E45E257"
# outputB = "87D702363D14F53C"

# Round 3
# outputA = "5BFA6BA65E45E257"
# outputB = "87D702363D14F53C"

# Round 4
# outputA = "5BFA6BA65E45E257"
# outputB = "87D702363D14F53C"

outputA = hex2bin(outputA)
print(outputA)

outputB = hex2bin(outputB)
print(outputB)

diff = bitXOR(outputA, outputB)
print(diff)

bits = diff.count('1')
print(bits)