import json
import requests
import base64
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta

# token renewal
session_fitbit = requests.session()

response = session_fitbit.post(
    'https://api.fitbit.com/oauth2/token',
    headers={
        'Authorization':
            'Basic {}'.format(
                base64.b64encode('{}:{}'.format(
                    '228RY9','4dd4118872d1497da1d253a16b13fb50'
                ).encode('utf-8')).decode('utf-8')
            )
    },
    data={
        'grant_type': 'refresh_token',
        'refresh_token': '02082c3183c4581a775402ad17d9bc08906b57ee0bfd7cfdcd8572196fa6aaf7',
        'redirect_uri': 'https://tractdb.org/configure/fitbit/callback'
    }
)
# prints out a new set of tokens that can be used (access and refresh tokens)
print response.text

# logging in
login = session_fitbit.post(
    '{}/{}'.format(
        'https://tractdb.org/api',
        'login'
    ),
    json = {'account': 'essiecee', 'password': 'zxczxc'}
)

first_active = session_fitbit.get(
   "https://api.fitbit.com/1/user/{}/profile.json".format(
      "6Q9B5C"
   ),
   headers={
      'Authorization':'Bearer {}'.format(
            'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI2UTlCNUMiLCJhdWQiOiIyMjhSWTkiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJ3aHIgd251dCB3cHJvIHdzbGUgd3dlaSB3c29jIHdzZXQgd2FjdCB3bG9jIiwiZXhwIjoxNTM1MDE5NTYxLCJpYXQiOjE1MzQ5OTA3NjF9.oB0rxKx-CX_sr3y4yrY2xHLzZxcFPweC0u3OsKuDFyM'
      )
   }
)
   
memberStart = first_active.json()["user"]["memberSince"]

print("user has been a member since %s" % memberStart)
# memberStart is currently in the format of 2018-06-22, a string

today = date.today();
print("today's date is %s" % today)

# printing out the months between memberSince and today 

cur_date = datetime.strptime(memberStart, '%Y-%m-%d').date()

while cur_date < today:
   print(cur_date.strftime("%m/%y"))
   cur_date += relativedelta(months=1)
