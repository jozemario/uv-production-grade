from typing import Final, Union
import contextlib
import json
import logging
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.users import get_user_db, get_user_manager
from app.schemas import UserCreate
from app.models.tables import Priority, Category, Todo, TodoCategory, User
from app.core.config import TestSettings, get_test_config

logger = logging.getLogger(__name__)

TESTS_DATA_FILE_PATH: Final[str] = 'tests/tests_data.json'

get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


def get_tests_data() -> dict[str, Union[list[dict], dict]]:
    with open(TESTS_DATA_FILE_PATH, 'r') as f:
        return json.load(f)


async def insert_test_data(session: AsyncSession) -> None:
    tests_data = get_tests_data()
    priorities = [Priority(name=p['name']) for p in tests_data['priorities']]
    categories = [Category(name=c['name'], created_by_id=None) 
                 for c in tests_data['categories']]
    
    session.add_all(priorities)
    session.add_all(categories)
    
    for user in tests_data['users']:
        async with get_user_db_context(session) as user_db:
            async with get_user_manager_context(user_db) as user_manager:
                db_user: User = await user_manager.create(
                    UserCreate(email=user['email'], password=user['password'])
                )
                
        users_categories = [
            Category(name=c['name'], created_by_id=db_user.id) 
            for c in user['categories']
        ]
        session.add_all(users_categories)
        
        todos = [
            Todo(
                content=t['content'],
                priority_id=t['priority']['id'],
                created_by_id=db_user.id,
                todos_categories=[TodoCategory(category_id=c['id']) 
                                for c in t['categories']]
            ) for t in user['todos']
        ]
        session.add_all(todos)
    
    await session.commit()


async def get_user_token_headers(client: AsyncClient) -> dict[str, str]:
    config = get_test_config()
    tests_data = get_tests_data()
    login_data = {
        'username': tests_data['users'][0]['email'],
        'password': tests_data['users'][0]['password'],
    }
    res = await client.post(f'{config.API_V1_STR}/auth/login', data=login_data)
    access_token = res.json()['access_token']
    return {'Authorization': f'Bearer {access_token}'}
