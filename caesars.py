from lib import Ru, Rotor


def caesars_cipher(number, text):
    text_list = list()
    for i in range(len(text)):
        if text[i] == ' ':
            text_list.append(' ')
            i += 1
        elif text[i] == ',':
            text_list.append(',')
            i += 1
        elif text[i] == '!':
            text_list.append('!')
            i += 1
        elif text[i] == '.':
            text_list.append('.')
            i += 1
        elif text[i] == '?':
            text_list.append('?')
            i += 1
        elif text[i] == '–':
            text_list.append('–')
            i += 1
        elif text[i] == '—':
            text_list.append('—')
            i += 1
        if text[i] in Ru:
            if ord(text[i]) + number > 1103:
                text_list.append((chr((ord(text[i]) - 32) + number)).lower())
            elif ord(text[i]) + number < 1072:
                text_list.append((chr((ord(text[i]) + 32) + number)).lower())
            else:
                text_list.append(chr(ord(text[i]) + number).lower())
        elif text[i].upper() in Rotor:
            if (ord(text[i]) + number) > 122:
                text_list.append((chr((ord(text[i]) - 26) + number)).lower())
            elif ord(text[i]) + number < 97:
                text_list.append((chr((ord(text[i]) + 26) + number)).lower())
            else:
                text_list.append(chr(ord(text[i]) + number).lower())

    return ''.join(text_list)
