from rpc import get, post
import requests

def search(cookies, url, query, segment):
    return get(cookies, url, f"/search?query={query}&segment={segment}&format=&available=Any&language=&sort=&orderBy=relevance&owned=yes&", "routes/library/$name/search")["results"]["search"]

def details(cookies, url, bookId):
    print(bookId)
    print(url)
    return get(cookies, url, f"/detail/{bookId}?", "routes/library/$name/detail/$id")["book"]

def checkout(cookies, url, bookId):
    return get(cookies, url, f"/detail/{bookId}?action=borrow&itemId={bookId}&", "routes/library/$name/detail/$id")["book"]

def downloadACSM(cookies, rpc_url, reaktor, loanId):
    headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
    return requests.get(rpc_url + f"/delivery/metadata?token={reaktor}&exporter=com.bookpac.exporter.fulfillmenttoken&udid={loanId}&tokenType=deviceVendorID", cookies=cookies, headers=headers, verify=False).text

def checkin(cookies, url, bookId):
    return get(cookies, url, f"/detail/{bookId}?action=return&itemId={bookId}&", "routes/library/$name/detail/$id")["book"]

def hold(cookies, url, bookId):
    return get(cookies, url, f"/detail/{bookId}?action=hold&itemId={bookId}&", "routes/library/$name/detail/$id")["book"]

def cancelHold(cookies, url, bookId):
    return get(cookies, url, f"/detail/{bookId}?action=remove&itemId={bookId}&", "routes/library/$name/detail/$id")["book"]

def listCheckedOut(cookies, url):
    return post(cookies, url, f"/mybooks/current?", "routes/library/$name/mybooks/current")["patronItems"]

def listHolds(cookies, url):
    return get(cookies, url, f"/mybooks/holds?", "routes/library/$name/mybooks/holds")["patronItems"]

