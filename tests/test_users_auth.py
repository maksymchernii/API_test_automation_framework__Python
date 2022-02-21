import pytest
import requests

from utils.base_case import BaseCase
from utils.assertions import Assertions


class TestUsersAuth(BaseCase):
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

        self.auth_sid = self.get_cookie(response=response, cookie_name="auth_sid")
        self.token = self.get_header(response=response, headers_name="x-csrf-token")
        self.user_id_from_auth_endpoint = self.get_json_value(response=response, name="user_id")

        self.headers = {"x-csrf-token": self.token}
        self.cookies = {"auth_sid": self.auth_sid}

    def test_auth_user(self):
        response = requests.get(url=self.check_user_auth_url, headers=self.headers, cookies=self.cookies)
        Assertions.assert_json_value_by_name(
            response=response,
            name="user_id",
            expected_value=self.user_id_from_auth_endpoint,
            error_message="User id from auth endpoint is not equal to user id from check endpoint"
        )

    @pytest.mark.parametrize("condition", exclude_params)
    def test_negative_auth_check(self, condition):
        response = \
            requests.get(url=self.check_user_auth_url, headers=self.headers) if condition == "no_cookie" \
            else requests.get(url=self.check_user_auth_url, cookies=self.cookies)

        Assertions.assert_json_value_by_name(
            response=response,
            name="user_id",
            expected_value=0,
            error_message=f"User is authorize with condition {condition}."
        )
