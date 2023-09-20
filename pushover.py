import http.client, urllib
conn = http.client.HTTPSConnection("api.pushover.net:443")
conn.request("POST", "/1/messages.json",
  urllib.parse.urlencode({
    "token": "an1dqxb4ejf1rjdpxq7ofopvzm31f7",
    "user": "uf1kmr522vv4x6gm76fj9g96s67qwo",
    "message": "hello world",
  }), { "Content-type": "application/x-www-form-urlencoded" })
conn.getresponse()
