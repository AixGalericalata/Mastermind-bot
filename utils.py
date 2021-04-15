def to_byte_array(s, num_symbols, num_colors, repetition):
    if len(s) != num_symbols:
        return 'Неправильное кол-во символов.'

    array = bytearray()
    for i in s:
        if i.isdigit():
            t = int(i)
            if 1 <= t <= num_colors:
                array.append(t - 1)
            else:
                return 'Одна из цифр неправильная.'
        else:
            return 'Одна из цифр неправильная.'

    if not repetition:
        if len(array) != len(set(array)):
            return 'Мы играем без повторений цифр.'

    return array
