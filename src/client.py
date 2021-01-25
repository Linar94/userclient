import aiohttp

from abc import ABCMeta
from dataclasses import dataclass
from typing import Optional, Dict


user_info_resp_json_success = {
    "status": "OK",
    "active": "1",
    "blocked": False,
    "created_at": 1587457590,
    "id": 23,
    "name": "Ivanov Ivan",
    "permissions": [
        {"id": 1, "permission": "comment"},
        {"id": 2, "permission": "upload photo"},
        {"id": 3, "permission": "add event"}
    ]
}


auth_token_resp_json_success = {"status": "OK", "token": "dsfd79843r32d1d3dx23d32d"}


@dataclass
class ApiClient:
    base_url: str

    async def fetch(self, method: str, path: str, params: Optional[Dict] = None, body: Optional[Dict] = None,
                    headers: Optional[Dict] = None):
        full_url = self.base_url + path

        _params, _body = {}, {}
        if params:
            _params.update(params)
        if body:
            _body.update(body)

        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.request(method, full_url, params=_params, json=_body) as response:
                # if path == 'auth':
                #     return 200, auth_token_resp_json_success
                # elif 'get-user' in path:
                #     return 200, user_info_resp_json_success
                # else:
                #     return 200, {"status": "OK"}
                return response.status, await response.json()


class BaseApi(metaclass=ABCMeta):
    api_client: ApiClient

    def __init__(self, base_url: str):
        self.api_client = ApiClient(base_url)
