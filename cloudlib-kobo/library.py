from rpc import sendRPC

COUNTRIES = {
	"Austria": "3m.at",
	"Australia": "3m.au",
	"Belgium": "3m.be",
	"Brazil": "3m.br",
	"Canada": "3m.ca",
	"NewZealand": "3m.nz",
	"Germany": "3m.de",
	"Israel": "3m.il",
	"Japan": "3m.jp",
	"Romania": "3m.ro",
	"Spain": "3m.es",
	"SouthAfrica": "3m.za",
	"SaudiArabia": "3m.sa",
	"Singapore": "3m.sg",
	"Switzerland": "3m.ch",
	"UAE": "3m.ae",
	"UnitedKingdom": "3m.gb",
	"UnitedStates": "3m.us"
}

def tokenizeCountry(country):
	return sendRPC("WSAuth.authenticateAnonymousUser", [country]).token

def getCountries():
	return COUNTRIES

def getStates(anonymousToken):
	return sendRPC("WSLibraryMgmt.getStates", [anonymousToken])["result"]

def listLibraries(anonymousToken, state):
	return sendRPC("WSLibraryMgmt.getLibraryBranchesByState", [anonymousToken, state["abbreviation"]])["result"]

def getLibrary(anonymousToken, library):
	return sendRPC("WSLibraryMgmt.getLibraryByID", [anonymousToken, library["libraryID"]])["result"]

def getURL(libraryDetails):
	return f'https://ebook.yourcloudlibrary.com/library/{libraryDetails["urlName"]}'