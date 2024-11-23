import pytest
from httpx import AsyncClient
from tests.conftest_utils import get_tests_data
from app.core.config import TestSettings, get_config, get_test_config

config = get_test_config()

@pytest.mark.asyncio
class TestCategories:
    @pytest.mark.parametrize('test_data', [
        pytest.param(
            {
                'headers': None,
                'status_code': 401,
                'res_body': {'detail': 'Unauthorized'}
            },
            id='unauthorized'
        ),
        pytest.param(
            {
                'headers': 'user_token_headers',
                'status_code': 200,
                'res_body': get_tests_data()['categories'] + get_tests_data()['users'][0]['categories']
            },
            id='authorized'
        )
    ])
    async def test_get_categories(
        self,
        client: AsyncClient,
        user_token_headers: dict,
        test_data: dict
    ):
        headers = user_token_headers if test_data['headers'] == 'user_token_headers' else None
        res = await client.get(f'{config.API_V1_STR}/categories', headers=headers)
        assert res.status_code == test_data['status_code']
        assert res.json() == test_data['res_body']


@pytest.mark.asyncio
@pytest.mark.parametrize('test_data', [
    pytest.param(
        {
            'headers': None,
            'data': {'name': 'Work'},
            'status_code': 401,
            'res_body': {'detail': 'Unauthorized'}
        },
        id='unauthorized access'
    ),
    pytest.param(
        {
            'headers': 'user_token_headers',
            'data': {'name': 'Personal'},
            'status_code': 409,
            'res_body': {'detail': 'category name already exists'}
        },
        id='authorized access default existing category'
    ),
    pytest.param(
        {
            'headers': 'user_token_headers',
            'data': {'name': 'Chess'},
            'status_code': 409,
            'res_body': {'detail': 'category name already exists'}
        },
        id='authorized access another users existing category'
    ),
    pytest.param(
        {
            'headers': 'user_token_headers',
            'data': {'name': 'Nintendo'},
            'status_code': 201,
            'res_body': {'name': 'Nintendo', 'id': 5}
        },
        id='authorized access non existing category'
    ),
])
async def test_add_category(
    client: AsyncClient,
    user_token_headers: dict,
    test_data: dict
):
    headers = user_token_headers if test_data['headers'] == 'user_token_headers' else None
    res = await client.post(f'{config.API_V1_STR}/categories', headers=headers, json=test_data['data'])
    assert res.status_code == test_data['status_code']
    assert res.json() == test_data['res_body']


@pytest.mark.asyncio
@pytest.mark.parametrize('test_data', [
    pytest.param(
        {
            'headers': None,
            'category_id': 1,
            'status_code': 401,
            'res_body': {'detail': 'Unauthorized'}
        },
        id='unauthorized access'
    ),
    pytest.param(
        {
            'headers': 'user_token_headers',
            'category_id': 5,
            'status_code': 404,
            'res_body': {'detail': 'category does not exist'}
        },
        id='authorized access non existing category'
    ),
    pytest.param(
        {
            'headers': 'user_token_headers',
            'category_id': 1,
            'status_code': 403,
            'res_body': {'detail': 'a user can not delete a category that was not created by him'}
        },
        id='authorized access default existing category'
    ),
    pytest.param(
        {
            'headers': 'user_token_headers',
            'category_id': 4,
            'status_code': 403,
            'res_body': {'detail': 'a user can not delete a category that was not created by him'}
        },
        id='authorized access another users existing category'
    ),
])
async def test_delete_category_failure(
    client: AsyncClient,
    user_token_headers: dict,
    test_data: dict
):
    headers = user_token_headers if test_data['headers'] == 'user_token_headers' else None
    res = await client.delete(f'{config.API_V1_STR}/categories/{test_data["category_id"]}', headers=headers)
    assert res.status_code == test_data['status_code']
    assert res.json() == test_data['res_body']


@pytest.mark.asyncio
async def test_delete_category_success(
    client: AsyncClient,
    user_token_headers: dict
):
    res = await client.delete(f'{config.API_V1_STR}/categories/3', headers=user_token_headers)
    assert res.status_code == 204
    assert len(res.content) == 0
