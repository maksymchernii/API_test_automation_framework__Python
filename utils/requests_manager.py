import requests
import allure

from requests                   import Response
from utils.logger               import Logger
from environment                import ENV_OBJECT


class RequestsManager:

    @staticmethod
    def post(uri: str, data: dict = None, headers: dict = None, cookies: dict = None) -> Response:
        with allure.step(f"POST request to URI: \"{uri}\""):
            return RequestsManager._send(uri=uri, data=data, headers=headers, cookies=cookies, method="POST")

    @staticmethod
    def put(uri: str, data: dict = None, headers: dict = None, cookies: dict = None) -> Response:
        with allure.step(f"PUT request to URI: \"{uri}\""):
            return RequestsManager._send(uri=uri, data=data, headers=headers, cookies=cookies, method="PUT")

    @staticmethod
    def delete(uri: str, data: dict = None, headers: dict = None, cookies: dict = None) -> Response:
        with allure.step(f"DELETE request to URI: \"{uri}\""):
            return RequestsManager._send(uri=uri, data=data, headers=headers, cookies=cookies, method="DELETE")

    @staticmethod
    def get(uri: str, data: dict = None, headers: dict = None, cookies: dict = None) -> Response:
        with allure.step(f"GET request to URI: \"{uri}\""):
            return RequestsManager._send(uri=uri, data=data, headers=headers, cookies=cookies, method="GET")

    @staticmethod
    def _send(uri: str, data: dict, headers: dict, cookies: dict, method: str) -> Response:
        url = f"{ENV_OBJECT.get_base_url()}/{uri}"

        if headers is None:
            headers = {}

        if cookies is None:
            cookies = {}

        if method not in ("GET", "POST", "PUT", "DELETE"):
            raise Exception(f"Bad HTTP method \"{method}\" was received.")

        Logger.add_request(url=url, data=data, headers=headers, cookies=cookies, method=method)

        if method == "GET":
            response = requests.get(url, params=data, headers=headers, cookies=cookies)

        if method == "POST":
            response = requests.post(url, data=data, headers=headers, cookies=cookies)

        if method == "PUT":
            response = requests.put(url, data=data, headers=headers, cookies=cookies)

        if method == "DELETE":
            response = requests.delete(url, data=data, headers=headers, cookies=cookies)

        Logger.add_response(response=response)

        return response
