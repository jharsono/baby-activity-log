import pickle
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from datetime import datetime, timedelta


class GcalApiClient:
    def __init__(self, path_to_secret, path_to_token):
        self.path_to_secret = '../%s' % path_to_secret
        self.path_to_token = '../%s' % path_to_token
        self.service = None
        self.calendar_id = None

        self.set_credentials()

        self.last_sleep = self.get_last_sleep()

    def set_credentials(self):
        scopes = ['https://www.googleapis.com/auth/calendar']

        try:
            credentials = pickle.load(open(os.path.abspath(os.path.join(
                os.path.dirname(__file__), self.path_to_token)), "rb"))
        except:
            flow = InstalledAppFlow.from_client_secrets_file(os.path.abspath(os.path.join(
                os.path.dirname(__file__), self.path_to_secret)), scopes=scopes)
            credentials = flow.run_console()
            pickle.dump(credentials, open(os.path.abspath(os.path.join(
                os.path.dirname(__file__), self.path_to_token)), "wb"))

        self.service = build("calendar", "v3", credentials=credentials)

        result = self.service.calendarList().list().execute()
        self.calendar_id = result['items'][0]['id']

    def create_event(self, summary):
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
        print('Added %s' % summary)
        try:
            new_event = self.service.events().insert(
                calendarId=self.calendar_id,
                body=event_data).execute()

            if summary == 'sleep':
                sleep_obj = {
                    'id': new_event['id'],
                    'start': new_event['start']['dateTime']
                }
                print(sleep_obj)

                self.last_sleep = sleep_obj
            return new_event
        except:
            return False

    def get_last_sleep(self):
        last_sleep_query = self.service.events().list(
                calendarId=self.calendar_id,
                q='sleep',
                singleEvents=True,
                orderBy="startTime"
            ).execute()
        last_sleep_item = last_sleep_query['items'][-1]
        print(last_sleep_item)
        last_sleep_obj = {
            'id': last_sleep_item['id'],
            'start': last_sleep_item['start']['dateTime']
        }
        return last_sleep_obj

    def end_sleep(self):
        print('ending sleep id %s' % self.last_sleep['id'])
        end_time = datetime.now()

        start_time = self.last_sleep['start']
        event_data = {
            'end': {
                'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
            },
            'start': {
                'dateTime': start_time,
            },
        }
        try:
            event = self.service.events().patch(
                calendarId=self.calendar_id,
                eventId=self.last_sleep['id'],
                body=event_data).execute()

            new_end_time = event.get('end')['dateTime']
            return 'Sleep ended at %s' % new_end_time
        except:
            return False

    # Last sleep scheduled task
    def set_last_sleep(self):
        try:
            last_sleep = self.get_last_sleep()
            self.last_sleep = last_sleep
            return last_sleep
        except:
            print('error setting last sleep')
            return False
