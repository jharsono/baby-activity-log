from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from datetime import datetime, timedelta
import pickle
import unicodedata

scopes = ['https://www.googleapis.com/auth/calendar']

# USE FOR FIRST TIME AUTHENTICATION
# flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", scopes=scopes)
# credentials = flow.run_console()
# pickle.dump(credentials, open("token.pkl", "wb"))

credentials = pickle.load(open("token.pkl", "rb"))

service = build("calendar", "v3", credentials=credentials)

result = service.calendarList().list().execute()
calendar_id = result['items'][0]['id']

last_sleep = pickle.load(open('last_sleep.pkl', 'rb'))

def create_event(summary):
    start_time = datetime.now()
    end_time = start_time + timedelta(minutes=15)
    timezone = 'America/Los_Angeles'
    
    event_data = {
        'summary': summary,
        'start': {
            'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': timezone,
        },
        'end': {
            'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': timezone,
        },
    }
    print 'Added %s' % summary
    new_event = service.events().insert(calendarId=calendar_id, body=event_data).execute()
    if summary is 'sleep':
        sleep_id = {'id': new_event.get('id')}
        last_sleep = pickle.dump(sleep_id, open('last_sleep.pkl','wb'))
        sleep_obj = pickle.load(open('last_sleep.pkl', 'rb'))
        print sleep_obj['id']



def end_sleep():
    print 'ending sleep id %s' % last_sleep['id']
    end_time = datetime.now() + timedelta(hours=3)
    
    last_sleep_event = service.events().get(calendarId=calendar_id, eventId=last_sleep['id']).execute()
    start_time = unicodedata.normalize('NFKD', last_sleep_event['start']['dateTime']).encode('ascii', 'ignore')
    event_data = {
        'end': {
            'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
        },
        'start': {
            'dateTime': start_time,
        },
    }
    
    print event_data
    
    event = service.events().patch(calendarId=calendar_id, eventId=last_sleep['id'], body=event_data).execute()
    new_end_time = event.get('end')['dateTime']
    print 'Sleep ended at %s' % new_end_time
    
# create_event('eat')
# create_event('sleep')
# end_sleep()