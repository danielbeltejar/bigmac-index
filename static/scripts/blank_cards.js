            for (var i = 0; i < 25; i++) {
                // Create the card element
                var card = document.createElement("div");
                card.classList.add("card", "flex-row", "flex-center", "white-background");


                // Add the button
                var button = document.createElement("div");
                button.classList.add("button", "yellow-background", "white-color");
                button.innerHTML = '<img src="static/images/chart-simple-solid.svg">';
                card.appendChild(button);

                document.querySelector(".index").appendChild(card);
            }  
