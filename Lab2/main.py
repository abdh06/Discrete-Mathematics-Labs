# Project 2 - Task 2.1.2

KEY_FILE = "key pairs.txt"
MESSAGE_FILE = "encrypted texts.txt"


# Euclidian Forward Algorithm
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


# Extended Euclidean (Forward and Backward) algorithm
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

# --------------------------------------------------
# Factoring so we can get our p and q
# --------------------------------------------------

# Finds and Returns any shared primes by checking gcd of both ns. 
def find_shared_primes(ns):
    known = dict()
    for i in range(len(ns)):
        for j in range(i+1, len(ns)):
            g = gcd(ns[i], ns[j])
            if g > 1 and g < ns[i]: # So 2 keys aren't equal
                known[i] = g
                known[j] = g
    return known

# Finds a factor.
def pollard_rho(n):
    c = 1
    count = 0
    while(True):
        x = 2
        y = 2
        g = 1
        while g == 1:
            x = x*x + c
            x = x % n
            y = (y*y + c) % n
            y = (y*y + c) % n
            g = gcd(abs(x-y), n)
            count += 1
            if g > 1 and g != n:
                print(count, " steps.")
                return g
        c = c + 1


# Finds the remaining prime if found thru shared primes, otherwise uses pollard_rho to find the prime.
def factor(i, n, known):
    if i in known:
        p = known[i]
    else:
       print(i +1, "Key doesn't share a factor. \n")
       p = pollard_rho(n)
    
    q = n // p

    if p > q:
        p, q = q, p

    if p * q != n:
       raise ValueError("incorrect divison.")
    
    return (p,q)


# --------------------------------------------------
# RSA keys, and getting their primes.
#
# Format:
# (e, n)
# --------------------------------------------------

# Reads the keys and extracts e and n
def read_keys(filename):
    keys = []
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line.startswith("Key"):
                continue
            right_part = line.split(":", 1)[1]
            e_part, n_part = right_part.split(",")
            e = int(e_part.split("=")[1])
            n = int(n_part.split("=")[1])
            keys.append((e, n))
    return keys


# --------------------------------------------------
# Read encrypted texts.txt
# --------------------------------------------------

# Converts a decrypted number into text
def number_to_text(number):
    characters = []

    while number > 0:
        value = number % 256
        characters.append(chr(value))
        number = number // 256

    characters.reverse()

    return "".join(characters)


# Check if it's readable
def readable(text):
    for ch in text:
        if ord(ch) < 32 or ord(ch) > 126:
            return False
    return True





# --------------------------------------------------
# Decrypt Message by finding the right key
# --------------------------------------------------


def find_key(message, private_keys):
    for k, (d, n) in enumerate(private_keys):
        # Skip this key if any ciphertext value is too large for the modulus
        if any(c >= n for c in message):
            continue

        text = ""
        for c in message:
            m = mod_power(c, d, n)
            text += number_to_text(m)

        if readable(text):
            return (k+1, text)

    return None


# Get our Keys from the file

keys = read_keys(KEY_FILE)
print("PUBLIC KEYS")
print(keys, "\n")

# Find our primes (or factors)

private_keys = []

print("PRIVATE KEYS\n")

ns = [n for e, n in keys]
known = find_shared_primes(ns)

for i in range(len(keys)):

    e, n = keys[i]
    p, q = factor(i, n, known) 

    # Euler's phi function
    phi = (p - 1) * (q - 1)

    # Calculate d
    d = mod_inverse(e, phi)

    private_keys.append((d, n))

    if (e * d) % phi != 1:
       raise ValueError("incorrect d.")

    print("Key", i + 1)
    print("p =", p)
    print("q =", q)
    print("phi =", phi)
    print("d =", d, "\n")

# Begin Decrypting After grabbing all the messages

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



print("DECRYPTED MESSAGES, \n")


for i in range(len(messages)):

    result = find_key(messages[i], private_keys)

    if result == None:
        print("No keys work for this message. \n")
        continue
    
    (key_number, text) = result

    print("Message", i + 1, "\n")
    print("Key", key_number)
    print(text, "\n")