import asyncio

import enum
from dataclasses import dataclass
from typing import List, Optional


from src.client import BaseApi


class STATUS(str, enum.Enum):
    OK = 'OK'
    ERROR = 'Error'
    NOT_FOUND = 'Not found'


@dataclass
class UserAuthModel:
    login: str = 'test'
    pswd: str = '12345'


@dataclass
class TokenModel:
    status: STATUS
    token: Optional[str] = None


@dataclass
class PermissionsModel:
    id: int
    permission: str


@dataclass
class UserInfoModel:
    status: STATUS
    active: Optional[str] = None
    blocked: Optional[bool] = None
    created_at: Optional[int] = None
    id: Optional[int] = None
    name: Optional[str] = None
    permissions: Optional[List[PermissionsModel]] = None


@dataclass
class CommonModel:
    status: STATUS


class UserApi(BaseApi):
    async def get_auth_token(self, login: str, pswd: str) -> TokenModel:
        status_code, content = await self.api_client.fetch("get", "auth", params={'login': login, 'pass': pswd})
        return status_code, TokenModel(**content)

    async def get_user_info(self, username: str, token: str) -> UserInfoModel:
        status_code, content = await self.api_client.fetch(
            "get", f"get-user/{username}", headers={'Authorization': f'Basic {token}'})
        return status_code, UserInfoModel(**content)

    async def update_user_info(self, user_id: int, token: str, body: dict) -> CommonModel:
        status_code, content = await self.api_client.fetch(
            "post", f"user/{user_id}/update", body=body, headers={'Authorization': f'Basic {token}'})
        return status_code, CommonModel(**content)


async def process_user_info(user_info: UserInfoModel) -> dict:
    # do something ...
    # after return changed user info
    return {
        "active": user_info.active,
        "blocked": user_info.blocked,
        "name": user_info.name,
        "permissions": user_info.permissions
    }


async def do_update():
    base_url = 'https://testapi.ru/'
    user_api = UserApi(base_url)
    
    _, token_obj = await user_api.get_auth_token(UserAuthModel.login, UserAuthModel.pswd)
    if token_obj.status == STATUS.OK:
        _, user_info_obj = await user_api.get_user_info('ivanov', token_obj.token)
        modified_user_info = await process_user_info(user_info_obj)
        await user_api.update_user_info(user_info_obj.id, token_obj.token, modified_user_info)


if __name__ == '__main__':
    asyncio.run(do_update())
