from knap import gen_keys, encode, decode

# Generate keys
pub_key, priv_key, p, m, n  = gen_keys()

# Print public key
pub_key = [str(pi) for pi in p]
print("Public key: " + ','.join(pub_key))

# Prompt user to enter data to be encrypted
data = input("Enter data to be encrypted: ")

# Encrypt data
ciphertext = encode(data, p, n, m)
print("Encrypted ciphertext: " + ciphertext)

# Decrypt data
priv_key = [pow(pi, -1, m) for pi in p]
plaintext = decode(ciphertext, priv_key, p, m)
print("Decrypted plaintext: " + data)
