

const stripePublicKey = JSON.parse(document.getElementById('id_stripe-public-key').textContent);
const stripeClientSecret = JSON.parse(document.getElementById('id_stripe-client-secret').textContent);
const stripe = stripe(stripePublicKey);
const elements = stripe.elements(); 
const style = {
  base: {
    color: 'green',
    fontWeight: '500',
    iconColor: '#32325d',
    fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
    fontSmoothing: "antialiased",
    fontSize: "16px",
    '::placeholder': {
      color: '#aab7c4'
    }
  },
  invalid: {
    color: '#fa755a',
    iconColor: '#fa755a'
  }
};
const cardElement = elements.create('card', { style });
cardElement.mount('#card-element');




cardElement.on('change', function(event) {
  const displayError = document.getElementById('card-errors');
  if (event.error) {
    displayError.textContent = event.error.message;
    displayError.classList.add('text-danger');
  } else {
    displayError.textContent = '';
  }
});


form = document.getElementById('checkout-form');
form.addEventListener('submit', function(event) {
  event.preventDefault();
  const displayError = document.getElementById('card-errors');
  displayError.textContent = '';
  cardElement.update({ disabled: true });
  form.querySelector('button').disabled = true; // Disable the submit button
  
  stripe.confirmCardPayment(stripeClientSecret, {
    payment_method: {
      card: cardElement,
     
    }
  }).then(function(result) {
    if (result.error) {
      displayError.textContent = result.error.message;
      displayError.classList.add('text-danger');
      cardElement.update({ disabled: false });
      form.querySelector('button').disabled = false; // Enable the submit button
    } else {
      if (result.paymentIntent.status === 'succeeded') {
        form.submit();
      }
    }
  });
});
