import json.decoder

from requests               import Response
from typing                 import Any, AnyStr


class Assertions:

    @staticmethod
    def assert_json_value_by_name(
            response: Response,
            name: AnyStr,
            expected_value: Any,
            error_message: AnyStr
    ) -> None:
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            raise f"Response in not in JSON Format. Response text is \"{response.text}\"."

        assert name in response_as_dict, f"Response JSON doesn't have key \"{name}\"."
        assert response_as_dict[name] == expected_value, error_message
