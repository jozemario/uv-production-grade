from typing import Final
from tests.conftest import user_token_headers

import pytest
from httpx import AsyncClient
from tests.conftest_utils import get_tests_data
from app.core.config import TestSettings, get_config, get_test_config
from sqlalchemy.ext.asyncio import AsyncSession

config = get_test_config()
API_TODOS_PREFIX: Final[str] = f'{config.API_V1_STR}/todos'

@pytest.mark.asyncio
class TestTodos:
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
                'res_body': get_tests_data()['users'][0]['todos']
            },
            id='authorized'
        )
    ])
    async def test_get_todos(
        self,
        client: AsyncClient,
        test_session: AsyncSession,
        override_get_config: TestSettings,
        test_data: dict
    ):
        headers = user_token_headers if test_data['headers'] == 'user_token_headers' else None
        res = await client.get(API_TODOS_PREFIX, headers=headers)
        assert res.status_code == test_data['status_code']
        assert res.json() == test_data['res_body']
        assert override_get_config.ENVIRONMENT == "test"

    @pytest.mark.parametrize('test_data', [
        pytest.param(
            {
                'headers': None,
                'data': {'title': 'Test Todo'},
                'status_code': 401,
                'res_body': {'detail': 'Unauthorized'}
            },
            id='unauthorized'
        ),
        pytest.param(
            {
                'headers': 'user_token_headers',
                'data': {'title': 'Test Todo'},
                'status_code': 201,
                'res_body': {'id': 1, 'title': 'Test Todo', 'completed': False}
            },
            id='create_success'
        )
    ])
    async def test_create_todo(
        self,
        client: AsyncClient,
        user_token_headers: dict,
        test_data: dict
    ):
        headers = user_token_headers if test_data['headers'] == 'user_token_headers' else None
        res = await client.post(API_TODOS_PREFIX, headers=headers, json=test_data['data'])
        assert res.status_code == test_data['status_code']
        if res.status_code == 201:
            response_data = res.json()
            assert response_data['title'] == test_data['res_body']['title']
            assert response_data['completed'] == test_data['res_body']['completed']
            assert isinstance(response_data['id'], int)
        else:
            assert res.json() == test_data['res_body']

    @pytest.mark.parametrize('test_data', [
        pytest.param(
            {
                'headers': None,
                'todo_id': 1,
                'status_code': 401,
                'res_body': {'detail': 'Unauthorized'}
            },
            id='unauthorized'
        ),
        pytest.param(
            {
                'headers': 'user_token_headers',
                'todo_id': 999,
                'status_code': 404,
                'res_body': {'detail': 'Todo not found'}
            },
            id='not_found'
        )
    ])
    async def test_delete_todo_failure(
        self,
        client: AsyncClient,
        user_token_headers: dict,
        test_data: dict
    ):
        headers = user_token_headers if test_data['headers'] == 'user_token_headers' else None
        res = await client.delete(f"{API_TODOS_PREFIX}/{test_data['todo_id']}", headers=headers)
        assert res.status_code == test_data['status_code']
        assert res.json() == test_data['res_body']

    async def test_delete_todo_success(
        self,
        client: AsyncClient,
        user_token_headers: dict
    ):
        res = await client.delete(f'{API_TODOS_PREFIX}/1', headers=user_token_headers)
        assert res.status_code == 204
        assert len(res.content) == 0
