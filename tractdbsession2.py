import json
import requests
import base64

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
        'refresh_token': 'c65d079aafaeca913377f8916236932b36bbeca2a8876ffc7ac4941db2a0a41e',
        'redirect_uri': 'https://tractdb.org/configure/fitbit/callback'
    }
)

# part 2
# logging in
login = session_fitbit.post(
    '{}/{}'.format(
        'https://tractdb.org/api',
        'login'
    ),
    json = {'account': 'essiecee', 'password': 'zxczxc'}
)

# retrieving all the data from fitbit, currently stored in JSON format
doc_response = session_fitbit.get('https://tractdb.org/api/document/fitbit_tokens')

# trying to obtain the list of tokens under "fitbit_tokens" from the JSON
# by first decoding the JSON into a readable Python object and accessing it
# like a dictionary
doc_decoded = doc_response.json()

print doc_decoded

# obtains the list of tokens from the readable JSON (Python) document and prints it out
list_tokens = doc_decoded["fitbit_tokens"][0]

# places all the list values into a map
fitbittokens_by_id = {
   list_tokens["user_id"]:list_tokens for list_tokens in doc_decoded["fitbit_tokens"]
}

print fitbittokens_by_id

doc_decoded["fitbit_tokens"] = list(fitbittokens_by_id.values())


"""
update = session_fitbit.put(
   "{}/{}/{}".format(
      "https://tractdb.org/api"
      "document",
      "fitbit_tokens"
   ),
   json=doc_decoded
)
"""
# this works, but not the format fogarty wrote- the commented out section
update = session_fitbit.put("https://tractdb.org/api/document/fitbit_tokens", json=doc_decoded)

activitylogs = session_fitbit.get(
   "https://api.fitbit.com/1/user/{}/{}/date/{}/{}.json".format(
      "6Q9B5C",
      "activities/calories",
      "today",
      "30d"
   ),
   headers={
      'Authorization':'Bearer {}'.format(
            'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI2UTlCNUMiLCJhdWQiOiIyMjhSWTkiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJ3aHIgd251dCB3cHJvIHdzbGUgd3dlaSB3c29jIHdhY3Qgd3NldCB3bG9jIiwiZXhwIjoxNTMzMzY4NDk2LCJpYXQiOjE1MzMzMzk2OTZ9.odhYbBzUF9o384LUG7G0rfGp3j1152vfrJFtI9NNeZk'
      )
   }
)
print activitylogs.text
