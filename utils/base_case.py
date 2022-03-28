import json.decoder

from requests import Response


class BaseCase(object):

    @staticmethod
    def get_cookie(response: Response, cookie_name: str) -> str:
        assert cookie_name in response.cookies, f"Cannot find cookie with name {cookie_name} in the last response."
        return response.cookies[cookie_name]

    @staticmethod
    def get_header(response: Response, headers_name: str) -> str:
        assert headers_name in response.headers, f"Cannot find header with name {headers_name} in the last response."
        return response.headers[headers_name]

    @staticmethod
    def get_json_value(response: Response, name: str) -> str:
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            raise f"Response is not in JSON Format. Response text is {response.text}."

        assert name in response_as_dict, f"Response JSON dosn't have key \"{name}\"."
        return response_as_dict[name]
