import requests

from .constants import API_OFF_PARAMS as params
from .constants import API_OFF_URL as url


class Download:
    def __init__(self):
        pass

    def raw_data(self, page):
        params['page'] = page
        try:
            raw_data = requests.get(url, params=params).json()
            return raw_data['products']
        except requests.exceptions.HTTPError:
            print("Http Error")
            raise SystemExit()
        except requests.exceptions.ConnectionError:
            print("Error Connecting")
            raise SystemExit()
        except requests.exceptions.Timeout:
            print("Timeout Error")
            raise SystemExit()
        except requests.exceptions.RequestException:
            print("error")
            raise SystemExit()
