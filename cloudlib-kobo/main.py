import cherrypy

import authentication
import library
import book
import user
import schema
import cherrypy_jinja2
import acsmserver
import connection
import configparser

local = False

CONFIG_DIRECTORY = "/config/addons_config/cloud-lib/"
TEMPLATE_DIRECTORY = "/templates"


if local:
    CONFIG_DIRECTORY = "c:/cloudlib/"
    TEMPLATE_DIRECTORY = "c:/cloudlib/templates"

SESSION_DIRECTORY = CONFIG_DIRECTORY + "sessions"
STATIC_DIRECTORY = CONFIG_DIRECTORY + "static"
USER_DATABASE = CONFIG_DIRECTORY + "users.db"

config = configparser.ConfigParser()
config.read(CONFIG_DIRECTORY + "config.cfg")

CONVERSION_ENDPOINT = config.get('General', 'acsmserver')

class Handler(object):
    def checkAuth(self):
        cookies = cherrypy.session.get("auth")
        if cookies is None:
            raise cherrypy.HTTPRedirect("/")

    @cherrypy.tools.jinja2(template="index.html")
    @cherrypy.expose
    def index(self):
      cookies = cherrypy.session.get("auth")
      if cookies is None:
          users = user.read_all_users(connection.getConnection())

          if len(users) == 0:
            raise cherrypy.HTTPRedirect("/signup")
          else:
            raise cherrypy.HTTPRedirect("/choose")

      return {}

    @cherrypy.tools.jinja2(template="choose.html")
    @cherrypy.expose
    def choose(self):
        conn = connection.getConnection()
        users = user.read_all_users(conn)
        return { "users" : users }

    @cherrypy.tools.jinja2(template="signup.html")
    @cherrypy.expose
    def signup(self):
        return {}

    @cherrypy.expose
    def login(self, alias):
        print("Logging in as " + alias)
        conn = connection.getConnection()
        u = user.read_user(conn, alias)
        url = u["url"]

        response = authentication.login(url, u["login"],
                                        u["password"])
        cookies = response.cookies

        cherrypy.session["auth"] = cookies
        cherrypy.session["url"] = url

        userconfig = user.getConfig(cookies, url)

        print(userconfig)

        cherrypy.session["rpcurl"] = userconfig.get("RPC_DOMAIN_PUBLIC", "https://service.yourcloudlibrary.com")
        cherrypy.session["reaktor"] = userconfig["reaktor"]

        raise cherrypy.HTTPRedirect("/")

    @cherrypy.tools.jinja2(template="current.html")
    @cherrypy.expose
    def list(self):
        self.checkAuth()
        cookies = cherrypy.session.get("auth")
        url = cherrypy.session.get("url")
        patronItems = book.listCheckedOut(cookies, url)
        return {"patronItems" : patronItems}

    @cherrypy.expose
    def checkout(self, id):
        self.checkAuth()
        cookies = cherrypy.session.get("auth")
        url = cherrypy.session.get("url")
        return book.checkout(cookies, url, id)

    @cherrypy.expose
    def checkin(self, id):
        self.checkAuth()
        cookies = cherrypy.session.get("auth")
        url = cherrypy.session.get("url")
        return book.checkin(cookies, url, id)

    @cherrypy.expose
    def download(self, loanId):
        self.checkAuth()

        # Kobo is weird and won't download a file unless the URI ends in .epub even if the Content-Disposition is set
        if loanId.endswith('.epub'):
            loanId = loanId[0:-5]

        cookies = cherrypy.session.get("auth")
        rpc_url = cherrypy.session.get("rpcurl")
        reaktor = cherrypy.session.get("reaktor")
        acsm = book.downloadACSM(cookies, rpc_url, reaktor, loanId)
        response = acsmserver.convert(CONVERSION_ENDPOINT + '/download', acsm)
        cherrypy.response.headers['Content-Disposition'] = response.headers['Content-Disposition']
        cherrypy.response.headers['Content-Type'] = response.headers['Content-Type']
        cherrypy.response.headers['Content-Length'] = response.headers['Content-Length']
        return response.content

    @cherrypy.expose
    def downloadDrmFree(self, loanId):
        self.checkAuth()

        # Kobo is weird and won't download a file unless the URI ends in .epub even if the Content-Disposition is set
        if loanId.endswith('.epub'):
            loanId = loanId[0:-5]

        cookies = cherrypy.session.get("auth")
        rpc_url = cherrypy.session.get("rpcurl")
        reaktor = cherrypy.session.get("reaktor")
        acsm = book.downloadACSM(cookies, rpc_url, reaktor, loanId)
        response = acsmserver.convert(CONVERSION_ENDPOINT + '/downloadDrmFree', acsm)
        cherrypy.response.headers['Content-Disposition'] = response.headers['Content-Disposition']
        cherrypy.response.headers['Content-Type'] = response.headers['Content-Type']
        cherrypy.response.headers['Content-Length'] = response.headers['Content-Length']
        return response.content

    @cherrypy.tools.jinja2(template="detail.html")
    @cherrypy.expose
    def detail(self, id):
        self.checkAuth()
        cookies = cherrypy.session.get("auth")
        url = cherrypy.session.get("url")
        return book.details(cookies, url, id)

    @cherrypy.tools.jinja2(template="results.html")
    @cherrypy.expose
    def search(self, query, segment=1):
        self.checkAuth()
        cookies = cherrypy.session.get("auth")
        url = cherrypy.session.get("url")
        search = book.search(cookies, url, query, segment)
        return {"totalBooks" : search["totalItems"], "segment" : segment, "totalSegments" : search["totalSegments"], "items" : search["items"]}

if __name__ == '__main__':
    from pathlib import Path

    Path(CONFIG_DIRECTORY).mkdir(parents=True, exist_ok=True)
    Path(SESSION_DIRECTORY).mkdir(parents=True, exist_ok=True)
    Path(STATIC_DIRECTORY).mkdir(parents=True, exist_ok=True)


    cherrypy.config.update({'server.socket_host': '0.0.0.0',
                            'tools.sessions.on': True,
                            'tools.sessions.storage_type': "File",
                            'tools.sessions.storage_path': SESSION_DIRECTORY,
                            # One month minus 10 minutes to avoid funny business
                            'tools.sessions.timeout': 43790,
                            'tools.staticdir.on': True,
                            'tools.staticdir.dir': "static",
                            'tools.staticdir.root': STATIC_DIRECTORY,
                            'tools.jinja2.search_path': TEMPLATE_DIRECTORY
                            })

    schema.upgrade()

    cherrypy.quickstart(Handler(), '/')