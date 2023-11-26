import stripe
from util import buildResponse
import os

stripe.api_key = os.environ['TEST_STRIPE_KEY']

def payment_sheet(headers,cantidad,email):
    customer = stripe.Customer.create(
        email=email
    )
    ephemeralKey = stripe.EphemeralKey.create( customer=customer['id'], stripe_version='2023-10-16',)

    paymentIntent = stripe.PaymentIntent.create(
        amount=cantidad * 100,
        currency='mxn',
        customer=customer['id'],
        automatic_payment_methods={'enabled': True,},)
    return buildResponse(
        200,
        headers,
        {
            'paymentIntent': paymentIntent.client_secret,
            'ephemeralKey': ephemeralKey.secret,
            'customer': customer.id,
            'publishableKey': 'pk_test_51O9qWCA1N4jj7tFywDEElSoJY86l4sLHoO5vzUeg9NB96GQJvu9E7Xv5OA9nR8ex55b9rw3GlZICsAw8EIS6lX1Y002girw2w9'
        }
    )
