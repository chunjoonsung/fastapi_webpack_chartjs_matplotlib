
const MyChart = require('./mychart.js')

$(document).ready( () => {
     fetch(window.location.origin + "/data/chart", {
        method: "get", 
     })
     .then((response) => response.json())
     .then((data) => {
        console.log(data)
		MyChart.drawChart('chartId1','line',data)
		MyChart.drawChart('chartId','bar',data)
     }) 
})
