import stripe
from fastapi import APIRouter, Request, HTTPException, Header
from app.core.config import settings
from app.services.order_service import order_service
from beanie import PydanticObjectId

router = APIRouter()

@router.post("/stripe")
async def stripe_webhook(request: Request, stripe_signature: str = Header(None)):
    """
    Stripe webhook endpoint to handle asynchronous events
    """
    payload = await request.body()

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
        
        # Retrieve the user_id stored in metadata
        user_id = session.get('metadata', {}).get('user_id')
        
        if not user_id:
            print("CRITICAL: Stripe webhook received checkout.session.completed with no user_id in metadata.")
            raise HTTPException(status_code=400, detail="User ID not in metadata")

        print(f"Checkout session completed for user: {user_id}")
        
        # Call OrderService to finalize the purchase
        try:
            order_or_error = await order_service.create_order_from_cart(
                PydanticObjectId(user_id)
            )
            
            if isinstance(order_or_error, str):
                print(f"Webhook Error for user {user_id}: {order_or_error}")
                raise HTTPException(status_code=500, detail=f"Failed to create order: {order_or_error}")

        except Exception as e:
            print(f"Error processing order for user {user_id}: {e}")
            raise HTTPException(status_code=500, detail="Error processing order")

    return {"status": "success"}