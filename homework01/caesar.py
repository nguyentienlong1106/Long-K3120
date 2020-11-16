import typing as tp
upper = {ascii:chr(ascii) for ascii in range(65,91)}
lower = {ascii:chr(ascii) for ascii in range(97,123)}


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    # PUT YOUR CODE HERE
    
    for ch in plaintext:
        if ch.isalpha():
            x = ord(ch) + (shift % 26) 
            if ord(ch) in lower:
                if x > ord('z'):
                    x -= 26
            if ord(ch) in upper:
                if x > ord('Z'):
                    x -= 26
            y = chr(x)
        else:
            y=ch
        
        ciphertext += y

    print (ciphertext)
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    # PUT YOUR CODE HERE
    for ch in ciphertext:
        if ch.isalpha():
            x = ord(ch) - (shift % 26) 
            if ord(ch) in lower:
                if x < ord('a'):
                    x += 26
            if ord(ch) in upper:
                if x < ord('A'):
                    x += 26
            y = chr(x)
        else:
            y=ch
        
        plaintext += y
    print (plaintext)
    return plaintext


def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:
    """
    Brute force breaking a Caesar cipher.
    """
    best_shift = 0
    
    # PUT YOUR CODE HERE
    if ciphertext in dictionary:
        return best_shift
    else:
        for i in range(1,26):
            shift=i
            plaintext = ""
            for ch in ciphertext:
                if ch.isalpha():
                    x = ord(ch) - (shift % 26) 
                    if ord(ch) in lower:
                        if x < ord('a'):
                            x += 26
                    if ord(ch) in upper:
                        if x < ord('A'):
                            x += 26
                    y = chr(x)
                else:
                    y=ch
                
                plaintext += y

            if plaintext in dictionary:
                best_shift=shift
                return best_shift
