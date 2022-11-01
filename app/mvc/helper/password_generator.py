#  -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/11/2
#  Name: password_generator.py
#  Author: DoooReyn
#  Description: 密码生成
import random


class PasswordGenerator:
    upper_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    lower_letters = 'abcdefghijklmnopqrstuvwxyz'
    numbers = '0123456789'
    specials = ',./!@?-_'

    @staticmethod
    def generateAllInLength(length, upper=True, lower=True, number=True, special=False):

        if length < 6:
            length = 6

        passwords = []
        dictionary = []

        if upper:
            dictionary.extend(PasswordGenerator.upper_letters)
            passwords.append(random.choice(PasswordGenerator.upper_letters))
            length -= 1
        if lower:
            dictionary.extend(PasswordGenerator.lower_letters)
            passwords.append(random.choice(PasswordGenerator.lower_letters))
            length -= 1
        if number:
            dictionary.extend(PasswordGenerator.numbers)
            passwords.append(random.choice(PasswordGenerator.numbers))
            length -= 1
        if special:
            dictionary.extend(PasswordGenerator.specials)
            passwords.append(random.choice(PasswordGenerator.specials))
            length -= 1

        if len(dictionary) == 0:
            raise RuntimeError('未指定字符集')

        passwords.extend(random.choices(dictionary, k=length))

        return ''.join(passwords)

    @staticmethod
    def generateEveryInLength(upper=1, lower=1, number=1, special=1):
        passwords = []
        if upper > 0:
            passwords.extend(random.choices(PasswordGenerator.upper_letters, k=upper))
        if lower > 0:
            passwords.extend(random.choices(PasswordGenerator.lower_letters, k=lower))
        if number > 0:
            passwords.extend(random.choices(PasswordGenerator.numbers, k=number))
        if special > 0:
            passwords.extend(random.choices(PasswordGenerator.specials, k=special))

        if len(passwords) < 6:
            raise RuntimeError('密码总长不少于6位数')

        random.shuffle(passwords)
        return ''.join(passwords)


if __name__ == '__main__':
    print('----------')
    print(PasswordGenerator.generateAllInLength(10, upper=False))
    print(PasswordGenerator.generateAllInLength(10, lower=False))
    print(PasswordGenerator.generateAllInLength(10, number=False))
    print(PasswordGenerator.generateAllInLength(10, upper=False, special=True))
    print(PasswordGenerator.generateAllInLength(10, lower=False, special=True))
    print(PasswordGenerator.generateAllInLength(10, number=False, special=True))
    print('----------')
    print(PasswordGenerator.generateEveryInLength(upper=1, lower=2, number=3, special=4))
    print(PasswordGenerator.generateEveryInLength(upper=2, lower=1, number=4, special=3))
    print(PasswordGenerator.generateEveryInLength(upper=3, lower=4, number=1, special=2))
    print(PasswordGenerator.generateEveryInLength(upper=4, lower=3, number=2, special=1))
    print(PasswordGenerator.generateEveryInLength(upper=0, lower=6, number=4, special=0))
