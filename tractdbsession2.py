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
        'refresh_token': '1ba7724ac3e501a94deb8dc6be3d1ee2ac3ffef0fb8895645efc16db5e47ece8',
        'redirect_uri': 'https://tractdb.org/configure/fitbit/callback'
    }
)

print response.text

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

# obtains the list of tokens from the readable JSON (Python) document and prints it out
list_tokens = doc_decoded["fitbit_tokens"][0]

# places all the list values into a map
fitbittokens_by_id = {
   list_tokens["user_id"]:list_tokens for list_tokens in doc_decoded["fitbit_tokens"]
}

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
            'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI2UTlCNUMiLCJhdWQiOiIyMjhSWTkiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJ3aHIgd251dCB3cHJvIHdzbGUgd3dlaSB3c29jIHdhY3Qgd3NldCB3bG9jIiwiZXhwIjoxNTMzNjAzNDUwLCJpYXQiOjE1MzM1NzQ2NTB9.R0pmd7zf8cBvw9sZBd8Ye0CCnwEfGo7In8hzeKHv3mc'
      )
   }
)
print activitylogs.text
