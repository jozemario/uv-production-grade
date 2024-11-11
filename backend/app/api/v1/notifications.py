from asyncio.log import logger
from fastapi import APIRouter, HTTPException, Depends, Request, Header
from app.websockets.manager import websocket_manager
from app.users.auth import verify_token
from uuid import UUID
import json

router = APIRouter(prefix='/notifications', tags=['Notifications'])

@router.post("/webhook/{user_id}")
async def webhook_notification(
    user_id: UUID, 
    request: Request,
    authorization: str = Header(None)
):
    try:
        if authorization:
            token = authorization.replace("Bearer ", "")
            user_data = await verify_token(token)
            if str(user_id) != user_data.get("user_id"):
                raise HTTPException(status_code=403, detail="Not authorized")
        
        payload = await request.json()
        await websocket_manager.broadcast_to_user(
            str(user_id),
            {
                "type": "webhook.notification",
                "data": payload
            }
        )
        return {"status": "success"}
    except Exception as e:
        logger.error(f"Webhook notification error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e)) 