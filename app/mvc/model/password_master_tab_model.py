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
        self._passwords = dict()
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
                print('----------------')
            else:
                public, private = newkeys(1024)
                self._public = public.save_pkcs1().decode()
                self._private = private.save_pkcs1().decode()
                print('================')
            print("public", self._public)
            print("private", self._private)
            self.save()

    def passwords(self):
        return self._passwords

    def hasPassword(self, comment: str):
        comment = Encoder.base64(comment)
        return self._passwords.get(comment, None) is not None

    def getPassword(self, comment: str):
        comment = Encoder.base64(comment)
        password = self._passwords.get(comment, None)
        if password:
            return Decoder.rsa(password, self._private)

    def setPassword(self, comment: str, password: str):
        comment = Encoder.base64(comment)
        if self._passwords.get(comment, None):
            self._passwords[comment] = Encoder.rsa(password, self._public)

    def addPassword(self, comment: str, password: str):
        comment = Encoder.base64(comment)
        self._passwords[comment] = Encoder.rsa(password, self._public)

    def delPassword(self, comment: str):
        comment = Encoder.base64(comment)
        del self._passwords[comment]

    def format(self):
        return {
            "master": self._master,
            "public": Encoder.base64(self._public),
            "private": Encoder.base64(self._private),
            "passwords": self._passwords,
        }
