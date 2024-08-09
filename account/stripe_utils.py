import stripe

stripe.api_key = 'your_stripe_secret_key'

def create_payment_intent(amount):
    intent = stripe.PaymentIntent.create(
        amount=int(amount * 100),  # Convertir en cents
        currency='eur',  # La devise doit être définie
        payment_method_types=['card'],
    )
    return intent
