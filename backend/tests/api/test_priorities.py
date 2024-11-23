import pytest
from httpx import AsyncClient
from tests.conftest_utils import get_tests_data
from app.core.config import TestSettings, get_config, get_test_config

config = get_test_config()

@pytest.mark.asyncio
class TestPriorities:
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
                'res_body': get_tests_data()['priorities']
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
        res = await client.get(f'{config.API_V1_STR}/priorities', headers=headers)
        assert res.status_code == test_data['status_code']
        assert res.json() == test_data['res_body']
