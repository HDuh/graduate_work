var createCheckoutSession = function (productId) {
    return fetch("/api/v1/order", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            product_id: productId,
        })
    }).then(function (result) {
        return result.json();
    });
};

const MONTHLY = "25b3c1fc-383a-4575-95dc-1542c60b9db6";
const QUARTER = "8120c1e7-e8ee-495d-b3fe-8f2f10f661a5";
const HALF = "68b0cc8a-debf-425c-8d33-5ed009cde428";

const stripe = Stripe('pk_test_51M9x7LInWuMfFLjmMhKVb4K6NXWj5UfFFkiJ7gGFQxWyc0DpzMaYGrJBiX4MIf6yOsSiMeXh7q330gkSfcjxbKf400EuCjNCXJ');


document.addEventListener("DOMContentLoaded", function (event) {
    document
        .getElementById("checkout_monthly")
        .addEventListener("click", function (evt) {
            createCheckoutSession(MONTHLY).then(function (data) {
                stripe
                    .redirectToCheckout({
                        sessionId: data.sessionId
                    });
            });

        });
    document
        .getElementById("checkout_quarter")
        .addEventListener("click", function (evt) {
            createCheckoutSession(QUARTER).then(function (data) {
                stripe
                    .redirectToCheckout({
                        sessionId: data.sessionId
                    });
            });

        });
    document
        .getElementById("checkout_half_year")
        .addEventListener("click", function (evt) {
            createCheckoutSession(HALF).then(function (data) {
                stripe
                    .redirectToCheckout({
                        sessionId: data.sessionId
                    });
            });

        });

})