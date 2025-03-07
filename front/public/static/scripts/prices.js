fetch(`${window.location.origin}/api/prices/actual`)
    .then(response => response.json())
    .then(data => {
        var cards = document.getElementsByClassName("card");

        while (cards.length > 0) {
            cards[0].parentNode.removeChild(cards[0]);
        }


        data.sort((a, b) => a[4] - b[4]);
        data.forEach(country => {
            var countryName = country[0];
            var price = country[1];
            var currency = country[3];
            var priceDollars = country[4];

            var card = document.createElement("div");
            card.classList.add("card", "flex-row", "flex-center", "white-background");

            var flagIcon = document.createElement("i");
            flagIcon.classList.add("flag-icon", "flag-icon-" + countryName.toLowerCase());
            card.appendChild(flagIcon);

            var priceElement = document.createElement("p");
            priceElement.classList.add("text-bold", "default");
            priceElement.textContent = price + " " + currency;
            card.appendChild(priceElement);

            var priceDollarsElement = document.createElement("p");
            priceDollarsElement.classList.add("text-bold", "dollars");
            if(priceDollars == 0) {
                priceDollarsElement.textContent = "No data"    
            } else {
            priceDollarsElement.textContent = priceDollars + " USD";
            }

            priceDollarsElement.classList.add("hide")
            card.appendChild(priceDollarsElement);


            var button = document.createElement("div");
            button.classList.add("button", "yellow-background", "white-color");
            button.id = countryName.toLowerCase
            button.innerHTML = '<img src="static/images/chart-simple-solid.svg">';
            button.addEventListener("click", function () {
                floatingWindow.style.display = "block";
                chart(countryName);
            });


            card.appendChild(button);

            document.querySelector(".index").appendChild(card);
        });
    })
    .catch(error => {
        console.error('Error:', error);
    });

let showingDollars = false;

function convertPricesToDollars() {
    var priceElements = document.querySelectorAll(".card p.dollars");
    priceElements.forEach(element => {
        if (showingDollars) {
            element.classList.add("hide");
        } else {
            element.classList.remove("hide");
        }
    });
    var priceElements = document.querySelectorAll(".card p.default");
    priceElements.forEach(element => {
        if (showingDollars) {
            element.classList.remove("hide");
        } else {
            element.classList.add("hide");
        }
    });
    showingDollars = !showingDollars;
}

document.querySelector(".button-dollars").addEventListener("click", convertPricesToDollars);

