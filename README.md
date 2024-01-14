# Usage

Set key size and message

```python
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
```

Run the script

```bash
python rsa.py
```
