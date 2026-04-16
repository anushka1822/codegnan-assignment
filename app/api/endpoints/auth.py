from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db
from app.schemas.api_key import ApiKeyCreate, ApiKeyCreateResponse
from app.models.api_key import ApiKey
from app.core.security import generate_api_key, hash_api_key

router = APIRouter()

@router.post("/keys", response_model=ApiKeyCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_api_key(
    request: ApiKeyCreate,
    db: AsyncSession = Depends(get_db)
):
    raw_key = generate_api_key()
    prefix = raw_key[:4]
    hashed_key = hash_api_key(raw_key)

    new_key = ApiKey(
        name=request.name,
        hashed_key=hashed_key,
        prefix=prefix
    )

    db.add(new_key)
    await db.commit()
    await db.refresh(new_key)

    return ApiKeyCreateResponse(
        id=new_key.id,
        name=new_key.name,
        prefix=new_key.prefix,
        created_at=new_key.created_at,
        total_requests=new_key.total_requests,
        is_active=new_key.is_active,
        current_minute_requests=new_key.current_minute_requests,
        last_request_timestamp=new_key.last_request_timestamp,
        raw_key=raw_key
    )
