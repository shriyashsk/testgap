import hmac
import hashlib
from decimal import Decimal

from fastapi import APIRouter, Request, HTTPException
from sqlalchemy import select

from app.database import AsyncSessionLocal
from app.models.models import Settlement
from app.services.balance_service import apply_settlement
from app.services.edit_log_service import write_log
from app.config import settings

router = APIRouter(tags=["webhooks"])


@router.post("/webhooks/razorpay")
async def razorpay_webhook(request: Request):
    body = await request.body()
    signature = request.headers.get("X-Razorpay-Signature", "")

    expected = hmac.new(
        settings.RAZORPAY_WEBHOOK_SECRET.encode(),
        body,
        hashlib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(expected, signature):
        raise HTTPException(status_code=400, detail="Invalid signature")

    payload = await request.json()
    if payload.get("event") != "payment.captured":
        return {"status": "ignored"}

    payment_entity = payload["payload"]["payment"]["entity"]
    order_id = payment_entity["order_id"]
    payment_id = payment_entity["id"]

    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(Settlement).where(Settlement.razorpay_order_id == order_id)
        )
        settlement = result.scalar_one_or_none()

        if not settlement:
            return {"status": "no_matching_settlement"}
        if settlement.status == "confirmed":
            # Razorpay can send the same webhook more than once — don't double-apply
            return {"status": "already_confirmed"}

        settlement.status = "confirmed"
        settlement.razorpay_payment_id = payment_id

        await apply_settlement(
            db, settlement.group_id, settlement.paid_by_user_id,
            settlement.paid_to_user_id, Decimal(str(settlement.amount)),
            settlement.currency, multiplier=1,
        )
        await write_log(
            db, "settlement", settlement.id, settlement.paid_by_user_id, "create",
            after={"amount": str(settlement.amount), "currency": settlement.currency,
                   "via": "razorpay", "payment_id": payment_id},
        )
        await db.commit()

    return {"status": "ok"}