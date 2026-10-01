# IX1500 Discrete Mathematics
# Project 2 - Task 2.1.2


MESSAGE_FILE = "encrypted texts.txt"


# Extended Euclidean algorithm
def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0

    g, x1, y1 = extended_gcd(b, a % b)

    x = y1
    y = x1 - (a // b) * y1

    return g, x, y


# Finds the private exponent d
def mod_inverse(e, phi):
    g, x, y = extended_gcd(e, phi)

    if g != 1:
        return None

    return x % phi


# Calculates base^exponent mod n
def mod_power(base, exponent, n):
    result = 1
    base = base % n

    while exponent > 0:

        if exponent % 2 == 1:
            result = (result * base) % n

        base = (base * base) % n
        exponent = exponent // 2

    return result


# Converts a decrypted number into text
def number_to_text(number):
    characters = []

    while number > 0:
        value = number % 256
        characters.append(chr(value))
        number = number // 256

    characters.reverse()

    return "".join(characters)


# --------------------------------------------------
# RSA keys
#
# Format:
# (e, n, p, q)
# --------------------------------------------------

keys = [
    (23, 100289621329340257, 123456791, 812345927),
    (7, 882238272068111039, 912345671, 967000009),
    (19, 182469164307407143, 200000033, 912345671),
    (29, 799710404000289581, 876543211, 912345671),
    (29, 901082142384103049, 912345671, 987654319)
]


# --------------------------------------------------
# Calculate private keys
# --------------------------------------------------

private_keys = []


print("PRIVATE KEYS")
print()


for i in range(len(keys)):

    e, n, p, q = keys[i]

    # Euler's phi function
    phi = (p - 1) * (q - 1)

    # Calculate d
    d = mod_inverse(e, phi)

    private_keys.append((d, n))

    print("Key", i + 1)
    print("p =", p)
    print("q =", q)
    print("phi =", phi)
    print("d =", d)
    print()


# --------------------------------------------------
# Read encrypted texts.txt
# --------------------------------------------------

file = open(MESSAGE_FILE, "r", encoding="utf-8")

lines = file.readlines()

file.close()


messages = []
current_message = []


for line in lines:

    line = line.strip()

    if line.startswith("Message"):

        if len(current_message) > 0:
            messages.append(current_message)
            current_message = []

    elif line != "" and not line.startswith("RSA") and not line.startswith("="):

        numbers = line.split()

        for number in numbers:

            if number.isdigit():
                current_message.append(int(number))


if len(current_message) > 0:
    messages.append(current_message)


# --------------------------------------------------
# Decrypt
# --------------------------------------------------

# We found that:
# Message 1 uses Key 4
# Message 2 uses Key 5
# Message 3 uses Key 4

message_keys = [4, 5, 4]


print()
print("DECRYPTED MESSAGES")
print()


for i in range(len(messages)):

    key_number = message_keys[i]

    d, n = private_keys[key_number - 1]

    text = ""

    for c in messages[i]:

        # RSA decryption:
        # m = c^d mod n

        m = mod_power(c, d, n)

        text += number_to_text(m)


    print("Message", i + 1)
    print("Key", key_number)
    print(text)
    print()