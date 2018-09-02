import json
import requests
import base64
from dateutil.relativedelta import relativedelta
from datetime import timedelta, date, datetime

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
        'refresh_token': 'afa3a6319b45623d58cba0daa758068c85ac837975a31861ae0a7348d9aefe28',
        'redirect_uri': 'https://tractdb.org/configure/fitbit/callback'
    }
)
# prints out a new set of tokens that can be used (access and refresh tokens)
print response.text

first_active = session_fitbit.get(
   "https://api.fitbit.com/1/user/{}/profile.json".format(
      "6Q9B5C"
   ),
   headers={
      'Authorization':'Bearer {}'.format(
            'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI2UTlCNUMiLCJhdWQiOiIyMjhSWTkiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJ3aHIgd251dCB3cHJvIHdzbGUgd3dlaSB3c29jIHdhY3Qgd3NldCB3bG9jIiwiZXhwIjoxNTM1OTQwNzQ3LCJpYXQiOjE1MzU5MTE5NDd9.uhAligiaeAZ0byZKlLGQ91LgxGcOPUEN1qlhbyQi7IE'
      )
   }
)
   
memberStart = first_active.json()["user"]["memberSince"]

print("user has been a member since %s" % memberStart)

today = date.today()
print("today's date is %s" % today)

# printing out the months between memberSince and today 
memberStart_datetime = datetime.strptime(memberStart, '%Y-%m-%d').date()
cur_date = datetime.strptime(memberStart, '%Y-%m-%d').date()

while cur_date.month < today.month:
   print(cur_date.strftime("%m/%Y"))
   if cur_date.month == memberStart_datetime.month:
      beginning_date_day = memberStart_datetime.day
      next_month = memberStart_datetime.replace(day=28) + timedelta(days=4)
   else:
      end_date = cur_date + relativedelta(months=1)
      beginning_date_day = "01"
      next_month = cur_date.replace(day=28) + timedelta(days=4)
   end_date = next_month - timedelta(days=next_month.day)
   month_summary = session_fitbit.get(
      "https://api.fitbit.com/1/user/{}/{}/date/{}-0{}-{}/{}.json".format(
         "6Q9B5C",
         "activities/calories",
          cur_date.year,
          cur_date.month,
          beginning_date_day,
          end_date
      ),
      headers={
      'Authorization':'Bearer {}'.format(
            'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI2UTlCNUMiLCJhdWQiOiIyMjhSWTkiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJ3aHIgd251dCB3cHJvIHdzbGUgd3dlaSB3c29jIHdhY3Qgd3NldCB3bG9jIiwiZXhwIjoxNTM1OTQwNzQ3LCJpYXQiOjE1MzU5MTE5NDd9.uhAligiaeAZ0byZKlLGQ91LgxGcOPUEN1qlhbyQi7IE'
         )
      }
   )
   for day in month_summary.json()["activities-calories"]:
      print day
   cur_date += relativedelta(months=1)

