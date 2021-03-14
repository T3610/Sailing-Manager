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
        $("#resultsTable").empty();
        $.each(response, function(i, item) {
            const lapBtn = '<button class="btn btn-outline-secondary" onclick=handleAddLap('+item[0]+')>ADD LAP</button>';
            const finishBtn = '<button class="btn btn-outline-secondary" onclick=handleFinish('+item[0]+')>FINISH</button>';
            const finishBtnDisabled = '<button disabled class="btn btn-outline-secondary" onclick=handleFinish('+item[0]+')>FINISH</button>';

            var $tr = $('<tr>').append(
                $('<td>').text(item[0]), //ID
                $('<td>').text(item[1]), //Helm
                $('<td>').text(item[2]), //Crew
                $('<td>').text(item[3]), //Sail No
                $('<td>').text(item[4]), //Class
                $('<td>').text(item[5]), //Laps
                $('<td>').append(lapBtn), //LapBTN
                (item[6])?$('<td>').append(finishBtnDisabled):$('<td>').append(finishBtn), //finishBTN
            );
            console.log($tr)
            $("#resultsTable").append($tr);
        });
      });
}
