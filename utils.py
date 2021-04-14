def to_byte_array(s, num_symbols, num_colors):
    if len(s) != num_symbols:
        return None

    array = bytearray()
    for i in s:
        if i.isdigit():
            t = int(i)
            if 0 <= t < num_colors:
                array.append(t)
            else:
                return None
        else:
            return None

    return array
