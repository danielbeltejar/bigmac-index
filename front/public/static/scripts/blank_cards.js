for (var i = 0; i < 25; i++) {
    // Create the card element
    var card = document.createElement("div");
    card.classList.add("card", "flex-row", "flex-center", "white-background");

    //Add flag container skeleton
    var flag = document.createElement("div");
    flag.classList.add("square-sm", "m-right-auto", "skeleton");
    card.appendChild(flag);

    // Add the text skeleton
    var text = document.createElement("div");
    text.classList.add("rectangle-sm", "m-left-auto", "skeleton");
    card.appendChild(text);

    // Add the button skeleton
    var button = document.createElement("div");
    button.classList.add("square-sm", "m-left-auto", "skeleton");
    card.appendChild(button);

    document.querySelector(".index").appendChild(card);
}  
