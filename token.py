def encrypt(data):
    key = 'D4v1Nc!j4R4k134rp4K4130ff1c3*72@1}a1-=+121D4v1Nc!j4R4k134rp4K4130ff1c3*72@1}a1-=+121D4v1Nc!j4R4k134rp4K4130ff1c3*72@1}a1-=+121D4v1Nc!j4R4k134rp4K4130ff1c3*72@1}a1-=+121'
    textASCII = [ord(x) for x in data]
    keyASCII = [ord(x) for x in key]
    encASCII = [(41+((x+y)%26)) for x, y in zip (textASCII, keyASCII)]
    encText = ''.join(chr(x) for x in encASCII)
    return encText
