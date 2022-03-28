import json.decoder

from requests import Response


class Assertions:

    @staticmethod
    def assert_json_value_by_name(
            response: Response, name: str, expected_value: (str, int), error_message: str) -> None:

        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            raise f"Response in not in JSON Format. Response text is \"{response.text}\"."

        assert name in response_as_dict, f"Response JSON doesn't have key \"{name}\"."
        assert response_as_dict[name] == expected_value, error_message

    @staticmethod
    def assert_json_has_key(response: Response, name: str) -> None:

        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            raise f"Response in not in JSON Format. Response text is \"{response.text}\"."

        assert name in response_as_dict, f"Response JSON doesn't have key \"{name}\"."

    @staticmethod
    def assert_status_code(response: Response, expected_status_code: int) -> None:
        assert response.status_code == expected_status_code, \
            f"Unexpected status code. Expected: \"{expected_status_code}\". Actual: \"{response.status_code}\"."
