# tests for todos

import json
import pytest
from httpx import AsyncClient

API_V1_STR = "/api/v1"

def get_tests_data():
    # get from tests_data.json
    with open('tests/tests_data.json', 'r') as f:
        return json.load(f)


@pytest.mark.asyncio
class TestTodos:
    @pytest.mark.parametrize('test_data', [
        pytest.param(
            {
                'headers': None,
                'status_code': 401,
                'res_body': {'detail': 'Not authenticated'}
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
        user_token_headers: dict,
        test_data: dict
    ):
        headers = user_token_headers if test_data['headers'] == 'user_token_headers' else None
        res = await client.get(f"{API_V1_STR}/todos", headers=headers)
        assert res.status_code == test_data['status_code']
        assert res.json() == test_data['res_body']

    @pytest.mark.parametrize('test_data', [
        pytest.param(
            {
                'headers': None,
                'data': {
                    'content': 'Learn the sicilian opening',
                    'priority_id': '123e4567-e89b-12d3-a456-426614174001',
                    'categories_ids': ['123e4567-e89b-12d3-a456-426614174003', '123e4567-e89b-12d3-a456-426614174006']
                },
                'status_code': 401,
                'res_body': {'detail': 'Not authenticated'}
            },
            id='unauthorized'
        ),
        pytest.param(
            {
                'headers': 'user_token_headers',
                'data': {
                    'content': 'Learn the sicilian opening',
                    'priority_id': '123e4567-e89b-12d3-a456-426614174001',
                    'categories_ids': ['123e4567-e89b-12d3-a456-426614174003', '123e4567-e89b-12d3-a456-426614174006']
                },
                'status_code': 201,
                'res_body': get_tests_data()['users'][0]['todos'][0]
            },
            id='create todo'
        )
    ])
    async def test_create_todo(
        self,
        client: AsyncClient,
        user_token_headers: dict,
        test_data: dict
    ):
        headers = user_token_headers if test_data['headers'] == 'user_token_headers' else None
        res = await client.post(
            f"{API_V1_STR}/todos",
            headers=headers,
            json=test_data['data']
        )
        assert res.status_code == test_data['status_code']
        if res.status_code == 201:
            response_data = res.json()
            # Remove timestamp fields for comparison since they'll be different
            del response_data['created_at']
            del response_data['updated_at']
            expected_data = test_data['res_body'].copy()
            del expected_data['created_at']
            del expected_data['updated_at']
            assert response_data == expected_data

