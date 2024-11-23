# tests for priorities

import json
import pytest
from httpx import AsyncClient

def get_tests_data():
    # get from tests_data.json
    with open('tests/tests_data.json', 'r') as f:
        return json.load(f)

API_V1_STR = "/api/v1"
@pytest.mark.asyncio
class TestPriorities:
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
                'res_body': [
                    {
                        'id': '123e4567-e89b-12d3-a456-426614174001',
                        'name': 'High'
                    },
                    {
                        'id': '123e4567-e89b-12d3-a456-426614174002',
                        'name': 'Medium'
                    },
                    {
                        'id': '123e4567-e89b-12d3-a456-426614174003',
                        'name': 'Low'
                    }
                ]
            },
            id='authorized'
        )
    ])
    async def test_get_priorities(
        self,
        client: AsyncClient,
        user_token_headers: dict,
        test_data: dict
    ):
        headers = user_token_headers if test_data['headers'] == 'user_token_headers' else None
        res = await client.get(f'{API_V1_STR}/priorities', headers=headers)
        assert res.status_code == test_data['status_code']
        assert res.json() == test_data['res_body']
