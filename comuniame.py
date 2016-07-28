#!/usr/bin/python

import urllib2
import json

class endPoint:
    urlAuth = 'http://app.comunia.me/api/v3/auth/login'
    urlHome = 'http://app.comunia.me/api/v1/home'
    urlAccount = 'http://app.comunia.me/api/v1/account'
    urlMarket = 'http://app.comunia.me/api/v1/market'
    urlLeague = 'http://app.comunia.me/api/v1/league?fields=*,standings&include=all'
    urlNews = 'http://app.comunia.me/api/v1/league/news?limit=10'

class Player(object):
    id = 0
    teamSize = 0
    name = ""
    position = 0
    points = 0
    teamValue = 0

def callAPI(url, data, headers=[]):
    """Call to the API entry point

    Create a request to url with the headers and the data provided.
    Data is previously converted to json for compatibility issues.

    Args:
        url: URL where we want to do the request
        data: data for the request in a dictionary
        headers: list of headers we want/need to add to the request.


    Returns:
        (#code,Object with the result) if successful
        (#error,Description of error) otherwise
    """
    req = urllib2.Request(url)

    #This is needed for all
    req.add_header('Content-Type', 'application/json;charset=utf-8')
    for a,b in headers:
        req.add_header(a,b)

    jsondata = json.dumps(data).encode('utf-8')
    try:
        if ( not data ):
            response = urllib2.urlopen(req)
        else:
            response = urllib2.urlopen(req,jsondata)
        html = response.read()
        json_obj = json.loads(html)
        return response.getcode(),json_obj
    except urllib2.HTTPError as err:
        return err.code,err.reason
    # print response.geturl()
    # print response.info()
    # print response.getcode()
    # token = json_obj["token"];
    # print token


def auth(email, password):
    """Log in to Comuniame

    Retrieves Bearer token to use it for protected calls.

    Args:
        email: email used as login in Comuniame
        password: password used as password for the email

    Returns:
        (code,Bearer token) if successful
        (errorCode,Error) Otherwise
    """

    data = {
            'email':email,
            'password':password
    }
    code,ans = callAPI(endPoint.urlAuth,data)
    if code == 200:
        global globalToken
        globalToken = ans["token"]
        return code,ans["token"]
    else:
        return code,"error"

def getLeagueID(token):
    """Log in to Comuniame

    Retrieves Bearer token to use it for protected calls.

    Args:
        email: email used as login in Comuniame
        password: password used as password for the email

    Returns:
        Bearer token if successful
        Error code Otherwise
    """
    header = [
                ("Authorization", "Bearer %s" % token)
            ]
    code,ans = callAPI(endPoint.urlAccount,"",header)
    print json.dumps(ans)
    if code == 200:
        league_id =ans["data"]["leagues"][0]["id"]
    else:
        league_id = -1
    return code,league_id


def getNews(token, league_id):
    """Log in to Comuniame

    Retrieves Bearer token to use it for protected calls.

    Args:
        email: email used as login in Comuniame
        password: password used as password for the email

    Returns:
        Bearer token if successful
        Error code Otherwise
    """
    header = [
                ("Authorization", "Bearer %s" % token),
                ("X-League", league_id)
            ]
    i = 0;
    urlOffset = endPoint.urlNews+"&offset="+str(i)
    code,ans = callAPI(urlOffset,"",header)
    if code != 200:
        return code,"Error"
    totalNews = ans["meta"]["list"]["total"]
    newsVector = []
    newSeason = False
    urlOffset = endPoint.urlNews+"&offset="+str(i)
    print urlOffset
    while ( i < totalNews and not newSeason ):

        i += 10
        urlOffset = endPoint.urlNews+"&offset="+str(i)
        print urlOffset
        code,ans = callAPI(urlOffset,"",header)
        if code != 200:
            return code,"Error"

    #Ask news until arrive to new season
    return code,ans

def getMarket(token, league_id):
    """Log in to Comuniame

    Retrieves Bearer token to use it for protected calls.

    Args:
        email: email used as login in Comuniame
        password: password used as password for the email

    Returns:
        Bearer token if successful
        Error code Otherwise
    """
    header = [
                ("Authorization", "Bearer %s" % token),
                ("X-League", league_id)
            ]
    code,ans = callAPI(endPoint.urlMarket,"",header)
    return code,ans

def getPlayers(token, league_id):
    header = [
                ("Authorization", "Bearer %s" % token),
                ("X-League", league_id)
            ]
    code,ans = callAPI(endPoint.urlLeague,"",header)
    if code != 200:
        return code,ans

    playerVector = []
    players = ans["data"]["standings"]
    i = 1
    for player in players:
        a = Player()
        a.id = player["id"]
        a.teamSize = player["teamSize"]
        a.name = player["name"]
        a.position = i
        a.points = player["points"]
        a.teamValue = player["teamValue"]
        playerVector.append(a)
        i += 1

    return code,playerVector





