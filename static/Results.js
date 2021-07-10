const raceID = window.location.href.split("/")[4];
console.log("Race ID = " + raceID + " from URL");

document.onload = updateTable();

function handleAddLap(id) {
  console.log(id);
  var currentTime = Math.round(Date.now() / 1000);

  var settings = {
    url: "/addlap/" + raceID + "/" + id + "?lapTime=" + currentTime,
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
    url: "/removelap/" + raceID + "/" + id,
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
    url: "/finish/" + raceID + "/" + id + "?finishTime=" + currentTime,
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
    url: "/unfinish/" + raceID + "/" + id,
    method: "PATCH",
    timeout: 0,
  };

  $.ajax(settings).done(function (response) {
    console.log(response);
    updateTable();
  });
}

function handleBeforeLappingFinish(id) {
  console.log(id);

  var currentTime = Math.round(Date.now() / 1000);

  var settings = {
    url: "/finishbefore/" + raceID + "/" + id + "?finishTime=" + currentTime,
    method: "PATCH",
    timeout: 0,
  };

  $.ajax(settings).done(function (response) {
    console.log(response);
    updateTable();
  });
}

function handleBeforeLappingUnfinish(id) {
  console.log(id);
  var settings = {
    url: "/unfinishbefore/" + raceID + "/" + id,
    method: "PATCH",
    timeout: 0,
  };

  $.ajax(settings).done(function (response) {
    console.log(response);
    updateTable();
  });
}

function handleRetire(id, name) {
  console.log(id);
  var r = confirm("Confirm you want to retire " + name);
  if (r == true) {
    var settings = {
      url: "/retire/" + raceID + "/" + id,
      method: "PATCH",
      timeout: 0,
    };

    $.ajax(settings).done(function (response) {
      console.log(response);
      updateTable();
    });
  }
}

function handleDNS(id, name) {
  console.log(id);
  var r = confirm("Confirm you want to DNS " + name);
  if (r == true) {
    var settings = {
      url: "/DNS/" + raceID + "/" + id,
      method: "PATCH",
      timeout: 0,
    };

    $.ajax(settings).done(function (response) {
      console.log(response);
      updateTable();
    });
  }
}

function updateTable() {
  var settings = {
    url: "/api/results/" + raceID,
    method: "GET",
    timeout: 0,
  };

  $.ajax(settings).done(function (response) {
    response = $.parseJSON(response);
    console.log(response);
    $("#resultsTable").empty();
    $.each(response, function (i, item) {
      console.log(item);
      const lapBtn = `
      <div class="btn-group">
          <button class="btn btn-primary btn-lg" onclick=handleAddLap(${item[0]})>ADD LAP (${item[8]})</button>
          <button type="button" class="btn btn-lg btn-outline-primary dropdown-toggle dropdown-toggle-split" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
              <span class="visually-hidden">Toggle Dropdown</span>
          </button>
          <ul class="dropdown-menu">
              <li><a class="dropdown-item dropdownOption" onclick="handleRemoveLap(${item[0]})">Remove lap</a></li>
          </ul>
      </div>
    `;

      const lapBtnDisabled = `
      <div class="btn-group">
          <button disabled class="btn btn-lg btn-outline-secondary" onclick=handleAddLap(${item[0]})>ADD LAP (${item[10]})</button>
          <button disabled type="button" class="btn btn-lg btn-secondary dropdown-toggle dropdown-toggle-split" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
              <span class="visually-hidden">Toggle Dropdown</span>
          </button>
          <ul class="dropdown-menu">
              <li><a class="dropdown-item dropdownOption" onclick="handleRemoveLap(${item[0]})">Remove lap</a></li>
          </ul>
      </div>
    `;

      const finishBtn = `        
  <button class="btn btn-lg btn-primary" onclick=handleFinish(${item[0]})>FINISH</button>
`;

      const finishBtnDisabled = `        
<div class="btn-group">
<button disabled class="btn btn-lg btn-outline-secondary" onclick=handleFinish(${item[0]})>FINISH</button>
<button type="button" class="btn btn-lg btn-secondary dropdown-toggle dropdown-toggle-split" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
    <span class="visually-hidden">Toggle Dropdown</span>
</button>
<ul class="dropdown-menu">
    <li><a class="dropdown-item dropdownOption" onclick="handleUnfinish(${item[0]})">Unfinish</a></li>
</ul>
</div>
`;

      const optionsBtn = `<div class="dropdown">
<button class="btn btn-lg btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton1" data-bs-toggle="dropdown" aria-expanded="false">
  Options
</button>
<ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1">
    <li><a class="dropdown-item dropdownOption" onclick="handleRetire(${
      item[0]
    },'${item[1].replace("'", "\\'")}')">Retire</a></li>
    <li><a class="dropdown-item dropdownOption" onclick="handleDNS(${
      item[0]
    },'${item[1].replace("'", "\\'")}')">Did not start</a></li>
</ul>
</div>`;

      var $tr = $("<tr>").append(
        $("<td>").text(item[3] + " (" + item[1] + ")"), //Sail No
        $("<td>").text(item[4]), //Class
        item[10] ? $("<td>").append(lapBtnDisabled) : $("<td>").append(lapBtn), //lapBTN
        item[10]
          ? $("<td>").append(finishBtnDisabled)
          : $("<td>").append(finishBtn), //finishBTN

        $("<td>").append(optionsBtn) //Laps
      );
      console.log($tr);
      $("#resultsTable").append($tr);
    });
  });
}
