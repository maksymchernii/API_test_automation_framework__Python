import pytest
import requests


class TestUsersAuth:
    exclude_params = [
        ("no_cookie"),
        ("no_token")
    ]

    def setup(self):
        self.login_url = "https://playground.learnqa.ru/api/user/login"
        self.check_user_auth_url = "https://playground.learnqa.ru/api/user/auth"

        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }

        response = requests.post(url=self.login_url, data=data)
        assert "auth_sid" in response.cookies, "There is no auth cookie in the response."
        assert "x-csrf-token" in response.headers, "There is no CSRF token header in the response."
        assert "user_id" in response.json(), "There is no user id in the response."

        self.auth_sid = response.cookies.get("auth_sid")
        self.token = response.headers.get("x-csrf-token")
        self.user_id_from_auth_endpoint = response.json()["user_id"]
        self.headers = {"x-csrf-token": self.token}
        self.cookies = {"auth_sid": self.auth_sid}

    def test_auth_user(self):
        response = requests.get(url=self.check_user_auth_url, headers=self.headers, cookies=self.cookies)

        assert "user_id" in response.json(), "There is no user_id in the second response."
        user_id_from_check_endpoint = response.json()["user_id"]

        assert self.user_id_from_auth_endpoint == user_id_from_check_endpoint, \
            "User id from auth endpoint is not equal to User id from check endpoint."

    @pytest.mark.parametrize("condition", exclude_params)
    def test_negative_auth_check(self, condition):
        response = \
            requests.get(url=self.check_user_auth_url, headers=self.headers) if condition == "no_cookie" \
            else requests.get(url=self.check_user_auth_url, cookies=self.cookies)

        assert "user_id" in response.json(), "There is no user id in the second response."

        user_id_from_check_endpoint = response.json()["user_id"]
        assert user_id_from_check_endpoint == 0, f"User is authorize with condition {condition}."
