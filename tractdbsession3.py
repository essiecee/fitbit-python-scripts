import json
import requests
import base64
from dateutil.relativedelta import relativedelta
from datetime import timedelta, date, datetime

# token renewal using the refresh token instead of manually signing in on tractdb
session_fitbit = requests.session()

# this changes each time the access token expires
access_token = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI2UTlCNUMiLCJhdWQiOiIyMjhSWTkiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJ3aHIgd3BybyB3bnV0IHdzbGUgd3dlaSB3c29jIHdzZXQgd2FjdCB3bG9jIiwiZXhwIjoxNTM2ODAwMDc5LCJpYXQiOjE1MzY3NzEyNzl9.I2EW0CVyoxn7Cufj7UJIPRJL-zpVS22p2_f_aYKGtv4"
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

login = session_fitbit.post(
    '{}/{}'.format(
        'https://tractdb.org/api',
        'login'
    ),
    json={
       'account': 'essiecee',
       'password': 'zxczxc'
    }
)

first_active = session_fitbit.get(
   "https://api.fitbit.com/1/user/{}/profile.json".format(
      "6Q9B5C"
   ),
   headers={
      'Authorization':'Bearer {}'.format(
            access_token
      )
   }
)
memberStart = first_active.json()["user"]["memberSince"]

print("user has been a member since %s" % memberStart)

today = date.today()
print("today's date is %s" % today)

# printing out the months between memberSince and today 
memberStart_datetime = datetime.strptime(memberStart, '%Y-%m-%d').date()

last_updated = session_fitbit.get(
   "{}/{}/{}".format(
      "https://tractdb.org/api",
      "document",
      "fitbit-6Q9B5C-activity-and-sleep-importstatus"
   )
)
if (last_updated.status_code == 200):
   last_updated_stringform = last_updated.json()["lastImportedDate"]
   print("last updated on %s" % last_updated_stringform)
   last_updated_dateform = datetime.strptime(last_updated_stringform, '%Y-%m-%d').date()
   start_update = last_updated_dateform + timedelta(days=1)
   cur_date = start_update
else:
   cur_date = datetime.strptime(memberStart, '%Y-%m-%d').date()

stack_of_dates = []
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
            access_token
         )
      }
   )
   
   for day in month_summary.json()["activities-calories"]:
      stack_of_dates.append(day["dateTime"])
      for x in ["activities", "sleep"]:
         if x == "activities":
               track = 1.2
         else:
               track = 1
         daily_summary = session_fitbit.get(
            "https://api.fitbit.com/{}/user/{}/{}/date/{}.json".format(
               track,
               "6Q9B5C",
               x, 
               day["dateTime"]
            ),
            headers={
               'Authorization':'Bearer {}'.format(
                     access_token
               )
            }
         )
         doc_daily_name = "fitbit-{}-{}-{}".format(
            "6Q9B5C",
            x,
            day["dateTime"]
         )
         print("DOC DAILY NAME IS %s" % doc_daily_name)
         document_retrieval = session_fitbit.get(
               "https://tractdb.org/api/document/{}".format(
               doc_daily_name
            ),
         )
         # if the document does not exist, the status code that will be returned is 404
         # inversely, if the document does exist, it will return a status code of 200
         if (document_retrieval.status_code == 404):
            update = session_fitbit.put(
               "{}/{}/{}".format(
                  "https://tractdb.org/api",
                  "document",
                  doc_daily_name
               ),
               json=daily_summary.json()
            )
   # for loop ends here         
   cur_date += relativedelta(months=1)  
   
if len(stack_of_dates) != 0:
   print(stack_of_dates)
   most_recent = stack_of_dates.pop()
   print("MOST RECENT DATE IS %s" % most_recent)
   document_last_imported = "fitbit-{}-activity-and-sleep-importstatus".format(
      "6Q9B5C",
   )
   print("document last imported name is %s" % document_last_imported)
   
   lastdateupdate = session_fitbit.put(
      "{}/{}/{}".format(
         "https://tractdb.org/api",
         "document",
         document_last_imported
      ),
      json={"lastImportedDate": most_recent}
   )
