var createCheckoutSession = function (priceId) {
    return fetch("/api/v1/billing/create_checkout_session", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            priceId: priceId
        })
    }).then(function (result) {
        return result.json();
    });
};

const MONTHLY_PRICE_ID = "price_1MEZxXInWuMfFLjmByMHSQOw";
const QUARTER_PRICE_ID = "price_1MEZz8InWuMfFLjm6SsqGLaM";
const HALF_YEAR_PRICE_ID = "price_1MEckhInWuMfFLjmdXPeD7Ud";
const ONE_ITEM_PRICE_ID = "price_1MEa2CInWuMfFLjm4NDJsd3s";
const stripe = Stripe('pk_test_51M9x7LInWuMfFLjmMhKVb4K6NXWj5UfFFkiJ7gGFQxWyc0DpzMaYGrJBiX4MIf6yOsSiMeXh7q330gkSfcjxbKf400EuCjNCXJ');

document.addEventListener("DOMContentLoaded", function (event) {
    document
        .getElementById("checkout_monthly")
        .addEventListener("click", function (evt) {
            createCheckoutSession(MONTHLY_PRICE_ID).then(function (data) {
                stripe
                    .redirectToCheckout({
                        sessionId: data.sessionId
                    });
            });

        });
    document
        .getElementById("checkout_quarter")
        .addEventListener("click", function (evt) {
            createCheckoutSession(QUARTER_PRICE_ID).then(function (data) {
                stripe
                    .redirectToCheckout({
                        sessionId: data.sessionId
                    });
            });

        });
    document
        .getElementById("checkout_half_year")
        .addEventListener("click", function (evt) {
            createCheckoutSession(HALF_YEAR_PRICE_ID).then(function (data) {
                stripe
                    .redirectToCheckout({
                        sessionId: data.sessionId
                    });
            });

        });
    // document
    //     .getElementById("checkout_one_item")
    //     .addEventListener("click", function (evt) {
    //
    //     });
})