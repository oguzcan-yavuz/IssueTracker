$("#txtSearch").change(function() {
  var text = document.getElementById("txtSearch").value;
  $("#listResult").html("");
  $(".mask").show();
  $.ajax({
    method : "GET",
    url : "http://127.0.0.1:8000/charts/rest/"
  }).then(function (response){
    $("#listResult").append("<li>" + response.labels + "</li>");
  });
});

$("#search").submit(function(e){
    return false;
});

$("#close").click(function(e){
    $(".mask").hide();
});

window.onkeyup = function(e) {
   var key = e.keyCode ? e.keyCode : e.which;
   if (key == 27) {
       $(".mask").hide();
   }

}
