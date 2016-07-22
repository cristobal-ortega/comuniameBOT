#!/usr/bin/python2

from httplib2 import Http
import urllib2
import json
my_mail = ""
my_pass = ""
data = {
        'email':my_mail,
        'password':my_pass
}
jsondata = json.dumps(data).encode('utf-8')
print (jsondata)

url = 'http://app.comunia.me/api/v1/auth/login'
req = urllib2.Request(url)
req.add_header('Content-Type', 'application/json;charset=utf-8')
response = urllib2.urlopen(req,jsondata)
print response.geturl()
print response.info()
print response.getcode()
html = response.read()
print html
json_obj = json.loads(html)
token = json_obj["token"];
print token


#got the token, ask for info
# url_account_info = 'http://app.comunia.me/api/v1/account'
#to get home:
url_account_info = 'http://app.comunia.me/api/v1/home'
#to get market:
url_account_info = 'http://app.comunia.me/api/v1/market'

req = urllib2.Request(url_account_info)
req.add_header("Authorization", "Bearer %s" %token)

#Header not needed
req.add_header("Referer", "http://app.comunia.me/market")

#Needed for all but account call, DUNNO
req.add_header("X-League", "154483")
print req
response = urllib2.urlopen(req)
html = response.read()
json_obj = json.loads(html)
print json_obj
