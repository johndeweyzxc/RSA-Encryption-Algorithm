import os
import time

DEFAULT_EXPONENT = 65537


def random_bits(n_bits):
    n_bytes, _ = divmod(n_bits, 8)
    random_data = os.urandom(n_bytes)
    return random_data


def random_int(n_bits):
    random_data = random_bits(n_bits)
    val = int.from_bytes(
        random_data, 'big', signed=False
    )
    return val


def random_odd_int(n_bits):
    val = random_int(n_bits)
    return val | 1


def randint(max_val):
    bit_size = int(max_val).bit_length()

    tried = 0
    while True:
        val = random_int(bit_size)
        if val <= max_val:
            break

        if tried % 10 == 0 and tried:
            bit_size -= 1

        tried += 1

    return val


def miller_rabin_test(n, k):
    if not (n & 1):
        return False

    if n < 2:
        return False

    d = n - 1
    r = 0

    while not (d & 1):
        r += 1
        d >>= 1

    for _ in range(k):
        a = randint(n - 3) + 1
        x = pow(a, d, n)

        if x == 1 or x == n - 1:
            continue

        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == 1:
                return False
            if x == n - 1:
                break
        else:
            return False

    return True


def find_prime(n_bits):
    bit_size = 0

    if n_bits >= 1500:
        bit_size = 3
    elif n_bits >= 1024:
        bit_size = 4
    elif n_bits >= 512:
        bit_size = 7

    while True:
        prime_number = random_odd_int(n_bits)

        if miller_rabin_test(prime_number, bit_size + 1):
            return prime_number


def is_acceptable(p, q, total):
    if p == q:
        return False

    found_size = int(p * q).bit_length()
    return total == found_size


def find_two_primes(n_bits):
    total_bits = n_bits * 2
    shift_bits = n_bits // 16
    p_bits = n_bits + shift_bits
    q_bits = n_bits - shift_bits

    p = find_prime(p_bits)
    q = find_prime(q_bits)

    change_p = False
    while not is_acceptable(p, q, total_bits):
        if change_p:
            p = find_prime(p_bits)
        else:
            q = find_prime(q_bits)

        change_p = not change_p

    return max(p, q), min(p, q)


def calc_private_key(p, q):
    """
    The Euler totient function φ(n) = (p - 1)(q - 1) is used instead of λ(n) 
    for calculating the private exponent d. Since φ(n) is always 
    divisible by λ(n), the algorithm works as well.
    """

    euler_toutient = (p - 1) * (q - 1)
    d = pow(DEFAULT_EXPONENT, -1, euler_toutient)
    if (DEFAULT_EXPONENT * d) % euler_toutient != 1:
        """
        Determine d as d ≡ e - 1 (mod φ(n)). d must be modular 
        multiplicative inverse of e modulo φ(n).
        """
        raise ValueError('e and d are not multiplicative inverse')

    return DEFAULT_EXPONENT, d


def generate_rsa_key(n_bits):
    if n_bits >= 2048:
        print(
            f'Generating RSA {n_bits} bit key. This may take some time...')
    else:
        print(
            f'Generating RSA {n_bits} bit key...'
        )
    start = time.perf_counter()

    while True:
        p, q = find_two_primes(n_bits // 2)
        try:
            e, d = calc_private_key(p, q)
            break
        except ValueError:
            pass

    end = time.perf_counter()
    print(
        f'Finish generating RSA {n_bits} bit key after {end - start} seconds.'
    )
    return p, q, e, d


def encrypt(n, e, m):
    print('Encrypting message...')
    c = pow(m, e, n)
    return c


def decrypt(n, d, c):
    print('Decrypting message...')
    m = pow(c, d, n)
    return m


# You can change the key size from 2048 to any number but a larger number
# will take some time to generate.
p, q, e, d = generate_rsa_key(2048)
print(f"p: {str(p)}\n")
print(f"q: {str(q)}\n")
n = p * q
print(f"n: {str(n)}\n")
# Set the message you want to encrypt, integer value only
message = 1234567890
# Sender encrypts message using public modulo n and constant e = 65537
encrypted = encrypt(n, e, message)
print(f"ENCRYPTED MESSAGE: {encrypted}")
# Receiver decrypts the cipher using public modulo n and private key d
decrypted = decrypt(n, d, encrypted)
print(f"DECRYPTED MESSAGE: {decrypted}")
