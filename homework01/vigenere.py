upper = {ascii:chr(ascii) for ascii in range(65,91)}
lower = {ascii:chr(ascii) for ascii in range(97,123)}
def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    # PUT YOUR CODE HERE
    arr=[]
    for i in range(len(plaintext)):
        keyword_c=keyword[i % len(keyword)]
        if plaintext[i].isalpha():
            if ord(plaintext[i]) in upper:
                x=ord(plaintext[i])-65
                y=ord(keyword_c)-65
                z=chr((x+y)%26+65)
            if ord(plaintext[i]) in lower:
                x=ord(plaintext[i])-97
                y=ord(keyword_c)-97
                z=chr((x+y)%26+97)
        else:
            z=plaintext[i]
        arr.append(z)
    
    ciphertext=ciphertext.join(arr)
    print(ciphertext)
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    # PUT YOUR CODE HERE
    arr=[]
    for i in range(len(ciphertext)):
        keyword_c=keyword[i % len(keyword)]
        if ciphertext[i].isalpha():
            if ord(ciphertext[i]) in upper:
                x=ord(ciphertext[i])-65
                y=ord(keyword_c)-65
                z=chr((x-y+26)%26+65)
            if ord(ciphertext[i]) in lower:
                x=ord(ciphertext[i])-97
                y=ord(keyword_c)-97
                z=chr((x-y+26)%26+97)
        else:
            z=ciphertext[i]
        arr.append(z)
    
    plaintext=plaintext.join(arr)
    print(plaintext)
    return plaintext
