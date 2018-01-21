document.addEventListener('DOMContentLoaded', function() {

    var jsoncontent = "https://raw.githubusercontent.com/pypolitics/pficontracts/master/data/plot_data.json";
    var plot = document.getElementById('plot');

    Plotly.d3.json(jsoncontent, function(err, fig) {
    	var config = {'displayModeBar': true, 'showLink': false, 'scrollZoom': true, 'displaylogo' : false, 'modeBarButtonsToRemove': ['lasso2d', 'toggleSpikelines', 'sendDataToCloud', 'hoverCompareCartesian', 'hoverClosestCartesian', 'tableRotation', 'select2d', 'hoverClosest3d']}
    	Plotly.purge(plot);
    	Plotly.plot(plot, fig.data, fig.layout, config);
    });
}, false);
