

const stripePublicKey = JSON.parse(document.getElementById('id_stripe-public-key').textContent);
const stripeClientSecret = JSON.parse(document.getElementById('id_stripe-client-secret').textContent);
const stripe = Stripe(stripePublicKey);
const elements = stripe.elements(); 
const cardElement = elements.create('card');
cardElement.mount('#card-element');