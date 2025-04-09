import requests


class APIClient:
    BASE_URL = "http://127.0.0.1:8000/api/transactions"

    @staticmethod
    def fetch_data(endpoint, params={}):
        """Generic API request handler"""
        url = f"{APIClient.BASE_URL}/{endpoint}"
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"API Error [{endpoint}]: {e}")
            return None  # Return None if API fails
