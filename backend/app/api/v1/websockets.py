from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.users.auth import verify_token
from app.websockets.manager import websocket_manager
from asyncio.log import logger
import json

router = APIRouter(prefix='/ws', tags=['WebSockets'])

@router.websocket("/{token}")
async def websocket_endpoint(websocket: WebSocket, token: str, channel: str = "default"):
    try:
        # Log the initial connection attempt
        logger.info(f"WebSocket connection attempt - Token: {token[:20]}...")
        logger.info(f"WebSocket headers: {websocket.headers}")
        logger.info(f"WebSocket query params: {websocket.query_params}")
        
        try:
            user_data = await verify_token(token)
            logger.info(f"Token verification successful: {user_data}")
        except Exception as e:
            logger.error(f"Token verification failed: {str(e)}")
            await websocket.close(code=4001, reason="Invalid token")
            return
            
        user_id = user_data.get("user_id")
        logger.info(f"User ID from token: {user_id}")
        
        if not user_id:
            logger.error("No user_id found in token")
            await websocket.close(code=4001, reason="Unauthorized: No user_id in token")
            return

        # Log before WebSocket accept
        logger.info("Attempting to accept WebSocket connection")
        await websocket_manager.connect(websocket, user_id, channel)
        logger.info(f"WebSocket connection accepted for user {user_id} on channel {channel}")
        
        try:
            while True:
                data = await websocket.receive_text()
                message = json.loads(data)
                logger.info(f"Received message from user {user_id}: {message}")
                await websocket_manager.broadcast_to_user(
                    user_id,
                    message,
                    channel
                )
                
        except WebSocketDisconnect:
            logger.info(f"WebSocket disconnected for user {user_id}")
            await websocket_manager.disconnect(websocket, user_id)
            
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}", exc_info=True)
        await websocket.close(code=4000, reason=str(e))