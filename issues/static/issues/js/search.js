//Issues objesinin içindeki veriye göre sonuçları listeler.
function searchFunc(response,name){
  if(name.length > 1){
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
        // serial_number is null diyor konsolda
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
$(document).keyup(function(e){
  var key = e.keyCode ? e.keyCode : e.which;
    if (e.keyCode == 27) {
      $(".mask").hide();
    }
});

$("#txtSearch").keyup(function(event){
  event.preventDefault();
  $(".mask").show();
  var name = document.getElementById("txtSearch").value.toUpperCase();
  $.ajax({
    method : "GET",
    url : "http://127.0.0.1:8000/charts/rest/"
  }).then(function (response){
    searchFunc(response,name);
  })

});

$('#getProfits').click(function(){
    var first_date = new Date("2017-08-23T12:00:00Z").toISOString();
    var last_date = new Date("2017-09-01T12:00:00Z").toISOString();
  $.ajax({
    method : "GET",
    url : "http://127.0.0.1:8000/profit_json/",
    data :
    {
      first_date: first_date,
      last_date: last_date
    },
    success:function(response){
      // data: [{"model": "issues.issue", "pk": 1, "fields": {"name": "delivery time issue", "creation_time": "2017-08-24T12:05:28.067Z", "delivery_time": "2017-08-31T00:00:00Z", "product": 1, "tech_guy": 1, "status": "DO", "price": "0", "customer": 1, "todo_list": "", "done_list": ""}}]
      console.log(response);
    }
  })
});
