import json
from app.core.config import get_config
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.users.auth import oauth2_scheme, verify_token
from app.schemas.webhook import WebhookCreate, WebhookRead
from app.models.tables import Webhook
from typing import List
import httpx
from sqlalchemy import select
from uuid import UUID
from asyncio.log import logger
config = get_config()


router = APIRouter(prefix='/webhooks',
                   dependencies=[
                       Depends(oauth2_scheme),
                       Depends(get_async_session)
                   ],
                   tags=['Webhooks'])

async def trigger_webhook(url: str, payload: dict, retry_count: int = 3):
    for attempt in range(retry_count):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url, 
                    json=payload,
                    timeout=10.0,
                    headers={"Content-Type": "application/json"}
                )
                response.raise_for_status()
                logger.info(f"Webhook delivered to {url}: Status {response.status_code}")
                return
        except Exception as e:
            if attempt == retry_count - 1:
                logger.error(f"Webhook delivery failed to {url} after {retry_count} attempts: {str(e)}")
            else:
                logger.warning(f"Webhook delivery attempt {attempt + 1} failed: {str(e)}")

@router.post("", response_model=WebhookRead, status_code=status.HTTP_201_CREATED)
async def create_webhook(
    webhook: WebhookCreate,
    background_tasks: BackgroundTasks,
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_async_session)
):
    user = await verify_token(token)
    user_id = UUID(user.get("user_id"))
    
    db_webhook = Webhook(
        url=str(webhook.url),
        events=webhook.events,
        is_active=webhook.is_active,
        created_by_id=user_id
    )
    
    session.add(db_webhook)
    await session.commit()
    await session.refresh(db_webhook)
    
    return db_webhook

@router.get("", response_model=List[WebhookRead])
async def get_webhooks(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_async_session)
):
    user = await verify_token(token)
    user_id = UUID(user.get("user_id"))
    
    result = await session.execute(
        select(Webhook).where(Webhook.created_by_id == user_id)
    )
    return result.scalars().all()

@router.delete("/{webhook_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_webhook(
    webhook_id: UUID,
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_async_session)
):
    user = await verify_token(token)
    user_id = UUID(user.get("user_id"))
    
    result = await session.execute(
        select(Webhook).where(
            Webhook.id == webhook_id,
            Webhook.created_by_id == user_id
        )
    )
    webhook = result.scalar_one_or_none()
    
    if not webhook:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Webhook not found"
        )
    
    await session.delete(webhook)
    await session.commit()

async def notify_webhooks(
    session: AsyncSession,
    user_id: UUID, 
    event: str, 
    payload: dict
):
    result = await session.execute(
        select(Webhook).where(
            Webhook.created_by_id == str(user_id),
            Webhook.is_active == True,
            Webhook.events.any(event)
        )
    )
    logger.info(f"notify_webhooks Webhooks: {payload}")    
    logger.info(f"notify_webhooks Webhooks: {result}")

    
    webhooks = result.scalars().all()
        
    for webhook in webhooks:
        background_tasks = BackgroundTasks()
        background_tasks.add_task(trigger_webhook, str(webhook.url), payload)
        await background_tasks()  # Execute the background tasks