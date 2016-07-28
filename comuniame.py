#!/usr/bin/python

import urllib2
import json

globalToken = 0;

class endPoint:
    urlAuth = 'http://app.comunia.me/api/v3/auth/login'
    urlHome = 'http://app.comunia.me/api/v1/home'
    urlAccount = 'http://app.comunia.me/api/v1/account'
    urlMarket = 'http://app.comunia.me/api/v1/market'

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
    header = [("Authorization", "Bearer %s" % token)]
    code,ans = callAPI(endPoint.urlAccount,"",header)
    if code == 200:
        league_id =ans["data"]["leagues"][0]["id"]
    else:
        league_id = -1
    return code,league_id


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
    header = [("Authorization", "Bearer %s" % token), ("X-League", league_id)]
    code,ans = callAPI(endPoint.urlMarket,"",header)
    return code,ans
