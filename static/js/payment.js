const stripe = Stripe('pk_test_51JPTEyIpP9vN5HSdmkUVQzqvfMbsoq1vGbe2CTOkgh6KacZUiV6z5H6GCOxfaDlt0Ck7vwkgqOZ8ZW54dYCFU3WW00yrpdur8w');

let btnPurchase = document.getElementById("purchase-button");
clientSecret = btnPurchase.getAttribute('data-secret');

let elements = stripe.elements();
let style = {
    base: {
        color: "#000",
        lineHeight: "2.4",
        fontSize: "16px",
    }
};

let cardElement = elements.create("card", { style: style });
cardElement.mount('#card-element');

cardElement.on("change", function (event) {

    let displayError = document.getElementById("card-errors");
    if (event.error) {
        displayError.textContent = event.error.message;
        $("#card-errors").addClass("alert alert-info");
    } else {
        displayError.textContent = "";
        $("#card-errors").removeClass("alert alert-info");
    }
});


let form = document.getElementById("payment-form");
form.addEventListener("submit", function (e) {
    e.preventDefault();

    let fName = document.getElementById("firstName").value;
    let lName = document.getElementById("lastName").value;
    let fullName = fName + " " + lName;
    console.log(fName);
    console.log(fullName);

    let address1 = document.getElementById("address").value;
    let address2 = document.getElementById("address2").value;
    console.log(address1);
    console.log(address2);

    // Receive the https://domain_name/orders/add/
    let orderAddUrl = document.getElementById("orders-add-url");
    let URI = orderAddUrl.getAttribute("data-url");

    $.ajax({
        type: "POST",
        url: URI,
        data: {
            order_key: clientSecret,
            csrfmiddlewaretoken: CSRF_TOKEN,
            addr1: address1,
            addr2: address2,
            name: fullName,
            action: "post"
        },
        success: function (json) {
            console.log(json.success);

            stripe.confirmCardPayment(clientSecret, {
               payment_method: {
                   card: cardElement,
                   billing_details: {
                       address: {
                           line1: address1,
                           line2: address2
                       },
                       name: fullName
                   },
               }
            }).then(function (result) {
                if (result.error) {
                    console.log("payment error");
                    console.log(result.error.message);
                } else  {
                    if (result.paymentIntent.status === "succeeded") {
                        console.log("payment processed");
                        window.location.replace("http://127.0.0.1:8000/payment/orderplaced/");
                    }
                }
            })
        },
        error: function (xhr, errmsg, err) {
            console.log(errmsg);
        },
    })
});




