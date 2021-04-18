def to_cipher(text):
    bits = bin(int.from_bytes(text.encode('utf-8', 'surrogatepass'), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))


def from_cipher(code):
    n = int(code, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode('utf-8', 'surrogatepass')
