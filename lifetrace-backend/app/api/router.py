from fastapi import APIRouter

router = APIRouter(prefix="/api")

from . import auth, stall, schedule, product, queue_order, ai

router.include_router(auth.router)
router.include_router(stall.router)
router.include_router(schedule.router)
router.include_router(product.router)
router.include_router(queue_order.router)
router.include_router(ai.router)
