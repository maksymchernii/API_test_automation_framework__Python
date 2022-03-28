import allure

from requests                               import Response
from datetime                               import datetime
from utils.base_case                        import BaseCase
from utils.assertions                       import Assertions
from utils.requests_manager                 import RequestsManager


@allure.epic("Creation cases.")
class TestUserRegister(BaseCase):

    def setup(self):
        base_part: str = "learnqa"
        domain: str = "example.com"
        random_part: str = datetime.now().strftime("%m%d%Y%H%M%S")
        self.email: str = f"{base_part}{random_part}@{domain}"

    @allure.description("Verify is user created successfully.")
    def test_create_user_successfully(self):
        data: dict = {
            "password": "123",
            "username": "learnqa",
            "firstName": "learnqa",
            "lastName": "learnqa",
            "email": self.email
        }

        response: Response = RequestsManager.post(uri="user/", data=data)

        Assertions.assert_status_code(response=response, expected_status_code=200)
        Assertions.assert_json_has_key(response=response, name="id")

    @allure.description("Verify is user do not created with existing email.")
    def test_create_user_with_existing_email(self):
        email: str = "vinkotov@example.com"
        data: dict = {
            "password": "123",
            "username": "learnqa",
            "firstName": "learnqa",
            "lastName": "learnqa",
            "email": email
        }

        response: Response = RequestsManager.post(uri="user/", data=data)

        Assertions.assert_status_code(response=response, expected_status_code=400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", \
            f"Unexpected response content: \"{response.content}\"."

