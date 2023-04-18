#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Copyright (c) 2021-2023 Leseratte10
This file is part of the ACSM Input Plugin by Leseratte10
ACSM Input Plugin for Calibre / acsm-calibre_plugin

For more information, see: 
https://github.com/Leseratte10/acsm-calibre-plugin
'''

from libadobe import createDeviceKeyFile, VAR_VER_SUPP_CONFIG_NAMES
from libadobeAccount import createDeviceFile, createUser, signIn, activateDevice


#################################################################

def register(adobe_id, password, version):
    if password is None or password == "":
        print("Empty password, aborting")
        return

    if version is None or version >= len(VAR_VER_SUPP_CONFIG_NAMES):
        print("Invalid version")
        return

    createDeviceKeyFile()

    success = createDeviceFile(True, version)
    if success is False:
        print("Error, couldn't create device file.")
        exit(1)

    success, resp = createUser(version, None)
    if success is False:
        print("Error, couldn't create user: %s" % resp)
        exit(1)

    if adobe_id == "":
        success, resp = signIn("anonymous", "", "")
    else:
        success, resp = signIn("AdobeID", adobe_id, password)

    if success is False:
        print("Login unsuccessful: " + resp)
        exit(1)

    success, resp = activateDevice(version, None)
    if success is False:
        print("Couldn't activate device: " + resp)
        exit(1)

    print("Authorized to account " + adobe_id)
