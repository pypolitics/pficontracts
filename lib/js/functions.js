$('#plot').on("plotly_click", function(event, data) {
  var p = data.points[0];
  console.log(p);
});
