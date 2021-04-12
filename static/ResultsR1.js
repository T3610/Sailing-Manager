const raceID = 1;

document.onload = updateTable();

function handleAddLap(id) {
  console.log(id);
  var currentTime = Math.round(Date.now() / 1000);

  var settings = {
    url:
      "https://racing.dorchestersailingclub.org.uk/addlap/" +
      raceID +
      "/" +
      id +
      "?lapTime=" +
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
    url:
      "https://racing.dorchestersailingclub.org.uk/removelap/" +
      raceID +
      "/" +
      id,
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
      "https://racing.dorchestersailingclub.org.uk/finish/" +
      raceID +
      "/" +
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

function handleUnfinish(id) {
  console.log(id);
  var settings = {
    url:
      "https://racing.dorchestersailingclub.org.uk/unfinish/" +
      raceID +
      "/" +
      id,
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
    url:
      "https://racing.dorchestersailingclub.org.uk/finishbefore/" +
      raceID +
      "/" +
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

function handleBeforeLappingUnfinish(id) {
  console.log(id);
  var settings = {
    url:
      "https://racing.dorchestersailingclub.org.uk/unfinishbefore/" +
      raceID +
      "/" +
      id,
    method: "PATCH",
    timeout: 0,
  };

  $.ajax(settings).done(function (response) {
    console.log(response);
    updateTable();
  });
}

function handleRetire(id) {
  console.log(id);
  var settings = {
    url:
      "https://racing.dorchestersailingclub.org.uk/retire/" + raceID + "/" + id,
    method: "PATCH",
    timeout: 0,
  };

  $.ajax(settings).done(function (response) {
    console.log(response);
    updateTable();
  });
}

function handleDNS(id) {
  console.log(id);
  var settings = {
    url: "https://racing.dorchestersailingclub.org.uk/DNS/1/" + id,
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
    url: "https://racing.dorchestersailingclub.org.uk/api/results/" + raceID,
    method: "GET",
    timeout: 0,
  };

  $.ajax(settings).done(function (response) {
    response = $.parseJSON(response);
    console.log(response);
    $("#resultsTable").empty();
    $.each(response, function (i, item) {
      const lapBtn = `
        <div class="btn-group">
            <button class="btn btn-outline-secondary" onclick=handleAddLap(${item[0]})>ADD LAP</button>
            <button type="button" class="btn btn-secondary dropdown-toggle dropdown-toggle-split" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                <span class="visually-hidden">Toggle Dropdown</span>
            </button>
            <ul class="dropdown-menu">
                <li><a class="dropdown-item" onclick="handleRemoveLap(${item[0]})">Remove lap</a></li>
            </ul>
        </div>
      `;

      const lapBtnDisabled = `
      <div class="btn-group">
          <button disabled class="btn btn-outline-secondary" onclick=handleAddLap(${item[0]})>ADD LAP</button>
          <button disabled type="button" class="btn btn-secondary dropdown-toggle dropdown-toggle-split" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
              <span class="visually-hidden">Toggle Dropdown</span>
          </button>
          <ul class="dropdown-menu">
              <li><a class="dropdown-item" onclick="handleRemoveLap(${item[0]})">Remove lap</a></li>
          </ul>
      </div>
    `;
      const finishBeforeLappingBtn = `        
        <button class="btn btn-outline-secondary" onclick=handleBeforeLappingFinish(${item[0]})>FINISH</button>
    `;

      const finishBeforeLappingBtnDisabled = `        
    <div class="btn-group">
      <button disabled class="btn btn-outline-secondary" onclick=handleBeforeLappingFinish(${item[0]})>FINISH</button>
      <button type="button" class="btn btn-secondary dropdown-toggle dropdown-toggle-split" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
          <span class="visually-hidden">Toggle Dropdown</span>
      </button>
      <ul class="dropdown-menu">
          <li><a class="dropdown-item" onclick="handleBeforeLappingUnfinish(${item[0]})">Unfinish</a></li>
      </ul>
  </div>
  `;

      const finishAfterLappingBtn = `        
  <button class="btn btn-outline-secondary" onclick=handleFinish(${item[0]})>FINISH</button>
`;

      const finishAfterLappingBtnDisabled = `        
<div class="btn-group">
<button disabled class="btn btn-outline-secondary" onclick=handleFinish(${item[0]})>FINISH</button>
<button type="button" class="btn btn-secondary dropdown-toggle dropdown-toggle-split" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
    <span class="visually-hidden">Toggle Dropdown</span>
</button>
<ul class="dropdown-menu">
    <li><a class="dropdown-item" onclick="handleUnfinish(${item[0]})">Unfinish</a></li>
</ul>
</div>
`;

      const optionsBtn = `<div class="dropdown">
<button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton1" data-bs-toggle="dropdown" aria-expanded="false">
  Options
</button>
<ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1">
    <li><a class="dropdown-item" href="#">Retire</a></li>
    <li><a class="dropdown-item" href="#">Did not start</a></li>
</ul>
</div>`;

      var $tr = $("<tr>").append(
        $("<td>").text(item[1]), //Helm
        $("<td>").text(item[3]), //Sail No
        $("<td>").text(item[4]), //Class
        $("<td>").text(item[5]), //Laps
        item[7] ? $("<td>").append(lapBtnDisabled) : $("<td>").append(lapBtn), //lapBTN
        item[7]
          ? $("<td>").append(finishAfterLappingBtnDisabled)
          : $("<td>").append(finishAfterLappingBtn), //finishBTN
        item[7]
          ? $("<td>").append(finishBeforeLappingBtnDisabled)
          : $("<td>").append(finishBeforeLappingBtn), //finishBTNitem[6]
        $("<td>").append(optionsBtn) //Laps
      );
      console.log($tr);
      $("#resultsTable").append($tr);
    });
  });
}
