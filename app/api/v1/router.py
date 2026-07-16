from fastapi import APIRouter
from app.api.v1.endpoints import events, health, auth, orders, tickets

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(events.router, tags=["events"])
api_router.include_router(orders.router, tags=["orders"])
api_router.include_router(tickets.router, tags=["tickets"])

