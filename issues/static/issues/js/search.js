
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
    url : "http://127.0.0.1:8000/charts/rest/",
    data: {
      statistic: 1
    }
  }).then(function (response){
    searchFunc(response,name);
  })

});

function reformatDate(date){
  var formDate = date.split("/");
  var formatDate = formDate[2]+"-"+formDate[0]+"-"+ formDate[1]+"T00:00:00Z";
  return formatDate;
}


$('#getProfits').click(function(){
    var first_date =  document.getElementById("first_date").value;
    var last_date =  document.getElementById("last_date").value;

    first_date = new Date(reformatDate(first_date)).toISOString();
    last_date =  new Date(reformatDate(last_date)).toISOString();

  $.ajax({
    method : "GET",
    url : "http://127.0.0.1:8000/charts/statistics/",
    data :
    {
      first_date: first_date,
      last_date: last_date,
      statistic: 1
    }
  }).then(function(response){
      response = JSON.parse(response);
      var totalPrice= 0;
      $("#profitsTable").html("");
      $("#totalPrice").html("");
      console.log(response[0]);
      for (var i = 0; i < response.length; i++) {
        $("#profitsTable").append(
          "<tr>"+
              "<td>"+
              response[i].fields.name +
              "</td>"+
              "<td>"+
              response[i].fields.done_list +
              "</td>"+
              "<td>"+
              response[i].fields.price +
              " TL</td>"+
          "</tr>"
        );
        var totalPrice = totalPrice + parseInt(response[i].fields.price);
      }
      $("#totalPrice").append(totalPrice + " TL");
    }); //then
  }); // ajax
