$("#txtSearch").keypress(function() {
  $("#listResult").html("");
  $(".mask").show();
  $.ajax({
    method : "GET",
    url : "http://127.0.0.1:8000/charts/rest/"
  }).then(function (response){
    var results;
    var name = document.getElementById("txtSearch").value;
    name = name.toUpperCase();
    results = $.map(response.issues, function(entry) {
        if(entry.name.toUpperCase().indexOf(name) !== -1){
            $("#listResult").append("<li>" + entry.name + "</li>");
        }
    });

    // var results = [];
    // var searchField = "name";
    // for (var i=0 ; i < response.issues.length ; i++)
    // {
    //     if (response.issues[i][searchField] == text) {
    //         results.push(response.issues[i]);
    //         $("#listResult").append("<li>" + response.issues[i][searchField] + "</li>");
    //     }
    // }

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
