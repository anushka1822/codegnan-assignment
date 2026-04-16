from fastapi import APIRouter, Depends
from app.api.deps import verify_api_key_and_rate_limit
from app.models.api_key import ApiKey

router = APIRouter()

@router.get("/data")
async def get_secure_data(
    api_key: ApiKey = Depends(verify_api_key_and_rate_limit)
):
    return {
        "message": "Secure data accessed successfully!",
        "key_name": api_key.name,
        "total_requests_made": api_key.total_requests
    }
