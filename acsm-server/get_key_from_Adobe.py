#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Copyright (c) 2021-2023 Leseratte10
This file is part of the ACSM Input Plugin by Leseratte10
ACSM Input Plugin for Calibre / acsm-calibre_plugin

For more information, see:
https://github.com/Leseratte10/acsm-calibre-plugin
'''

'''
Run this tool to download the eBook DER encryption key
for a given ADE account from the Adobe server. 

I am not responsible if Adobe does ban your Account for using
nonstandard software, though in all my previous tests that has
never happened. 

Though I would suggest not running this script multiple times - 
just run it once and then make enough backups of the key file.

'''

import sys
import tempfile

if sys.version_info[0] < 3:
    print("This script requires Python 3.")
    exit(1)

from libadobe import createDeviceKeyFile, update_account_path, VAR_VER_SUPP_CONFIG_NAMES
from libadobeAccount import createDeviceFile, createUser, signIn, exportAccountEncryptionKeyDER, getAccountUUID


#################################################################

def exportKey(adobe_id, password, version):
    if version is None or version >= len(VAR_VER_SUPP_CONFIG_NAMES):
        print("Invalid version")
        return

    if adobe_id is None or adobe_id == "" or password is None or password == "":
        print("Empty credential, aborting")
        return

    filename = "adobekey_" + adobe_id + ".der"

    with tempfile.TemporaryDirectory() as temp_dir:
        update_account_path(temp_dir)

        print("Preparing keys ...")

        createDeviceKeyFile()
        success = createDeviceFile(True, version)
        if success is False:
            print("Error, couldn't create device file.")
            exit(1)

        success, resp = createUser(version, None)
        if success is False:
            print("Error, couldn't create user: %s" % resp)
            exit(1)

        print("Logging in ...")

        success, resp = signIn("AdobeID", adobe_id, password)
        if success is False:
            print("Login unsuccessful: " + resp)
            exit(1)

        print("Exporting keys ...")

        try:
            account_uuid = getAccountUUID()
            if account_uuid is not None:
                filename = "adobekey_" + adobe_id + "_uuid_" + account_uuid + ".der"
        except:
            pass

        success = exportAccountEncryptionKeyDER(filename)
        if success is False:
            print("Couldn't export key.")
            exit(1)

    print("Successfully exported key for account " + adobe_id + " to file " + filename)
