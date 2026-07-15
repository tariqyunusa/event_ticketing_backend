from app.core.redis import redis_client

async def blacklist_token(token: str, expires_in_seconds: int) -> None:
    key = f"blacklist:{token}"
    await redis_client.set(key, "true", ex=expires_in_seconds)
    
async def is_token_blacklisted(token: str) -> bool:
    key = f"blacklist:{token}"
    exists = await redis_client.exists(key)
    return exists == 1 