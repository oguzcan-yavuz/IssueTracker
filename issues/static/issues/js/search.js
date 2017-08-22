//Issues objesinin içindeki veriye göre sonuçları listeler.
function searchFunc(response,name){
  $("#issuesResult").html("");
  $.map(response.issues, function(entry) {
      if(entry.name.toUpperCase().indexOf(name) !== -1){
          $("#issuesResult").append("<li>" + entry.name + "</li>");
      }
  });

  $("#customersResult").html("");
  $.map(response.customers, function(entry) {
      if(entry.name.toUpperCase().indexOf(name) !== -1){
          $("#customersResult").append("<li>" + entry.name + "</li>");
      }
  });

  $("#productsResult").html("");
  $.map(response.products, function(entry) {
      if(entry.name.toUpperCase().indexOf(name) !== -1){
          $("#productsResult").append("<li>" + entry.name + "</li>");
      }
  });

}

$("#close").click(function(e){
    $(".mask").hide();
});

$("#txtSearch").keyup(function(e){
  $(".mask").show();
  var name = document.getElementById("txtSearch").value.toUpperCase();
  var key = e.keyCode ? e.keyCode : e.which;
    if (key == 27) {
      $(".mask").hide();
    }

  $.ajax({
    method : "GET",
    url : "http://127.0.0.1:8000/charts/rest/"
  }).then(function (response){
    searchFunc(response,name);
  });
});
