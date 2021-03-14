function handleAddLap(id){
    console.log(id)

    var settings = {
        "url": "http://ec2-35-178-146-200.eu-west-2.compute.amazonaws.com/addlap/"+id,
        "method": "PATCH",
        "timeout": 0,
      };
      
      $.ajax(settings).done(function (response) {
        console.log(response);
        location.reload();
      });
}
function handleFinish(id){
    console.log(id)

    var settings = {
        "url": "http://ec2-35-178-146-200.eu-west-2.compute.amazonaws.com/finish/"+id,
        "method": "PATCH",
        "timeout": 0,
      };
      
      $.ajax(settings).done(function (response) {
        console.log(response);
        location.reload();
      });
}

function updateTable(){
    var settings = {
        "url": "http://ec2-35-178-146-200.eu-west-2.compute.amazonaws.com/api/results",
        "method": "GET",
        "timeout": 0,
      };
      
      $.ajax(settings).done(function (response) {
        response = $.parseJSON(response);
        console.log(response);
        $.each(response, function(i, item) {
            var $tr = $('<tr>').append(
                $('<td>').text(item[0]),
                $('<td>').text(item[1]),
                $('<td>').text(item[2])
            );
            console.log($tr)
            $("#resultsTable").append($tr);
        });
      });
}
