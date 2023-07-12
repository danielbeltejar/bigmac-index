function chart(countryName) {
    const container = document.getElementById("container");
    container.innerHTML = ""; // Clear the container by removing its child elements
    
    const floatingWindow = document.getElementById("floatingWindow");
    const divEl = floatingWindow.querySelector(".flag");
    divEl.classList.add("flag-icon", "flag-icon-" + countryName.toLowerCase()); // Set the new text content for the <h2> element


    // create line chart
    var chart = anychart.line();

    // set X axis labels formatter
    chart
        .xAxis()
        .labels()
        .format(function () {
            return anychart.format.dateTime(this.value, 'dd/MM');
        });

    // make an HTTP request to fetch data
    fetch('https://bigmac.danielbeltejar.es/v1/prices/history/' + countryName)
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            // create data set on fetched data
            var dataSet = anychart.data.set(data);

            // map mapping
            var mapping = dataSet.mapAs({
                x: 0,
                value: 1
            });

            // create spline series
            var series = chart.spline();

            // set chart data
            series.data(mapping);

            // set series stroke settings
            series.stroke({
                angle: 90,
                keys: [{
                    color: '#2fa85a',
                    offset: 0.25
                }, {
                    color: '#ecef17',
                    offset: 0.5
                }, {
                    color: '#ee4237',
                    offset: 0.75
                }],
                thickness: 3
            });

            // set container id for the chart
            chart.container('container');

            // initiate chart drawing
            chart.draw();
        })
        .catch(function (error) {
            console.error('Error:', error);
        });
};

document.querySelector(".button-close").addEventListener("click", function () {
    const closeButton = document.getElementById("closeButton");
    const floatingWindow = document.getElementById("floatingWindow");

    floatingWindow.style.display = "none"; // Hide the floating window
});
