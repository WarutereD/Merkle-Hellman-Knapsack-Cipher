import random
import math

# Step 1: Generate private key
def generate_private_key(n):
    private_key = []
    s = 0
    for i in range(n):
        r = random.randint(s + 1, 2 * s)
        private_key.append(r)
        s += r
    return private_key


# Step 2: Find prime number greater than sum of private key elements
def find_prime(n):
    while True:
        n += 1
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                break
        else:
            return n

# Step 3: Generate W relatively prime to M
def generate_W(M):
    while True:
        W = random.randint(2, M - 1)
        if math.gcd(W, M) == 1:
            return W

# Step 4: Encrypt plaintext
def encrypt(plaintext, private_key, M, W):
    ciphertext = []
    for i in range(0, len(plaintext), 8):
        block = plaintext[i:i+8]
        x = sum(private_key[j] * int(block[j]) for j in range(8))
        y = (W * x) % M
        ciphertext.append(y)
    return ciphertext

# Step 5: Decrypt ciphertext
def decrypt(ciphertext, private_key, M, W):
    plaintext = ''
    for y in ciphertext:
        x = (W * egcd(M, W)[1] * y) % M
        block = ''
        for j in range(7, -1, -1):
            if private_key[j] <= x:
                x -= private_key[j]
                block = '1' + block
            else:
                block = '0' + block
        plaintext += block
    return plaintext

# Step 6: Generate private key, M, and W
n = 8
private_key = generate_private_key(n)
M = find_prime(sum(private_key))
W = generate_W(M)

# Example usage
plaintext = 'hello world'
binary_plaintext = ''.join(format(ord(c), '08b') for c in plaintext)
print("Plaintext (binary):", binary_plaintext)
ciphertext = encrypt(binary_plaintext, private_key, M, W)
print("Ciphertext:", ciphertext)
decrypted_binary_plaintext = decrypt(ciphertext, private_key, M, W)
decrypted_plaintext = ''.join(chr(int(decrypted_binary_plaintext[i:i+8], 2)) for i in range(0, len(decrypted_binary_plaintext), 8))
print("Decrypted plaintext:", decrypted_plaintext)
