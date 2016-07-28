#!/usr/bin/python2

from httplib2 import Http
import urllib2
import json
import comuniame
import getpass

my_mail = raw_input("Mail: ")
my_pass = getpass.getpass("Pass: ")
# my_mail = ""
# my_pass = ""
data = {
        'email':my_mail,
        'password':my_pass
}

# jsondata = json.dumps(data).encode('utf-8')
# print (jsondata)

print "Login..."
code,token = comuniame.auth(my_mail,my_pass)
if code != 200:
  print "Error on login"
else:
  print "Successful"

print "Asking for actual league id..."
code,league_id = comuniame.getLeagueID(token)
print code

print "Going to ask market..."
code,market = comuniame.getMarket(token,league_id)
print code

# req = urllib2.Request(url)
# req.add_header('Content-Type', 'application/json;charset=utf-8')
# response = urllib2.urlopen(req,jsondata)
# print response.geturl()
# print response.info()
# print response.getcode()
# html = response.read()
# print html
# json_obj = json.loads(html)
# token = json_obj["token"];
# print token


# #got the token, ask for info
# url_account_info = 'http://app.comunia.me/api/v1/account'
# req = urllib2.Request(url_account_info)
# req.add_header("Authorization", "Bearer %s" %token)
# response = urllib2.urlopen(req)
# json_obj = json.loads(response.read())


# # print json.dumps(json_obj["data"], indent=5, sort_keys=True)
# league_id =json_obj["data"]["leagues"][0]["id"]
# # print json.dumps(json_obj["data"]["leagues"][0]["id"], indent=5, sort_keys=True)

# #to get home:
# # url_account_info = 'http://app.comunia.me/api/v1/home'
# # #to get market:
# url_account_info = 'http://app.comunia.me/api/v1/market'

# req = urllib2.Request(url_account_info)
# req.add_header("Authorization", "Bearer %s" %token)

# #Header not needed
# req.add_header("Referer", "http://app.comunia.me/market")

# #Needed for all but account call, DUNNO, this is league_ID, at some point
# # will change
# req.add_header("X-League", league_id)
# print req
# response = urllib2.urlopen(req)
# html = response.read()
# json_obj = json.loads(html)
# print json_obj
