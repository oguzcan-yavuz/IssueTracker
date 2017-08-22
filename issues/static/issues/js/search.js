//Issues objesinin içindeki veriye göre sonuçları listeler.
function searchFunc(response,name){
  if(name.length > 2){
    $("#issuesResult").html("");
    $.map(response.issues, function(entry) {

        var selectCustomer = $.map(response.customers, function(customer){
          if(customer.id == entry.customer){
            return customer;
          }
        });

        var selectProduct = $.map(response.products, function(product){
          if(product.id == entry.product){
            return product;
          }
        });

        if(entry.name.toUpperCase().indexOf(name) !== -1 ){
            $("#issuesResult").append(
              "<li>" +
                "<a href='/issues/"+ entry.id + "'>" +
                entry.name +
                 "</a>" +
                 " - <span>"+ selectCustomer[0].name +"</span>" +
                 " - <span>"+ selectProduct[0].name +"</span>" +
              "</li>");
        }
    });

    $("#customersResult").html("");
    $.map(response.customers, function(entry) {
        if(entry.name.toUpperCase().indexOf(name) !== -1 || entry.phone.toUpperCase().indexOf(name) !== -1 ){
            $("#customersResult").append(
              "<li>" +
                "<a href='/customers/"+ entry.id + "'>" +
                entry.name +
                 "</a>" +
                 " - <span> "+ entry.phone +"</span>" +
              "</li>"
            );
        }
    });

    $("#productsResult").html("");
    $.map(response.products, function(entry) {
        if(entry.name.toUpperCase().indexOf(name) !== -1 || entry.serial_number.toUpperCase().indexOf(name) !== -1){
            $("#productsResult").append(
              "<li>" +
                "<a href='/products/"+ entry.id + "'>" +
                entry.name +
                 "</a>" +
                 " - <span>" + entry.serial_number + "</span>" +
              "</li>"
            );
        }
    });
  }else{
    $("#issuesResult").html("");
    $("#customersResult").html("");
    $("#productsResult").html("");
  }
}

$("#close").click(function(e){
    $(".mask").hide();
});

$(document).on('keyup',function(e){
  var key = e.keyCode ? e.keyCode : e.which;
    if (e.keyCode == 27) {
      $(".mask").hide();
    }else if (e.keyCode == 17){
      document.getElementById('txtSearch').focus();
      $(".mask").show();
    }
});

$("#txtSearch").keyup(function(e){
  var name = document.getElementById("txtSearch").value.toUpperCase();
  $.ajax({
    method : "GET",
    url : "http://127.0.0.1:8000/charts/rest/"
  }).then(function (response){
    searchFunc(response,name);
  });
});
