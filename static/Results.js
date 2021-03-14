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
        "url": "http://ec2-35-178-146-200.eu-west-2.compute.amazonaws.com/addlap/"+id,
        "method": "PATCH",
        "timeout": 0,
      };
      
      $.ajax(settings).done(function (response) {
        console.log(response);
        location.reload();
      });
}