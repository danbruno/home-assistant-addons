#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Copyright (c) 2021-2023 Leseratte10
This file is part of the ACSM Input Plugin by Leseratte10
ACSM Input Plugin for Calibre / acsm-calibre_plugin

For more information, see: 
https://github.com/Leseratte10/acsm-calibre-plugin
'''

# pyright: reportUndefinedVariable=false
import io
import time
import zipfile

from lxml import etree

from libadobe import sendHTTPRequest_FILE
from libadobeFulfill import buildRights
from libpdf import patch_drm_into_pdf


#######################################################################


def download(replyData):
    # replyData: str
    adobe_fulfill_response = etree.fromstring(replyData)
    NSMAP = {"adept": "http://ns.adobe.com/adept"}
    adNS = lambda tag: '{%s}%s' % ('http://ns.adobe.com/adept', tag)
    adDC = lambda tag: '{%s}%s' % ('http://purl.org/dc/elements/1.1/', tag)

    print(replyData)

    download_url = adobe_fulfill_response.find(
        "./%s/%s/%s" % (adNS("fulfillmentResult"), adNS("resourceItemInfo"), adNS("src"))).text
    resource_id = adobe_fulfill_response.find(
        "./%s/%s/%s" % (adNS("fulfillmentResult"), adNS("resourceItemInfo"), adNS("resource"))).text
    license_token_node = adobe_fulfill_response.find(
        "./%s/%s/%s" % (adNS("fulfillmentResult"), adNS("resourceItemInfo"), adNS("licenseToken")))

    rights_xml_str = buildRights(license_token_node)

    if (rights_xml_str is None):
        print("Building rights.xml failed!")
        return False, None, None

    book_name = None

    try:
        metadata_node = adobe_fulfill_response.find(
            "./%s/%s/%s" % (adNS("fulfillmentResult"), adNS("resourceItemInfo"), adNS("metadata")))
        book_name = metadata_node.find("./%s" % (adDC("title"))).text
    except:
        book_name = "Book"

    # Download eBook: 

    print(download_url)

    filename_tmp = book_name + ".tmp"

    dl_start_time = int(time.time() * 1000)
    ret, fileData = sendHTTPRequest_FILE(download_url)
    dl_end_time = int(time.time() * 1000)
    print("Download took %d milliseconds" % (dl_end_time - dl_start_time))

    if (ret != 200):
        print("Download failed with error %d" % (ret))
        return False, None, None

    book_content = fileData[:10]
    filetype = ".bin"

    if (book_content.startswith(b"PK")):
        print("That's a ZIP file -> EPUB")
        filetype = ".epub"
    elif (book_content.startswith(b"%PDF")):
        print("That's a PDF file")
        filetype = ".pdf"

    filename = book_name + filetype

    if filetype == ".epub":
        # Store EPUB rights / encryption stuff
        file_like_object = io.BytesIO(fileData)
        zf = zipfile.ZipFile(file_like_object, "a")
        zf.writestr("META-INF/rights.xml", rights_xml_str)
        zf.close()

        return True, file_like_object.getvalue(), filename

    elif filetype == ".pdf":
        print("Successfully downloaded PDF, patching encryption ...")

        adobe_fulfill_response = etree.fromstring(rights_xml_str)
        adNS = lambda tag: '{%s}%s' % ('http://ns.adobe.com/adept', tag)
        resource = adobe_fulfill_response.find("./%s/%s" % (adNS("licenseToken"), adNS("resource"))).text

        file_in = io.BytesIO(fileData)
        file_out = io.BytesIO()
        ret = patch_drm_into_pdf(file_in, rights_xml_str, file_out, resource)
        if ret:
            print("File successfully fulfilled to " + filename)
            return True, file_out.getvalue(), filename
        else:
            print("Errors occurred while patching " + filename)
            return False, None, None

    else:
        print("Error: Weird filetype")
        return False, None, None
