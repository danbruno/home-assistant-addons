import cherrypy
from lxml import etree

import calibre_plugin.register_ADE_account
from calibre_plugin.libadobeFulfill import fulfill
from calibre_plugin.fulfill import download


class DownloadHandler(object):
    @cherrypy.expose
    def download(self):
        if not cherrypy.request.process_request_body:
            raise cherrypy.HTTPError(
                400,
                'Only PUT or POST are supported'
            )

        file = cherrypy.request.body.read()

        print(len(file))

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
                'Could not fulfill the request'
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


class RegisterHandler(object):
    @cherrypy.expose
    def register(self, username, password, version=0):
        calibre_plugin.register_ADE_account.register(username, password, version)
        return "Hit register stub"


class CloneHandler(object):
    @cherrypy.expose
    def clone(self):
        # TODO: Take a zip file containing the three files and upload them to the config directory
        return "Hit clone stub"


class AnonymousHandler(object):
    @cherrypy.expose
    def clone(self):
        # TODO: Make this throw an error if already registered and then upload to the config directory
        calibre_plugin.register_ADE_account.register("", "", 0)
        return "Hit anonymous stub"


class ExportConfig(object):
    @cherrypy.expose
    def export(self):
        # TODO: Read all three files, zip them up, and return to the caller
        return "Hit export stub"


class KeyHandler(object):
    @cherrypy.expose
    def exportKey(self):
        # TODO: Call export function, return to the browser
        return "Hit export key stub"


if __name__ == '__main__':
    cherrypy.quickstart(DownloadHandler(), '/download')
    cherrypy.quickstart(RegisterHandler(), '/register')
    cherrypy.quickstart(CloneHandler(), '/clone')
    cherrypy.quickstart(AnonymousHandler(), '/registerAnonymous')
    cherrypy.quickstart(ExportConfig(), '/exportConfig')
    cherrypy.quickstart(KeyHandler(), '/exportKey')
