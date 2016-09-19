#!/usr/bin/python

import urllib2
import json
import sys

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
    money = 20000000

class New(object):
    type = ""
    name = ""
    price = 0
    amount = 0
    fromID = 0
    toID = 0
    content = []

jornadaPoints = []

def printNews(news, players):
    for new in news:
        if new.type == "transfer":
            print "TRANSFER for: ", new.name
            print idToName(new.fromID,players) + " ---> " + idToName(new.toID,players) + ":" + str(new.amount)
        if new.type == "market":
            print "MARKET for: ", new.name
            print idToName(new.fromID,players) + " ---> " + idToName(new.toID,players) + ":" + str(new.amount)



def updatePlayers(new, players):
    print "Transaction for: ",new.name
    print idToName(new.fromID,players) + " ---> " + idToName(new.toID,players) + ":" + str(new.amount)

    for player in players:
        if new.fromID == player.id:
            player.money = player.money + new.amount
        if new.toID == player.id:
            player.money = player.money - new.amount

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


def idToName(id,players):
    if id == 0:
        return "Mercado"
    for player in players:
        if id == player.id and id != 0:
            return player.name
    return "UNKNOWN"

def readNews(new):
    """Log in to Comuniame

    Retrieves Bearer token to use it for protected calls.

    Args:
        email: email used as login in Comuniame
        password: password used as password for the email

    Returns:
        Bearer token if successful
        Error code Otherwise
    """
    size = len(new["content"])
    print new["content"]
    vectorNews = []
    print "SIZE ",size
    for i in range(0,size):
        n = New()
        n.type = new["type"]
        print n.type
        if n.type == "roundStarted" or n.type == "roundPre" or n.type == "adminText" or n.type == "text" or n.type == "userLeave" or n.type == "playerMovements" or n.type == "roundFinished":
            print new["content"]
            break;
        if n.type == "leagueReset":
            print new["content"]
            return vectorNews,1;
        if n.type == "roundFinished":
            continue
            n.content = new["content"]
            print n.content
            jornada = new["content"]["round"]["label"]
            if jornada in jornadaPoints:
                continue
            jornadaPoints.append(n.name)
            for aux in range(0,len(n.content)):
                n = New()
                n.content = new["content"]["results"]
                n.name = "BONUS " + new["content"]["round"]["label"]
                n.fromID = n.content[aux]["user"]["id"]
                n.amount = n.content[aux]["bonus"]
                vectorNews.append(n)
            break
        if n.type == "bonus":
            for aux in range(0,len(n.content)):
                n = New()
                n.content = new["content"][i]
                n.name = "BONUS"
                n.amount = new["content"][aux]["amount"]
                n.fromID = new["content"][aux]["user"]["id"]
                vectorNews.append(n)
            # sys.exit()
        if n.type == "market" or n.type == "transfer":
            n.content = new["content"][i]
            # if "name" in new["content"][i]["player"]:
            n.name = new["content"][i]["player"]["name"]
            print n.name
            # if "price" in new["content"][i]["player"]:
            n.price = new["content"][i]["player"]["price"]
            print n.price
            if "amount" in new["content"][i]:
                n.amount =  new["content"][i]["amount"]
                print n.amount

            if "to" in new["content"][i] and type(new["content"][i]["to"]) is not int:
                print "to is in"
                print new["content"][i]["to"]["id"]
                n.toID = new["content"][i]["to"]["id"]
                print n.toID
            if "from" in new["content"][i] and type(new["content"][i]["from"]) is not int:
                print "from is in"
                print new["content"][i]["from"]["id"]
                n.fromID = new["content"][i]["from"]["id"]
                print n.fromID
            vectorNews.append(n)
    return vectorNews,0;

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
    urlOffset = endPoint.urlNews
    code,ans = callAPI(urlOffset,"",header)
    if code != 200:
        return code,"Error"
    totalNews = ans["meta"]["list"]["total"]
    newsVector = []
    newSeason = False
    for new in range(0,len(ans["data"])):
        news,reset = readNews(ans["data"][new])
        newsVector = newsVector + news
        if reset:
            newSeason = True
    n = newsVector[0]
    print n.type
    print n.price
    print n.amount
    print n.fromID
    print n.toID
    urlOffset = endPoint.urlNews+"&offset="+str(i)
    print urlOffset
    while ( i < totalNews and not newSeason ):

        i += 10
        urlOffset = endPoint.urlNews+"&offset="+str(i)
        print urlOffset
        code,ans = callAPI(urlOffset,"",header)
        for new in range(0,len(ans["data"])):
            news,reset = readNews(ans["data"][new])
            newsVector = newsVector + news
            if reset:
                newSeason = True
        if code != 200:
            return code,"Error"

    #Ask news until arrive to new season
    print len(newsVector)
    ans = []
    for i in reversed(newsVector):
        ans.append(i)
    return code,newsVector

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
        a.money = 20000000
        playerVector.append(a)
        i += 1

    return code,playerVector





