from app.core.redis import redis_client

MAX_ATTEMPTS = 5
WINDOW_SECONDS = 300

async def is_rate_limited(email: str) -> bool:
    key = f"login_attempts:{email}"
    attempts = await redis_client.get(key)
    if attempts is not None and int(attempts) >= MAX_ATTEMPTS:
        return True
    return False

async def record_failed_attempt(email: str) -> None:
    key =f"login_attempts:{email}"
    attempts = await redis_client.incr(key)
    if attempts == 1:
        await redis_client.expire(key, WINDOW_SECONDS)
        
async def clear_failed_attempts(email: str) -> None:
    key = f"login_attempts:{email}"
    await redis_client.delete(key)