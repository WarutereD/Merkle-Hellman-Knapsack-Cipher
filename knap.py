import random

def gen_super(q):
    s = []
    s = [1] + [random.randint(max(sum(s[:i]), 1), sum(s[:i+1])+1) for i in range(q-1)]
    return s


def gen_keys():

    seq = input("Enter the superincreasing sequence (comma-separated integers): ")
    q = [int(x) for x in seq.split(",")]
    s = gen_super(len(q))
    r = int(input("Enter the value for r: "))
    m = int(input("Enter the value for m: "))
    p = [r*x % m for x in s]
    n = random.randint(sum(s)+1, 2*sum(s))

    # Generate a random permutation of the sequence 1 to sum(p) - 1
    s = list(range(1, sum(p)))
    random.shuffle(s)
    
    # Calculate the public key
    pub_key = [(r * p[i]) % m for i in range(len(p))]
    
    # Calculate the private key
    priv_key = [(s[i] * pow(p[i], -1, m)) % m for i in range(len(p))]
    
    return pub_key, priv_key, p, n, m


def encode(data, p, n, m):
    bin_data = [bin(ord(char))[2:].rjust(8, '0') for char in data]
    bin_data = ''.join(bin_data)
    
    # Pad bin_data so its length is divisible by len(p)
    pad_len = len(p) - (len(bin_data) % len(p))
    bin_data += '0' * pad_len
    
    cypher_key = []
    for i in range(0, len(bin_data), len(p)):
        cypher_key.append(sum([int(bin_data[i+j])*p[j] for j in range(len(p))]))
    cypher_text = ''.join(['1' if i > n else '0' for i in cypher_key])
    return cypher_text


def decode(cypher_text, priv_key, pub_key, modulus):
    priv_key_sum = sum(priv_key)
    pub_key_sum = sum(pub_key)
    chunk_size = len(priv_key)
    cypher_key = [int(cypher_text[i:i+chunk_size], 2) for i in range(0, len(cypher_text), chunk_size)]
    dec_list = [(x * pow(pub_key_sum, modulus - 2, modulus) * priv_key_sum % modulus) for x in cypher_key]
    plaintext = ''.join([chr(int(x)) for x in dec_list])
    return plaintext





# Main code
if __name__ == '__main__':
    # Generate keys
    pub_key, priv_key, p, m, n  = gen_keys()

    
    # Print public key
    #pub_key = [str(pi) for pi in p]
    print("Public key: " + ','.join(str(x) for x in pub_key))

    
    # Prompt user to enter data to be encrypted
    data = input("Enter data to be encrypted: ")
    
    # Encrypt data
    ciphertext = encode(data, p, n, m)
    print("Encrypted ciphertext: " + ciphertext)
    
   
