import pytest

from src.api import UserApi, STATUS


@pytest.fixture(name='client')
async def _client(loop):
    return UserApi('https://testapi.ru/')


@pytest.fixture(name='auth')
async def _auth(client, loop):
    status, token_obj = await client.get_auth_token(login='test', pswd='12345')
    assert status == 200
    assert token_obj.status == STATUS.OK
    assert token_obj.token is not None
    return token_obj


async def test_get_user_info(client, auth):
    status, userinfo_obj = await client.get_user_info(username='ivanov', token=auth.token)
    assert status == 200
    assert userinfo_obj.status == STATUS.OK
    assert userinfo_obj.name == 'Ivanov Ivan'


async def test_update_user_info(client, auth):
    body = {
        "active": '1',
        "blocked": True,
        "name": 'Ivanov Ivanov',
        "permissions": []
    }
    status, userinfo_obj = await client.update_user_info(user_id=23, token=auth.token, body=body)
    assert status == 200
    assert userinfo_obj.status == STATUS.OK
