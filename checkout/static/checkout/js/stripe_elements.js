let stripe_public_key = $('#id_stripe_public_key').text().slice(1, -1);
let stripe_client_secret_key = $('#id_client_secret_key').text().slice(1, -1);
let stripe = Stripe(stripe_public_key);
let elements = stripe.elements();

let style = {
    base: {
        color: '#000000',
        fontFamily: '"Heuvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: 'aab7c4'
        }
    },
    invalid : {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};

let card = elements.create('card', {style: style});
card.mount('#card-element');