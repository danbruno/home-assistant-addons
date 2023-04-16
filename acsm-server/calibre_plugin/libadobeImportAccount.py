'''
Copyright (c) 2021-2023 Leseratte10
This file is part of the ACSM Input Plugin by Leseratte10
ACSM Input Plugin for Calibre / acsm-calibre_plugin

For more information, see: 
https://github.com/Leseratte10/acsm-calibre-plugin
'''

from Cryptodome.Cipher import AES as _AES


class AES(object):
    def __init__(self, key, iv):
        self._aes = _AES.new(key, _AES.MODE_CBC, iv)

    def decrypt(self, data):
        return self._aes.decrypt(data)
