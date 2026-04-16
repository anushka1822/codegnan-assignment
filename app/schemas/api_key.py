from pydantic import BaseModel, ConfigDict
from datetime import datetime

class ApiKeyCreate(BaseModel):
    name: str

class ApiKeyResponse(BaseModel):
    id: int
    name: str
    prefix: str
    created_at: datetime
    total_requests: int
    is_active: bool
    current_minute_requests: int
    last_request_timestamp: datetime | None = None

    model_config = ConfigDict(from_attributes=True)

class ApiKeyCreateResponse(ApiKeyResponse):
    raw_key: str
