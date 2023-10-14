import cherrypy
from lxml import etree

import register_ADE_account
from libadobeFulfill import fulfill
from fulfill import download
from libadobe import CONFIG_DIRECTORY
from inetepub import decryptBook

class Handler(object):
    @cherrypy.expose
    def download(self):
        if not cherrypy.request.process_request_body:
            raise cherrypy.HTTPError(
                400,
                'Only PUT or POST are supported'
            )

        file = cherrypy.request.body.read()

        if len(file) == 0:
            raise cherrypy.HTTPError(
                400,
                'Please provide an ACSM file'
            )

        try:
            acsmxml = etree.fromstring(file)
        except:
            raise cherrypy.HTTPError(
                400,
                'Please provide a valid ACSM file'
            )

        success, replyData = fulfill(acsmxml)

        if success is False:
            raise cherrypy.HTTPError(
                400,
                replyData
            )

        success, filedata, filename = download(replyData)

        if success is False:
            raise cherrypy.HTTPError(
                400,
                'Could not download the file'
            )

        if filename.endswith("epub"):
            cherrypy.response.headers['content-type'] = 'application/epub+zip'
        else:
            cherrypy.response.headers['content-type'] = 'application/pdf'

        cherrypy.response.headers['content-disposition'] = 'attachment; filename=' + filename

        return filedata

    @cherrypy.expose
    def downloadDrmFree(self):
        if not cherrypy.request.process_request_body:
            raise cherrypy.HTTPError(
                400,
                'Only PUT or POST are supported'
            )

        file = cherrypy.request.body.read()

        if len(file) == 0:
            raise cherrypy.HTTPError(
                400,
                'Please provide an ACSM file'
            )

        try:
            acsmxml = etree.fromstring(file)
        except:
            raise cherrypy.HTTPError(
                400,
                'Please provide a valid ACSM file'
            )

        success, replyData = fulfill(acsmxml)

        if success is False:
            raise cherrypy.HTTPError(
                400,
                replyData
            )

        success, filedata, filename = download(replyData)

        if success is False:
            raise cherrypy.HTTPError(
                400,
                'Could not download the file'
            )

        filedata = decryptBook(filedata)

        if filedata is None:
            raise cherrypy.HTTPError(
                500,
                'Failed to decrypt ' + filename
            )

        if filename.endswith("epub"):
            cherrypy.response.headers['content-type'] = 'application/epub+zip'
        else:
            cherrypy.response.headers['content-type'] = 'application/pdf'

        cherrypy.response.headers['content-disposition'] = 'attachment; filename=' + filename

        return filedata

    @cherrypy.expose
    def register(self, username, password, version=0):
        register_ADE_account.register(username, password, version)
        return "Hit register stub"

    @cherrypy.expose
    def clone(self):
        # TODO: Take a zip file containing the three files and upload them to the config directory
        return "Hit clone stub"

    @cherrypy.expose
    def anonymousRegister(self):
        # TODO: Make this throw an error if already registered and then upload to the config directory
        register_ADE_account.register("", "", 0)
        return "Hit anonymous stub"

    @cherrypy.expose
    def export(self):
        # TODO: Read all three files, zip them up, and return to the caller
        return "Hit export stub"

    @cherrypy.expose
    def exportKey(self):
        # TODO: Call export function, return to the browser
        return "Hit export key stub"




if __name__ == '__main__':
    from pathlib import Path

    Path(CONFIG_DIRECTORY).mkdir(parents=True, exist_ok=True)

    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.quickstart(Handler(), '/')
