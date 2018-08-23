import json
import requests
import base64
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datetime import timedelta

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
        'refresh_token': 'fc3b61cf8159197778fb701e23618a8f4abce165ef82ce0abf9854edfcdab94d',
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
            'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI2UTlCNUMiLCJhdWQiOiIyMjhSWTkiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJ3aHIgd3BybyB3bnV0IHdzbGUgd3dlaSB3c29jIHdzZXQgd2FjdCB3bG9jIiwiZXhwIjoxNTM1MDIzMDY1LCJpYXQiOjE1MzQ5OTQyNjV9.OPyVxm2XaqgjMRc4bMgOn_yIcjcn-YDNrsZmjBwot6Y'
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
end_date = today
while cur_date < today:
   print(cur_date.strftime("%m/%y"))
   month_summary = session_fitbit.get(
      "https://api.fitbit.com/1/user/{}/{}/date/{}/{}".format(
         "6Q9B5C",
         "activities/calories",
         cur_date,
         end_date
      ),
      headers={
      'Authorization':'Bearer {}'.format(
            'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI2UTlCNUMiLCJhdWQiOiIyMjhSWTkiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJ3aHIgd3BybyB3bnV0IHdzbGUgd3dlaSB3c29jIHdzZXQgd2FjdCB3bG9jIiwiZXhwIjoxNTM1MDIzMDY1LCJpYXQiOjE1MzQ5OTQyNjV9.OPyVxm2XaqgjMRc4bMgOn_yIcjcn-YDNrsZmjBwot6Y'
         )
      }
   )
   print month_summary.text
   cur_date += relativedelta(months=1)
   end_date = cur_date

