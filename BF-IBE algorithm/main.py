import hashlib
from Crypto.Util import number
import time

class RevocableIBE:
    def __init__(self):
        pass

    def setup(self):
        # Generate system parameters
        q = number.getPrime(160)
        alpha = number.getRandomNBitInteger(160)
        h = pow(alpha, 2, q)
        params = {'q': q, 'h': h, 'alpha': alpha}
        return params

    def keygen(self, params, master_secret, identity):
        q, h, alpha = params['q'], params['h'], params['alpha']

        # Generate user private key
        user_secret_key = (master_secret + int(hashlib.sha256(identity.encode()).hexdigest(), 16)) % q

        # Generate user public key
        user_public_key = pow(h, user_secret_key, q)

        return {'public_key': user_public_key, 'secret_key': user_secret_key}

    def encrypt(self, params, public_key, message):
        q, h, alpha = params['q'], params['h'], params['alpha']

        # Generate random values
        r = number.getRandomRange(1, q)
        s = number.getRandomRange(1, q)

        # Compute ciphertext components
        C1 = pow(h, r, q)
        C2 = (pow(public_key, r, q) * pow(alpha, s, q)) % q
        ciphertext = (message * pow(alpha, s, q)) % q

        return {'C1': C1, 'C2': C2, 'ciphertext': ciphertext}

    def decrypt(self, params, secret_key, ciphertext):
        q, h, alpha = params['q'], params['h'], params['alpha']
        C1, C2, c = ciphertext['C1'], ciphertext['C2'], ciphertext['ciphertext']

        # Compute the shared secret
        shared_secret = pow(C1, secret_key, q)

        # Invert the shared secret to decrypt the message
        inverse_shared_secret = pow(shared_secret, -1, q)
        decrypted_message = (c * inverse_shared_secret) % q

        return decrypted_message

def run_simulation():
    revocable_ibe = RevocableIBE()
    params = revocable_ibe.setup()

    with open("output.txt", "w") as output_file:
        total_time = 0

        for _ in range(10):
            start_time = time.time()

            # Generate master secret
            master_secret = number.getRandomNBitInteger(160)

            # Generate user identity
            user_identity = "user" + str(_)

            # Key Generation
            user_keys = revocable_ibe.keygen(params, master_secret, user_identity)

            # Encryption
            message = number.getRandomNBitInteger(160)
            ciphertext = revocable_ibe.encrypt(params, user_keys['public_key'], message)

            # Decryption
            decrypted_message = revocable_ibe.decrypt(params, user_keys['secret_key'], ciphertext)

            # Display results
            result_string = (
                f"Test Case {_ + 1}:\n"
                f"  Original Message: {message}\n"
                f"  Encrypted Ciphertext: {ciphertext['ciphertext']}\n"
                f"  Decrypted Message: {decrypted_message}\n\n"
            )
            print(result_string)
            output_file.write(result_string)

            end_time = time.time()
            total_time += end_time - start_time

        average_time = total_time / 10
        print(f"Average Computation Time: {average_time} seconds")

if __name__ == "__main__":
    run_simulation()
