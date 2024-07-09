import requests
from django.conf import settings
import json
from datetime import datetime
import pytz

class Booker:
    session_token = None
    user_id = None

    def authenticate(self):
        url = settings.LIBREBOOKING_URL + "/Web/Services/Authentication/Authenticate"
        payload = {
            "username": settings.LIBREBOOKING_USERNAME,
            "password": settings.LIBREBOOKING_PASSWORD,
        }
        response = requests.post(url, json=payload)
        try:
            response.raise_for_status()
            response_json = response.json()
            self.session_token = response_json["sessionToken"]
            self.user_id = response_json["userId"]
        except requests.exceptions.HTTPError as e:
            print(e)
            print(response.text)
            raise e

    def get_headers(self):
        return {
            "X-Booked-SessionToken": self.session_token,
            "X-Booked-UserId": self.user_id,
            "X-LibreBooking-SessionToken": self.session_token,
            "X-LibreBooking-UserId": self.user_id,
        }

    def sign_out(self):
        url = settings.LIBREBOOKING_URL + "/Web/Services/Authentication/SignOut"
        headers = self.get_headers()
        response = requests.post(url, headers=headers)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(e)
            print(response.text)
        self.session_token = None
        self.user_id = None

    def get_all_resources(self):
        url = settings.LIBREBOOKING_URL + "/Web/Services/Resources"
        headers = self.get_headers()
        response = requests.get(url, headers=headers)
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(e)
            print(response.text)
            raise e
        
    def book_resource(self, resource_id, title, start_time: datetime, end_time: datetime):
        url = settings.LIBREBOOKING_URL + "/Web/Services/Reservations/"
        headers = self.get_headers()
        payload = {
            "resourceId": resource_id,
            "resources": [
                resource_id
            ],
            "description": "Booked by Pigeon",
            "startDateTime": start_time.astimezone(pytz.utc).isoformat(),
            "endDateTime": end_time.astimezone(pytz.utc).isoformat(),
            "title": title,
            "userId": self.user_id,
            "allowParticipation": True,
            "termsAccepted": True,
        }
        response = requests.post(url, headers=headers, json=payload)
        try:
            response.raise_for_status()
            print(json.dumps(payload, indent=4))
            print(json.dumps(response.json(), indent=4))
            return response.json()['referenceNumber']
        except requests.exceptions.HTTPError as e:
            print(e)
            print(response.text)
            raise e
        
    def unbook(self, reservation_id):
        url = settings.LIBREBOOKING_URL + f"/Web/Services/Reservations/{reservation_id}"
        headers = self.get_headers()
        response = requests.delete(url, headers=headers)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(e)
            print(response.text)
            raise e
        
    def is_available(self, resource_id, start_date_time, end_date_time):
        url = settings.LIBREBOOKING_URL + "/Web/Services/Resources/Availability"

        headers = self.get_headers()
        query_params = {
            "dateTime": start_date_time.astimezone(pytz.utc).isoformat(),
        }
        response = requests.get(url, headers=headers, params=query_params)

        try:
            response.raise_for_status()
            jsonr = response.json()
        except requests.exceptions.HTTPError as e:
            print(e)
            print(response.text)
            raise e
        
        resources = jsonr['resources'][0]
        def find_resource(resource_id):
            for element in resources:
                if element['resource']['resourceId'] == str(resource_id):
                    return element
            return None
        
        print(json.dumps(resources, indent=4))
                
        resource = find_resource(resource_id)
        if resource is None:
            print("Resource not found")
            return False
        
        available = resource['available']
        available_until = resource['availableUntil']
        available_at = resource['availableAt']

        start_ok = available_at is None or start_date_time >= datetime.fromisoformat(available_at)
        end_ok = end_date_time <= datetime.fromisoformat(available_until)

        if available and start_ok and end_ok:
            print("Resource is available")
        else:
            print("Resource is not available")
        return available and start_ok and end_ok
        
        

    