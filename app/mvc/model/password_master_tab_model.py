#  -*- coding:utf-8 -*-
#
#  Copyright 2020-2022 DoooReyn. All rights reserved.
#  Licensed under the MIT License.
#
#  Since: 2022/11/2
#  Name: password_master_tab_model.py
#  Author: DoooReyn
#  Description:
from base64 import urlsafe_b64encode, urlsafe_b64decode
from hashlib import md5

from rsa import encrypt, decrypt, newkeys, PublicKey, PrivateKey

from mvc.base.base_model import BaseModel


class Encoder:
    @staticmethod
    def md5(password: str):
        return md5(password.encode()).hexdigest()

    @staticmethod
    def base64(public: str):
        return urlsafe_b64encode(public.encode()).decode()

    @staticmethod
    def rsa(msg: str, public: str):
        return urlsafe_b64encode(encrypt(msg.encode(), PublicKey.load_pkcs1(public.encode()))).decode()


class Decoder:
    @staticmethod
    def base64(private: str):
        return urlsafe_b64decode(private.encode()).decode()

    @staticmethod
    def rsa(msg: str, private: str):
        return decrypt(urlsafe_b64decode(msg.encode()), PrivateKey.load_pkcs1(private.encode())).decode()


class PasswordMasterTabModel(BaseModel):
    def __init__(self):
        super(PasswordMasterTabModel, self).__init__()

        self.identifier = 'password_master'
        self._master = ""
        self._public = ""
        self._private = ""
        self._passwords = []
        self._inited = False
        self.inited.connect(self._onInited)

    def hasMaster(self):
        return not not self._master

    def setMasterPassword(self, password: str):
        self._master = Encoder.md5(password)

    def isValidMaster(self, password):
        return self._master == Encoder.md5(password)

    def _onInited(self):
        if not self._inited:
            self._inited = True
            if self._public:
                self._public = Decoder.base64(self._public)
                self._private = Decoder.base64(self._private)
            else:
                public, private = newkeys(1024)
                self._public = public.save_pkcs1().decode()
                self._private = private.save_pkcs1().decode()
            self.save()

    def passwords(self):
        return self._passwords

    def restore(self, account: str, comment: str, password: str):
        return Decoder.base64(account), Decoder.base64(comment), Decoder.rsa(password, self._private)

    def set(self, row: int, account: str, comment: str, password: str):
        if row < len(self._passwords):
            a = Encoder.base64(account)
            c = Encoder.base64(comment)
            p = Encoder.rsa(password, self._public)
            self._passwords[row] = (c, p,)
            self.save()

    def add(self, account: str, comment: str, password: str):
        a = Encoder.base64(account)
        c = Encoder.base64(comment)
        p = Encoder.rsa(password, self._public)
        self._passwords.append((a, c, p,))
        self.save()

    def remove(self, row: int):
        if row < len(self._passwords):
            del self._passwords[row]
            self.save()

    def arrange(self):
        self._passwords.sort(key=lambda e: e[0])

    def format(self):
        return {
            "master": self._master,
            "public": Encoder.base64(self._public),
            "private": Encoder.base64(self._private),
            "passwords": self._passwords,
        }
