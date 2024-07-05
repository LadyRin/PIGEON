import requests
from django.conf import settings

class Booker:
    session_token = None
    user_id = None

    def authenticate(self, username, password):
        url = settings.LIBREBOOKING_URL + "/Web/Services/Authentication/Authenticate"
        payload = {
            "username": username,
            "password": password
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