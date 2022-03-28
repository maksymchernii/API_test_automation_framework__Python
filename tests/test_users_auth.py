import pytest
import allure

from requests import Response, Request
from utils.base_case import BaseCase
from utils.assertions import Assertions
from utils.requests_manager import RequestsManager


@allure.epic("Authorization cases.")
class TestUsersAuth(BaseCase):
    EXCLUDE_PARAMS: list = [
        ("no_cookie"),
        ("no_token")
    ]

    def setup(self):
        data: dict = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }

        response: Response = RequestsManager.post(uri="user/login", data=data)

        self.auth_sid: str = self.get_cookie(response=response, cookie_name="auth_sid")
        self.token: str = self.get_header(response=response, headers_name="x-csrf-token")
        self.user_id_from_auth_endpoint: str = self.get_json_value(response=response, name="user_id")

        self.headers: dict = {"x-csrf-token": self.token}
        self.cookies: dict = {"auth_sid": self.auth_sid}

    @allure.description("Verify is user do auth successfully.")
    def test_auth_user(self):
        response: Response = RequestsManager.get(uri="user/auth", headers=self.headers, cookies=self.cookies)

        Assertions.assert_json_value_by_name(
            response=response,
            name="user_id",
            expected_value=self.user_id_from_auth_endpoint,
            error_message="User id from auth endpoint is not equal to user id from check endpoint"
        )

    @allure.description("Verify auth status w/o sending auth cookie or token.")
    @pytest.mark.parametrize("condition", EXCLUDE_PARAMS)
    def test_negative_auth_check(self, condition):
        response: Response = \
            RequestsManager.get(uri="user/auth", headers=self.headers) if condition == "no_cookie" \
            else RequestsManager.get(uri="user/auth", cookies=self.cookies)

        Assertions.assert_json_value_by_name(
            response=response,
            name="user_id",
            expected_value=0,
            error_message=f"User is authorize with condition {condition}."
        )
