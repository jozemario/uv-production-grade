from pydantic import BaseModel, HttpUrl
from typing import List
from uuid import UUID
class WebhookBase(BaseModel):
    url: HttpUrl
    events: List[str]
    is_active: bool = True

class WebhookCreate(WebhookBase):
    pass

class WebhookRead(WebhookBase):
    id: UUID
    created_by_id: UUID

    class Config:
        from_attributes = True