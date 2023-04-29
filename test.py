from knap import decode, gen_super

seq = input("Enter the superincreasing sequence (comma-separated integers): ")
p = [int(x) for x in seq.split(",")]
r = int(input("Enter r: "))
m = int(input("Enter m: "))
cypher_text = input("Enter cypher_text: ")

try:
    # Calculate the public key
    pub_key = [(r * p[i]) % m for i in range(len(p))]
    
    # Calculate the private key
    priv_key = [(s[i] * pow(p[i], -1, m)) % m for i in range(len(p))]
    modulus = m
    decrypted_text = decode(cypher_text, priv_key, pub_key, modulus)
    print(f"Decrypted message: {decrypted_text}")
except ValueError as e:
    print("Invalid input:", e)
