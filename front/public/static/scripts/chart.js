function chart(countryName) {
    const container = document.getElementById("container");
    container.innerHTML = "";

    const floatingWindow = document.getElementById("floatingWindow");
    const divEl = floatingWindow.querySelector(".flag");
    divEl.classList.add("flag-icon", "flag-icon-" + countryName.toLowerCase());

    var chart = anychart.line();

    chart
        .xAxis()
        .labels()
        .format(function () {
            return anychart.format.dateTime(this.value, 'dd/MM');
        });

    fetch(`${window.location.origin}/api/prices/history/` + countryName)
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            var dataSet = anychart.data.set(data);

            var mapping = dataSet.mapAs({
                x: 0,
                value: 1
            });

            var series = chart.spline();

            series.data(mapping);

            series.stroke({
                color: "var(--primary-color)",
                thickness: 3
            });

            chart.container('container');

            chart.draw();
        })
        .catch(function (error) {
            console.error('Error:', error);
        });
};

document.querySelector(".button-close").addEventListener("click", function () {
    const closeButton = document.getElementById("closeButton");
    const floatingWindow = document.getElementById("floatingWindow");

    floatingWindow.style.display = "none";
});
