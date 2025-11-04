# app/api/v1/endpoints/webhooks.py
import stripe
from fastapi import APIRouter, Request, HTTPException, Header
from app.core.config import settings
from app.services.order_service import order_service
from beanie import PydanticObjectId

router = APIRouter()

@router.post("/stripe")
async def stripe_webhook(request: Request, stripe_signature: str = Header(None)):
    """
    Stripe webhook endpoint to handle asynchronous events.
    """
    # 1. Read the raw request body (Stripe needs this)
    payload = await request.body()
    
    # 2. Get the webhook secret from our config
    secret = settings.STRIPE_WEBHOOK_SECRET

    # try:
    #     # verify the event signature to ensure it's from Stripe
    #     event = stripe.Webhook.construct_event(
    #         payload=payload, sig_header=stripe_signature, secret=secret
    #     )
    # except ValueError as e:
    #     # invalid payload
    #     raise HTTPException(status_code=400, detail="Invalid payload")
    # except stripe.SignatureVerificationError as e:
    #     # Invalid signature
    #     raise HTTPException(status_code=400, detail="Invalid signature")

    import json
    event = json.loads(payload)

    # handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        # Retrieve the user_id we stored in metadata
        user_id = session.get('metadata', {}).get('user_id')
        
        if not user_id:
            # We have a payment but don't know who it's for.
            # This is a critical error, log it.
            print("CRITICAL: Stripe webhook received checkout.session.completed with no user_id in metadata.")
            raise HTTPException(status_code=400, detail="User ID not in metadata")

        print(f"Checkout session completed for user: {user_id}")
        
        # 5. Call our OrderService to finalize the purchase
        try:
            # Convert the string ID from metadata back to PydanticObjectId
            order_or_error = await order_service.create_order_from_cart(
                PydanticObjectId(user_id)
            )
            
            if isinstance(order_or_error, str):
                # The service failed (e.g., stock changed at the last second)
                print(f"Webhook Error for user {user_id}: {order_or_error}")
                # We'd typically email the user or admin here
                raise HTTPException(status_code=500, detail=f"Failed to create order: {order_or_error}")

        except Exception as e:
            print(f"Error processing order for user {user_id}: {e}")
            raise HTTPException(status_code=500, detail="Error processing order")

    # Acknowledge the event to Stripe
    return {"status": "success"}