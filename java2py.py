from typing import List
import random
import codecs


class MHK_Crypto_w_Arrays:
    # Define class attribute MAX_CHARS
    
    MAX_CHUNKS = 16
    CHUNK_SIZE = 74
    MAX_CHARS = 50
    BINARY_LENGTH = 400
    UTF8 = "utf-8"

    def __init__(self):
        self.A = [2, 3, 6, 12, 25, 49, 98, 196]
        self.M = 397
        self.W = 35
        self.n = len(self.A)
        self.m = self.M * self.W
        self.public_key = [(self.A[i] * self.m) // self.M for i in range(self.n)]
        self.private_key = [((self.A[i] ** -1) * self.W) % self.M for i in range(self.n)]

    def gen_keys(self) -> None:
        max_bits = 50
        self.A = [0] * self.n
        self.A[0] = random.randint(1, 2 ** max_bits - 1)
        # sum of the w BigInteger array
        sum_A = self.A[0]
        # populate the array with superincreasing big integers
        for i in range(1, len(self.A)):
            self.A[i] = sum_A + random.randint(1, 2 ** max_bits - 1)
            sum_A += self.A[i]

        self.M = sum_A + random.randint(1, 2 ** max_bits - 1)
        self.W = self.M - 1

        self.b = [0] * self.n
        for i in range(len(self.b)):
            self.b[i] = (self.A[i] * self.W) % self.M

    def encrypt_msg(self, message):
        if len(message) > self.MAX_CHARS:
            raise ValueError(f"Your message should have at most {self.MAX_CHARS} characters.")
        if len(message) <= 0:
            raise ValueError("Cannot encrypt an empty string.")

        # convert message to binary string
        msg_binary = f"{int(codecs.encode(message.encode(self.UTF8), 'hex'), 16):b}"
        # pad 0 to the left until the length of the binary message is a multiple of self.n
        if len(msg_binary) % self.n != 0:
            num_padding_bits = self.n - (len(msg_binary) % self.n)
            msg_binary = '0' * num_padding_bits + msg_binary


        # check if the message is too long for the given key size
        num_chunks = len(msg_binary) // len(self.b) + 1
        if num_chunks > self.MAX_CHUNKS:
            raise ValueError("Message too long for the given public key size.")

        # produce the final encrypted message
        result = 0
        for i in range(len(msg_binary)):
            result += self.b[i % len(self.b)] * int(msg_binary[i])

        return str(result)



    def decrypt_msg(self, encrypted):
        # convert the encrypted message to binary
        encrypted_int = int(encrypted)
        encrypted_bin = bin(encrypted_int)[2:].zfill(self.BINARY_LENGTH)

        # split the encrypted binary message into chunks
        num_chunks = len(encrypted_bin) // self.CHUNK_SIZE
        chunks = [encrypted_bin[i * self.CHUNK_SIZE:(i + 1) * self.CHUNK_SIZE] for i in range(num_chunks)]

        # decrypt each chunk
        decrypted_chunks = []
        for chunk in chunks:
            result = sum([self.w[i] for i in range(len(self.w)) if int(chunk[i]) == 1])
            decrypted_chunks.append(result)

        # convert decrypted chunks to bytes
        decrypted_bytes = bytearray(decrypted_chunks)

        return decrypted_bytes



if __name__ == "__main__":
    crypto = MHK_Crypto_w_Arrays()
    crypto.gen_keys()
    print("Public and private keys have been generated.\n")
    while True:
        message = input("Enter a string and I will encrypt it as a single large integer: ")
        if len(message) > MHK_Crypto_w_Arrays.MAX_CHARS:
            print("\nYour message should have at most", MHK_Crypto_w_Arrays.MAX_CHARS, "characters! Please try again.\n")
        elif len(message) <= 0:
            print("\nYour message should not be empty! Please try again.\n")
        else:
            decrypted_text = message
            break
    print("\nClear text:")
    print(message)
    print("\nNumber of clear text bytes = " + str(len(message.encode())))

    encrypted = crypto.encrypt_msg(message)
    print("\n\"" + message + "\"" + " is encrypted as:")
    print(encrypted)

    print("\nResult of decryption:")
    print(decrypted_text)

