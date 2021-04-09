document.onload = updateTable();

function handleAddLap(id) {
  console.log(id);

  var settings = {
    url: "https://racing.dorchestersailingclub.org.uk/addlap/1/" + id,
    method: "PATCH",
    timeout: 0,
  };

  $.ajax(settings).done(function (response) {
    console.log(response);
    updateTable();
  });
}

function handleFinish(id) {
  console.log(id);

  var currentTime = Math.round(Date.now() / 1000);

  var settings = {
    url:
      "https://racing.dorchestersailingclub.org.uk/finish/1/" +
      id +
      "?finishTime=" +
      currentTime,
    method: "PATCH",
    timeout: 0,
  };

  $.ajax(settings).done(function (response) {
    console.log(response);
    updateTable();
  });
}

function handleRemoveLap(id) {
  console.log(id);
  var settings = {
    url: "https://racing.dorchestersailingclub.org.uk/removelap/1/" + id,
    method: "PATCH",
    timeout: 0,
  };

  $.ajax(settings).done(function (response) {
    console.log(response);
    updateTable();
  });
}

function handleUnfinish(id) {
  console.log(id);
  var settings = {
    url: "https://racing.dorchestersailingclub.org.uk/unfinish/1/" + id,
    method: "PATCH",
    timeout: 0,
  };

  $.ajax(settings).done(function (response) {
    console.log(response);
    updateTable();
  });
}

function updateTable() {
  var settings = {
    url: "https://racing.dorchestersailingclub.org.uk/api/results/1",
    method: "GET",
    timeout: 0,
  };

  $.ajax(settings).done(function (response) {
    response = $.parseJSON(response);
    console.log(response);
    $("#resultsTable").empty();
    $.each(response, function (i, item) {
      const lapBtn =
        '<div class="btn-group"><button class="btn btn-outline-secondary" onclick=handleAddLap(' +
        item[0] +
        ')>ADD LAP</button><button type="button" class="btn btn-secondary dropdown-toggle dropdown-toggle-split" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"><span class="sr-only">Toggle Dropdown</span><div class="dropdown-menu"><a class="dropdown-item" onclick="handleRemoveLap(' +
        item[0] +
        ')">Remove lap</a></div></div>';
      const lapBtnDisabled =
        '<div class="btn-group"><button disabled class="btn btn-outline-secondary" onclick=handleAddLap(' +
        item[0] +
        ')>ADD LAP</button><button disabled type="button" class="btn btn-secondary dropdown-toggle dropdown-toggle-split" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"><span class="sr-only">Toggle Dropdown</span><div class="dropdown-menu"><a class="dropdown-item" onclick="handleRemoveLap(' +
        item[0] +
        ')">Remove lap</a></div></div>';
      const finishBtn =
        '<button class="btn btn-outline-secondary" onclick=handleFinish(' +
        item[0] +
        ")>FINISH</button>";
      const finishBtnDisabled =
        '<div class="btn-group"><button disabled class="btn btn-outline-secondary" onclick=handleFinish(' +
        item[0] +
        ')>FINISH</button><button type="button" class="btn btn-secondary dropdown-toggle dropdown-toggle-split" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"><div class="dropdown-menu"><a class="dropdown-item" onclick="handleUnfinish(' +
        item[0] +
        ')">Unfinish</a></div></div>';

      var $tr = $("<tr>").append(
        $("<td>").text(item[0]), //ID
        $("<td>").text(item[1]), //Helm
        $("<td>").text(item[2]), //Crew
        $("<td>").text(item[3]), //Sail No
        $("<td>").text(item[4]), //Class
        $("<td>").text(item[5]), //Laps
        item[6] ? $("<td>").append(lapBtnDisabled) : $("<td>").append(lapBtn), //finishBTN
        item[6]
          ? $("<td>").append(finishBtnDisabled)
          : $("<td>").append(finishBtn) //finishBTN
      );
      console.log($tr);
      $("#resultsTable").append($tr);
    });
  });
}
