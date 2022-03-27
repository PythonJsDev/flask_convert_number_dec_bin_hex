from flask import flash

import string
from typing import Dict


def is_bin(value) -> bool:
    return all(c in ['0', '1'] for c in value.data)


def is_hex(value) -> bool:
    return all(c in string.hexdigits for c in value.data)


def is_dec(value) -> bool:
    return all(c in string.digits for c in value.data)


def is_data_valid(value) -> bool:
    return any([is_bin(value), is_hex(value), is_dec(value)])


def check_base_data(base, value) -> bool:
    if base.data == 'bin':
        if not is_bin(value):
            flash(f"{value.data} n'est pas une valeur binaire!", "danger")
            return False
    elif base.data == 'hex':
        if not is_hex(value):
            flash(f"{value.data} n'est pas une valeur hexadécimale!", "danger")
            return False
    elif base.data == 'dec':
        if not is_dec(value):
            flash(f"{value.data} n'est pas une valeur décimale!", "danger")
            return False
    return True


def convert(base: str, value) -> Dict[str, str]:
    data = {}
    if base == 'bin':
        data['bin'] = str(value)
        data['dec'] = str(int(value, 2))
        data['hex'] = str(hex(int(value, 2))[2::].upper())
        return data
    if base == 'dec':
        data['dec'] = str(value)
        data['bin'] = str(bin(int(value, 10))[2::])
        data['hex'] = str(hex(int(value, 10))[2::].upper())
        return data
    if base == 'hex':
        data['hex'] = str(value)
        data['bin'] = str(bin(int(value, 16))[2::])
        data['dec'] = str(int(value, 16))
        return data
