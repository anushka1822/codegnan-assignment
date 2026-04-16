from typing import AsyncGenerator
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import Depends, HTTPException, status, Security
from fastapi.security import APIKeyHeader

from app.db.session import AsyncSessionLocal
from app.models.api_key import ApiKey
from app.core.security import hash_api_key

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

api_key_header_scheme = APIKeyHeader(name="X-API-Key")

async def verify_api_key_and_rate_limit(
    api_key_header: str = Security(api_key_header_scheme),
    db: AsyncSession = Depends(get_db)
) -> ApiKey:
    hashed_input_key = hash_api_key(api_key_header)

    result = await db.execute(select(ApiKey).where(ApiKey.hashed_key == hashed_input_key))
    api_key_obj = result.scalars().first()

    if not api_key_obj or not api_key_obj.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key"
        )

    RATE_LIMIT_PER_MINUTE = 5
    now = datetime.now(timezone.utc)

    # Time Check
    if api_key_obj.last_request_timestamp is None or (now - api_key_obj.last_request_timestamp).total_seconds() > 60:
        api_key_obj.current_minute_requests = 1
        api_key_obj.last_request_timestamp = now
    else:
        # Limit Check
        if api_key_obj.current_minute_requests >= RATE_LIMIT_PER_MINUTE:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded"
            )
        api_key_obj.current_minute_requests += 1

    # Global Check
    api_key_obj.total_requests += 1

    # Save and return
    await db.commit()
    await db.refresh(api_key_obj)

    return api_key_obj
