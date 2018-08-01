import json
import requests

# starts a session
session = requests.session()
response = session.post(
    '{}/{}'.format(
        'https://tractdb.org/api',
        'login'
    ),
    json = {'account': 'essiecee', 'password': 'zxczxc'}
)
# let's see if this was successful!
print("response code is %s" % response.status_code)

# returns the account name 
returned = session.get('https://tractdb.org/api/authenticated')
print returned.text

# gets the fitbit tokens
tokens = session.get('https://tractdb.org/api/document/fitbit_tokens')
print tokens.text

# prints out the data for a specified activity, like sleep
fitbit_response = session.get(
     'https://api.fitbit.com/1/user/{}/activities/date/{}.json'.format(
         "6Q9B5C",
         '2018-07-06'
     ),
     headers={
         'Authorization':'Bearer {}'.format(
            'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI2UTlCNUMiLCJhdWQiOiIyMjhSWTkiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJ3aHIgd251dCB3cHJvIHdzbGUgd3dlaSB3c29jIHdhY3Qgd3NldCB3bG9jIiwiZXhwIjoxNTMyODU1ODc0LCJpYXQiOjE1MzI4MjcwNzR9.-SBqxdngbZqqC2fCpFHXTYhwfWaI6YrGqRIB1U9fGj0'
         )
     }
)
print fitbit_response.text



