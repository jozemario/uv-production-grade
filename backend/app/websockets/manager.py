from fastapi import WebSocket
from typing import Dict, List, Set
import json
from asyncio.log import logger

class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}
        self.user_channels: Dict[str, Set[str]] = {}
        logger.info("WebSocket manager initialized")

    async def connect(self, websocket: WebSocket, user_id: str, channel: str = "default"):
        try:
            logger.info(f"Attempting to accept WebSocket for user {user_id}")
            await websocket.accept()
            logger.info(f"WebSocket accepted for user {user_id}")
            
            if user_id not in self.active_connections:
                self.active_connections[user_id] = set()
                self.user_channels[user_id] = set()
                logger.info(f"Created new connection set for user {user_id}")
                
            self.active_connections[user_id].add(websocket)
            self.user_channels[user_id].add(channel)
            logger.info(f"Added connection for user {user_id} on channel {channel}")
            logger.info(f"Active connections count for user {user_id}: {len(self.active_connections[user_id])}")
            
        except Exception as e:
            logger.error(f"Error in connect: {str(e)}", exc_info=True)
            raise

    async def disconnect(self, websocket: WebSocket, user_id: str):
        try:
            logger.info(f"Disconnecting WebSocket for user {user_id}")
            if user_id in self.active_connections:
                self.active_connections[user_id].remove(websocket)
                logger.info(f"Removed connection for user {user_id}")
                
                if not self.active_connections[user_id]:
                    del self.active_connections[user_id]
                    if user_id in self.user_channels:
                        del self.user_channels[user_id]
                    logger.info(f"Removed all connection data for user {user_id}")
        except Exception as e:
            logger.error(f"Error in disconnect: {str(e)}", exc_info=True)

    async def broadcast_to_user(self, user_id: str, message: dict, channel: str = "default"):
        try:
            logger.info(f"Broadcasting to user {user_id} on channel {channel}")
            if user_id in self.active_connections:
                dead_websockets = set()
                for connection in self.active_connections[user_id]:
                    try:
                        await connection.send_json({
                            "channel": channel,
                            "data": message
                        })
                        logger.info(f"Message sent to user {user_id}")
                    except Exception as e:
                        logger.error(f"Error sending message: {str(e)}")
                        dead_websockets.add(connection)
                
                for dead_ws in dead_websockets:
                    await self.disconnect(dead_ws, user_id)
        except Exception as e:
            logger.error(f"Error in broadcast_to_user: {str(e)}", exc_info=True)

websocket_manager = WebSocketManager() 